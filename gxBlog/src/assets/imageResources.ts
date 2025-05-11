/**
 * 本地图片资源列表
 */

// 文章封面图片列表
export const coverImages = [
  '/wallhaven-d8xvzm.jpg',
  '/wallhaven-je9d75.png',
  '/wallhaven-je9lmw.png',
  '/wallhaven-mlqydm.jpg',
  '/wallhaven-og97jp.jpg',
  '/wallhaven-rq36vm.jpg'
]

// 获取随机封面图片
export const getRandomCoverImage = (): string => {
  const randomIndex = Math.floor(Math.random() * coverImages.length)
  return coverImages[randomIndex]
}

// 头像图片列表
export const avatarImages = [
  '/vite.svg',
  '/header-backgroundPic.png'
]

// 获取随机头像图片
export const getRandomAvatarImage = (): string => {
  const randomIndex = Math.floor(Math.random() * avatarImages.length)
  return avatarImages[randomIndex]
}

// 背景图片列表
export const backgroundImages = [
  '/header-backgroundPic.png',
  '/wallhaven-mlqydm.jpg',
  '/wallhaven-og97jp.jpg'
]

// 获取随机背景图片
export const getRandomBackgroundImage = (): string => {
  const randomIndex = Math.floor(Math.random() * backgroundImages.length)
  return backgroundImages[randomIndex]
}