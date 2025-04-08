<template>
  <div class="friend_list">
    <div class="friend_item">
        <div class="friend_info" @click="select_sys_notice()">
            <img src="https://www.sunyuanling.com/server/static/svg/管理员.svg" alt="头像">
            <span style="display:flex;flex-direction:column;justify-content:center">系统通知</span>
        </div>
    </div>
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useStore } from '@assets/model/store/index'
import { BaseApi } from '@/base_api'
import { useRouter } from 'vue-router'
import { useChatStore } from './chat_store'

const chat_store = useChatStore()
const store = useStore()
const router = useRouter()
const api = new BaseApi()

// 统一使用 target_user_id 作为键
const chat_list = ref([])
const heartbeats = ref({})
const limit = ref(10)
const offset = ref(0)
const total = ref(0)
const check_point = ref(null)
let heartbeatTimer = null
let checkTimer = null

// 选择好友
function select_friend(item) {
    chat_store.$state.now_chat_user = item;
}
//选择系统通知
function select_sys_notice() {
    chat_store.$state.now_chat_user = null;
}

// 删除该聊天
function delete_chat(item) {
    chat_list.value = chat_list.value.filter((friend) => friend.userid !== item.userid);
    console.log(item);
}

// 获取聊天列表
async function get_chat_list() {
  const res = await api.post('GetUserInfo/GetChatList', {
    limit: limit.value,
    offset: offset.value
  })
  
  if (res.status === 200) {
    chat_list.value = res.result.data.map(item => ({
      ...item,
      is_online: false // 初始化在线状态
    }))
    total.value = res.result.total
  }
}

// 统一用户标识获取
function get_user_id(item) {
  return item.target_user_id || item.userid
}

// 检查在线状态
function check_online() {
  const ids = chat_list.value.map(get_user_id).filter(Boolean)
  
  if (ids.length > 0) {
    chat_store.$state.ws.send(JSON.stringify({
      target_user_ids: ids,
      type: 'heart_beats'
    }))
  }

  // 清除旧定时器
  if (heartbeatTimer) clearTimeout(heartbeatTimer)
  heartbeatTimer = setTimeout(check_online, 10000)
}

// 心跳超时检查
function start_heartbeat_checker() {
  checkTimer = setInterval(() => {
    const now = Date.now()
    chat_list.value.forEach(item => {
      const userId = get_user_id(item)
      const heartbeat = heartbeats.value[userId]
      
      if (heartbeat && now - heartbeat.timestamp <= 10000) {
        item.is_online = true
      } else {
        item.is_online = false
        if (heartbeat) delete heartbeats.value[userId]
      }
    })
  }, 5000)
}

// WebSocket 消息处理
function setup_websocket_handler() {
  chat_store.$state.ws.onmessage = (e) => {
    const data = JSON.parse(e.data)
    
    if (data.type === 'group_heartbeat_ack') {
      const userId = data.from_user || data.from // 兼容不同字段名
      const user = chat_list.value.find(item => get_user_id(item) === userId)
      
      if (user) {
        heartbeats.value[userId] = {
          received: true,
          timestamp: Date.now()
        }
      }
    }
  }
}

onMounted(async () => {
  await get_chat_list()
  setup_websocket_handler()
  check_online()
  start_heartbeat_checker()
})

onUnmounted(() => {
  if (heartbeatTimer) clearTimeout(heartbeatTimer)
  if (checkTimer) clearInterval(checkTimer)
  if (obs) obs.disconnect()
})
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