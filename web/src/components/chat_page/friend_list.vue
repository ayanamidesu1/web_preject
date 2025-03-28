<template>
  <div class="friend_list">
    <div class="friend_item" v-for="(item,index) in chat_list" :key="index">
        <div class="friend_info" @click="select_friend(item)">
            <img :src="api.s_base_url+'/image/avatar_thumbnail/'+(item.avatar||'default.jpg')" alt="头像">
            <span style="display:flex;flex-direction:column;justify-content:center"><span>{{item.username}}</span>
                    <span :style="item.is_online?'color:green':'color:red'">·{{item.is_online?'[在线]':'[离线]'}}</span>
        </span>
            <div class="delete_chat" @click="delete_chat(item.userid)">x</div>
        </div>
    </div>
    <div class="check_point" ref="check_point" style="display:none;width:100%;height:1px;opacity:0"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watchEffect, onUnmounted, nextTick } from 'vue';
import { useStore } from '@assets/model/store/index';
import { BaseApi } from '@/base_api';
import { useRouter } from 'vue-router';
import { useChatStore } from './chat_store';

const chat_store = useChatStore();
const store = useStore();
const router = useRouter();
const api = new BaseApi();

let check_point = ref();
let limit = ref(10);
let offset = ref(0);
let total = ref(0);
let chat_list = ref([]);

// 用于记录每个用户的心跳状态
let heartbeats = ref({});

// 获取聊天列表
async function get_chat_list() {
    let res = await api.post('GetUserInfo/GetChatList', {
        limit: limit.value,
        offset: offset.value
    });
    if (res.status == 200) {
        console.log(res);
        chat_list.value = res.result.data;
        total.value = res.result.total;
    } else {
        console.log(res);
    }
}

// 选择好友
function select_friend(item) {
    chat_store.$state.now_chat_user = item;
}

// 删除该聊天
function delete_chat(item) {
    chat_list.value = chat_list.value.filter((friend) => friend.userid !== item.userid);
    console.log(item);
}

// 检查聊天列表用户在线状态
async function check_online() {
    let ids = chat_list.value.map((item) => item.target_user_id);
    chat_store.$state.ws.send(JSON.stringify({
        target_user_ids: ids,
        type: 'heart_beats'
    }));

    // 清空已经超时的用户的在线状态
    setTimeout(() => {
        // 检查超时用户
        chat_list.value.forEach((item) => {
            if (!heartbeats.value[item.target_user_id] || !heartbeats.value[item.target_user_id].received) {
                // 如果10秒内没有接收到心跳，设置为离线
                item.is_online = false;
            }
        });

        // 继续定时检查
        check_online();
    }, 10000);  // 每10秒发一次心跳检查
}

nextTick(() => {
    chat_store.$state.ws.onmessage = (e) => {
        let data = JSON.parse(e.data);
        if (data.type === 'group_heartbeat_ack') {
            let online_user_id = data.from_user;

            // 更新对应用户的心跳状态
            const user = chat_list.value.find((item) => item.target_user_id === online_user_id);
            if (user) {
                heartbeats.value[online_user_id] = { received: true, timestamp: Date.now() };
                if (!user.is_online) {
                    user.is_online = true;
                }
            }
        }
    };
});

// 监听用户的心跳超时
function heartbeatTimeoutChecker() {
    setInterval(() => {
        Object.keys(heartbeats.value).forEach((userId) => {
            const lastHeartbeat = heartbeats.value[userId];
            if (lastHeartbeat && Date.now() - lastHeartbeat.timestamp > 10000) {  // 10秒未收到心跳
                const user = chat_list.value.find((item) => item.target_user_id == userId);
                if (user) {
                    user.is_online = false;  // 设置为离线
                }
                delete heartbeats.value[userId];  // 清除超时用户
            }
        });
    }, 5000);  // 每5秒检查一次
}

let obs = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting) {
        if (offset.value < total.value) {
            offset.value += limit.value;
            await get_chat_list();
        }
    }
}, {
    root: check_point.value,
    rootMargin: '0px',
});

onMounted(async () => {
    await get_chat_list();
    obs.observe(check_point.value);

    // 初始化用户的在线状态
    chat_list.value.forEach((item) => {
        item.is_online = false;
    });

    // 开始心跳检查
    check_online();
    heartbeatTimeoutChecker();
});

onUnmounted(() => {
    obs.disconnect();
});
</script>

<style scoped>
.friend_list{
    width: calc(100% - 16px);
    height: 100%;
    display: flex;
    flex-direction: column;
    gap:10px;
}
.friend_item{
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    gap:10px;
}
.friend_item::-webkit-scrollbar{
    display: none;
}
.friend_info{
    display: flex;
    gap:5px;
    border-bottom: 1px solid #ccc;
    cursor: pointer;
    background-color: rgba(244,244,244,1);
    padding: 3px;
    border-radius: 3px;
    transition: all 0.3s;
    overflow: hidden;
    /*禁止换行*/
    white-space: nowrap;
    text-overflow: ellipsis;
    align-items: center;
    width: 100%;
    font-size: 12px;
    position: relative;
}
.friend_info:hover{
    opacity: 0.9;
    background-color: white;
    transform: scale(1.03);
}
.friend_info img{
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
}
.delete_chat{
    position: absolute;
    right: 10px;
    width: 20px;
    height: 20px;
    padding: 5px;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
}
.delete_chat:hover{
    background-color: rgba(255,0,0,0.5);
    color: white;
    border-radius: 50%;
}
</style>