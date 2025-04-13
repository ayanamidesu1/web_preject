<template>
    <div class="user_info" v-if="user_info">
        <div class="content">
            <div class="user_avatar">
                <img :src="'https://www.sunyuanling.com/server/static/image/avatar_thumbnail/' + user_info.user_avatar" alt="用户头像">
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
                <div class="user_more_info_box" @click="more_info_box_show = true">
                    <span>查看个人资料</span>
                </div>
            </div>
            <div class="follow_box">
                <div class="follow_btn" @click="follow()" :class="follow_status ? 'is_follow' : 'not_follow'">
                    <span>{{ (follow_status == true ? '已关注' : '关注') }}</span>
                </div>
                <div class="chat_btn" @click="chat()">
                    <span>发起私聊</span>
                </div>
                <div class="add_work_order" @click="add_work_order(user_info.userid)">
                    <img src="https://www.sunyuanling.com/server/static/svg/约稿.svg" alt="约稿" width="25px" height="25px">
                    <span>发起约稿</span>
                </div>
            </div>
        </div>
        <more_info_box :user_info="user_info" v-if="more_info_box_show" @close_page="more_info_box_show = false">
        </more_info_box>
    </div>
</template>

<script setup>
import { ref, defineProps, onMounted } from 'vue';
import more_info_box from './more_info_box.vue';
import {useRouter} from 'vue-router'
import { BaseApi } from '@/base_api';

const router = useRouter();
const api = new BaseApi();

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
let more_info_box_show = ref(false);
let follow_status = ref(false);
//请求关注状态
async function get_follow_status() {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserFollowList/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                target_id: props.user_info.userid
            })
        })
        if (res.ok) {
            const data = await res.json();
            if (data.status == 'success') {
                if (data.data.length > 0) {
                    follow_status.value = true
                }
            }
            else {
                console.log(data.message)
            }
        }
        else {
            const data = await res.json();
            console.log(data)
        }
    }
    catch (e) {
        console.log(e);
    }
}

//关注
async function follow() {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/UserAddFollow/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                target_id: props.user_info.userid,
                target_username: props.user_info.username
            })
        })
        if (res.ok) {
            const data = await res.json();
            if (data.status == 'success') {
                alert(data.message)
                if (data.message == '关注成功') { follow_status.value = true }
                else { follow_status.value = false }
            }
            else {
                console.log(data.message)
            }
        }
        else {
            const data = await res.json();
            console.log(data)
        }
    }
    catch (e) {
        console.log(e);
    }
}

//发起私聊
async function chat(){
    let target_user_id=router.currentRoute.value.query.id;
    try{
        let res=await api.post('GetUserInfo/AddChatList',{
            target_user_id:target_user_id
        })
        if(res.status==200){
            router.push('/chat')
        }
        else{
            console.log(res)
        }
    }
    catch(e){
        console.log(e);
    }
}
//发起约稿订单
function add_work_order(user_id){
    router.push(`/add_work_order?id=${user_id}`)
}

onMounted(async () => {
    await get_follow_status();
})
</script>

<style scoped lang="scss">
.user_info {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    padding: 20px;
}

.content {
    display: flex;
    width: 100%;
    gap: 20px;
    justify-content: flex-start;
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
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 60%;
    width: auto;
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

.user_more_info_box {
    color: rgba(133, 133, 133, 1);
    font-size: 14px;
}

.edit_info_btn {
    align-self: flex-start;
    width: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 20px;
    background-color: rgba(133, 133, 133, 1);
    border-radius: 15px;
}

.btn:hover {
    opacity: 0.7;
    transition: all 0.2s;
    transform: translateY(-2px);
    cursor: pointer;
}

.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.follow_box {
    width: fit-content;
    height: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    align-self: center;
    gap:10px;
}

.follow_btn {
    width: fit-content;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    min-width: 100px;
    max-width: 150px;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    height: 40px;
}

.follow_btn:hover {
    opacity: 0.8;
    transition: all 0.2s;
    transform: translateY(-2px);
}
.chat_btn{
    padding: 5px 10px;
    background-color: rgb(0, 150, 250);
    border-radius: 5px;
    color: white;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.2s;
}
.chat_btn:hover{
    opacity: 0.8;
    transition: all 0.2s;
    transform: translateY(-2px)
}
.add_work_order{
    display: flex;
    flex-direction: row;
    gap:5px;
    background-color: rgb(0, 150, 250);
    cursor: pointer;
    padding: 5px 10px;
    border-radius: 5px;
    color: white;
    transition: all 0.2s;
    font-weight: bold;
    &:hover{
        opacity: 0.8;
        transition: all 0.2s;
        transform: translateY(-2px)
    }
    &:active{
        opacity: 0.6;
        transition: all 0.2s;
        transform: translateY(-2px);
        transform:scale(0.9)
    }
}
.is_follow {
    background-color: rgba(133, 133, 133, 1);
}

.not_follow {
    background-color: rgba(0, 150, 250, 1);
}
</style>