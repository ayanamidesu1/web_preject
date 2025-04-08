<template>
    <div class="notice-container">
      <div class="notice-card">
        <h1 class="notice-title">发送通知</h1>
        
        <div class="form-group">
          <label for="title-input" class="form-label">通知标题</label>
          <input 
            id="title-input"
            type="text" 
            placeholder="请输入通知标题" 
            v-model="title" 
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="content-input" class="form-label">通知内容</label>
          <textarea 
            id="content-input"
            placeholder="请输入通知内容" 
            v-model="content"
            class="form-textarea"
            rows="5"
          ></textarea>
        </div>
        
        <button 
          @click="send_notice"
          class="send-button"
          :disabled="!isFormValid"
        >
          <span v-if="!isSending">发送通知</span>
          <span v-else class="loading">
            <span class="spinner"></span> 发送中...
          </span>
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { BaseApi } from '@/base_api';
  import { useStore } from '@/model/store/store';
  
  const api = new BaseApi();
  const store = useStore();
  const title = ref('')
  const content = ref('')
  const isSending = ref(false)
  
  const msg = computed(() => ({
    type: 'group_msg',
    content: {
      title: title.value,
      content: content.value
    }
  }))
  
  // 验证表单是否有效
  const isFormValid = computed(() => {
    return title.value.trim() !== '' && content.value.trim() !== ''
  })
  
  // 发送全局消息
  async function send_notice() {
    if (!isFormValid.value || isSending.value) return
    
    try {
      isSending.value = true
      store.$state.ws.send(JSON.stringify(msg.value))
      
      // 清空表单
      title.value = ''
      content.value = ''
      
      // 模拟发送延迟
      await new Promise(resolve => setTimeout(resolve, 1000))
    } catch (error) {
      console.error('发送通知失败:', error)
    } finally {
      isSending.value = false
    }
  }
  </script>
  
  <style scoped>
  .notice-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f7fa;
    padding: 20px;
  }
  
  .notice-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    padding: 32px;
    width: 100%;
    max-width: 600px;
  }
  
  .notice-title {
    font-size: 24px;
    font-weight: 600;
    color: #333;
    margin-bottom: 24px;
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-label {
    display: block;
    font-size: 14px;
    color: #555;
    margin-bottom: 8px;
    font-weight: 500;
  }
  
  .form-input,
  .form-textarea {
    width: calc(100% - 32px);
    padding: 12px 16px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.3s ease;
  }
  
  .form-input:focus,
  .form-textarea:focus {
    outline: none;
    border-color: #409eff;
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
  }
  
  .form-input {
    height: 44px;
  }
  
  .form-textarea {
    min-height: 120px;
    resize: vertical;
  }
  
  .send-button {
    width: 100%;
    padding: 12px;
    background-color: #409eff;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 16px;
  }
  
  .send-button:hover {
    background-color: #66b1ff;
  }
  
  .send-button:active {
    background-color: #3a8ee6;
  }
  
  .send-button:disabled {
    background-color: #c0c4cc;
    cursor: not-allowed;
  }
  
  .loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  
  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 1s ease-in-out infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  /* 响应式设计 */
  @media (max-width: 640px) {
    .notice-card {
      padding: 24px 16px;
    }
    
    .notice-title {
      font-size: 20px;
    }
  }
  </style>