import { debugLog } from "../utils/debug";
import { Food, type Position, Snake } from "./SnakeModel";

// 游戏控制器类
export class GameController {
    snake: Snake;
    food: Food | null;
    stones: Position[]; // 石头位置
    stoneTimer: number | null; // 石头计时器
    currentWarning: Position | null; // 当前预警位置
    warningTimer: number | null; // 预警计时器
    gridWidth: number;
    gridHeight: number;
    gridSize: number;
    canvasWidth: number;
    canvasHeight: number;
    score: number;
    level: number;
    isRunning: boolean;
    gameInterval: number | null;
    onGameOver: () => void;

    constructor(gridSize: number, onGameOver: () => void) {
        this.gridSize = gridSize;
        this.gridWidth = 20;
        this.gridHeight = 15;
        this.canvasWidth = this.gridWidth * this.gridSize;
        this.canvasHeight = this.gridHeight * this.gridSize;
        this.snake = new Snake();
        this.food = null;
        this.score = 0;
        this.level = 1;
        this.isRunning = false;
        this.gameInterval = null;
        this.onGameOver = onGameOver;

        this.stones = [];
        this.stoneTimer = null;
        this.currentWarning = null;
        this.warningTimer = null;

        this.generateFood();
    }

    // 开始游戏
    startGame(): void {
        // debugLog(`开始游戏, 蛇的身体为${this.snake.body}`)
        if (this.isRunning) return;

        this.isRunning = true;
        this.gameInterval = window.setInterval(() => this.gameLoop(), this.snake.speed);

        // 如果没有石头计时器在运行，安排新的石头事件
        if (this.stoneTimer === null) {
            this.scheduleRandomStone();
        }
    }

    // 暂停游戏
    pauseGame(): void {
        if (!this.isRunning) return;

        this.isRunning = false;
        if (this.gameInterval !== null) {
            clearInterval(this.gameInterval);
            this.gameInterval = null;
        }

        // 暂停石头计时器
        if (this.stoneTimer !== null) {
            clearTimeout(this.stoneTimer);
            this.stoneTimer = null;
        }

        // 暂停预警计时器
        if (this.warningTimer !== null) {
            clearTimeout(this.warningTimer);
            this.warningTimer = null;
        }
    }

    // 重置游戏
    resetGame(): void {
        this.pauseGame();
        this.snake = new Snake();
        this.generateFood();
        this.score = 0;
        this.level = 1;
        this.snake.speed = 200;
    }

    // 生成石头
    generateStone(): void {
        if (this.currentWarning === null) {
            debugLog(`没有石头预警, 不生成石头`)
            return;
        }

        let x: number = this.currentWarning.x, y: number = this.currentWarning.y;
        // 添加石头位置
        this.stones.push({ x, y });
        debugLog(`生成石头, 位置: (${x}, ${y})`);

        // 清除预警
        this.currentWarning = null;

        // 安排下一次石头生成
        this.scheduleRandomStone();
    }

    // 安排随机石头事件
    scheduleRandomStone(): void {
        // 随机间隔 5-10 秒
        const interval = Math.floor(Math.random() * 5000) + 5000;

        this.stoneTimer = setTimeout(() => {
            if (!this.isRunning) {
                // 如果游戏已暂停，重新安排石头生成
                this.scheduleRandomStone();
                return;
            }

            // 显示预警
            this.showWarning();

            // 2秒后生成石头
            this.warningTimer = setTimeout(() => {
                this.generateStone();
            }, 2000);

        }, interval);
    }

    // 显示预警
    showWarning(): void {
        let validPosition = false;
        let x: number = 0, y: number = 0;

        // 确保预警位置不会在蛇身上
        while (!validPosition) {
            x = Math.floor(Math.random() * this.gridWidth);
            y = Math.floor(Math.random() * this.gridHeight);

            validPosition = !this.snake.body.some(segment => segment.x === x && segment.y === y);
        }

        // 设置当前预警位置
        this.currentWarning = { x, y };
        debugLog(`显示石头预警, 位置: (${x}, ${y})`);
    }


    // 游戏主循环
    gameLoop(): void {
        // 移动蛇并检查是否吃到食物
        const ateFood = this.snake.move(this.food);

        // 检查是否撞墙
        if (this.checkCollisionWithWall()) {
            this.gameOver();
            return;
        }

        // 检查是否撞到自己
        if (this.snake.checkCollisionWithSelf()) {
            this.gameOver();
            return;
        }

        // 检查是否撞到石头
        if (this.checkCollisionWithStones()) {
            this.gameOver();
            return;
        }

        // 如果吃到食物，生成新的食物并增加分数
        if (ateFood) {
            this.generateFood();
            this.increaseScore();
        }
    }

    // 生成食物
    generateFood(): void {
        this.food = Food.generateFood(this.snake, this.gridWidth, this.gridHeight);
    }

    // 检查是否撞墙
    checkCollisionWithWall(): boolean {
        const head = this.snake.body[0];
        return (
            head.x < 0 ||
            head.y < 0 ||
            head.x >= this.gridWidth ||
            head.y >= this.gridHeight
        );
    }

    // 检查是否撞到石头
    checkCollisionWithStones(): boolean {
        const head = this.snake.body[0];
        return this.stones.some(stone => stone.x === head.x && stone.y === head.y);
    }

    // 增加分数
    increaseScore(): void {
        this.score += 10;

        // 每50分升一级，提高速度
        if (this.score % 50 === 0) {
            this.level += 1;
            this.snake.speed = Math.max(50, this.snake.speed - 20); // 最快速度为50ms

            // 更新游戏速度
            if (this.gameInterval !== null) {
                clearInterval(this.gameInterval);
                this.gameInterval = window.setInterval(() => this.gameLoop(), this.snake.speed);
            }
        }
    }

    // 游戏结束
    gameOver(): void {
        this.pauseGame();
        this.onGameOver();
    }
}