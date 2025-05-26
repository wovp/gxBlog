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
        debugLog(`移动蛇`)
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
            // 根据食物类型增加不同长度
            if (food.style < 10) {
                this.growByFoodType(food.style);
            }
            // 处理速度
            else if (food.style < 20) {
                // 蛇身翻倍
                this.body = this.body.concat(this.body);
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
    style: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
        this.style = Math.floor(Math.random() * 3); // 随机生成食物样式
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

        return new Food(x, y);
    }
}