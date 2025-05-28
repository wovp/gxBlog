import { debugLog } from "../utils/debug";

// 定义坐标接口
export interface Position {
    x: number;
    y: number;
}

// 方向枚举
export enum Direction {
    UP = 'UP',
    DOWN = 'DOWN',
    LEFT = 'LEFT',
    RIGHT = 'RIGHT',
}

// 蛇类
export class Snake {
    body: Position[];
    direction: Direction;
    nextDirection: Direction;

    // 速度属性
    baseSpeed: number; // 基础速度
    currentSpeed: number; // 当前速度

    // 加速相关属性
    isSpeedingUp: boolean;
    speedUpFactor: number;
    speedUpDuration: number;
    speedUpCooldown: number;
    speedUpEnergy: number;
    maxSpeedUpEnergy: number;
    energyRegenRate: number;
    lastEnergyUpdate: number;
    speedUpTimer: number | null;
    cooldownTimer: number | null;

    // 加速结束回调
    onSpeedUpEnd: (() => void) | null;

    constructor() {
        // 初始化蛇的身体，从中间开始，长度为3
        this.body = [
            { x: 10, y: 10 },
            { x: 9, y: 10 },
            { x: 8, y: 10 }
        ];
        this.direction = Direction.RIGHT;
        this.nextDirection = Direction.RIGHT;

        // 初始化速度属性
        this.baseSpeed = 200; // 基础速度
        this.currentSpeed = this.baseSpeed; // 当前速度初始为基础速度秒

        // 初始化加速属性
        this.isSpeedingUp = false;
        this.speedUpFactor = 0.5; // 加速到原速度的50%
        this.speedUpDuration = 3000; // 加速持续3秒
        this.speedUpCooldown = 5000; // 冷却时间5秒
        this.speedUpEnergy = 100; // 初始能量满格
        this.maxSpeedUpEnergy = 100;
        this.energyRegenRate = 20; // 每秒恢复20点能量
        this.lastEnergyUpdate = Date.now();
        this.speedUpTimer = null;
        this.cooldownTimer = null;

        // 初始化回调
        this.onSpeedUpEnd = null;
    }

    // 移动蛇
    move(): void {
        // 更新方向
        this.direction = this.nextDirection;

        // 获取蛇头位置
        const head = { ...this.body[0] };

        // 根据方向移动蛇头
        switch (this.direction) {
            case Direction.UP:
                head.y -= 1;
                break;
            case Direction.DOWN:
                head.y += 1;
                break;
            case Direction.LEFT:
                head.x -= 1;
                break;
            case Direction.RIGHT:
                head.x += 1;
                break;
        }

        // 将新的头部添加到身体的前面
        this.body.unshift(head);

        // 如果没有吃到食物，移除尾部
        // 注意：现在食物碰撞检测由GameController处理
        this.body.pop();

        // 更新加速能量
        this.updateSpeedUpEnergy();
    }

    // 增加长度
    grow(degree: number): void {
        // 增加长度，不需要移除尾部
        // 由于在move方法中已经移除了尾部，这里需要添加回来
        const tail = this.body[this.body.length - 1];

        // 根据食物样式决定增长节数
        const segmentsToAdd = degree + 1; // degree 0 = 1节, degree 1 = 2节, degree 2 = 3节

        // 复制尾部并添加到蛇身
        for (let i = 0; i < segmentsToAdd; i++) {
            this.body.push({ ...tail });
        }

        debugLog(`吃到增长食物，程度: ${degree}, 增加 ${segmentsToAdd} 节`);
    }

    // 减少长度
    shrink(degree: number): void {
        // 减少长度，额外移除尾部
        const shrinkAmount = degree;
        // 确保蛇至少有3个部分
        const maxShrink = Math.max(0, this.body.length - 3);
        const actualShrink = Math.min(shrinkAmount, maxShrink);

        for (let i = 0; i < actualShrink; i++) {
            this.body.pop();
        }
        debugLog(`吃到缩短食物，程度: ${degree}, 实际缩短: ${actualShrink}`);
    }

    // 减速
    slow(degree: number): void {
        // 减速
        const slowFactor = degree; // 11-20 映射到 1-10
        const newSpeed = Math.min(this.baseSpeed + slowFactor * 10, 200); // 最大减速到200ms
        this.currentSpeed = newSpeed;
        debugLog(`吃到减速食物，程度: ${degree + 10}, 新速度: ${this.currentSpeed}ms`);
    }

    // 加速
    speedUp(degree: number): void {
        // 加速
        const speedFactor = degree; // 21-30 映射到 1-10
        const newFastSpeed = Math.max(this.baseSpeed - speedFactor * 5, 50); // 最小加速到50ms
        this.currentSpeed = newFastSpeed;
        debugLog(`吃到加速食物，程度: ${degree + 20}, 新速度: ${this.currentSpeed}ms`);
    }

    // 主动加速
    activateSpeedUp(): boolean {
        // 检查是否可以加速
        if (this.isSpeedingUp || this.speedUpEnergy < 100 || this.cooldownTimer !== null) {
            return false;
        }

        // 开始加速
        this.isSpeedingUp = true;
        this.speedUpEnergy = 0; // 消耗所有能量

        // 保存当前速度
        const originalSpeed = this.currentSpeed;

        // 应用加速
        this.currentSpeed = Math.max(50, this.currentSpeed * this.speedUpFactor); // 确保最小速度为50ms

        debugLog(`激活加速, 速度从 ${originalSpeed}ms 变为 ${this.currentSpeed}ms`);
        // 设置加速结束计时器
        this.speedUpTimer = setTimeout(() => {
            // 结束加速
            this.isSpeedingUp = false;
            this.currentSpeed = originalSpeed;

            debugLog(`加速结束, 恢复速度 ${this.currentSpeed}ms`);

            // 调用回调通知加速结束
            if (this.onSpeedUpEnd) {
                this.onSpeedUpEnd();
            }

            // 设置冷却计时器
            this.cooldownTimer = setTimeout(() => {
                this.cooldownTimer = null;
                debugLog(`加速冷却结束`);
            }, this.speedUpCooldown);

        }, this.speedUpDuration);

        return true;
    }

    // 设置加速结束回调
    setSpeedUpEndCallback(callback: () => void): void {
        this.onSpeedUpEnd = callback;
    }

    // 更新加速能量
    updateSpeedUpEnergy(): void {
        if (!this.isSpeedingUp && this.speedUpEnergy < this.maxSpeedUpEnergy) {
            const now = Date.now();
            const deltaTime = (now - this.lastEnergyUpdate) / 1000; // 转换为秒
            this.lastEnergyUpdate = now;

            // 恢复能量
            this.speedUpEnergy = Math.min(
                this.maxSpeedUpEnergy,
                this.speedUpEnergy + deltaTime * this.energyRegenRate
            );
        }
    }
    // 调整基础速度（用于升级）
    adjustBaseSpeed(newBaseSpeed: number): void {
        // 保存当前是否在加速
        const wasSpeedingUp = this.isSpeedingUp;

        // 如果不在加速，当前速度直接设置为新的基础速度
        if (!wasSpeedingUp) {
            this.currentSpeed = newBaseSpeed;
        }

        // 更新基础速度
        this.baseSpeed = newBaseSpeed;

        debugLog(`调整基础速度为 ${this.baseSpeed}ms, 当前速度为 ${this.currentSpeed}ms`);
    }

    // 重置蛇的状态
    reset(): void {
        this.body = [
            { x: 10, y: 7 },
            { x: 9, y: 7 },
            { x: 8, y: 7 },
        ];
        this.direction = Direction.RIGHT;
        this.nextDirection = Direction.RIGHT;

        // 重置加速状态
        this.isSpeedingUp = false;
        this.speedUpEnergy = this.maxSpeedUpEnergy;
        this.lastEnergyUpdate = Date.now();

        // 清除计时器
        if (this.speedUpTimer !== null) {
            clearTimeout(this.speedUpTimer);
            this.speedUpTimer = null;
        }

        if (this.cooldownTimer !== null) {
            clearTimeout(this.cooldownTimer);
            this.cooldownTimer = null;
        }
    }



    // 改变方向
    changeDirection(newDirection: Direction): void {
        // 防止180度转弯
        if (
            (this.direction === Direction.UP && newDirection === Direction.DOWN) ||
            (this.direction === Direction.DOWN && newDirection === Direction.UP) ||
            (this.direction === Direction.LEFT && newDirection === Direction.RIGHT) ||
            (this.direction === Direction.RIGHT && newDirection === Direction.LEFT)
        ) {
            return;
        }

        this.nextDirection = newDirection;
    }

    // 检查是否撞到自己
    checkCollisionWithSelf(): boolean {
        const head = this.body[0];
        return this.body.slice(1).some(segment => segment.x === head.x && segment.y === head.y);
    }
}

// 食物类
export class Food {
    x: number;
    y: number;
    degree: number;
    type: FoodType; // 食物类型

    constructor(x: number, y: number, degree: number, type: FoodType) {
        this.x = x;
        this.y = y;
        this.degree = degree;
        this.type = type;
    }

    // 生成新的食物位置
    static generateFood(snake: Snake, gridWidth: number, gridHeight: number): Food {
        let x: number = 0, y: number = 0;
        let validPosition = false;

        // 确保食物不会生成在蛇身上
        while (!validPosition) {
            x = Math.floor(Math.random() * gridWidth);
            y = Math.floor(Math.random() * gridHeight);

            validPosition = !snake.body.some(segment => segment.x === x && segment.y === y);
        }

        // 随机生成食物类型和样式
        const randomType = Math.random();
        let degree: number;
        let type: FoodType;

        if (randomType < 0.6) {
            // 60% 概率是普通食物 (增加长度)
            degree = Math.floor(Math.random() * 11); // 0-10
            type = FoodType.GROW;
        }
        else if (randomType < 0.7) {
            // 10% 概率是减少长度食物
            degree = -Math.floor(Math.random() * 10) - 1; // -10 到 -1
            type = FoodType.SHRINK;
        }
        else if (randomType < 0.85) {
            // 15% 概率是减速食物
            degree = Math.floor(Math.random() * 10) + 11; // 11-20
            type = FoodType.SLOW;
        }
        else {
            // 15% 概率是加速食物
            degree = Math.floor(Math.random() * 10) + 21; // 21-30
            type = FoodType.FAST;
        }

        return new Food(x, y, degree, type);
    }
}

// 食物类型枚举
export enum FoodType {
    GROW = 'grow',      // 增加长度
    SHRINK = 'shrink',  // 减少长度
    SLOW = 'slow',      // 减少速度
    FAST = 'fast',      // 增加速度
}
