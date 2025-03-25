import {createRouter, createWebHistory} from 'vue-router';

const routes=[
    {
        path: '/',
        name: '',
        children:[
            {
               path:'',
               name:'',
               component:()=>import('@/components/root_page.vue'),//主页
               children:[
                {
                    path:'/',
                    name:'illustration',
                    component:()=>import('@/components/Illustration_page/Illustration_page.vue'),//插画
                }
               ] 
            }
        ]
    },
    {
        path:'/login',
        name:'login',
        component:()=>import('@/components/login/login_page.vue')//登录
    },
    {
        path:'/register',
        name:'register',
        component:()=>import('@/components/register/register_page.vue')//注册
    }
]
const router = createRouter({
    history: createWebHistory(),
    routes
})

export {router};