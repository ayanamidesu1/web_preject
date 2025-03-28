<template>
    <div class="header_box">
        <div class="header_box_back mt">
            <div class="header_box_background">
                <div class="header_box_background_img"><img :src="api.s_base_url+'image/'+(user.user_back_img||'default_back.png')"></div>
            </div>
            <router-link to="/self_user_center">
                <div class="header_box_avatar" style="cursor:pointer;" @click="jump_usercenter">
                    <div class="header_box_avatar_img"><img :src="api.s_base_url+'image/avatar_thumbnail/'+user.user_avatar"></div>
                </div>
            </router-link>
        </div>
        <div class="header_box_username mt"><span>{{ user.username }}</span></div>
        <div class="header_box_userid mt"><span>@{{ user.userid }}</span></div>
        <div class="header_box_userdata mt">
            <div class="header_box_user_fldata" style="cursor:pointer;">
                <span>{{ follow_num }}</span>
                <span>关注</span>
            </div>
            <div class="header_box_user_fans" style="cursor:pointer;">
                <span>{{ fans_num }}</span>
                <span>粉丝</span>
            </div>
        </div>
        <br>
        <div class="data_analysis mt hv" @click="open_data_analysis()"><span>数据分析</span></div>
        <div class="appointment_management mt hv"><span>约稿管理</span></div>
        <div class="mt hv" @click="open_contribute()"><span>投稿作品状态</span></div>
        <br>
        <div class="browseing_history mt hv" @click="open_history()"><span>浏览历史</span></div>
        <br>
        <div class="title mt"><span>Language</span></div>
        <div class="setting mt hv"><span>设置</span></div>
        <div class="send_backword mt hv"><span>发送反馈</span></div>
        <div class="logout mt hv" @click="logout"><span>退出登录</span></div>
    </div>
</template>

<script setup>
//import { useStore } from 'vuex';
import { ref, reactive, toRefs, watch, onMounted, onUnmounted,computed } from 'vue'
import { useRouter } from 'vue-router';
import { useStore } from '@assets/model/store';
import { BaseApi } from '@/base_api';
const api=new BaseApi();
const store = useStore();
const router = useRouter();

const user=computed(()=>{
    return store.$state.user;
})

let follow_num = ref(100)
let fans_num = ref(100)

//获取粉丝和管理数量和列表
async function get_fans_and_follow_num() {
    let res=await api.post('GetUserInfo/GetUserFollow/',{

    })
    if(res.status==200){
       follow_num.value=res.result.data.follow_count
       fans_num.value=res.result.data.fans_count
    }
    else{
        console.log(res)
    }
}

onMounted(async() => {
    await get_fans_and_follow_num();
})

function jump_usercenter() {
}

function open_data_analysis(){
    console.log("数据分析跳转");
    store.commit('SET_SINGLE_PAGE_STATUS',{'key':'data_analysis_page','value':true})
}

//投稿作品页面
function open_contribute(){
    console.log("投稿作品页面跳转");
    store.commit('SET_SINGLE_PAGE_STATUS',{'key':'work_contribute_page','value':true})
}

//打开历史浏览页面
function open_history(){
    store.commit('SET_SINGLE_PAGE_STATUS',{'key':'br_his_page','value':true})
}

//退出登录
function logout() {
    console.log("退出登录");
    localStorage.removeItem('token');
    window.location.href = "/login";

}
</script>

<style scoped>
/*通用样式*/
@charset "utf-8";

.mt {
    margin-top: 5px;
}

.mb {
    margin-bottom: 5px;
}

.ml {
    margin-left: 5px;
}

.mr {
    margin-right: 5px;
}

.pt {
    padding-top: 5px;
}

.pb {
    padding-bottom: 5px;
}

.pl {
    padding-left: 5px;
}

.pr {
    padding-right: 5px;
}

.hv:hover {
    cursor: pointer;
    background-color: rgba(236, 236, 236, 1);
    transition: 0.2s;
    border-radius: 5px;
    opacity: 0.8;
}

.header_box {
    display: flex;
    flex-direction: column;
    width: 200px;
    height: auto;
    min-height: 200px;
    background-color: rgba(214, 214, 215, 1);
    position: absolute;
    right: 0px;
    top: 60px;
    overflow-y: auto;
    padding: 5px;
    border-radius: 15px;
    z-index: 6;
}

.header_box_back {
    width: 100%;
    height: 120px;
    position: relative;
}

.header_box_background {
    width: 100%;
    height: 70%;
    overflow: hidden;
}

.header_box_background_img {
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.header_box_background_img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.header_box_avatar {
    width: 100%;
    height: 30%;
    position: absolute;
    top: 60%;
    justify-content: center;
    align-self: center;
    display: flex;
}

.header_box_avatar_img {
    width: 50px;
    height: 50px;
    overflow: hidden;
    border-radius: 50%;
}

.header_box_avatar_img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.header_box_userdata {
    display: flex;
    width: 95%;
    height: auto;
    justify-content: space-between;
    padding: 5px;
    align-items: center;
    margin-left: auto;
    margin-right: auto;
}

.header_box_user_fldata {
    display: flex;
    flex-direction: column;
    align-self: center;
}

.header_box_user_fans {
    display: flex;
    flex-direction: column;
    align-self: center;
}

.title {
    color: rgba(243, 243, 243, 1);
    border-bottom: 1px solid rgba(243, 243, 243, 1);
}
</style>