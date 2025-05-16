/**
 * SVG图标集合
 * 用于集中管理应用中使用的SVG图标
 */

// 定义图标组件接口
interface IconComponent {
    name: string;
    render: () => any; // Using 'any' instead of JSX.Element for Vue compatibility
}

// GitHub图标
export const GithubIcon: IconComponent = {
    name: 'github',
    render() {
        return (
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                    d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5c.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34c-.46-1.16-1.11-1.47-1.11-1.47c-.91-.62.07-.6.07-.6c1 .07 1.53 1.03 1.53 1.03c.87 1.52 2.34 1.07 2.91.83c.09-.65.35-1.09.63-1.34c-2.22-.25-4.55-1.11-4.55-4.92c0-1.11.38-2 1.03-2.71c-.1-.25-.45-1.29.1-2.64c0 0 .84-.27 2.75 1.02c.79-.22 1.65-.33 2.5-.33c.85 0 1.71.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02c.55 1.35.2 2.39.1 2.64c.65.71 1.03 1.6 1.03 2.71c0 3.82-2.34 4.66-4.57 4.91c.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"
                    fill="currentColor"
                />
            </svg>
        )
    }
}

// 过滤器图标
export const FilterIcon: IconComponent = {
    name: 'filter',
    render() {
        return (
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                    d="M20.52 3.449C20.192 3.16 19.76 3 19.28 3H4.72c-.48 0-.88.16-1.24.449c-.35.288-.56.64-.56 1.101c0 .288.07.56.18.8L9 13.601v6.649c0 .129.05.24.12.32c.08.08.17.13.28.13c.08 0 .17-.03.24-.08l2.26-1.27c.24-.129.36-.359.36-.649v-5.1l5.88-8.451c.12-.24.18-.511.18-.8c0-.46-.2-.812-.56-1.101z"
                    fill="currentColor"
                />
            </svg>
        )
    }
}

// 知乎图标
export const ZhihuIcon: IconComponent = {
    name: 'zhihu',
    render() {
        return (
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                    d="M7.5 6.75V0h9v6.75h-9zm9 3.75H24V24H0V10.5h7.5v6.75h9V10.5z"
                    fill="currentColor"
                />
            </svg>
        )
    }
}

// 网站/地球图标
export const GlobeIcon: IconComponent = {
    name: 'globe',
    render() {
        return (
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                    d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10s-4.477 10-10 10zm-2.29-2.333A17.9 17.9 0 0 1 8.027 13H4.062a8.008 8.008 0 0 0 5.648 6.667zM10.03 13c.151 2.439.848 4.73 1.97 6.752A15.905 15.905 0 0 0 13.97 13h-3.94zm9.908 0h-3.965a17.9 17.9 0 0 1-1.683 6.667A8.008 8.008 0 0 0 19.938 13zM4.062 11h3.965A17.9 17.9 0 0 1 9.71 4.333A8.008 8.008 0 0 0 4.062 11zm5.969 0h3.938A15.905 15.905 0 0 0 12 4.248A15.905 15.905 0 0 0 10.03 11zm4.259-6.667A17.9 17.9 0 0 1 15.973 11h3.965a8.008 8.008 0 0 0-5.648-6.667z"
                    fill="currentColor"
                />
            </svg>
        )
    }
}

// 导出所有图标集合
export const icons: Record<string, IconComponent> = {
    GithubIcon,
    FilterIcon,
    ZhihuIcon,
    GlobeIcon
}

export default icons