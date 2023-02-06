import { createRouter, createWebHashHistory } from "vue-router"
// createRouter 用于创建路由的实例对象
// createWebHashHistory 用于指定路由的工作模式 (hash 模式)

// 导入需要切换的组件
import Login from './components/LoginPage.vue'
import About from './components/MyAbout.vue'
import Home from '@/Home/HomePage.vue'
import Course from '@/Home/course/CoursePage.vue'
import Homework from '@/Home/HoneworkPage.vue'

// 创建路由实例对象
const router = createRouter({
    // 指定路由工作模式
    history: createWebHashHistory(),
    // 定义 hash 与组件之间的对应关系
    routes: [
        { path: '/', component: Login },
        {
            path: '/home', component: Home, redirect: { name: "course" }, children: [
                { path: '/about',name:'about', component: About },
                { path: '/course', name:'course',component: Course },
                { path: '/homework', name:'homework',component: Homework },
                

            ]
        },
    ]
})

// 向外共享路由模块
export default router