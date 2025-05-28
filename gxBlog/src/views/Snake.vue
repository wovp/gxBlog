<template>
  <div class="snake-game-container">
    <!-- 游戏头部和信息区域 -->
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
        <div class="speed-container speed-container-custom">
          <span class="speed-label">速度:</span>
          <span class="speed-value">{{ getSpeedInMetersPerSecond() }} m/s</span>
        </div>
      </div>

      <!-- 加速能量条 -->
      <div class="speedup-container">
        <div class="speedup-header">
          <div class="speedup-icon" :class="{ 'active': gameController.snake.isSpeedingUp }">
            <div class="wing wing-left"></div>
            <div class="wing wing-right"></div>
            <div class="boost-icon"></div>
          </div>
          <div class="speedup-label">加速能量</div>
        </div>
        <div class="speedup-bar">
          <div class="speedup-fill" :style="{
            width: `${gameController.snake.speedUpEnergy}%`,
            backgroundColor: getSpeedUpColor()
          }">
            <div class="speedup-particles" v-if="gameController.snake.isSpeedingUp"></div>
          </div>
        </div>
        <div class="speedup-status">
          {{ gameController.snake.isSpeedingUp ? '加速中!' :
            gameController.snake.cooldownTimer ? '冷却中...' :
              gameController.snake.speedUpEnergy >= 100 ? '按K键加速' :
                '恢复中' }}
        </div>
      </div>
    </div>

    <div class="game-area-container">
      <div ref="gameCanvas" class="game-canvas"
        :style="{ width: `${gameController.canvasWidth}px`, height: `${gameController.canvasHeight}px` }" tabindex="0"
        @keydown="handleKeyDown">
        <!-- 蛇身体 -->
        <div v-for="(segment, index) in gameController.snake.body" :key="index" class="snake-segment" :class="{
          'snake-head': index === 0,
          'speeding-up': gameController.snake.isSpeedingUp,
          'direction-up': gameController.snake.direction === 'UP',
          'direction-down': gameController.snake.direction === 'DOWN',
          'direction-left': gameController.snake.direction === 'LEFT',
          'direction-right': gameController.snake.direction === 'RIGHT'
        }" :style="{
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
          <!-- 加速时的风效果 -->
          <div v-if="gameController.snake.isSpeedingUp" class="wind-effect" :class="{
            'wind-up': gameController.snake.direction === 'UP',
            'wind-down': gameController.snake.direction === 'DOWN',
            'wind-left': gameController.snake.direction === 'LEFT',
            'wind-right': gameController.snake.direction === 'RIGHT'
          }">
            <div class="wind-line"></div>
            <div class="wind-line"></div>
            <div class="wind-line"></div>
          </div>
        </div>

        <!-- 食物 -->
        <div v-for="(food, foodIndex) in gameController.foods" :key="foodIndex" class="food" :class="{
          'food-grow': food.type === 'grow',
          'food-shrink': food.type === 'shrink',
          'food-slow': food.type === 'slow',
          'food-fast': food.type === 'fast'
        }" :style="{
          left: `${food.x * gameController.gridSize}px`,
          top: `${food.y * gameController.gridSize}px`,
          width: `${gameController.gridSize}px`,
          height: `${gameController.gridSize}px`
        }">
          <div class="food-inner">
            <!-- 增加长度食物图标 -->
            <svg v-if="food.type === 'grow'" class="food-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <!-- 水果图标 - 根据degree值显示不同水果 -->
              <!-- 香蕉 (degree 0-2) -->
              <g v-if="food.degree >= 0 && food.degree <= 2">
                <path
                  d="M7,15C5.34,15 4,13.66 4,12C4,11.25 4.27,10.56 4.71,10C4.27,9.44 4,8.75 4,8C4,6.34 5.34,5 7,5C8.66,5 10,6.34 10,8C10,8.75 9.73,9.44 9.29,10C9.73,10.56 10,11.25 10,12C10,13.66 8.66,15 7,15M7,13C7.55,13 8,12.55 8,12C8,11.45 7.55,11 7,11C6.45,11 6,11.45 6,12C6,12.55 6.45,13 7,13M7,7C6.45,7 6,7.45 6,8C6,8.55 6.45,9 7,9C7.55,9 8,8.55 8,8C8,7.45 7.55,7 7,7M19,12C19,15.87 15.87,19 12,19C9.5,19 7.33,17.7 6.14,15.73C6.58,15.91 7.04,16 7.5,16C9.33,16 10.83,14.67 11,13C11.17,14.67 12.67,16 14.5,16C16.33,16 17.83,14.67 18,13C18.17,14.67 19.67,16 21.5,16C21.96,16 22.42,15.91 22.86,15.73C21.67,17.7 19.5,19 17,19C14.13,19 11,15.87 11,12C11,8.13 14.13,5 18,5C19.5,5 20.92,5.33 22.14,5.73C20.97,3.7 18.79,2 16.24,2C12.37,2 9.24,5.13 9.24,9C9.24,10.45 9.77,11.79 10.66,12.86C9.77,13.93 9.24,15.27 9.24,16.72C9.24,17.5 9.4,18.23 9.66,18.92C6.55,17.5 4.24,14.03 4.24,10C4.24,4.5 8.74,0 14.24,0C19.74,0 24.24,4.5 24.24,10C24.24,14.03 21.93,17.5 18.82,18.92C19.08,18.23 19.24,17.5 19.24,16.72C19.24,15.27 18.71,13.93 17.82,12.86C18.71,11.79 19.24,10.45 19.24,9C19.24,5.13 16.11,2 12.24,2C9.68,2 7.5,3.7 6.33,5.73C7.56,5.33 8.97,5 10.47,5C14.34,5 17.47,8.13 17.47,12C17.47,15.87 14.34,19 10.47,19C7.97,19 5.8,17.3 4.63,15.27C5.87,14.87 7.28,14.54 8.78,14.54C12.65,14.54 15.78,17.67 15.78,21.54C15.78,22.33 15.62,23.08 15.36,23.77C18.47,22.35 20.78,18.88 20.78,14.85C20.78,9.35 16.28,4.85 10.78,4.85C5.28,4.85 0.78,9.35 0.78,14.85C0.78,18.88 3.09,22.35 6.2,23.77C5.94,23.08 5.78,22.33 5.78,21.54C5.78,17.67 8.91,14.54 12.78,14.54C14.28,14.54 15.69,14.87 16.93,15.27C15.76,17.3 13.59,19 11.09,19C7.22,19 4.09,15.87 4.09,12C4.09,8.13 7.22,5 11.09,5C12.59,5 14.01,5.33 15.23,5.73C14.06,3.7 11.88,2 9.33,2C5.46,2 2.33,5.13 2.33,9C2.33,12.87 5.46,16 9.33,16C9.79,16 10.25,15.91 10.69,15.73C9.5,17.7 7.33,19 4.83,19C1.96,19 -1.17,15.87 -1.17,12C-1.17,8.13 1.96,5 4.83,5C6.33,5 7.75,5.33 8.97,5.73C7.8,3.7 5.62,2 3.07,2C-0.8,2 -3.93,5.13 -3.93,9C-3.93,12.87 -0.8,16 3.07,16C3.53,16 3.99,15.91 4.43,15.73C3.24,17.7 1.07,19 -1.43,19C-4.3,19 -7.43,15.87 -7.43,12C-7.43,8.13 -4.3,5 -1.43,5C0.07,5 1.49,5.33 2.71,5.73C1.54,3.7 -0.64,2 -3.19,2C-7.06,2 -10.19,5.13 -10.19,9C-10.19,12.87 -7.06,16 -3.19,16C-2.73,16 -2.27,15.91 -1.83,15.73C-3.02,17.7 -5.19,19 -7.69,19C-10.56,19 -13.69,15.87 -13.69,12C-13.69,8.13 -10.56,5 -7.69,5C-6.19,5 -4.77,5.33 -3.55,5.73C-4.72,3.7 -6.9,2 -9.45,2C-13.32,2 -16.45,5.13 -16.45,9C-16.45,12.87 -13.32,16 -9.45,16C-8.99,16 -8.53,15.91 -8.09,15.73C-9.28,17.7 -11.45,19 -13.95,19C-16.82,19 -19.95,15.87 -19.95,12C-19.95,8.13 -16.82,5 -13.95,5C-12.45,5 -11.03,5.33 -9.81,5.73C-10.98,3.7 -13.16,2 -15.71,2C-19.58,2 -22.71,5.13 -22.71,9C-22.71,12.87 -19.58,16 -15.71,16C-15.25,16 -14.79,15.91 -14.35,15.73C-15.54,17.7 -17.71,19 -20.21,19C-23.08,19 -26.21,15.87 -26.21,12C-26.21,8.13 -23.08,5 -20.21,5"
                  fill="#FFE135" />
              </g>
              <!-- 番茄 (degree 3-5) -->
              <g v-else-if="food.degree >= 3 && food.degree <= 5">
                <circle cx="12" cy="12" r="10" fill="#E53935" />
                <path
                  d="M12,2C6.48,2 2,6.48 2,12C2,17.52 6.48,22 12,22C17.52,22 22,17.52 22,12C22,6.48 17.52,2 12,2M12,20C7.58,20 4,16.42 4,12C4,7.58 7.58,4 12,4C16.42,4 20,7.58 20,12C20,16.42 16.42,20 12,20M15,6.5L14.38,7.12C13.63,6.43 12.63,6 11.5,6C9.02,6 7,8.02 7,10.5C7,12.98 9.02,15 11.5,15C12.83,15 14,14.47 14.83,13.62L14,13.25C13.46,13.82 12.53,14.25 11.5,14.25C9.43,14.25 7.75,12.57 7.75,10.5C7.75,8.43 9.43,6.75 11.5,6.75C12.33,6.75 13.08,7.05 13.67,7.53L13.05,8.15L15,8.5"
                  fill="#4CAF50" />
              </g>
              <!-- 桃子 (degree 6-8) -->
              <g v-else-if="food.degree >= 6 && food.degree <= 8">
                <path
                  d="M12,2C9.3,2 7.1,4.1 7,6.7C4.7,7.1 3,9.2 3,11.5C3,14 5,16 7.5,16H18.5C21,16 23,14 23,11.5C23,9.2 21.3,7.1 19,6.7C18.9,4.1 16.7,2 14,2H12M12,4H14C15.7,4 17,5.3 17,7H18C19.7,7 21,8.3 21,10C21,11.7 19.7,13 18,13H8C6.3,13 5,11.7 5,10C5,8.3 6.3,7 8,7H9C9,5.3 10.3,4 12,4M7.5,18C5,18 3,20 3,22.5V24H20V22.5C20,20 18,18 15.5,18H7.5Z"
                  fill="#FFCDD2" />
              </g>
              <!-- 西瓜 (degree 9-10) -->
              <g v-else>
                <circle cx="12" cy="12" r="10" fill="#4CAF50" />
                <circle cx="12" cy="12" r="8" fill="#E53935" />
                <path
                  d="M12,4C7.58,4 4,7.58 4,12C4,16.42 7.58,20 12,20C16.42,20 20,16.42 20,12C20,7.58 16.42,4 12,4M12,6C15.31,6 18,8.69 18,12C18,15.31 15.31,18 12,18C8.69,18 6,15.31 6,12C6,8.69 8.69,6 12,6M12,8C9.79,8 8,9.79 8,12C8,14.21 9.79,16 12,16C14.21,16 16,14.21 16,12C16,9.79 14.21,8 12,8M12,10C13.1,10 14,10.9 14,12C14,13.1 13.1,14 12,14C10.9,14 10,13.1 10,12C10,10.9 10.9,10 12,10Z"
                  fill="#000" fill-opacity="0.2" />
              </g>
            </svg>

            <!-- 减少长度食物图标 -->
            <svg v-else-if="food.type === 'shrink'" class="food-icon" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <!-- 书本 (degree -1 到 -3) -->
              <g v-if="food.degree >= -3 && food.degree <= -1">
                <path
                  d="M21,5C19.89,4.65 18.67,4.5 17.5,4.5C15.55,4.5 13.45,4.9 12,6C10.55,4.9 8.45,4.5 6.5,4.5C4.55,4.5 2.45,4.9 1,6V20.65C1,20.9 1.25,21.15 1.5,21.15C1.6,21.15 1.65,21.1 1.75,21.1C3.1,20.45 5.05,20 6.5,20C8.45,20 10.55,20.4 12,21.5C13.35,20.65 15.8,20 17.5,20C19.15,20 20.85,20.3 22.25,21.05C22.35,21.1 22.4,21.1 22.5,21.1C22.75,21.1 23,20.85 23,20.6V6C22.4,5.55 21.75,5.25 21,5M21,18.5C19.9,18.15 18.7,18 17.5,18C15.8,18 13.35,18.65 12,19.5V8C13.35,7.15 15.8,6.5 17.5,6.5C18.7,6.5 19.9,6.65 21,7V18.5Z"
                  fill="#795548" />
              </g>
              <!-- 电脑 (degree -4 到 -6) -->
              <g v-else-if="food.degree >= -6 && food.degree <= -4">
                <path
                  d="M4,6H20V16H4M20,18A2,2 0 0,0 22,16V6C22,4.89 21.1,4 20,4H4C2.89,4 2,4.89 2,6V16A2,2 0 0,0 4,18H0V20H24V18H20Z"
                  fill="#607D8B" />
              </g>
              <!-- 粑粑 (degree -7 到 -8) -->
              <g v-else-if="food.degree >= -8 && food.degree <= -7">
                <path
                  d="M12,2C14.21,2 16,3.79 16,6C16,7.68 14.96,9.13 13.5,9.68C13.5,9.68 14,10.5 14,12C14,13.5 13.5,14.32 13.5,14.32C14.96,14.87 16,16.32 16,18C16,20.21 14.21,22 12,22C9.79,22 8,20.21 8,18C8,16.32 9.04,14.87 10.5,14.32C10.5,14.32 10,13.5 10,12C10,10.5 10.5,9.68 10.5,9.68C9.04,9.13 8,7.68 8,6C8,3.79 9.79,2 12,2M12,4C10.9,4 10,4.9 10,6C10,7.1 10.9,8 12,8C13.1,8 14,7.1 14,6C14,4.9 13.1,4 12,4M12,18C13.1,18 14,17.1 14,16C14,14.9 13.1,14 12,14C10.9,14 10,14.9 10,16C10,17.1 10.9,18 12,18Z"
                  fill="#795548" />
              </g>
              <!-- 地雷 (degree -9 到 -10) -->
              <g v-else>
                <path
                  d="M17,14V17H14V19H17V22H19V19H22V17H19V14H17M5,3H19C20.1,3 21,3.9 21,5V12.8C20.4,12.3 19.7,11.9 19,11.6V5H5V19H11.6C11.9,19.7 12.3,20.4 12.8,21H5C3.9,21 3,20.1 3,19V5C3,3.9 3.9,3 5,3Z"
                  fill="#F44336" />
              </g>
            </svg>

            <!-- 加速度食物图标 -->
            <svg v-else-if="food.type === 'fast'" class="food-icon" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <!-- 飞机 (degree 21-24) -->
              <g v-if="food.degree >= 21 && food.degree <= 24">
                <path
                  d="M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z"
                  fill="#2196F3" />
              </g>
              <!-- 火车 (degree 25-27) -->
              <g v-else-if="food.degree >= 25 && food.degree <= 27">
                <path
                  d="M18,10H6V5H18M12,17C10.89,17 10,16.1 10,15C10,13.89 10.89,13 12,13A2,2 0 0,1 14,15A2,2 0 0,1 12,17M4,15.5A3.5,3.5 0 0,0 7.5,19L6,20.5V21H18V20.5L16.5,19A3.5,3.5 0 0,0 20,15.5V5C20,1.5 16.42,1 12,1C7.58,1 4,1.5 4,5V15.5Z"
                  fill="#F44336" />
              </g>
              <!-- 汽车 (degree 28-30) -->
              <g v-else>
                <path
                  d="M18,18.5A1.5,1.5 0 0,1 16.5,17A1.5,1.5 0 0,1 18,15.5A1.5,1.5 0 0,1 19.5,17A1.5,1.5 0 0,1 18,18.5M19.5,9.5L21.46,12H17V9.5M6,18.5A1.5,1.5 0 0,1 4.5,17A1.5,1.5 0 0,1 6,15.5A1.5,1.5 0 0,1 7.5,17A1.5,1.5 0 0,1 6,18.5M20,8L23,12V17H21A3,3 0 0,1 18,20A3,3 0 0,1 15,17H9A3,3 0 0,1 6,20A3,3 0 0,1 3,17H1V6C1,4.89 1.89,4 3,4H17V8H20Z"
                  fill="#FFC107" />
              </g>
            </svg>

            <!-- 减速度食物图标 -->
            <svg v-else-if="food.type === 'slow'" class="food-icon" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <!-- 泥巴 (degree 11-15) -->
              <g v-if="food.degree >= 11 && food.degree <= 15">
                <path
                  d="M12,3C7.03,3 3,7.03 3,12C3,16.97 7.03,21 12,21C16.97,21 21,16.97 21,12C21,7.03 16.97,3 12,3M12,19C8.14,19 5,15.86 5,12C5,8.14 8.14,5 12,5C15.86,5 19,8.14 19,12C19,15.86 15.86,19 12,19M12,7C9.24,7 7,9.24 7,12C7,14.76 9.24,17 12,17C14.76,17 17,14.76 17,12C17,9.24 14.76,7 12,7M12,15C10.34,15 9,13.66 9,12C9,10.34 10.34,9 12,9C13.66,9 15,10.34 15,12C15,13.66 13.66,15 12,15Z"
                  fill="#795548" />
              </g>
              <!-- 炸弹 (degree 16-20) -->
              <g v-else>
                <path
                  d="M11.25,6A3.25,3.25 0 0,1 14.5,2.75A3.25,3.25 0 0,1 17.75,6C17.75,6.42 18.08,6.75 18.5,6.75C18.92,6.75 19.25,6.42 19.25,6V5.25H20.75V6A2.25,2.25 0 0,1 18.5,8.25A2.25,2.25 0 0,1 16.25,6A1.75,1.75 0 0,0 14.5,4.25A1.75,1.75 0 0,0 12.75,6H14V7.29C16.89,8.15 19,10.83 19,14A7,7 0 0,1 12,21A7,7 0 0,1 5,14C5,10.83 7.11,8.15 10,7.29V6H11.25Z"
                  fill="#212121" />
              </g>
            </svg>
          </div>
        </div>

        <!-- 石头 -->
        <div v-for="(stone, index) in gameController.stones" :key="`stone-${index}`" class="stone" :style="{
          left: `${stone.x * gameController.gridSize}px`,
          top: `${stone.y * gameController.gridSize}px`,
          width: `${gameController.gridSize}px`,
          height: `${gameController.gridSize}px`
        }">
          <div class="stone-inner">
            <svg class="stone-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M21,16.5C21,16.88 20.79,17.21 20.47,17.38L12.57,21.82C12.41,21.94 12.21,22 12,22C11.79,22 11.59,21.94 11.43,21.82L3.53,17.38C3.21,17.21 3,16.88 3,16.5V7.5C3,7.12 3.21,6.79 3.53,6.62L11.43,2.18C11.59,2.06 11.79,2 12,2C12.21,2 12.41,2.06 12.57,2.18L20.47,6.62C20.79,6.79 21,7.12 21,7.5V16.5M12,4.15L5,8.09V15.91L12,19.85L19,15.91V8.09L12,4.15Z"
                class="stone-outline" />
              <path
                d="M12,4.15L5,8.09V15.91L12,19.85L19,15.91V8.09L12,4.15M12,6.23L17,9.11V14.89L12,17.77L7,14.89V9.11L12,6.23Z"
                class="stone-fill" />
              <path
                d="M12,6.23L17,9.11V14.89L12,17.77L7,14.89V9.11L12,6.23M12,8.31L14.5,10V14L12,15.69L9.5,14V10L12,8.31Z"
                class="stone-inner-fill" />
            </svg>
          </div>
        </div>

        <!-- 预警标记 -->
        <div v-if="gameController.currentWarning" class="warning" :style="{
          left: `${gameController.currentWarning.x * gameController.gridSize}px`,
          top: `${gameController.currentWarning.y * gameController.gridSize}px`,
          width: `${gameController.gridSize}px`,
          height: `${gameController.gridSize}px`
        }">
          <div class="warning-inner">
            <svg class="warning-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16" class="warning-outline" />
              <path d="M12,6L19.53,19H4.47L12,6" class="warning-fill" />
              <path d="M11,10V14H13V10H11M11,16V18H13V16H11" class="warning-symbol" />
            </svg>
          </div>
        </div>
      </div>

      <!-- 游戏控制按钮 -->
      <div class="game-controls">
        <n-button class="control-btn" :class="{ 'btn-active': !gameController.isRunning }" @click="handleStartGame"
          :disabled="gameController.isRunning">
          <div class="btn-content">
            <span class="btn-text">开始游戏</span>
            <span v-if="!gameController.isRunning" class="btn-status">就绪</span>
          </div>
        </n-button>
        <n-button class="control-btn" :class="{ 'btn-active': gameController.isRunning }"
          @click="gameController.pauseGame()" :disabled="!gameController.isRunning">
          <div class="btn-content">
            <span class="btn-text">暂停游戏</span>
            <span v-if="gameController.isRunning" class="btn-status">游戏中</span>
          </div>
        </n-button>
        <n-button class="control-btn" @click="handleResetGame">
          <div class="btn-content">
            <span class="btn-text">重新开始</span>
          </div>
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
        <n-button class="restart-btn" @click="handleRestart">
          <div class="btn-content">
            <span class="btn-text">再来一局</span>
          </div>
        </n-button>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { NButton, NModal, NIcon } from 'naive-ui';
import { ArrowUpOutline, ArrowDownOutline, ArrowBackOutline, ArrowForwardOutline } from '@vicons/ionicons5';
import { debugLog } from '../utils/debug';
import { Direction, FoodType } from '../model/SnakeModel';
import { GameController } from '../model/SnakeGameController';

// 音效对象
const audioEatGrow = ref<HTMLAudioElement | null>(null);
const audioEatShrink = ref<HTMLAudioElement | null>(null);
const audioEatFast = ref<HTMLAudioElement | null>(null);
const audioEatSlow = ref<HTMLAudioElement | null>(null);


// 组件逻辑
const gameCanvas = ref<HTMLElement | null>(null);
const showGameOver = ref(false);

// 创建游戏控制器
const gameController = ref<GameController>(new GameController(20, () => {
  showGameOver.value = true;
}));

// 设置食物碰撞回调函数
gameController.value.setFoodCollisionCallback = (foodType: FoodType) => {
  // 播放对应类型的食物音效
  playFoodSound(foodType);
};

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
    case 'k': // 加速
      if (gameController.value.isRunning) {
        const activated = gameController.value.activateSpeedUp();
        if (activated) {
          debugLog(`用户按下K键，激活加速`);
        }
      }
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

// 计算加速条颜色
const getSpeedUpColor = () => {
  const energy = gameController.value.snake.speedUpEnergy;

  if (gameController.value.snake.isSpeedingUp) {
    return '#ff9500'; // 橙色 - 加速中
  } else if (gameController.value.snake.cooldownTimer) {
    return '#e74c3c'; // 红色 - 冷却中
  } else if (energy >= 100) {
    return '#ff7700'; // 深橙色 - 已满
  } else {
    // 渐变色：从浅橙色到深橙色
    return `linear-gradient(90deg, #ffcc00 ${energy}%, #ff9500 ${energy}%)`;
  }
};

// 将毫秒刷新速度转换为米/秒的移动速度
const getSpeedInMetersPerSecond = () => {
  // 基础转换：毫秒越小，速度越快
  // 假设1000ms对应1m/s，200ms对应5m/s
  const baseSpeed = 1000 / gameController.value.snake.currentSpeed;

  // 四舍五入到一位小数
  return Math.round(baseSpeed * 10) / 10;
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

// 播放食物音效的方法
const playFoodSound = (foodType: FoodType) => {
  switch (foodType) {
    case FoodType.GROW:
      if (audioEatGrow.value) {
        audioEatGrow.value.currentTime = 0;
        audioEatGrow.value.play();
      }
      break;
    case FoodType.SHRINK:
      if (audioEatShrink.value) {
        audioEatShrink.value.currentTime = 0;
        audioEatShrink.value.play();
      }
      break;
    case FoodType.FAST:
      if (audioEatFast.value) {
        audioEatFast.value.currentTime = 0;
        audioEatFast.value.play();
      }
      break;
    case FoodType.SLOW:
      if (audioEatSlow.value) {
        audioEatSlow.value.currentTime = 0;
        audioEatSlow.value.play();
      }
      break;
  }
};

onMounted(() => {
  // 设置焦点以捕获键盘事件
  if (gameCanvas.value) {
    gameCanvas.value.focus();
  }

  // 添加全局键盘事件监听
  window.addEventListener('keydown', handleKeyDown);

  // 初始化音频对象
  audioEatGrow.value = new Audio('/sounds/eat-grow.mp3');
  audioEatShrink.value = new Audio('/sounds/eat-shrink.mp3');
  audioEatFast.value = new Audio('/sounds/eat-fast.mp3');
  audioEatSlow.value = new Audio('/sounds/eat-slow.mp3');
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
  overflow: visible;
}

.snake-head {
  background: linear-gradient(135deg, #3498db, #2980b9);
  border-radius: 8px;
  z-index: 2;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

/* 加速状态的蛇身体样式 */
.snake-segment.speeding-up {
  filter: blur(1px) brightness(1.2);
  box-shadow: 0 2px 15px rgba(46, 204, 113, 0.6);
}

.snake-head.speeding-up {
  filter: blur(1px) brightness(1.3);
  box-shadow: 0 2px 15px rgba(52, 152, 219, 0.7);
}



/* 风效果样式 */
.wind-effect {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: visible;
  z-index: -1;
}

/* 默认风向（向右移动时的风效果） */
.wind-effect {
  left: -100%;
  top: 0;
}

/* 根据方向调整风效果位置 */
.wind-effect.wind-up {
  left: 0;
  top: 100%;
  width: 100%;
  height: 100%;
  transform: rotate(90deg);
  transform-origin: center top;
}

.wind-effect.wind-down {
  left: 0;
  top: -100%;
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
  transform-origin: center bottom;
}

.wind-effect.wind-left {
  left: 100%;
  top: 0;
  transform: rotate(180deg);
}

.wind-effect.wind-right {
  left: -100%;
  top: 0;
}

.wind-line {
  position: absolute;
  height: 2px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.8), transparent);
  width: 100%;
  left: 0;
  opacity: 0;
  animation: wind-animation 0.5s infinite;
}

.wind-line:nth-child(1) {
  top: 20%;
  animation-delay: 0s;
  width: 80%;
}

.wind-line:nth-child(2) {
  top: 50%;
  animation-delay: 0.15s;
  width: 100%;
}

.wind-line:nth-child(3) {
  top: 80%;
  animation-delay: 0.3s;
  width: 60%;
}

@keyframes wind-animation {
  0% {
    transform: translateX(0);
    opacity: 0;
  }

  20% {
    opacity: 0.8;
  }

  100% {
    transform: translateX(-20px);
    opacity: 0;
  }
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
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
}

.food-inner {
  width: 90%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  animation: pulse 1s infinite alternate;
  background-color: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(2px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: inset 0 0 8px rgba(255, 255, 255, 0.5);
}

.food-icon {
  width: 80%;
  height: 80%;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.3));
  animation: rotate 10s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  from {
    transform: scale(0.85);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  }

  to {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
  }
}

.game-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.control-btn {
  min-width: 160px;
  font-weight: bold;
  font-size: 1.2rem;
  padding: 1rem 1.8rem;
  border-radius: 30px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #3a7bd5, #2c3e50);
  border: 2px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.restart-btn {
  margin-top: 1.5rem;
  padding: 1rem 1.8rem;
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 30px;
  background: linear-gradient(135deg, #3a7bd5, #2c3e50);
  color: white;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  border: 2px solid rgba(255, 255, 255, 0.1);
  min-width: 160px;
}

.control-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.control-btn:active {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.btn-active {
  background: linear-gradient(135deg, #11998e, #38ef7d);
  box-shadow: 0 8px 20px rgba(56, 239, 125, 0.3), inset 0 0 10px rgba(255, 255, 255, 0.2);
}

.btn-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.btn-text {
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  margin-bottom: 4px;
}

.btn-status {
  font-size: 0.7rem;
  font-weight: normal;
  color: #ffcc00;
  background-color: rgba(0, 0, 0, 0.3);
  padding: 2px 8px;
  border-radius: 10px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  animation: pulse-status 1.5s infinite alternate;
}

@keyframes pulse-status {
  from {
    opacity: 0.7;
    transform: scale(0.95);
  }

  to {
    opacity: 1;
    transform: scale(1.05);
  }
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

/* 旧的restart-btn样式已移至上方并更新 */

.restart-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, #11998e, #38ef7d);
}

.restart-btn:active {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

/* 确保按钮内容居中对齐 */
.btn-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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

.food-grow {
  background: linear-gradient(135deg, rgba(46, 204, 113, 0.8), rgba(39, 174, 96, 0.9));
  box-shadow: 0 0 15px rgba(46, 204, 113, 0.6);
}

.food-shrink {
  background: linear-gradient(135deg, rgba(231, 76, 60, 0.8), rgba(192, 57, 43, 0.9));
  box-shadow: 0 0 15px rgba(231, 76, 60, 0.6);
}

.food-slow {
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.8), rgba(41, 128, 185, 0.9));
  box-shadow: 0 0 15px rgba(52, 152, 219, 0.6);
}

.food-fast {
  background: linear-gradient(135deg, rgba(155, 89, 182, 0.8), rgba(142, 68, 173, 0.9));
  box-shadow: 0 0 15px rgba(155, 89, 182, 0.6);
}

.stone {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1;
  filter: drop-shadow(0 0 8px rgba(44, 62, 80, 0.7));
  animation: float 3s ease-in-out infinite;
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-2px);
  }
}

.stone-inner {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 3px;
}

.stone-icon {
  width: 90%;
  height: 90%;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.4));
}

.stone-outline {
  fill: #34495e;
  stroke: rgba(255, 255, 255, 0.5);
  stroke-width: 0.3;
}

.stone-fill {
  fill: #7f8c8d;
}

.stone-inner-fill {
  fill: #2c3e50;
}

.warning {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1;
  animation: pulse-warning 1s infinite alternate;
  filter: drop-shadow(0 0 10px rgba(231, 76, 60, 0.8));
}

@keyframes pulse-warning {
  0% {
    transform: scale(0.9);
    opacity: 0.7;
  }

  100% {
    transform: scale(1.1);
    opacity: 1;
  }
}

.warning-inner {
  width: 90%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: rotate-warning 8s linear infinite;
}

@keyframes rotate-warning {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.warning-icon {
  width: 90%;
  height: 90%;
}

.warning-outline {
  fill: none;
  stroke: #ffffff;
  stroke-width: 0.7;
}

.warning-fill {
  fill: rgba(231, 76, 60, 0.9);
}

.warning-symbol {
  fill: #ffffff;
}

@keyframes blink {
  from {
    opacity: 0.3;
    transform: scale(0.8);
  }

  to {
    opacity: 1;
    transform: scale(1.2);
  }
}

.speedup-container {
  margin: 1rem auto 0;
  width: 100%;
  max-width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.2);
  padding: 10px 15px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), inset 0 0 10px rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.speedup-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  width: 100%;
  justify-content: center;
}

.speedup-icon {
  position: relative;
  width: 24px;
  height: 24px;
  margin-right: 8px;
  transition: all 0.3s ease;
}

.boost-icon {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ff9500, #ff7700);
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(255, 149, 0, 0.7);
  z-index: 1;
}

.wing {
  position: absolute;
  top: 50%;
  width: 0;
  height: 0;
  opacity: 0;
  transition: all 0.3s ease;
  z-index: 0;
}

.wing-left {
  left: -5px;
  border-top: 8px solid transparent;
  border-right: 12px solid rgba(255, 149, 0, 0.7);
  border-bottom: 8px solid transparent;
  transform: translateY(-50%) scaleX(0);
  transform-origin: right center;
}

.wing-right {
  right: -5px;
  border-top: 8px solid transparent;
  border-left: 12px solid rgba(255, 149, 0, 0.7);
  border-bottom: 8px solid transparent;
  transform: translateY(-50%) scaleX(0);
  transform-origin: left center;
}

.speedup-icon.active .wing {
  opacity: 1;
  transform: translateY(-50%) scaleX(1);
}

.speedup-icon.active .wing-left {
  animation: wingFlap 0.5s infinite alternate;
}

.speedup-icon.active .wing-right {
  animation: wingFlap 0.5s infinite alternate;
}

@keyframes wingFlap {
  from {
    transform: translateY(-50%) scaleX(0.7);
  }

  to {
    transform: translateY(-50%) scaleX(1);
  }
}

.speedup-label {
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

.speedup-bar {
  width: 100%;
  height: 18px;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 9px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
  position: relative;
}

.speedup-fill {
  height: 100%;
  transition: width 0.1s linear;
  box-shadow: 0 0 10px rgba(255, 149, 0, 0.7);
  position: relative;
  overflow: hidden;
}

.speedup-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.3) 50%, transparent 100%);
  background-size: 200% 100%;
  animation: shimmer 1s infinite linear;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }

  100% {
    background-position: 200% 0;
  }
}

.speedup-status {
  margin-top: 6px;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

.speedup-container:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25), inset 0 0 15px rgba(255, 255, 255, 0.15);
}

.score-container,
.level-container,
.speed-container-custom {
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
.level-container:hover,
.speed-container-custom:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25), inset 0 0 15px rgba(255, 255, 255, 0.15);
}

.score-label,
.level-label,
.speed-label {
  font-weight: bold;
  margin-right: 0.5rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
}

.score-value,
.level-value,
.speed-value {
  font-size: 1.3rem;
  font-weight: bold;
  color: #ffcc00;
  text-shadow: 0 0 5px rgba(255, 204, 0, 0.5);
}
</style>
