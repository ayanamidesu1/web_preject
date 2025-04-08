<template>
  <div class="sys_notice">
    <div class="header">
      <div class="sys_info">
        <img
          src="https://www.sunyuanling.com/server/static/svg/管理员.svg"
          alt="头像"
          class="avatar"
        />
        <span class="sys_name">系统通知</span>
      </div>
    </div>

    <div class="notice_container">
      <div class="notice_list">
        <div class="check_point" ref="check_point" style="display:flex;width:100%;height:1px;opacity: 0;"></div>
        <div
          class="notice_item"
          v-for="(item, index) in sys_notice"
          :key="index"
          :class="{ unread: item.receiver_read_status === '未读' }"
        >
        <review_msg :msg="item.content" :time="item.time" v-if="(item.msg_type=='review_msg')" :key="index"></review_msg>
        <div v-else>
            <div class="notice_header">
                <span class="notice_title">{{ item.content.title }}</span>
                <span class="notice_time">{{ api.formatTimeAgo(item.time) }}</span>
              </div>
              <div class="notice_content">{{ item.content.content }}</div>
        </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script setup>
import { ref, onMounted, nextTick, onUnmounted,watchEffect } from "vue";
import { BaseApi } from "@/base_api";
import { useChatStore } from "./chat_store";
import review_msg from "./review_msg.vue";

const chat_store = useChatStore();
const api = new BaseApi();
const sys_notice = ref([]);
let limit = ref(10);
let offset = ref(0);
let total = ref(0);
let check_point = ref(null);
let ws_ready = ref(false);

async function ws_connect(){
  // 实时消息通知
  chat_store.$state.ws.addEventListener('message',(e)=>{
    let data = JSON.parse(e.data);
    console.log(data);
    if(data.msg_type=='all'||data.msg_type=='review_msg'){
      console.log(data);
    }
    if (data.msg_type == "all") {
      sys_notice.value.push({
        ...data,
        content:
          typeof data.content === "string"
            ? JSON.parse(data.content.replace(/'/g, '"'))
            : data.content,
      });
    }
    if(data.msg_type=='review_msg'){
        sys_notice.value.push({
            ...data,
            content: typeof data.content==="string"?JSON.parse(data.content.replace(/'/g, '"')):JSON.parse(data.content)
        });
    }
  })
  console.log("WebSocket连接成功，监听消息");
};

watchEffect(
  ()=>{
    
    if(!chat_store.$state.ws){
      console.log('websocket连接未就绪，等待中...')
      return ;
    }
    try{
      if(chat_store.$state.ws.readyState===WebSocket.OPEN){
      ws_connect()
      if(chat_store.$state.ws.onmessage){
          console.log("WebSocket连接成功，监听消息，不再重试");
          return ;
        }
    }else{
      console.log("WebSocket连接失败，正在重试...");
      setTimeout(() => {
        ws_connect()
        if(chat_store.$state.ws.onmessage){
          console.log("WebSocket连接成功，监听消息，不再重试");
          return ;
        }
      }, 1000);
    }
    }
    catch(e){
      console.error("WebSocket连接失败，正在重试...");
      setTimeout(() => {        
        ws_connect()
        if(chat_store.$state.ws.onmessage){
          console.log("WebSocket连接成功，监听消息，不再重试");
          return ;
        }
      }, 1000);
    }
  }
)

function safeParseContent(content) {
  if (typeof content !== "string") return content;

  // 尝试1：直接解析标准JSON
  try {
    return JSON.parse(content);
  } catch (e) {
    // 不是标准JSON，继续尝试
  }

  // 尝试2：处理单引号包裹的类JSON
  if (content.trim().startsWith("{") && content.trim().endsWith("}")) {
    try {
      return JSON.parse(content.replace(/'/g, '"'));
    } catch (e) {
      // 仍然失败，按纯文本处理
    }
  }

  // 最终回退：作为纯文本返回
  return {
    title: "系统消息",
    content: content,
  };
}

// 获取系统通知
async function get_sys_notice() {
  try {
    const res = await api.post("GetUserInfo/get_sys_msg_list", {
      limit: limit.value,
      offset: offset.value,
    });

    if (res.status == 200) {
      sys_notice.value = res.result.data.map((item) => ({
        ...item,
        content: safeParseContent(item.content),
      }));
      total.value = res.result.total;
      //翻转数组
      sys_notice.value.reverse();
      //按时间重排
      sys_notice.value = sort_by_time(sys_notice.value);
    }
  } catch (e) {
    console.error("获取系统通知失败:", e);
    // 可选：显示用户友好的错误提示
    showToast("加载通知失败，请稍后重试");
  }
}
//获取更多
async function get_more_sys_notice() {
  offset.value += limit.value;
  try {
    const res = await api.post("GetUserInfo/get_sys_msg_list", {
      limit: limit.value,
      offset: offset.value,
    });

    if (res.status == 200) {
      sys_notice.value.push(...res.result.data);
      //按时间重排
        sys_notice.value = sort_by_time(sys_notice.value);
      total.value = res.result.total;
    }
  } catch (e) {
    console.error("获取更多系统通知失败:", e);
  }
}

let observer = new IntersectionObserver((entries) => {
  entries.forEach(async (entry) => {
    if (entry.isIntersecting) {
      await get_more_sys_notice();
    }
  });
},{
    root: null,
    rootMargin: "0px",
    threshold: 1.0,
});
//通过time进行重排序，旧的消息在栈顶新的在栈底
function sort_by_time(value){
    return value.sort((a, b) => {
        return new Date(a.time) - new Date(b.time);
    });
}

onMounted(() => {
  get_sys_notice();
  
  observer.observe(check_point.value);
});
onUnmounted(() => {
  observer.disconnect(check_point.value);
  chat_store.$state.ws.removeEventListener('notice_msg',(e)=>{})
});
</script>
  
  <style scoped>
.sys_notice {
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
  max-width: 100%;
  margin: 0 auto;
  background-color: #f5f7fa;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  height: 100%;
  min-width: calc(100% - 20px);
  padding: 10px;
}

.header {
  padding: 16px;
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
  width: calc(100% - 20px);
  border-radius: 8px 8px 0 0;
}

.sys_info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
  border: 2px solid white;
}

.sys_name {
  font-size: 18px;
  font-weight: 500;
}

.notice_container {
  padding: 16px;
  max-height: calc(100% - 40px);
  min-width: calc(100% - 20px);
  overflow-y: auto;
}

.notice_list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: calc(100vh - 300px);
    overflow-y: auto;
}

.notice_item {
  background-color: white;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

.notice_item.unread {
  border-left: 4px solid #409eff;
  background-color: #f0f7ff;
}

.notice_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.notice_title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.notice_time {
  font-size: 12px;
  color: #909399;
}

.notice_content {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

/* 滚动条样式 */
.notice_container::-webkit-scrollbar {
  width: 6px;
}

.notice_container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.notice_container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.notice_container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>