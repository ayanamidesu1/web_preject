<template>
    <div class="init-pay-account">
      <div class="card">
        <h2>初始化支付账户</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="pay-password">支付密码 (6位数字)</label>
            <input
              id="pay-password"
              v-model="form.pay_password"
              type="password"
              placeholder="请输入6位数字支付密码"
              maxlength="6"
              :class="{ 'error': errors.pay_password }"
            />
            <span class="error-message" v-if="errors.pay_password">{{ errors.pay_password }}</span>
          </div>
  
          <div class="form-group">
            <label for="confirm-password">确认支付密码</label>
            <input
              id="confirm-password"
              v-model="form.confirm_password"
              type="password"
              placeholder="请再次输入支付密码"
              maxlength="6"
              :class="{ 'error': errors.confirm_password }"
            />
            <span class="error-message" v-if="errors.confirm_password">{{ errors.confirm_password }}</span>
          </div>
  
          <button type="submit" :disabled="loading">
            {{ loading ? '处理中...' : '确认初始化' }}
          </button>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { BaseApi } from '@/base_api'
  
  const router = useRouter()
  const api = new BaseApi()
  const loading = ref(false)
  
  // 表单数据
  const form = reactive({
    pay_password: '',
    confirm_password: ''
  })
  
  // 错误信息
  const errors = reactive({
    pay_password: '',
    confirm_password: ''
  })
  
  // 验证表单
  const validateForm = () => {
    let isValid = true
    
    // 清空错误信息
    errors.pay_password = ''
    errors.confirm_password = ''
  
    // 验证支付密码
    if (!form.pay_password) {
      errors.pay_password = '请输入支付密码'
      isValid = false
    } else if (!/^\d{6}$/.test(form.pay_password)) {
      errors.pay_password = '支付密码必须为6位数字'
      isValid = false
    }
  
    // 验证确认密码
    if (!form.confirm_password) {
      errors.confirm_password = '请确认支付密码'
      isValid = false
    } else if (form.confirm_password !== form.pay_password) {
      errors.confirm_password = '两次输入的密码不一致'
      isValid = false
    }
  
    return isValid
  }
  
  // 提交处理
  const handleSubmit = async () => {
    if (!validateForm()) return
    
    try {
      loading.value = true
      
      // 调用API
      const response = await api.post('api/InitPayAccount', {
        pay_password: form.pay_password
      })
      
      if (response.status === 200) {
        alert(response.result.msg || '支付账户初始化成功')
        router.push('/') // 跳转到首页
      } else {
        console.error('初始化失败:', response.result)
        alert(response.result.msg || '初始化失败')
      }
    } catch (error) {
      console.error('初始化失败:', error)
      alert('初始化失败，请稍后再试')
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .init-pay-account {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f5f5;
    padding: 20px;
  }
  
  .card {
    width: 100%;
    max-width: 500px;
    padding: 30px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
  
  h2 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
  }
  
  input {
    width: 100%;
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
    box-sizing: border-box;
  }
  
  input.error {
    border-color: #f56c6c;
  }
  
  .error-message {
    color: #f56c6c;
    font-size: 12px;
    margin-top: 5px;
    display: block;
  }
  
  button {
    width: 100%;
    padding: 12px;
    background-color: #409eff;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #66b1ff;
  }
  
  button:disabled {
    background-color: #a0cfff;
    cursor: not-allowed;
  }
  </style>