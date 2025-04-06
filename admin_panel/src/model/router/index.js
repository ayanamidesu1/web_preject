import {createRouter, createWebHistory} from 'vue-router'

const routes=[
    {
        path:'/',
        name:'index',
        children:[
            {
                path:'/',
                name:'',
                component:()=>import('@/components/index.vue'),
                children:[
                    {
                        path:'/',
                        name:'',
                        component:()=>import('@/components/content.vue'),
                        children:[
                            {
                                path:'/',
                                name:'user',
                                component:()=>import('@/components/model/user_control.vue')
                            },
                            {
                                path:'/ill',
                                name:'ill',
                                component:()=>import('@/components/model/ill_control.vue')
                            },
                            {
                                path:'/comic',
                                name:'comic',
                                component:()=>import('@/components/model/comic_control.vue')
                            },
                            {
                                path:'/novel',
                                name:'novel',
                                component:()=>import('@/components/model/novel_control.vue')
                            }
                        ]
                    }
                ]
            }
        ]
    },
    {
        path:'/login',
        name:'login',
        component:()=>import('@/components/model/login_page.vue')
    }
]
const router=createRouter({
    history:createWebHistory(),
    routes
})
export {router}