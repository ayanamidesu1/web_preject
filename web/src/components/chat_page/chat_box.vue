<template>
  <div class="chat_box">
    <div class="friend_list">
      <h4>好友列表</h4>
      <friend_list></friend_list>
    </div>
    <div class="chat_content">
      <span><strong>聊天</strong></span>
      <chat_content v-if="chat_show"></chat_content>
    </div>
  </div>
</template>


<script setup>
import { ref,onMounted, computed, onUnmounted } from 'vue'
import friend_list from './friend_list.vue';
import chat_content from './chat_content.vue';
import { useChatStore } from './chat_store';
import { BaseApi } from '@/base_api';
import { useStore } from '@assets/model/store';
const chatStore = useChatStore();
const store = useStore();
const api=new BaseApi();
//wss连接配置
const ws_url = `wss://127.0.0.1:2234/chat?token=${localStorage.getItem('token')}`
const MAX_RETRIES = 3 // 最大重试次数
const RETRY_DELAY = 5000 // 重试间隔(ms)
let retryCount = 0

// WebSocket管理
function initWebSocket() {
  // 清理现有连接
  if (chatStore.$state.ws) {
    chatStore.$state.ws.onclose = null
    chatStore.$state.ws.close()
  }

  chatStore.$state.ws = new WebSocket(ws_url)
  
  chatStore.$state.ws.onopen = () => {
    console.log("WebSocket连接成功")
    retryCount = 0 // 重置重试计数器
  }
  
  chatStore.$state.ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    // 处理业务消息...
  }
  
  chatStore.$state.ws.onerror = () => {
    console.error("WebSocket连接错误")
    scheduleReconnect()
  }
  
  chatStore.$state.ws.onclose = () => {
    console.log("WebSocket连接关闭")
    scheduleReconnect()
  }
}

function scheduleReconnect() {
  if (retryCount >= MAX_RETRIES) {
    console.warn(`已达到最大重试次数(${MAX_RETRIES})，停止自动重连`)
    return
  }
  
  retryCount++
  console.log(`将在${RETRY_DELAY/1000}秒后尝试第${retryCount}次重连...`)
  setTimeout(initWebSocket, RETRY_DELAY)
}

onMounted(() => {
  initWebSocket()
})

onUnmounted(() => {
  if (chatStore.$state.ws) {
    chatStore.$state.ws.onclose = null // 防止触发重连
    chatStore.$state.ws.close()
  }
})

</script>

<style scoped>
.chat_box{
  display: grid;
  width: 85%;
  height: 100%;
  max-height: calc(100% - 65px);
  grid-template-columns: 200px 1fr;
  margin: 0 auto;
  gap:10px;
}
.friend_list{
  display: flex;
  flex-direction: column;
  gap:10px;
  padding: 8px;
  border-radius: 8px;
  background-color: rgb(233, 233, 233);
  height: 100%;
}
.chat_content{
  display: flex;
  flex-direction: column;
  gap:5px;
  padding: 5px;
  border-radius: 8px;
  background-color: rgb(233, 233, 233);
  height: 100%;
  min-height: calc(100vh - 180px);
}
</style>