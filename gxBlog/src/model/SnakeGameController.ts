import { debugLog } from "../utils/debug";
import { Food, type Position, Snake, FoodType } from "./SnakeModel";

// 游戏控制器类
export class GameController {
    snake: Snake;
    foods: Food[]; // 改为食物数组
    foodTimer: number | null; // 食物生成计时器
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

    // 动画优化相关属性
    animationFrameId: number | null;
    lastFrameTime: number | null;

    // 食物碰撞回调函数
    foodCollisionCallback: ((foodType: FoodType) => void) | null = null;

    onGameOver: () => void;

    // 设置食物碰撞回调函数
    set setFoodCollisionCallback(callback: (foodType: FoodType) => void) {
        this.foodCollisionCallback = callback;
    }

    constructor(gridSize: number, onGameOver: () => void) {
        this.gridSize = gridSize;
        this.gridWidth = 40;
        this.gridHeight = 40;
        this.canvasWidth = this.gridWidth * this.gridSize;
        this.canvasHeight = this.gridHeight * this.gridSize;
        this.snake = new Snake();
        this.foods = []; // 初始化为空数组
        this.foodTimer = null;
        this.score = 0;
        this.level = 1;
        this.isRunning = false;
        this.gameInterval = null;
        this.onGameOver = onGameOver;

        // 石头相关属性
        this.stones = [];
        this.stoneTimer = null;
        this.currentWarning = null;
        this.warningTimer = null;

        // 动画优化相关属性
        this.animationFrameId = null;
        this.lastFrameTime = null;

        // 生成第一个食物
        this.generateFood();
        // 设置加速结束回调
        this.snake.setSpeedUpEndCallback(() => {
            this.onSnakeSpeedUpEnd();
        });
    }

    // 安全地更新游戏循环
    updateGameLoop(): void {
        // 重置帧计时器，确保立即更新
        this.lastFrameTime = performance.now();

        // 强制触发一次游戏循环，确保页面渲染
        this.gameLoop(performance.now());

        debugLog(`更新游戏循环速度为 ${this.snake.currentSpeed}ms`);
    }

    // 开始游戏
    startGame(): void {
        // debugLog(`开始游戏, 蛇的身体为${this.snake.body}`)
        if (this.isRunning) return;

        this.isRunning = true;

        this.lastFrameTime = performance.now();
        // 使用requestAnimationFrame替代setInterval
        this.gameLoop(performance.now());

        // 如果没有石头计时器在运行，安排新的石头事件
        if (this.stoneTimer === null) {
            this.scheduleRandomStone();
        }

        // 如果没有食物定时器在运行，启动食物生成定时器
        if (this.foodTimer === null) {
            this.scheduleFoodGeneration();
        }
    }

    // 暂停游戏
    pauseGame(): void {
        if (!this.isRunning) return;

        this.isRunning = false;
        // 取消动画帧
        if (this.animationFrameId !== null) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
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

        // 暂停食物生成定时器
        if (this.foodTimer !== null) {
            clearTimeout(this.foodTimer);
            this.foodTimer = null;
        }

        // 取消动画帧
        if (this.animationFrameId !== null) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }

    }

    // 重置游戏
    resetGame(): void {
        // 先暂停游戏
        this.pauseGame();

        // 重置游戏状态
        this.snake = new Snake();
        this.score = 0;
        this.level = 1;
        this.stones = [];
        this.currentWarning = null;

        // 重置食物
        this.foods = [];
        this.generateFood();

        // 设置加速结束回调
        this.snake.setSpeedUpEndCallback(() => {
            this.onSnakeSpeedUpEnd();
        });

        // 重置游戏循环状态
        this.lastFrameTime = null;
    }
    // -------------------------------------石头障碍部分------------------------------------//
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
    gameLoop(currentTime: number): void {

        // 记录当前帧ID
        this.animationFrameId = requestAnimationFrame(this.gameLoop.bind(this));

        // 计算时间差
        if (this.lastFrameTime === null) {
            this.lastFrameTime = currentTime;
            return;
        }

        const deltaTime = currentTime - this.lastFrameTime;
        if (deltaTime >= this.snake.currentSpeed) {
            debugLog(`游戏主循环，deltaTime: ${deltaTime}, 当前速度: ${this.snake.currentSpeed}`);

            // 更新上一帧时间
            this.lastFrameTime = currentTime;

            // 移动蛇
            this.snake.move(); // 先移动蛇，然后单独检查食物碰撞

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

            // 检查是否吃到食物
            this.checkFoodCollisions();
        }
    }

    // 生成食物
    generateFood(): void {
        const newFood = Food.generateFood(this.snake, this.gridWidth, this.gridHeight);
        this.foods.push(newFood);
        debugLog(`生成新食物，当前食物数量: ${this.foods.length}`);
    }

    // 安排食物生成
    scheduleFoodGeneration(): void {
        // 每5秒生成一个新食物
        this.foodTimer = setTimeout(() => {
            if (!this.isRunning) {
                // 如果游戏已暂停，不生成新食物
                return;
            }

            // 生成新食物
            this.generateFood();

            // 继续安排下一次食物生成
            this.scheduleFoodGeneration();
        }, 5000); // 5秒间隔
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
            // 调整蛇的基础速度
            const newBaseSpeed = Math.max(50, this.snake.baseSpeed - 10); // 每级减少10ms，最低50ms
            this.snake.adjustBaseSpeed(newBaseSpeed);

            debugLog(`升级! 等级: ${this.level}, 蛇的基础速度: ${this.snake.baseSpeed} ms, 当前速度: ${this.snake.currentSpeed} ms`);
            // 更新游戏速度
            if (this.gameInterval !== null) {
                // 安全地更新游戏循环
                this.updateGameLoop();
            }
        }
    }
    // 主动加速
    activateSpeedUp(): boolean {
        const activated = this.snake.activateSpeedUp();
        if (activated) {
            // 安全地更新游戏循环
            this.updateGameLoop();
        }
        return activated;
    }

    // 加速结束回调
    onSnakeSpeedUpEnd(): void {
        debugLog(`收到蛇加速结束通知，更新游戏循环速度`);

        // 更新游戏循环速度
        if (this.isRunning) {
            // 安全地更新游戏循环
            this.updateGameLoop();

        }
    }
    // 检查食物碰撞
    // TODO: 待优化，性能有问题
    checkFoodCollisions(): void {
        const head = this.snake.body[0];

        // 遍历所有食物，检查是否有碰撞
        for (let i = this.foods.length - 1; i >= 0; i--) {
            const food = this.foods[i];

            // 检查蛇头是否与食物碰撞
            if (head.x === food.x && head.y === food.y) {
                // 处理食物效果
                this.handleFoodEffect(food);

                // 从数组中移除被吃掉的食物
                this.foods.splice(i, 1);

                // 增加分数
                this.increaseScore();
            }
        }
    }

    // 处理食物效果
    handleFoodEffect(food: Food): void {
        // 根据食物类型应用不同效果
        switch (food.type) {
            case FoodType.GROW:
                // 增加长度
                this.snake.grow(food.degree);
                break;
            case FoodType.SHRINK:
                // 减少长度
                this.snake.shrink(Math.abs(food.degree));
                break;
            case FoodType.SLOW:
                // 减速
                this.snake.slow(food.degree - 10);
                break;
            case FoodType.FAST:
                // 加速
                this.snake.speedUp(food.degree - 20);
                break;
        }

        // 调用食物碰撞回调函数
        if (this.foodCollisionCallback) {
            this.foodCollisionCallback(food.type);
        }

        debugLog(`吃到食物类型: ${food.type}, 程度: ${food.degree} `);
    }

    // 游戏结束
    gameOver(): void {
        this.pauseGame();
        this.onGameOver();
    }
}