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
    speed: number;

    constructor() {
        // 初始化蛇的身体，从中间开始，长度为3
        this.body = [
            { x: 10, y: 10 },
            { x: 9, y: 10 },
            { x: 8, y: 10 }
        ];
        this.direction = Direction.RIGHT;
        this.nextDirection = Direction.RIGHT;
        this.speed = 200; // 蛇的移动速度，单位为毫秒
    }

    // 移动蛇
    move(food: Food | null): boolean {
        // debugLog(`移动蛇`)
        // 更新方向
        this.direction = this.nextDirection;

        // 获取头部位置
        const head = { ...this.body[0] };

        // 根据方向移动头部
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

        // 将新头部添加到身体前面
        this.body.unshift(head);
        // 检查并处理食物碰撞
        return this.handleFoodCollision(food);
    }

    // 处理食物碰撞
    private handleFoodCollision(food: Food | null): boolean {
        if (!food) return false;

        const head = this.body[0];
        const ateFood = head.x === food.x && head.y === food.y;

        if (ateFood) {
            switch (food.type) {
                case FoodType.GROW:
                    this.growByFoodType(food.degree);
                    break;
                case FoodType.SHRINK:
                    this.shrinkByFoodType(food.degree);
                    break;
                case FoodType.SLOW:
                    this.decreaseSpeed(food.degree);
                    break;
                case FoodType.FAST:
                    this.increaseSpeed(food.degree);
                    break;
            }

        } else {
            // 如果没有吃到食物，移除尾部
            this.body.pop();
        }

        return ateFood;
    }

    // 根据食物类型增加蛇的长度
    private growByFoodType(foodStyle: number): void {
        // 根据食物样式决定增长节数
        const segmentsToAdd = foodStyle + 1; // style 0 = 1节, style 1 = 2节, style 2 = 3节

        debugLog(`吃到食物, 类型: ${foodStyle}, 增加 ${segmentsToAdd} 节`)

        // 获取尾部位置
        const tail = this.body[this.body.length - 1];

        // 复制尾部并添加到蛇身
        for (let i = 0; i < segmentsToAdd; i++) {
            this.body.push({ ...tail });
        }
    }
    // 根据食物类型减少蛇的长度
    private shrinkByFoodType(foodStyle: number): void {
        // 计算减少的节数 (取绝对值)
        const segmentsToRemove = Math.abs(foodStyle);

        debugLog(`吃到减少食物, 类型: ${foodStyle}, 减少 ${segmentsToRemove} 节`)

        // 确保不会减少到0长度
        const segmentsToKeep = Math.max(1, this.body.length - segmentsToRemove);
        this.body = this.body.slice(0, segmentsToKeep);
    }

    // 减少速度
    private decreaseSpeed(foodStyle: number): void {
        // 根据食物类型计算减速比例 (11-20 转换为 1.1-2.0 倍减速)
        const slowdownFactor = 1 + (foodStyle - 10) / 10;
        const newSpeed = Math.min(1000, this.speed * slowdownFactor); // 最大减速到1000ms

        debugLog(`吃到减速食物, 类型: ${foodStyle}, 速度变为 ${newSpeed}ms`)

        this.speed = newSpeed;
    }

    // 增加速度
    private increaseSpeed(foodStyle: number): void {
        // 根据食物类型计算加速比例 (21-30 转换为 0.1-0.9 倍加速)
        const speedupFactor = 1 - (foodStyle - 20) / 20;
        const newSpeed = Math.max(50, this.speed * speedupFactor); // 最小加速到50ms

        debugLog(`吃到加速食物, 类型: ${foodStyle}, 速度变为 ${newSpeed}ms`)

        this.speed = newSpeed;
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
