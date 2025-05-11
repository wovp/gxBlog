/**
 * 标题ID生成工具函数
 * 用于生成唯一的标题ID，支持中文标题
 */

/**
 * 将文本转换为slug格式
 * @param text 标题文本
 * @returns 生成的slug
 */
export const generateSlug = (text: string): string => {
    // 首先尝试使用常规方法生成slug
    let slug = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w\-]/g, '');

    // 如果slug为空（可能是纯中文标题），则使用文本的哈希值作为ID
    if (!slug) {
        slug = 'heading-' + hashString(text);
    }

    // 添加随机后缀确保唯一性
    const randomSuffix = Math.random().toString(36).substring(2, 8);
    return `${slug}-${randomSuffix}`;
};

/**
 * 简单的字符串哈希函数
 * @param str 要哈希的字符串
 * @returns 哈希值的字符串表示
 */
export const hashString = (str: string): string => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // 转换为32位整数
    }
    return Math.abs(hash).toString(36);
};