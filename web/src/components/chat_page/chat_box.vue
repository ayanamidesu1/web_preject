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
const ws_url=`wss://127.0.0.1:2234/chat?token=${localStorage.getItem('token')}`

//创建ws连接并设置5s重试
function createWebSocket() {
    chatStore.$state.ws = new WebSocket(ws_url);
    chatStore.$state.ws.onopen = function () {
      console.log("WebSocket连接成功");
    }
    //连接失败重试
    chatStore.$state.ws.onerror = function () {
      console.log("WebSocket连接失败，尝试重连...");
      setTimeout(createWebSocket, 5000);
    };
    //退出重试
    chatStore.$state.ws.onclose = function () {
      console.log("WebSocket连接关闭，尝试重连...");
      setTimeout(createWebSocket, 5000);
    }
    //接收消息
    chatStore.$state.ws.onmessage = function (event) {
      let data = JSON.parse(event.data);
      //console.log(data);
    }
}


let chat_show=computed(()=>{
  return chatStore.now_chat_user==null?false:true;
})
onMounted(()=>{
  createWebSocket();
})
onUnmounted(()=>{
  chatStore.$state.ws.close();
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