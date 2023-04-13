import { createRouter, createWebHashHistory } from "vue-router"
// createRouter 用于创建路由的实例对象
// createWebHashHistory 用于指定路由的工作模式 (hash 模式)

// 导入需要切换的组件
import Login from './components/LoginPage.vue'
import About from './components/MyAbout.vue'
import Home from '@/Home/HomePage.vue'
import Course from '@/Home/course/CoursePage.vue'
import Homework from '@/Home/HoneworkPage.vue'
import Detail from "@/Home/SimilarityDetail.vue"
import CompareDetail from "@/Home/Compare/ComparePage.vue"
import Compare from "@/Home/SimilarityCompare.vue"
import StudentInfor from "@/Home/Compare/StudentInformation.vue"
import Infor from "@/Home/InformationPage.vue"
import StuHome from "@/Student/StuHome.vue"
import Movie from "@/components/MyMovie.vue"
import StuInformation from "@/Student/StuInformathon.vue"
import StuCourse from "@/Student/StuCourse.vue"
import StuHomework from "@/Student/StuHomework.vue"
import HomeworkDetail from "@/Student/HomeworkDetail.vue"
import SubmittedStuend from "@/Home/HomeworkSubmited.vue"
import SubmitView from "@/Home/SubmitView.vue"

// 创建路由实例对象
const router = createRouter({
    // 指定路由工作模式
    history: createWebHashHistory(),
    // 定义 hash 与组件之间的对应关系
    routes: [
        { path: '/', component: Login },
        { path: '/detail', component: Detail },
        { path: '/infor', component: StudentInfor },
        { path: '/comparepage', component: CompareDetail },
        { path: '/movie', component: Movie },
        { path: '/homeworkdetail', component: HomeworkDetail },
        { path: '/submitview', component: SubmitView },
        {
            path: '/home', component: Home, redirect: { name: "course" }, children: [
                { path: '/about', name: 'about', component: About },
                { path: '/course', name: 'course', component: Course },
                { path: '/homework', name: 'homework', component: Homework },
                { path: '/compare', name: 'compare', component: Compare },
                { path: '/information', component: Infor },
                { path: '/submitted', component: SubmittedStuend },

            ]
        },
        {
            path: '/stuhome', component: StuHome, redirect: { name: "stucourse" }, children: [
                { path: '/stucourse', name: 'stucourse', component: StuCourse },
                { path: '/stuinformation', component: StuInformation },
                { path: '/stuhomework', component: StuHomework }
            ]
        },
    ]
})

// 向外共享路由模块
export default router