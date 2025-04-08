<template>
    <div class="generate-password-card">
      <div class="card">
        <div class="card-header">
          <h2>生成密码卡</h2>
        </div>
        
        <form @submit.prevent="submitForm" class="generate-form">
          <div class="form-group">
            <label>生成数量 (1-10000)</label>
            <input 
              type="number" 
              v-model.number="form.count" 
              min="1" 
              max="10000"
              required
              class="form-input"
            >
          </div>
          
          <div class="form-group">
            <label>有效天数 (1-365)</label>
            <input 
              type="number" 
              v-model.number="form.day" 
              min="1" 
              max="365"
              required
              class="form-input"
            >
          </div>
          
          <div class="form-group">
            <label>卡片价格 (≥0)</label>
            <input 
              type="number" 
              v-model.number="form.price" 
              min="0" 
              step="0.00000001"
              required
              class="form-input"
            >
          </div>
          
          <div class="form-actions">
            <button 
              type="submit" 
              :disabled="loading"
              class="btn btn-primary"
            >
              <span v-if="!loading">生成卡密</span>
              <span v-else>生成中...</span>
            </button>
            <button 
              type="button" 
              @click="resetForm"
              class="btn"
            >
              重置
            </button>
          </div>
        </form>
        
        <div v-if="result" class="result-section">
          <h3>生成结果</h3>
          <div class="alert success">
            成功生成 {{ result.count }} 张密码卡
          </div>
          <div class="action-buttons">
            <button @click="exportCards" class="btn btn-primary">
              <span class="icon">↓</span>
              导出卡密
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive } from 'vue'
  import { BaseApi } from '@/base_api'
  
  const api = new BaseApi()
  const loading = ref(false)
  const result = ref(null)
  
  // 表单数据
  const form = reactive({
    count: 10,
    day: 30,
    price: 0.00000000
  })
  
  // 提交表单
  const submitForm = async () => {
    // 客户端验证
    if (form.count < 1 || form.count > 10000) {
      alert('数量必须在1-10000之间')
      return
    }
    if (form.day < 1 || form.day > 365) {
      alert('天数必须在1-365之间')
      return
    }
    if (form.price < 0) {
      alert('价格不能为负数')
      return
    }
  
    loading.value = true
    try {
      const res = await api.post('admin_control/GeneratePasswordCard', {
        count: form.count,
        day: form.day,
        price: form.price
      })
      
      if (res.status === 200) {
        result.value = res.data
        alert('生成成功')
      } else {
        alert(res.msg || '生成失败')
      }
    } catch (error) {
      console.error(error)
      alert('请求失败，请检查网络')
    } finally {
      loading.value = false
    }
  }
  
  // 重置表单
  const resetForm = () => {
    form.count = 10
    form.day = 30
    form.price = 0.00000000
    result.value = null
  }
  
  // 导出卡密
  const exportCards = () => {
    alert('导出功能开发中...')
  }
  </script>
  
  <style scoped>
  .generate-password-card {
    max-width: 800px;
    margin: 20px auto;
    font-family: Arial, sans-serif;
  }
  
  .card {
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
  }
  
  .card-header {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .card-header h2 {
    margin: 0;
    color: #333;
  }
  
  .generate-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .form-group label {
    font-weight: bold;
    color: #555;
  }
  
  .form-input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  
  .form-input:focus {
    outline: none;
    border-color: #409eff;
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
  }
  
  .form-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
  }
  
  .btn {
    padding: 10px 16px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-primary {
    background-color: #409eff;
    color: white;
  }
  
  .btn-primary:hover {
    background-color: #66b1ff;
  }
  
  .btn-primary:disabled {
    background-color: #a0cfff;
    cursor: not-allowed;
  }
  
  .btn {
    background-color: #f4f4f5;
    color: #606266;
  }
  
  .btn:hover {
    background-color: #e9e9eb;
  }
  
  .result-section {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #eee;
  }
  
  .alert {
    padding: 12px;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  
  .alert.success {
    background-color: #f0f9eb;
    color: #67c23a;
    border: 1px solid #e1f3d8;
  }
  
  .action-buttons {
    margin-top: 15px;
  }
  
  .icon {
    margin-right: 5px;
  }
  </style>