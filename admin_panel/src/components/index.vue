<template>
    <div class="index">
      <header_page></header_page>
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted, watch } from "vue";
  import { useRouter } from "vue-router";
  import { useStore } from "@/model/store/store";
  import header_page from "@/components/model/header_page.vue";
  import { BaseApi } from "@/base_api";
  
  const router = useRouter();
  const store = useStore();
  const api = new BaseApi();
  
  // 连接管理状态
  const connectionStatus = ref('disconnected');
  const retryCount = ref(0);
  const maxRetries = 5;
  const baseRetryDelay = 3000;
  let reconnectTimer = null;
  let connectionTimeout = null;
  
  // 获取 WebSocket 配置
  const getWsConfig = () => ({
    url: "wss://www.sunyuanling.com/ws/chat",
    token: localStorage.getItem("token") || '',
    role: "sys_admin",
    user_id: store.$state.user?.userid || '',
    target_url:`wss://www.sunyuanling.com/ws/chat?role=sys_admin&user_id=${store.$state.user?.userid}&token=${localStorage.getItem("token")}`
  });
  
  // 安全关闭连接
  const safeCloseConnection = () => {
    if (store.$state.ws) {
      // 移除所有事件监听器避免内存泄漏
      store.$state.ws.onopen = null;
      store.$state.ws.onclose = null;
      store.$state.ws.onerror = null;
      store.$state.ws.onmessage = null;
      
      // 检查连接状态后再关闭
      if ([WebSocket.OPEN, WebSocket.CONNECTING].includes(store.$state.ws.readyState)) {
        store.$state.ws.close(1000, '正常关闭');
      }
      store.$state.ws = null;
    }
    clearTimeout(reconnectTimer);
    clearTimeout(connectionTimeout);
    connectionStatus.value = 'disconnected';
  };
  
  // 初始化 WebSocket 连接
  const initWebSocket = () => {
    safeCloseConnection();
    
    const config = getWsConfig();
    if (!config.token || !config.user_id) {
      console.warn('缺少连接必要参数: token 或 user_id');
      return;
    }
  
    try {
      //const wsUrl = `${config.url}?token=${config.token}&role=${config.role}&user_id=${config.user_id}`;
      store.$state.ws = new WebSocket(getWsConfig().target_url);
      connectionStatus.value = 'connecting';
      
      // 连接超时处理 (8秒)
      connectionTimeout = setTimeout(() => {
        if (store.$state.ws?.readyState === WebSocket.CONNECTING) {
          console.warn('连接超时，强制关闭');
          safeCloseConnection();
          handleReconnect();
        }
      }, 8000);
  
      // 事件处理器
      store.$state.ws.onopen = () => {
        clearTimeout(connectionTimeout);
        console.log("WebSocket 连接成功");
        connectionStatus.value = 'connected';
        retryCount.value = 0;
      };
  
      store.$state.ws.onclose = (event) => {
        clearTimeout(connectionTimeout);
        console.log(`连接关闭，代码: ${event.code}，原因: ${event.reason}`);
        connectionStatus.value = 'disconnected';
        
        // 非正常关闭时重连 (code 1000 为正常关闭)
        if (event.code !== 1000) {
          handleReconnect();
        }
      };
  
      store.$state.ws.onerror = (error) => {
        clearTimeout(connectionTimeout);
        console.error("WebSocket 错误:", error);
        connectionStatus.value = 'error';
        // 错误事件后会触发 onclose，所以不需要单独处理重连
      };
  
      store.$state.ws.onmessage = (event) => {
        let data=JSON.parse(event.data)
        //console.log("收到消息:", data);
        // 处理业务消息...
      };
  
    } catch (error) {
      console.error("WebSocket 初始化异常:", error);
      safeCloseConnection();
      handleReconnect();
    }
  };
  
  // 处理重连逻辑
  const handleReconnect = () => {
    if (retryCount.value >= maxRetries) {
      console.warn(`已达到最大重试次数 (${maxRetries})，停止自动重连`);
      return;
    }
  
    retryCount.value += 1;
    const delay = Math.min(baseRetryDelay * Math.pow(2, retryCount.value - 1), 30000); // 指数退避，最大30秒
  
    console.log(`将在 ${Math.round(delay/1000)} 秒后尝试第 ${retryCount.value} 次重连...`);
    connectionStatus.value = 'reconnecting';
  
    reconnectTimer = setTimeout(() => {
      initWebSocket();
    }, delay);
  };
  
  // 获取用户信息
  const get_self_info = async () => {
    try {
      const res = await api.get_self_info();
      if (res.status === 200) {
        store.$state.user = res.result.data;
        initWebSocket(); // 获取用户信息后初始化连接
      } else {
        console.error("获取用户信息失败:", res);
        router.push("/login");
      }
    } catch (error) {
      console.error("获取用户信息异常:", error);
    }
  };
  
  // 检查登录状态
  const check_login_status = async () => {
    try {
      const res = await api.verify_login();
      if (res.status !== 200) {
        console.error("登录验证失败:", res);
        router.push("/login");
      }
    } catch (error) {
      console.error("登录验证异常:", error);
    }
  };
  
  // 监听用户ID变化
  watch(() => store.$state.user?.userid, (newVal) => {
    if (newVal) {
      console.log("检测到 userid 变化，重新连接 WebSocket");
      initWebSocket();
    }
  });
  
  onMounted(() => {
    check_login_status().then(get_self_info);
  });
  
  onUnmounted(() => {
    safeCloseConnection();
  });
  </script>
  
  <style scoped>
  .index {
    display: grid;
    width: 90%;
    margin: 10px auto;
    grid-template-rows: 100px 1fr;
  }
  </style>