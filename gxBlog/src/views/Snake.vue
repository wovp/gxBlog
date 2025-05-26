<template>
  <div class="snake-game-container">
    <div class="game-header">
      <h1 class="game-title">贪吃蛇小游戏</h1>
      <div class="game-info">
        <div class="score-container">
          <span class="score-label">得分:</span>
          <span class="score-value">{{ gameController.score }}</span>
        </div>
        <div class="level-container">
          <span class="level-label">等级:</span>
          <span class="level-value">{{ gameController.level }}</span>
        </div>
      </div>
    </div>

    <div class="game-area-container">
      <div ref="gameCanvas" class="game-canvas"
        :style="{ width: `${gameController.canvasWidth}px`, height: `${gameController.canvasHeight}px` }" tabindex="0"
        @keydown="handleKeyDown">
        <!-- 蛇身体 -->
        <div v-for="(segment, index) in gameController.snake.body" :key="index" class="snake-segment"
          :class="{ 'snake-head': index === 0 }" :style="{
            left: `${segment.x * gameController.gridSize}px`,
            top: `${segment.y * gameController.gridSize}px`,
            width: `${gameController.gridSize}px`,
            height: `${gameController.gridSize}px`,
            transform: index === 0 ? `rotate(${getHeadRotation()}deg)` : 'none'
          }">
          <div v-if="index === 0" class="snake-eyes">
            <div class="snake-eye"></div>
            <div class="snake-eye"></div>
          </div>
        </div>

        <!-- 食物 -->
        <div v-if="gameController.food" class="food" :style="{
          left: `${gameController.food.x * gameController.gridSize}px`,
          top: `${gameController.food.y * gameController.gridSize}px`,
          width: `${gameController.gridSize}px`,
          height: `${gameController.gridSize}px`
        }">
          <div class="food-inner"></div>
        </div>
      </div>

      <!-- 游戏控制按钮 -->
      <div class="game-controls">
        <n-button class="control-btn" @click="handleStartGame" :disabled="gameController.isRunning">
          开始游戏
        </n-button>
        <n-button class="control-btn" @click="gameController.pauseGame()" :disabled="!gameController.isRunning">
          暂停游戏
        </n-button>
        <n-button class="control-btn" @click="handleResetGame">
          重新开始
        </n-button>
      </div>

      <!-- 移动端控制按钮 -->
      <div class="mobile-controls">
        <div class="direction-controls">
          <n-button class="direction-btn up-btn" @click="handleDirectionClick('W')">
            <n-icon><arrow-up-outline /></n-icon>
            <span class="key-hint">W</span>
          </n-button>
          <div class="horizontal-controls">
            <n-button class="direction-btn left-btn" @click="handleDirectionClick('A')">
              <n-icon><arrow-back-outline /></n-icon>
              <span class="key-hint">A</span>
            </n-button>
            <n-button class="direction-btn right-btn" @click="handleDirectionClick('D')">
              <n-icon><arrow-forward-outline /></n-icon>
              <span class="key-hint">D</span>
            </n-button>
          </div>
          <n-button class="direction-btn down-btn" @click="handleDirectionClick('S')">
            <n-icon><arrow-down-outline /></n-icon>
            <span class="key-hint">S</span>
          </n-button>
        </div>
      </div>

      <!-- 游戏说明 -->
      <div class="game-instructions">
        <n-card class="instructions-card">
          <template #header>
            <div class="instructions-header">游戏说明</div>
          </template>
          <div class="instructions-content">
            <p><strong>控制方式：</strong> 使用 W、A、S、D 键控制蛇的移动方向</p>
            <p><strong>游戏规则：</strong> 吃到食物得分，撞墙或撞到自己游戏结束</p>
            <p><strong>等级提升：</strong> 每得50分升一级，移动速度会加快</p>
            <p><strong>空格键：</strong> 暂停/继续游戏</p>
          </div>
        </n-card>
      </div>
    </div>

    <!-- 游戏结束弹窗 -->
    <n-modal v-model:show="showGameOver" preset="card" title="游戏结束" class="game-over-modal" :mask-closable="false">
      <div class="game-over-content">
        <h2>游戏结束!</h2>
        <p>你的得分: {{ gameController.score }}</p>
        <p>你的等级: {{ gameController.level }}</p>
        <n-button class="restart-btn" @click="handleRestart">再来一局</n-button>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { NButton, NModal, NIcon } from 'naive-ui';
import { ArrowUpOutline, ArrowDownOutline, ArrowBackOutline, ArrowForwardOutline } from '@vicons/ionicons5';
import { debugLog } from '../utils/debug';

// 定义坐标接口
interface Position {
  x: number;
  y: number;
}

// 方向枚举
enum Direction {
  UP = 'UP',
  DOWN = 'DOWN',
  LEFT = 'LEFT',
  RIGHT = 'RIGHT',
}

// 蛇类
class Snake {
  body: Position[];
  direction: Direction;
  nextDirection: Direction;

  constructor() {
    // 初始化蛇的身体，从中间开始，长度为3
    this.body = [
      { x: 10, y: 10 },
      { x: 9, y: 10 },
      { x: 8, y: 10 }
    ];
    this.direction = Direction.RIGHT;
    this.nextDirection = Direction.RIGHT;
  }

  // 移动蛇
  move(food: Position | null): boolean {
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

    // 检查是否吃到食物
    let ateFood = false;
    if (food && head.x === food.x && head.y === food.y) {
      ateFood = true;
    } else {
      // 如果没有吃到食物，移除尾部
      this.body.pop();
    }

    return ateFood;
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
class Food {
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

// 游戏控制器类
class GameController {
  snake: Snake;
  food: Food | null;
  gridWidth: number;
  gridHeight: number;
  gridSize: number;
  canvasWidth: number;
  canvasHeight: number;
  score: number;
  level: number;
  speed: number;
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
    this.speed = 200; // 初始速度，毫秒
    this.isRunning = false;
    this.gameInterval = null;
    this.onGameOver = onGameOver;

    this.generateFood();
  }

  // 开始游戏
  startGame(): void {
    debugLog(`开始游戏, 蛇的身体为${this.snake.body}`)
    if (this.isRunning) return;

    this.isRunning = true;
    this.gameInterval = window.setInterval(() => this.gameLoop(), this.speed);
  }

  // 暂停游戏
  pauseGame(): void {
    if (!this.isRunning) return;

    this.isRunning = false;
    if (this.gameInterval !== null) {
      clearInterval(this.gameInterval);
      this.gameInterval = null;
    }
  }

  // 重置游戏
  resetGame(): void {
    this.pauseGame();
    this.snake = new Snake();
    this.generateFood();
    this.score = 0;
    this.level = 1;
    this.speed = 200;
  }

  // 游戏主循环
  gameLoop(): void {
    debugLog(`游戏主循环`)
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

  // 增加分数
  increaseScore(): void {
    this.score += 10;

    // 每50分升一级，提高速度
    if (this.score % 50 === 0) {
      this.level += 1;
      this.speed = Math.max(50, this.speed - 20); // 最快速度为50ms

      // 更新游戏速度
      if (this.gameInterval !== null) {
        clearInterval(this.gameInterval);
        this.gameInterval = window.setInterval(() => this.gameLoop(), this.speed);
      }
    }
  }

  // 游戏结束
  gameOver(): void {
    this.pauseGame();
    this.onGameOver();
  }
}

// 组件逻辑
const gameCanvas = ref<HTMLElement | null>(null);
const showGameOver = ref(false);

// 创建游戏控制器
const gameController = ref<GameController>(new GameController(20, () => {
  showGameOver.value = true;
}));

// 处理键盘事件
const handleKeyDown = (event: KeyboardEvent) => {
  switch (event.key.toLowerCase()) {
    case 'w': // 上
      gameController.value.snake.changeDirection(Direction.UP)
      debugLog(`接受键盘参数，向上`)
      break;
    case 's': // 下
      gameController.value.snake.changeDirection(Direction.DOWN);
      debugLog(`接受键盘参数，向下`)
      break;
    case 'a': // 左
      gameController.value.snake.changeDirection(Direction.LEFT);
      debugLog(`接受键盘参数，向左`)
      break;
    case 'd': // 右
      gameController.value.snake.changeDirection(Direction.RIGHT);
      debugLog(`接受键盘参数，向右`)
      break;
    // 保留方向键控制作为备选
    case 'arrowup':
      gameController.value.snake.changeDirection(Direction.UP);
      break;
    case 'arrowdown':
      gameController.value.snake.changeDirection(Direction.DOWN);
      break;
    case 'arrowleft':
      gameController.value.snake.changeDirection(Direction.LEFT);
      break;
    case 'arrowright':
      gameController.value.snake.changeDirection(Direction.RIGHT);
      break;
    case ' ': // 空格键
      if (gameController.value.isRunning) {
        gameController.value.pauseGame();
      } else {
        gameController.value.startGame();
        // 确保游戏画布获得焦点
        if (gameCanvas.value) {
          gameCanvas.value.focus();
        }
      }
      break;
  }
};

// 处理方向按钮点击,移动端专用
const handleDirectionClick = (direction: string) => {
  switch (direction) {
    case 'ArrowUp':
    case 'W':
      gameController.value.snake.changeDirection(Direction.UP);
      break;
    case 'ArrowDown':
    case 'S':
      gameController.value.snake.changeDirection(Direction.DOWN);
      break;
    case 'ArrowLeft':
    case 'A':
      gameController.value.snake.changeDirection(Direction.LEFT);
      break;
    case 'ArrowRight':
    case 'D':
      gameController.value.snake.changeDirection(Direction.RIGHT);
      break;
  }
};

// 获取蛇头旋转角度
const getHeadRotation = () => {
  switch (gameController.value.snake.direction) {
    case Direction.UP:
      return 270;
    case Direction.DOWN:
      return 90;
    case Direction.LEFT:
      return 180;
    case Direction.RIGHT:
      return 0;
  }
};

// 重新开始游戏
const handleRestart = () => {
  showGameOver.value = false;
  gameController.value.resetGame();
  gameController.value.startGame();
  // 确保游戏画布获得焦点以捕获键盘事件
  if (gameCanvas.value) {
    gameCanvas.value.focus();
  }
};

onMounted(() => {
  // 设置焦点以捕获键盘事件
  if (gameCanvas.value) {
    gameCanvas.value.focus();
  }

  // 添加全局键盘事件监听
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  // 清除游戏循环
  if (gameController.value.gameInterval !== null) {
    clearInterval(gameController.value.gameInterval);
  }

  // 移除全局键盘事件监听
  window.removeEventListener('keydown', handleKeyDown);
});

// 处理开始游戏按钮点击
const handleStartGame = () => {
  gameController.value.startGame();
  // 确保游戏画布获得焦点以捕获键盘事件
  if (gameCanvas.value) {
    gameCanvas.value.focus();
  }
};

// 处理重置游戏按钮点击
const handleResetGame = () => {
  gameController.value.resetGame();
  // 确保游戏画布获得焦点以捕获键盘事件
  if (gameCanvas.value) {
    gameCanvas.value.focus();
  }
};
</script>

<style scoped>
.snake-game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  min-height: 100vh;
  background: linear-gradient(135deg, #8e44ad 0%, #3498db 100%);
  font-family: 'Arial', sans-serif;
  color: #fff;
}

.game-header {
  text-align: center;
  margin-bottom: 2rem;
  width: 100%;
}

.game-title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5), 0 0 20px rgba(255, 255, 255, 0.3);
  font-weight: bold;
  letter-spacing: 2px;
}

.game-info {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.score-container,
.level-container {
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.2);
  padding: 0.7rem 1.5rem;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), inset 0 0 10px rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.score-container:hover,
.level-container:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25), inset 0 0 15px rgba(255, 255, 255, 0.15);
}

.score-label,
.level-label {
  font-weight: bold;
  margin-right: 0.5rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
}

.score-value,
.level-value {
  font-size: 1.3rem;
  font-weight: bold;
  color: #ffcc00;
  text-shadow: 0 0 5px rgba(255, 204, 0, 0.5);
}

.game-area-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  width: 100%;
  max-width: 800px;
}

.game-canvas {
  position: relative;
  background-color: rgba(0, 0, 0, 0.4);
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3), inset 0 0 15px rgba(255, 255, 255, 0.1);
  overflow: hidden;
  outline: none;
  border: 2px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.game-canvas:focus {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 255, 255, 0.3), inset 0 0 15px rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.snake-segment {
  position: absolute;
  background: linear-gradient(135deg, #2ecc71, #27ae60);
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.1s linear;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.snake-head {
  background: linear-gradient(135deg, #3498db, #2980b9);
  border-radius: 8px;
  z-index: 2;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.snake-eyes {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 100%;
  padding: 0 4px;
}

.snake-eye {
  width: 5px;
  height: 5px;
  background-color: white;
  border-radius: 50%;
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
}

.food {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1;
}

.food-inner {
  width: 75%;
  height: 75%;
  background: radial-gradient(circle, #f39c12, #e74c3c);
  border-radius: 50%;
  box-shadow: 0 0 15px rgba(243, 156, 18, 0.7);
  animation: pulse 0.8s infinite alternate;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

@keyframes pulse {
  from {
    transform: scale(0.85);
    box-shadow: 0 0 10px rgba(243, 156, 18, 0.5);
  }

  to {
    transform: scale(1.15);
    box-shadow: 0 0 20px rgba(243, 156, 18, 0.8);
  }
}

.game-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.control-btn {
  min-width: 120px;
  font-weight: bold;
  font-size: 1rem;
  padding: 0.6rem 1.2rem;
  border-radius: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.control-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

.mobile-controls {
  display: none;
  margin-top: 2rem;
  width: 100%;
  max-width: 300px;
}

.direction-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}

.horizontal-controls {
  display: flex;
  gap: 2rem;
}

.direction-btn {
  width: 60px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), inset 0 0 10px rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
  position: relative;
}

.direction-btn:active {
  transform: scale(0.95);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2), inset 0 0 5px rgba(255, 255, 255, 0.1);
}

.key-hint {
  position: absolute;
  bottom: -5px;
  font-size: 0.7rem;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  background: rgba(0, 0, 0, 0.3);
  padding: 2px 5px;
  border-radius: 4px;
}

.game-over-modal {
  width: 350px;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
}

.game-over-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1rem;
}

.game-over-content h2 {
  color: #e74c3c;
  margin-bottom: 1.5rem;
  font-size: 2rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.game-over-content p {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.restart-btn {
  margin-top: 1.5rem;
  padding: 0.7rem 1.5rem;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 30px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.restart-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

.game-instructions {
  margin-top: 2rem;
  width: 100%;
  max-width: 600px;
}

.instructions-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2), inset 0 0 15px rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.instructions-header {
  font-size: 1.3rem;
  font-weight: bold;
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  padding: 0.5rem 0;
}

.instructions-content {
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
}

.instructions-content p {
  margin-bottom: 0.5rem;
}

.instructions-content strong {
  color: #ffcc00;
  text-shadow: 0 0 5px rgba(255, 204, 0, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .snake-game-container {
    padding: 1rem;
  }

  .game-title {
    font-size: 2rem;
  }

  .game-info {
    gap: 1rem;
  }

  .mobile-controls {
    display: block;
    margin-top: 1.5rem;
  }

  .game-instructions {
    margin-top: 2.5rem;
  }

  .instructions-header {
    font-size: 1.2rem;
  }

  .instructions-content {
    font-size: 0.9rem;
  }
}
</style>
