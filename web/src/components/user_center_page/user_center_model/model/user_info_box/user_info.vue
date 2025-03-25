<template>
    <div class="user_info" v-if="user_info">
        <div class="content">
            <div class="user_avatar">
                <img :src="'https://www.sunyuanling.com/image/avatar_thumbnail/' + user_info.user_avatar" alt="用户头像">
            </div>
            <div class="info_box">
                <span class="username" style="font-weight: bold;font-size:20px;">
                    {{ user_info.username }}
                </span>
                <div class="user_stats">
                    <span class="user_follow">
                        {{ user_info.follow }} 关注
                    </span>
                    <span class="user_fans">
                        {{ user_info.fans }} 粉丝
                    </span>
                </div>
                <div class="user_address">
                    <img src="https://www.sunyuanling.com/assets/location.svg" alt="地址图标" class="icon">
                    <span>{{ user_info.user_address }}</span>
                </div>
                <div class="user_more_info_box" @click="more_info_box_show=true">
                    <span>查看个人资料</span>
                </div>
            </div>
            <div class="edit_info_btn btn" @click="edit_info_box_show=true">
                <span>编辑个人资料</span>
            </div>
        </div>
        <more_info_box :user_info="user_info" v-if="more_info_box_show" @close_page="more_info_box_show=false"></more_info_box>
        <edit_info_box :user_info="user_info" 
        :token="token"
        v-if="edit_info_box_show" @close_page="edit_info_box_show=false"></edit_info_box>
    </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import more_info_box from './more_info_box.vue';
import edit_info_box from './edit_info_box.vue';
const props = defineProps({
    user_info: {
        type: Object,
        default: () => {
            return {};
        }
    },
    token: {
        type: String,
        default: ''
    }
});
let more_info_box_show=ref(false);
let edit_info_box_show=ref(false);
</script>

<style scoped>
.user_info {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    padding: 20px;
}

.content {
    display: flex;
    width: 100%;
}

.user_avatar {
    flex-shrink: 0;
    width: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding-left: 0px;
}

.user_avatar img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
}

.info_box {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 60%;
    justify-content: flex-start;
}

.user_stats {
    display: flex;
    gap: 10px;
}

.user_follow,
.user_fans {
    font-size: 14px;
}

.user_address {
    display: flex;
    align-items: center;
    gap: 10px;
}

.user_more_info_box,
.edit_info_btn {
    cursor: pointer;
}
.user_more_info_box{
    color: rgba(133,133,133,1);
    font-size: 14px;
}

.edit_info_btn {
    align-self: flex-start;
    width: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 20px;
    background-color: rgba(133,133,133,1);
    border-radius: 15px;
}
.btn:hover{
    opacity: 0.7;
    transition: all 0.2s;
    transform: translateY(-2px);
    cursor: pointer;
}
.icon{
    width: 25px;
    height: 25px;
    object-fit: cover;
}
</style>