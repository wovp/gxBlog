import Mock from 'mockjs'
import { getRandomCoverImage } from '../assets/imageResources'

// 文章列表数据
Mock.mock('/api/articles', 'get', {
  'code': 200,
  'message': 'success',
  'data|10': [{
    'id|+1': 1,
    'title': '@ctitle(5, 20)',
    'content': '@cparagraph(10, 20)',
    'author': '@cname',
    'createTime': '@datetime',
    'tags|1-3': ['@cword(2, 4)'],
    'viewCount|100-1000': 100,
    'commentCount|10-100': 10,
    'coverImage': getRandomCoverImage()
  }]
})

// 文章详情数据
Mock.mock(/\/api\/article\/\d+/, 'get', {
  'code': 200,
  'message': 'success',
  'data': {
    'id': '@natural(1, 100)',
    'title': '@ctitle(10, 20)',
    'content': '@cparagraph(50, 100)',
    'author': '@cname',
    'createTime': '@datetime',
    'tags|1-3': ['@cword(2, 4)'],
    'viewCount|100-1000': 100,
    'commentCount|10-100': 10,
    'coverImage': getRandomCoverImage(),
    'comments|5-10': [{
      'id|+1': 1,
      'content': '@cparagraph(1, 3)',
      'author': '@cname',
      'createTime': '@datetime'
    }]
  }
})