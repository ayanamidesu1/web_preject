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
                },
                {
                    path:'/comic',
                    name:'comic',
                    component:()=>import('@/components/cartoon/cartoon_page.vue')//漫画
                },
                {
                    path:'/novel',
                    name:'novel',
                    component:()=>import('@/components/novel_page/novel_page.vue')//小说
                },
                {
                    path:'/ill_content',
                    name:'ill_content',
                    component:()=>import('@/components/content_page/ill_page/ill_index.vue')//插画内容
                },
                {
                    path:'/comic_content',
                    name:'comic_content',
                    component:()=>import('@/components/content_page/comic_page/comic_index.vue')//漫画内容
                },
                {
                    path:'/novel_content',
                    name:'novel_content',
                    component:()=>import('@/components/content_page/novel_page/novel_index.vue')//小说内容
                },
                {
                    path:'/self_user_center',
                    name:'self_user_center',
                    component:()=>import('@/components/user_center_page/user_center_page.vue')//个人中心
                },
                {
                    path:'/comic_content',
                    name:'comic_content',
                    component:()=>import('@/components/content_page/comic_page/comic_index.vue')//漫画内容
                },{
                    path:'/novel_content',
                    name:'novel_content',
                    component:()=>import('@/components/content_page/novel_page/novel_index.vue')//小说内容
                },{
                    path:'/other_user_center',
                    name:'other_user_center',
                    component:()=>import('@/components/other_user_center_page/user_center_page.vue')//他人个人中心
                },
                {
                    path:'/chat',
                    name:'chat',
                    component:()=>import('@/components/chat_page/chat_box.vue')//聊天
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
    },
    {
        path:'/reset_password',
        name:'reset_password',
        component:()=>import('@assets/model/reset_password/reset_password.vue')//重置密码
    }
]
const router = createRouter({
    history: createWebHistory(),
    routes
})

export {router};