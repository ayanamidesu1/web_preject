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
            <div class="receiver" v-if="item.sender_id==user.target_user_id">
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
                    <p class="text">{{item.content}}</p>
                    <span class="time">{{api.formatTimeAgo(item.time)}}</span>
                  </div>
                </div>
              </div>
      
              <div class="sender" v-if="item.sender_id==self_user.userid">
                
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
        </div>
    </div>
    <div class="chat_input">
        <textarea v-model="msg" placeholder="输入消息" maxlength="1000"></textarea>
        <span @click="send_msg()" @keydown.enter.prevent="handleEnter"  @keyup.enter.ctrl.exact="msg += '\n'" >发送</span>
    </div>
  </div>
</template>


<script setup>
import { ref,onMounted,watchEffect,computed,onUnmounted,nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from './chat_store';
import { useStore } from '@assets/model/store';
import { BaseApi } from '@/base_api';

const store = useStore()
const chatStore = useChatStore()
const router = useRouter()
const api=new BaseApi()
const msg_list=ref([])
let limit=7
let offset=0
let total=0
let date=new Date()
let self_user=computed(()=>{
    return store.$state.user
})
const user=computed(()=>{
    return chatStore.$state.now_chat_user
})
const user_online=ref(false)
let msg=ref()
const messagesContainer = ref(null)
let check_point=ref(null)
let content=ref(null)

let obs = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && total > msg_list.value.length) {
        const container = messagesContainer.value
        const oldHeight = container.scrollHeight
        
        offset += limit
        const res = await get_history_msg(user.value.target_user_id, limit, offset)
        
        // 将新消息插入数组末尾
        msg_list.value.unshift(...res.data.reverse()) // 先反转，再插入头部
        total = res.total
        
        // 保持滚动位置
        await nextTick()
        container.scrollTop = container.scrollHeight - oldHeight
    }
}, {
    threshold: 0.5,
    rootMargin: '50px 0px 0px 0px'
})

//请求历史消息
async function get_history_msg(user_id,limit=10,offset=0){
    let res=await api.post('GetUserInfo/GetMsgList',{
        target_id:user_id,
        limit:limit,
        offset:offset
    })
    if(res.status==200){
        return res.result
    }
    return []
}
// 增强的输入处理
const handleEnter = (event) => {
  if (event.shiftKey || event.ctrlKey || event.altKey) {
    // 组合键换行
    msg.value += '\n'
  } else {
    if (!event.repeat) send_msg()
    event.preventDefault()
  }
}
// 发送消息
async function send_msg(){
  if(msg.value){
    console.log('发送消息',msg.value)
    chatStore.$state.ws.send(JSON.stringify({
      target_user_id:user.value.target_user_id,
      content:msg.value,
      chat_type:'one_to_one',
      group_id:null,
      type:'msg'
    }))
    scrollToBottom()
  }
  msg_list.value.push({
    sender_id:self_user.value.userid,
    content:msg.value,
    time:date.getTime(),
    id:date.getTime(),
    receiver_id:user.value.target_user_id,
    receiver_read_status:'未读'
  })
  msg.value=''
}
chatStore.$state.ws.addEventListener('message', function (e) {
    let data = JSON.parse(e.data)
    if (data.type=='heartbeat_notify'||data.type=='heartbeat_ack') return;
    console.log('收到消息', data)
    if (data.sender == user.value.target_user_id) {
        msg_list.value.push({
            sender_id: data.sender,
            content: data.content,
            time: data.timestamp,
            id: data.message_id,
            receiver_id: self_user.value.user_id,
            receiver_read_status: '未读'
        })
        scrollToBottom()
    }
})

// 修改消息监听器中的心跳处理
chatStore.$state.ws.addEventListener('message', function (e) {
    let data = JSON.parse(e.data)
    if (data.type == 'heartbeat_notify') {
        // 确认心跳来源
        if (data.from_user === user.value?.target_user_id) {
            user_online.value = true
            
            // 清除旧定时器
            if (window.offlineTimer) clearTimeout(window.offlineTimer)
            
            // 设置3秒离线判定
            window.offlineTimer = setTimeout(() => {
                user_online.value = false
                console.log('3秒未收到心跳，用户离线')
            }, 15000)
        }
    }
})

//建立目标用户心跳循环监察
async function create_heart_beat(){
  if(user.value){
    chatStore.$state.ws.send(JSON.stringify({
      target_user_id:user.value.target_user_id,
      content:'',
      chat_type:'one_to_on1',
      "type":'heart_beat'
    }))
  }
  setTimeout(()=>{
    create_heart_beat()
  },10000)
}

// 滚动到底部
function scrollToBottom() {
  nextTick(() => {
    if (content.value) {
      content.value.scrollTo({
        top: content.value.scrollHeight,
        behavior: 'smooth'  // 使用平滑滚动
      });
    }
  });
}


onMounted(async ()=>{
    if(!user.value){
        router.push('/chat')
    }
    let res=await get_history_msg(user.value.target_user_id,limit,offset)
    //翻转消息列表
    msg_list.value=res.data.reverse()
    total=res.total
    nextTick(()=>{
      scrollToBottom()
    })
   //监听消息列表
   obs.observe(check_point.value)
})
watchEffect(async()=>{
    if(user.value){
        let res=await get_history_msg(user.value.target_user_id,limit,offset)
    msg_list.value=res.data
    total=res.total
    }
    chatStore.$state.ws.send(JSON.stringify({
      target_user_id:user.value.target_user_id,
      content:'',
      chat_type:'one_to_on1',
      "type":'heart_beat'
    }))
    create_heart_beat()
})
onUnmounted(()=>{
    obs.disconnect()
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