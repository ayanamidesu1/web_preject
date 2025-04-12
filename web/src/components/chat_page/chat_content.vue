<template>
  <div class="chat_content">
    <div class="chat_user">
        <div class="chat_user_info">
            <img :src="api.s_base_url+'image/avatar_thumbnail/'+(user.avatar||'default.jpg')" alt="头像">
            <span>{{user.username}}</span>
            <div :class="user_online?'user_online':'user_offline'">
              <span><strong>·</strong>{{user_online?'在线':'离线'}}</span>
            </div>
        </div>
    </div>
    <div class="content" ref="content">
      <div ref="check_point" style="display:line-block;width:100%;height:1px;opacity:0;"></div>
        <div class="msg" v-for="(item,index) in msg_list" :key="index" ref="messagesContainer">
            <div class="receiver" v-if="item.sender_id==user.target_user_id &&item.msg_type!='review_msg'">
                <div class="user_info">
                  <img :src="api.s_base_url+'image/avatar_thumbnail/'+(user.avatar||'default.jpg')" 
                       alt="头像" 
                       class="avatar">
                  <div class="user_meta">
                    <span class="username">{{user.username}}</span>
                    <span class="user_id">ID:{{user.user_id}}</span>
                  </div>
                </div>
                <div class="msg_content">
                  <div class="bubble">
                    <span>{{item.content.type}}</span>
                    <p class="text">{{item.content}}</p>
                    <span class="time">{{api.formatTimeAgo(item.time)}}</span>
                  </div>
                </div>
              </div>
      
              <div class="sender" v-if="item.sender_id==self_user.userid &&item.msg_type!='review_msg'">                
                <img :src="api.s_base_url+'image/avatar_thumbnail/'+(self_user.avatar||'default.jpg')" 
                     alt="头像" 
                     class="avatar">
                     <div class="msg_content">
                  <div class="bubble self">
                    <p class="text">{{item.content}}</p>
                    <span class="time">{{api.formatTimeAgo(item.time)}}</span>
                  </div>
                </div>
              </div>
              <div class="receiver" v-if="item.msg_type=='review_msg'">
                <div class="user_info">
                  <img :src="api.s_base_url+'svg/管理员.svg'" alt="头像" class="avatar" width="30px" height="30px">
                  <div class="user_meta">
                    <span class="username">管理员消息</span>
                  </div>
                </div>
                <div class="msg_content">
                  <div class="bubble self">
                    <p class="text">
                      <review_msg :msg="JSON.parse(item.content)" :time="item.time"></review_msg>
                    </p>
                    <span class="time">{{api.formatTimeAgo(item.time)}}</span>
                  </div>
                </div>
              </div>
              <div class="receiver" v-if="item.msg_type=='sys_msg'">
                <div class="msg_content">
                  <div class="user_info">
                    <img :src="api.s_base_url+'svg/管理员.svg'" alt="头像" class="avatar" width="30px" height="30px">
                    <div class="user_meta" style="align-items: center;">
                      <span class="username">管理员消息</span>
                    </div>
                  </div>                  
                  <div class="bubble">
                    <span class="text">
                      {{ JSON.parse(item.content).text }}
                    </span>
                    <div class="time">{{api.formatTimeAgo(item.time)}}</div>
                  </div>                 
                </div>                
              </div>
        </div>
    </div>
    <div class="chat_input">
        <textarea v-model="msg" placeholder="输入消息" maxlength="1000"></textarea>
        <span @click="send_msg()" @keydown.enter.prevent="handleEnter"  @keyup.enter.ctrl.exact="msg += '\n'" >发送</span>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, watchEffect, computed, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from './chat_store';
import { useStore } from '@assets/model/store';
import { BaseApi } from '@/base_api';
import review_msg from './review_msg.vue';

const store = useStore()
const chatStore = useChatStore()
const router = useRouter()
const api = new BaseApi()
const msg_list = ref([])
let limit = 7
let offset = 0
let total = 0
let date = new Date()

// 使用ref存储定时器和监听器引用
const offlineTimer = ref(null)
const messageListener = ref(null)
const heartbeatListener = ref(null)
const heartbeatInterval = ref(null)

const self_user = computed(() => {
    return store.$state.user
})

const user = computed(() => {
    return chatStore.$state.now_chat_user
})

const user_online = ref(false)
let msg = ref()
const messagesContainer = ref(null)
let check_point = ref(null)
let content = ref(null)

// 创建IntersectionObserver
const obs = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && total > msg_list.value.length) {
        const container = messagesContainer.value
        const oldHeight = container.scrollHeight
        
        offset += limit
        const res = await get_history_msg(user.value.target_user_id, limit, offset)
        
        msg_list.value.unshift(...res.data.reverse())
        total = res.total
        
        await nextTick()
        container.scrollTop = container.scrollHeight - oldHeight
    }
}, {
    threshold: 0.5,
    rootMargin: '50px 0px 0px 0px'
})

// 请求历史消息
async function get_history_msg(user_id, limit = 10, offset = 0) {
    let res = await api.post('GetUserInfo/GetMsgList', {
        target_id: user_id,
        limit: limit,
        offset: offset
    })
    if (res.status == 200) {
        return res.result
    }
    return { data: [], total: 0 }
}

// 增强的输入处理
const handleEnter = (event) => {
    if (event.shiftKey || event.ctrlKey || event.altKey) {
        msg.value += '\n'
    } else {
        if (!event.repeat) send_msg()
        event.preventDefault()
    }
}

// 发送消息
async function send_msg() {
    if (msg.value) {
        console.log('发送消息', msg.value)
        chatStore.$state.ws.send(JSON.stringify({
            target_user_id: user.value.target_user_id,
            content: msg.value,
            chat_type: 'one_to_one',
            group_id: null,
            type: 'msg'
        }))
        scrollToBottom()
    }
    msg_list.value.push({
        sender_id: self_user.value.userid,
        content: msg.value,
        time: date.getTime(),
        id: date.getTime(),
        receiver_id: user.value.target_user_id,
        receiver_read_status: '未读'
    })
    msg.value = ''
}

// 滚动到底部
function scrollToBottom() {
    nextTick(() => {
        if (content.value) {
            content.value.scrollTo({
                top: content.value.scrollHeight,
                behavior: 'smooth'
            });
        }
    });
}

// 消息处理函数
function handleIncomingMessage(e) {
    let data = JSON.parse(e.data)
    if (data.type == 'heartbeat_notify' || data.type == 'heartbeat_ack') return;
    
    if (data.sender == user.value?.target_user_id) {
      console.log('收到消息', data)
        msg_list.value.push({
            sender_id: data.sender,
            content: data.content,
            time: data.timestamp,
            id: data.message_id,
            receiver_id: self_user.value.user_id,
            receiver_read_status: '未读',
            msg_type:'user'
        })
        scrollToBottom()
    }
    if(data.msg_type=='review_msg'){
      console.log('收到审核消息', data)
      let content=data.content
      msg_list.value.push({
        'msg_type':data.msg_type,
        'content':content,
        'time':data.time,
        'type':'review_msg',
      })
  }
}

// 心跳处理函数
function handleHeartbeat(e) {
    let data = JSON.parse(e.data)
    if (data.type == 'heartbeat_notify') {
        if (data.from_user === user.value?.target_user_id) {
            user_online.value = true
            
            if (offlineTimer.value) clearTimeout(offlineTimer.value)
            
            offlineTimer.value = setTimeout(() => {
                user_online.value = false
                console.log('15秒未收到心跳，用户离线')
            }, 15000)
        }
    }
}

// 建立目标用户心跳循环检查
function create_heart_beat() {
    if (user.value) {
        chatStore.$state.ws.send(JSON.stringify({
            target_user_id: user.value.target_user_id,
            content: '',
            chat_type: 'one_to_one',
            type: 'heart_beat'
        }))
    }
}

onMounted(async () => {
    if (!user.value) {
        router.push('/chat')
    }
    
    let res = await get_history_msg(user.value.target_user_id, limit, offset)
    msg_list.value = res.data.reverse()
    total = res.total
    
    nextTick(() => {
        scrollToBottom()
    })
    
    // 监听消息列表
    obs.observe(check_point.value)
    
    // 添加消息监听器
    messageListener.value = handleIncomingMessage
    chatStore.$state.ws.addEventListener('message', messageListener.value)
    
    // 添加心跳监听器
    heartbeatListener.value = handleHeartbeat
    chatStore.$state.ws.addEventListener('message', heartbeatListener.value)
    
    // 启动心跳循环
    heartbeatInterval.value = setInterval(() => {
        create_heart_beat()
    }, 10000)
})

watchEffect(async () => {
    if (user.value) {
        let res = await get_history_msg(user.value.target_user_id, limit, offset)
        msg_list.value = res.data
        total = res.total
    }
})

onUnmounted(() => {
    // 清理所有资源
    obs.disconnect()
    
    // 移除消息监听器
    if (messageListener.value) {
        chatStore.$state.ws.removeEventListener('message', messageListener.value)
    }
    
    // 移除心跳监听器
    if (heartbeatListener.value) {
        chatStore.$state.ws.removeEventListener('message', heartbeatListener.value)
    }
    
    // 清除定时器
    if (offlineTimer.value) {
        clearTimeout(offlineTimer.value)
    }
    
    if (heartbeatInterval.value) {
        clearInterval(heartbeatInterval.value)
    }
})
</script>

<style scoped lang="scss">
.chat_content{
    width:calc(100% - 20px);
    height: 100%;
    display: grid;
    grid-template-rows: 90px 1fr 100px;
    row-gap: 10px;
    max-height: calc(100vh - 200px);
}
.chat_user_info{
    width: calc(100% - 30px);
    height: 100%;
    display: flex;
    gap:10px;
    align-items: center;
    border-bottom: 1px solid #ccc;
}
.chat_user_info img{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
}
.chat_input{
    width: 100%;
    display: flex;
    gap:10px;
    align-items: center;
    justify-content: center;
    margin-bottom: 5px;
}
.chat_input textarea{
    width: calc(100% - 100px);
    height: 100%;
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 10px;
    resize: none;
}
.chat_input span{
    padding: 8px 13px;
    border-radius: 10px;
    background: rgb(0,150,250);
    cursor: pointer;
    color: white;
    transition: all 0.3s;
}
.chat_input span:hover{
    opacity: 0.8;
    transform: scale(1.03);
}
.chat_input span:active{
    opacity: 0.6;
    transform: scale(0.98);
}

.content{
    width: calc(100% - 30px);
    height: calc(100% - 30px);
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 10px;
    overflow-y:auto;
    margin-bottom: 10px;
}
.msg {
    margin: 12px 0;
  }
  
  /* 接收方消息样式 */
  .receiver {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    max-width: 70%;
    
    .user_info {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
      
      .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
      }
      
      .user_meta {
        display: flex;
        gap: 6px;
        align-items: baseline;
        
        .username {
          font-size: 14px;
          font-weight: 500;
        }
        
        .user_id {
          font-size: 12px;
          color: #666;
        }
      }
    }
    
    .bubble {
      background: #fff;
      border-radius: 12px;
      padding: 12px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      position: relative;
      
      &::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 12px;
        border: 8px solid transparent;
        border-right-color: #fff;
      }
    }
  }
  
  /* 发送方消息样式 */
  .sender {
    display: flex;
    flex-direction: row-reverse;
    align-items: flex-start;
    gap: 8px;
    margin-left: auto;
    max-width: 70%;
    
    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      object-fit: cover;
    }
    
    .bubble.self {
      background: #d9fdd3;
      border-radius: 12px;
      padding: 12px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      
      &::before {
        content: '';
        position: absolute;
        right: -8px;
        top: 12px;
        border: 8px solid transparent;
        border-left-color: #d9fdd3;
      }
    }
  }
  
  /* 公共消息内容样式 */
  .msg_content {
    position: relative;
    
    .text {
      margin: 0;
      font-size: 14px;
      line-height: 1.5;
      word-break: break-word;
    }
    
    .time {
      display: block;
      font-size: 12px;
      color: #666;
      text-align: right;
      margin-top: 4px;
    }
  }
  
  /* 移动端适配 */
  @media (max-width: 768px) {
    .receiver,
    .sender {
      max-width: 90%;
    }
    
    .avatar {
      width: 32px !important;
      height: 32px !important;
    }
  }
.user_online{
  color: rgb(158, 241, 125);
}
.user_offline{
  color: rgb(255, 0, 0);
}
</style>