<template>
    <div class="edit_info_box">
        <div class="content">
            <div class="title">
                <span></span>
                <span style="font-weight: bold;font-size:18px;">修改个人信息</span>
                <div class="close_btn btn" @click="close_page">
                    <img class="icon" src="https://www.sunyuanling.com/assets/close.svg" alt="关闭">
                </div>
            </div>
            <div class="user_background">
                <user_background :user_back_img="'https://www.sunyuanling.com/image/' + temp_user_info.user_back_img"></user_background>
            </div>
            <span class="b">个人头像</span>
            <div class="avatar">
                <img :src="avatarImgUrl" ref="avatar_img" alt="用户头像">
                <div class="upload_avatar" @click="change_img">
                    <img src="https://www.sunyuanling.com/assets/image.svg">
                </div>
                <input type="file" accept="image/*" ref="upload_img" @change="get_img_item" style="display: none;">
            </div>
            <span class="b">用户名</span>
            <div class="username">
                <input type="text" placeholder="用户名" v-model="temp_user_info.username" class="focus">
            </div>
            <span class="b">自我介绍</span>
            <div class="introduce focus">
                <auto_textarea v-model="temp_user_info.user_self_introduction"></auto_textarea>
            </div>
            <span class="b">个人网站</span>
            <div class="person_website">
                <input type="text" placeholder="个人网站" v-model="temp_user_info.user_self_website" class="focus">
            </div>
            <span class="b">性别</span>
            <div class="sex">
                <re_select v-model="temp_user_info.sex" :select_title="temp_user_info.sex" :select_list="['男', '女', '任意']"></re_select>
            </div>
            <span class="b">地址</span>
            <div class="address">
                <input type="text" v-model="temp_user_info.user_address" class="focus">
            </div>
            <span class="b">生日</span>
            <div class="birthday">
                <input type="date" v-model="temp_user_info.birthday" @change="updateBirthday" class="focus">
            </div>
            <div class="btn_box">
                <div class="sure_btn focus" @click="submit_info()">
                    <span>确定</span>
                </div>
                <div class="cancel_btn focus" @click="close_page">
                    <span>取消</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue';
import auto_textarea from './user_info_box_model/auto_textarea.vue';
import user_background from '../user_background.vue';
import re_select from './user_info_box_model/select.vue';
import { update_userinfo } from '../../js/update_userinfo';

const props = defineProps({
    user_info: {
        type: Object,
        default: () => ({})
    },
    token: {
        type: String,
        default: ''
    }
});

const emit = defineEmits(['close_page']);
const temp_user_info = ref({ ...props.user_info });
const avatarImgUrl = ref(`https://www.sunyuanling.com/image/avatar_thumbnail/${temp_user_info.value.user_avatar}`);
const files=ref()

watch(() => props.user_info, (newInfo) => {
    temp_user_info.value = { ...newInfo };
    avatarImgUrl.value = `https://www.sunyuanling.com/image/avatar_thumbnail/${newInfo.user_avatar}`;
});

function updateBirthday(event) {
    temp_user_info.value.birthday = event.target.value;
}

function change_img() {
    const fileInput = document.querySelector('input[type="file"]');
    fileInput?.click();
}

function get_img_item(e) {
    const file = e.target.files[0];
    if (file) {
        const imgUrl = URL.createObjectURL(file);
        avatarImgUrl.value = imgUrl;
        temp_user_info.value.avatar_file = file; // 可以在提交时使用
    }
    files.value = file;
}
async function submit_info(){
    let user_info={}
    user_info.token=props.token
    user_info.username=temp_user_info.value.username
    user_info.user_self_introduction=temp_user_info.value.user_self_introduction
    user_info.user_address=temp_user_info.value.user_address
    user_info.user_self_website=temp_user_info.value.user_self_website
    user_info.sex=temp_user_info.value.sex
    user_info.birthday=temp_user_info.value.birthday
    user_info=JSON.stringify(user_info)
    console.log(user_info)
    let status=await update_userinfo(props.token,user_info,files.value)
    if(status){
        close_page()
    }
    else{
        alert('上传失败')
    }
}

function close_page() {
    emit('close_page');
}
</script>



<style scoped>
.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.edit_info_box {
    width: 100vw;
    min-height: 100vh;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    display: flex;
    background-color: rgba(0, 0, 0, 0.5);
    overflow: auto;
    z-index: 10;
}

.user_background {
    width: 100%;
    height: 150px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: auto;
    border-radius: 15px;
}

.content {
    width: auto;
    max-width: 60%;
    padding: 10px;
    min-width: 400px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    height: auto;
    background-color: rgba(255, 255, 255, 1);
    margin: 20px auto;
    border-radius: 15px;
    gap: 10px;
    overflow: auto;
}

.content::-webkit-scrollbar {
    height: 0px;
}

.title {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: auto;
}

.close_btn {
    width: 35px;
    height: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 0px;
}

.btn:hover {
    cursor: pointer;
    transform: scale(1.1);
    transition: all 0.2s;
    opacity: 0.8;
    border-radius: 50%;
    background-color: rgba(0, 0, 0, 0.5);
}

.avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin: 0px auto;
    display: flex;
    overflow: hidden;
    min-height: 100px;
    position: relative;
}

.avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.sure_btn {
    width: 60%;
    height: auto;
    padding: 5px 10px;
    display: flex;
    border-radius: 15px;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 150, 250, 1);
    color: white;
    font-size: 18px;
    font-weight: bold;
    margin: 10px auto;
}

.sure_btn:hover {
    opacity: 0.7;
    transition: all 0.2s;
    transform: scale(1.05);
    cursor: pointer;
}

.cancel_btn {
    width: 60%;
    height: auto;
    padding: 5px 10px;
    display: flex;
    border-radius: 15px;
    justify-content: center;
    align-items: center;
    background-color: rgb(75, 75, 75);
    color: white;
    font-size: 18px;
    font-weight: bold;
    margin: 10px auto;
}

.cancel_btn:hover {
    opacity: 0.7;
    transition: all 0.2s;
    transform: scale(1.05);
    cursor: pointer;
}

.focus:focus {
    outline: none;
    border: 3px solid rgb(88, 188, 255);
    border-radius: 3px;
    box-shadow: 0px 2px 2px rgba(255, 255, 255, 0.3);
    transition: all 0.2s;
}

.focus:focus::placeholder {
    color: rgb(88, 188, 255);
}

input {
    width: 100%;
    background-color: rgba(133, 133, 133, 0.5);
    border: none;
    padding: 5px;
    border-radius: 5px;
}

.introduce {
    border-radius: 10px;
    border: 1px solid rgba(0, 0, 0, 0.5);
    padding: 5px;
}
.b{
    font-weight: bold;
}
.upload_avatar{
    width: 100%;
    height: 100%;
    display: flex;
    position: absolute;
    top: 0;
    left: 0;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;
}
.upload_avatar:hover{
    opacity: 1;
    transition: all 0.2s;
    background-color: rgba(0, 0, 0, 0.2);
}
.upload_avatar img{
    width: 40%;
    height: auto;
    object-fit: cover;
}
</style>