<template>
  <div class="header_page">
    <div class="content">
      <div class="user_item">
        <div class="username">
          <span>欢迎管理员：{{ username }}</span>
        </div>
        <div class="user_avatar">
          <img
            src="https://www.sunyuanling.com/server/static/image/avatar_thumbnail/65014220_p0.jpg"
            alt="User Avatar"
          />
        </div>
      </div>
      <div class="online_status">
        <span :class="statusClass">{{ statusText }}</span>
      </div>
      <div class="logout" @click="logout">
        <div class="logout_btn">
          <span>退出登录</span>
          <img
            class="icon"
            src="https://www.sunyuanling.com/assets/logout.svg"
            alt="Logout Icon"
          />
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup>
import { ref, computed, onMounted, onUnmounted,watch } from "vue";
import { useStore } from "@/model/store/store";

const store = useStore();
const username = ref("admin");
const lastActiveTime = ref(Date.now()); // 最后收到消息的时间戳
const checkInterval = ref(null); // 周期检查的定时器

// 判断服务器是否存活（6.5秒内收到过消息）
const isServerAlive = computed(() => {
  return Date.now() - lastActiveTime.value < 6500;
});

// 状态显示
const statusText = computed(() => isServerAlive.value ? "在线" : "离线");
const statusClass = computed(() => ({
  online: isServerAlive.value,
  offline: !isServerAlive.value
}));

// 处理服务器消息（更新最后活跃时间）
const handleServerMessage = (event) => {
  try {
    const data = JSON.parse(event.data);
    if (data.server) { // 只要是服务器消息都更新
      lastActiveTime.value = Date.now();
    }
  } catch (e) {
    console.warn('消息解析错误', e);
  }
};

// 初始化周期检查
const startHealthCheck = () => {
  checkInterval.value = setInterval(() => {
    // 空执行，仅触发computed重新计算
  }, 6500);
};

// 监听WebSocket状态变化
watch(() => store.$state.ws_ready, (ready) => {
  if (ready) {
    store.$state.ws.addEventListener('message', handleServerMessage);
    lastActiveTime.value = Date.now(); // 连接成功时立即标记为活跃
    startHealthCheck();
  } else {
    if (store.$state.ws) {
      store.$state.ws.removeEventListener('message', handleServerMessage);
    }
    clearInterval(checkInterval.value);
  }
});

onMounted(() => {
  // 初始化时若已连接则立即开始监听
  if (store.$state.ws_ready) {
    store.$state.ws.addEventListener('message', handleServerMessage);
    startHealthCheck();
  }
});

onUnmounted(() => {
  clearInterval(checkInterval.value);
  if (store.$state.ws) {
    store.$state.ws.removeEventListener('message', handleServerMessage);
  }
});
</script>
  
  <style scoped>
.header_page {
  width: 100%;
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f4f4f4;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 5;
}

.content {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
}

.user_item {
  display: flex;
  align-items: center;
}

.username {
  margin-right: 15px;
  font-size: 16px;
  color: #333;
}

.user_avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.logout {
  cursor: pointer;
  display: flex;
  align-items: center;
  width: auto;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5px 10px;
  border-radius: 5px;
}
.logout:hover {
  background-color: rgba(233, 233, 233, 1);
  transform: scale(1.05);
  transition: all 0.2s ease-in-out;
  transform: translateY(-2px);
}

.logout_btn {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #000000;
}

.icon {
  width: 20px;
  height: 20px;
  margin-left: 8px;
  object-fit: cover;
}
.online_status span {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 500;
}

.online {
  background-color: rgba(82, 196, 26, 0.1);
  color: #52c41a;
}

.offline {
  background-color: rgba(245, 34, 45, 0.1);
  color: #f5222d;
}
</style>
  