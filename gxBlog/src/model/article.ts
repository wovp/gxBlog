// 定义文章接口
import { getRandomCoverImage } from '../assets/imageResources'

export class Article {
    id: number = -1
    title: string = "默认标题"
    content: string = "默认内容"
    author: string = "默认作者"
    createTime: string = "默认时间"
    tags: string[] = ["默认标签"]
    viewCount: number = 0
    commentCount: number = 0
    coverImage: string = getRandomCoverImage()
    comments: Array<{id: number, content: string, author: string, createTime: string}> = []
}