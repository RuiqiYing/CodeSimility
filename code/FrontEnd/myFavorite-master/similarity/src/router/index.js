import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            component: resolve => require(['../login.vue'], resolve)
        },
     
        {
            // path: '/admin',
            // component: resolve => require(['../admin/common/Home.vue'], resolve),
            // children:[
            //     {
            //         path: '/account_admin',
            //         component: resolve => require(['../admin/page/account_admin.vue'], resolve)
            //     },
            //     {
            //         path: '/favorite_admin',
            //         component: resolve => require(['../admin/page/favorite_admin.vue'], resolve)
            //     }
            // ]
        path: '/admin',
        name: 'admin',
        component: '../admin/common/Home.vue',
        //路由嵌套
        children:[
            {path: '/admin/menu1',component: () => import('../admin/page/account_admin.vue')},
            {path: '/admin/menu2',component: () => import('../admin/page/favorite_admin.vue')}
           
        ]
        }
    ]
})
