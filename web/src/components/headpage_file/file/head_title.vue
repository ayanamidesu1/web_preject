<!-- eslint-disable vue/no-unused-components -->
<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="title" v-if="user_info">
        <div class="show_more">
            <div class="show_more_icon" @click="switch_show_sidebar">
                <img src="https://www.sunyuanling.com/assets/more.svg" class="icon">
            </div>
            <div class="sidebar" id="sidebar" v-show="show_sidebar" :style="action_left">
                <sidebar></sidebar>
            </div>
        </div>
        <div class="index_jump_img ml">
            <a href="https://localhost:3002/"><img :src="index_jump_img_src"></a>
        </div>
        <div class="input_box" ref="input_box">
            <input v-model="search_data" placeholder="搜索作品" @focus="input_box_focus">
            <div class="search_icon" @click="search_data_updata">
               <img class="icon" src="https://www.sunyuanling.com/assets/search.svg">
            </div>
        </div>
        <div class="join_vip ml mr">
            <span>{{ join_vip_text }}</span>
        </div>
        <div class="submission ml mr" @click="submission_work_box_show=!submission_work_box_show">
            <div class="submission_icon mr">
              <img class="icon" src="https://www.sunyuanling.com/assets/drop_down.svg">
            </div>
            <div class="submission_text"><span>{{ submission_text }}</span></div>
            <div class="submission_work_box"  :class="submission_work_box_show?'submission_work_box_drop':''">
                <submission_work_box></submission_work_box>
            </div>

        </div>
        <div class="message ml mr">
            <div class="message_icon" @click="chat_page_show_click()">
                <img class="icon" src="https://www.sunyuanling.com/assets/message.svg">
            </div>
        </div>
        <div class="notice ml mr" @click="show_notice()" @blur="notice_box_blur" ref="notice_box">
            <div class="notice_icon">
                <img class="icon" src="https://www.sunyuanling.com/assets/notice.svg">
            </div>
            <div class="notice_box" v-if="notice_info&&show_notice_box" @click="get_notice_info()">
                <div class="notice_item" v-for="(item,index) in notice_info" :key="index">
                    <div class="notice_title">{{item.title}}</div>
                    <div class="notice_content">{{item.content}}</div>
                    <div class="notice_time">{{item.last_modified_time}}</div>
                </div>
            </div>
        </div>
        <div class="useravatar ml mr" @click="useravatar_show_btn">
            <div class="useravatar_img">
                <img :src="avatar_img_src">
            </div>
            <div class="useravatar_icon ml">
               <img class="icon" src="https://www.sunyuanling.com/assets/drop_down.svg">
            </div>
        </div>
        <chat_page class="chat_page" v-if="chat_page_show" @close_page="close_chat_page"></chat_page>
        <header_box v-show="header_box_show"></header_box><!--这是头像，不是标题栏-->
        <search_page_index :search_item="search_data" @close_msg="close_search_page"
        ref="search_page_click"
         v-if="search_show_status">
        </search_page_index>
    </div>
</template>

<script setup>
import {useStore} from 'vuex'
import {get_notice_info} from '@/assets/js/get_notice'
import {get_userinfo} from '@/assets/js/get_userinfo'
import { onMounted, ref,watch,computed } from 'vue'
import sidebar from './sidebar/sidebar.vue'
import submission_work_box from './submission_work_box/submission_work_box.vue'
import header_box from './header_box/header_box.vue'
import chat_page from './chat_page/chat_page.vue'
import * as cookies from '../../../../../model/cookies.js'
import search_page_index from './search_page/search_page_index.vue'
const store = useStore()

let index_jump_img_src = ref('https://www.sunyuanling.com/image/主页.png')
let submission_text = ref('投稿作品')
let avatar_img_src = ref('https://www.sunyuanling.com/image/avatar_thumbnail/87328997_p0.jpg')
let join_vip_text = ref('加入ILLWeb会员')
let show_sidebar = ref(false)
let action_left = ref('left:0px;')
let submission_work_box_show = ref(false)
let header_box_show=ref(false)
let chat_page_show=computed(()=>store.getters.chat_page)
let user_info=ref([])
let search_data=ref()//搜索数据
user_info.value=JSON.parse(cookies.get_cookie('userinfo'))
let search_show_status=computed(()=>store.getters.search_page);
let input_box=ref(null)
let search_page_click=ref(null)
let notice_box=ref(null)
let notice_info=ref()
let store_token=computed(()=>store.getters.token)
let token=store_token.value
onMounted(async()=>{
    await get_notice_info()
    notice_info.value=await get_notice_info(token,'search')
    let temp=''
    temp=await get_userinfo(cookies.get_cookie('token'))
    console.log(temp)
    avatar_img_src.value='https://www.sunyuanling.com/image/avatar_thumbnail/'+temp[0].user_avatar
})
watch(()=>store.getters.token,async ()=>{
    await get_notice_info()
    notice_info.value=await get_notice_info(token,'search')
    let temp=''
    temp=await get_userinfo(cookies.get_cookie('token'))
    console.log(temp)
    avatar_img_src.value='https://www.sunyuanling.com/image/avatar_thumbnail/'+temp[0].user_avatar
})
//公告信息框的显示和隐藏
let show_notice_box=ref(false)
function show_notice(){
    if(token!=undefined&&token!=''){
        
        show_notice_box.value=!show_notice_box.value;
    }
   
}
function notice_box_blur()
{
    show_notice_box.value=false;
}
//不在元素及其子元素中点击隐藏公告框
function notice_box_click(e)
{
    if (!e.target.closest('.notice')) {
        show_notice_box.value = false;
      }
}
onMounted(()=>{
    document.addEventListener('click',notice_box_click);
    var mainpage = document.querySelector('.submission');
    document.addEventListener('click', function (event) {
        if (!mainpage.contains(event.target)) {
            submission_work_box_show.value = false;
        }
    });
})
//搜索实现
watch(search_data,(newValue,oldValue)=>{
    search_data.value=newValue;
})
//更新search_data以触发搜索页面的更新
async function search_data_updata(){
  if (search_page_click.value){
    try{
    const result=await search_page_click.value.get_search_data(search_data.value)
    }
    catch(error){
      console.log(error);
    }
  }

}
//获取焦点时显示搜索页面，失去焦点时隐藏搜索页面
function input_box_focus(){
   // search_show_status.value=true;
    store.commit('SET_SINGLE_PAGE_STATUS',{key:'search_page',value:true})
}

//接收搜索页面的关闭消息
function close_search_page(item){
    console.log(item);
    //search_show_status.value=false;
    store.commit('SET_SINGLE_PAGE_STATUS',{key:'search_page',value:false})
    search_data.value=null;
}

//聊天界面显示
function chat_page_show_click(){
   store.commit('SET_SINGLE_PAGE_STATUS',{key:'chat_page',value:true})
}
//接收子组件关闭消息
function close_chat_page(item){
    console.log(item);
    chat_page_show.value=false;
}

function useravatar_show_btn(){
    var mainpage=document.querySelector('.useravatar');
    document.addEventListener('click', function (event) {
        if (!mainpage.contains(event.target)) {
            header_box_show.value=false;
        }
    });
    if(header_box_show.value==true)
    {
        header_box_show.value=false;
    }
    else{
        header_box_show.value=true;
    }
}

function submission_work_box_show_btn() {
    
   
    if (submission_work_box_show.value == false) {
        submission_work_box_show.value = true;
    }
}

function switch_show_sidebar() {
    var step_len = 250 / 60;//步长
    var step = 60;//步数
    var mainpage = document.getElementById("sidebar");//包含元素的框
    var show_btn = document.querySelector(".show_more");
    document.addEventListener('click', function (event) {
        if (!mainpage.contains(event.target) && !show_btn.contains(event.target)) {
            animation_sidebar(0, -250, step_len, step, do_time);
        }
    });
    var do_time = 100;
    console.log('test');
    if (show_sidebar.value == false) {
        animation_sidebar(-250, 0, step_len, step, do_time);

        console.log('true');
    } else {
        animation_sidebar(0, -250, step_len, step, do_time);

        console.log('false');
    }
}

function animation_sidebar(startlo, endlo, step_len, step, do_time) {
    if (startlo >= endlo) {
        var count = 0;
        var interval = do_time / step; // 计算每步的时间间隔

        // eslint-disable-next-line no-inner-declarations
        function animate1() {
            if (count >= step) {
                action_left.value = 'left:' + (-250) + 'px;';

                show_sidebar.value = false;
                return;
            }
            action_left.value = 'left:' + (startlo - step_len * count) + 'px;';

            count++;
            setTimeout(animate1, interval);
        }
        animate1();
    }
    if (startlo <= endlo) {
        var count_1 = 0;
        var interval_1 = do_time / step;
        // eslint-disable-next-line no-inner-declarations
        function animate2() {
            if (count_1 >= step) {
                action_left.value = 'left:' + (0) + 'px;';
                show_sidebar.value = true;
                return;
            }
            show_sidebar.value = true;
            action_left.value = 'left:' + (startlo + step_len * count_1) + 'px;';
            count_1++;
            setTimeout(animate2, interval_1);
        }
        animate2();
    }

}
</script>

<style scoped>
/*通用样式*/
.mt {
    margin-top: 5px;
}

.ml {
    margin-left: 5px;
}

.mr {
    margin-right: 5px;
}

.mb {
    margin-bottom: 5px;
}

.pt {
    padding-top: 5px;
}

.pl {
    padding-left: 5px;
}

.pr {
    padding-right: 5px;
}

.pb {
    padding-bottom: 5px;
}
/*公告框*/
.notice_box{
    display: flex;
    width:250px;
    height: auto;
    max-height: 250px;
    position: absolute;
    top: 45px;
    left: auto;
    right: 0px;
    z-index: 15;
    flex-direction: column;
    cursor: default;
    overflow-y:auto ;
    background-color: rgba(255,255,255,1);
    border: 1px solid rgba(0,0,0,0.2);
    border-radius: 10px;
}
.notice_box::-webkit-scrollbar {
    display: none;
}
.notice_item{
    display: flex;
    width: 95%;
    height: auto;
    padding: 3px 5px;
    margin: 5px auto;
    flex-direction: column;
    border-bottom: 1px solid rgba(0,0,0,0.5);
}

/*作品上传框*/
.submission_work_box {
    display: flex;
    width: 200px;
    min-height: 150px;
    height: auto;
    position: absolute;
    top: 50px;
    overflow: hidden;
    background-color: rgba(211, 211, 211, 1);
    border-radius: 15px;
    z-index: 10;
    transition: all 0.3s ease-in-out;
    transform: translateY(-150%);
}
.submission_work_box_drop{
    transform: translateY(0px);
}

.submission_work_box:hover {
    cursor: auto !important;
}

/*侧边栏样式*/
.sidebar {
    width: 210px;
    height: 100%;
    
    position: fixed;
    top: 60px;
    z-index: 15;
    transition: left 0.2s ease;
    /* 添加过渡效果 */
    transition: right 0.2s ease;
}


/*加入会员文字样式*/
.join_vip {
    font-size: 16px;
    color: rgb(253, 158, 22);
    align-self: center;
    justify-content: center;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    white-space: pre;
    width: auto;
    height: auto;
}

/*用户头像样式*/
.useravatar {
    display: flex;
    
    width: 80px;
    height: 95%;
    align-self: center;
}

.useravatar:hover {
    cursor: pointer;
}

.useravatar_img {
    width: 46px;
    height: 46px;
    
    overflow: hidden;
    border-radius: 50%;
}

.useravatar_img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.useravatar_icon {
    width: 20px;
    height: 20px;
    overflow: hidden;
    justify-content: center;
    align-items: center;
    align-self: center;
}

.useravatar_icon img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/*通知样式*/
/*消息样式*/
.message,
.notice {
    display: flex;
    width: 35px;
    height: 35px;
    align-items: center;
    justify-content: center;
    align-self: center;
    position: relative;
}

.message:hover,
.notice:hover {
    background-color: rgba(211, 211, 211, 1);
    border-radius: 50%;
    transition: 0.2s;
    cursor: pointer;
}
.chat_page{
    position: fixed;
    top:0px;
    left: 0px;
    width: 100vw;
    height: 100vh;
    background-color: rgba(255, 255, 255, 1);
    z-index: 10;
}

.message_icon,
.notice_icon {
    width: 100%;
    height: 100%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.message_icon img,
.notice_icon img{
    width: 25px;
    height: 25px;
    object-fit: cover;
}

/*查看更多按钮样式*/
.title {
    display: flex;
    width: 99%;
    height: 50px;
    background-color: rgba(255, 255, 255, 1);
    
    position: relative;
    padding: 5px;
    margin-top: auto;
    margin-bottom: auto;
    margin-left: auto;
    margin-right: auto;
}

.show_more {
    display: flex;
    width: 45px;
    height: 45px;
    align-items: center;
    align-self: center;
}

.show_more_icon {
    width: 100%;
    height: 100%;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

.show_more_icon:hover {
    background-color: rgba(211, 211, 211, 1);
    border-radius: 10px;
    transition: 0.2s;
    cursor: pointer;
}


/*主页按钮图片*/
.index_jump_img {
    width: 150px;
    height: 100%;
    overflow: hidden;
    cursor: pointer;
}

.index_jump_img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/*搜索框*/
.input_box {
    display: flex;
    position: relative;
    width: 50%;
    height: 90%;
    background-color: rgba(211, 211, 211, 1);
    border: 1px solid rgba(211, 211, 211, 1);
    border-radius: 15px;
    margin-left: auto;
    margin-right: 20px;
    align-items: center;
    align-self: center;
}

.input_box input {
    display: flex;
    width: 90%;
    height: 100%;
    border: none;
    background: transparent;
    align-items: center;
}

.search_icon {
    width: 5%;
    height: 100%;
    overflow: hidden;
    position: absolute;
    right: 5px;
    align-items: center;
    align-self: center;
    cursor: pointer;
    display: flex;
    padding: 5px;
}

.submission {
    display: flex;
    width: auto;
    height: auto;
    background-color: rgba(211, 211, 211, 1);
    align-items: center;
    align-self: center;
    border-radius: 15px;
    justify-content: center;
    position: relative;
    gap: 5px;
    padding: 8px 10px;
    font-size: 12px;
    cursor: pointer;
    /*禁止换行*/
    white-space: nowrap;
}

.submission:hover {
    background-color: rgba(185, 185, 185, 1);
    cursor: pointer;
    transition: 0.2s;
}

.submission_icon {
   width: auto;
   height: auto;
   display: flex;
}
.submission_icon img{
    width: 20px;
    height: 20px;
    object-fit: cover;
}

.submission_icon svg img{
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.icon{
    width: 30px;
    height: 30px;
    object-fit: cover;
}
</style>
