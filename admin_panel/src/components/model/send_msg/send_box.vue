<template>
  <div class="private-message-sender">
    <div class="sender-header">
      <h3>系统消息发送</h3>
    </div>

    <div class="receiver-input">
      <label>目标用户ID：</label>
      <input
        type="text"
        v-model="targetUserId"
        placeholder="输入接收者用户ID"
        @keyup.enter="sendMessage"
      />
    </div>

    <div class="message-content">
      <label>消息内容：</label>
      <textarea
        v-model="messageContent"
        placeholder="输入系统消息内容"
        rows="4"
      ></textarea>
    </div>

    <div class="send-button">
      <button @click="sendMessage">发送系统消息</button>
    </div>

    <div class="status-message" :class="{ error: sendStatus.error }">
      {{ sendStatus.message }}
    </div>
  </div>
</template>
  
  <script setup>
import { ref } from "vue";
import { useStore } from "@/model/store/store";

const store = useStore();
const targetUserId = ref("");
const messageContent = ref("");

const sendStatus = ref({
  error: false,
  message: "",
});

const sendMessage = async () => {
  if (!targetUserId.value || !messageContent.value) {
    sendStatus.value = {
      error: true,
      message: "用户ID和消息内容不能为空",
    };
    return;
  }

  try {
    const message = {
      type: "sys_msg",
      target_user_id: targetUserId.value,
      content: {
        text: messageContent.value,
        timestamp: new Date().toISOString(),
      },
    };

    // 通过store中的WebSocket发送消息
    if (store.$state.ws?.readyState === WebSocket.OPEN) {
      store.$state.ws.send(JSON.stringify(message));
      sendStatus.value = {
        error: false,
        message: "系统消息发送成功",
      };
      messageContent.value = ""; // 清空消息内容
    } else {
      throw new Error("WebSocket连接未就绪");
    }
  } catch (error) {
    sendStatus.value = {
      error: true,
      message: `发送失败: ${error.message}`,
    };
  }
};
</script>
  
  <style scoped>
.private-message-sender {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.sender-header h3 {
  margin: 0 0 20px 0;
  color: #333;
  text-align: center;
}

.receiver-input,
.message-content {
  margin-bottom: 15px;
}

.receiver-input label,
.message-content label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.receiver-input input,
.message-content textarea {
  width: calc(100% - 16px);
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.message-content textarea {
  resize: vertical;
}

.send-button {
  text-align: center;
}

.send-button button {
  padding: 8px 16px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-button button:hover {
  background-color: #40a9ff;
}

.status-message {
  margin-top: 15px;
  padding: 8px;
  border-radius: 4px;
  text-align: center;
}

.status-message.error {
  background-color: #fff2f0;
  color: #f5222d;
  border: 1px solid #ffccc7;
}
</style>