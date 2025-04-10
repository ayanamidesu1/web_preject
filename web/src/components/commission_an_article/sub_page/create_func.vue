<template>
    <div class="create_func">
      <div class="form-container">
        <h2>新建约稿方案</h2>
        <form @submit.prevent="submitForm" class="func-form">
          <!-- 方案标题 -->
          <div class="form-group">
            <label for="title">方案标题</label>
            <input
              id="title"
              v-model="formData.title"
              type="text"
              placeholder="请输入方案标题"
              required
            />
          </div>
  
          <!-- 作品类型 -->
          <div class="form-group">
            <label>作品类型</label>
            <select v-model="formData.work_type" required>
              <option value="">请选择类型</option>
              <option value="illustration">插画</option>
              <option value="comic">漫画</option>
              <option value="novel">小说</option>
            </select>
          </div>
  
          <!-- 年龄分级 -->
          <div class="form-group">
            <label>年龄分级</label>
            <select v-model="formData.age_classification" required>
              <option value="">请选择分级</option>
              <option value="all">全年龄</option>
              <option value="r15">R15</option>
              <option value="r18">R18</option>
            </select>
          </div>
  
          <!-- 作品介绍 -->
          <div class="form-group">
            <label for="introduce">作品介绍</label>
            <textarea
              id="introduce"
              v-model="formData.introduce"
              placeholder="请详细描述约稿要求"
              required
            ></textarea>
          </div>
  
          <!-- 标签 -->
          <div class="form-group">
            <label for="tags">标签</label>
            <input
              id="tags"
              v-model="formData.tags"
              type="text"
              placeholder="用逗号分隔多个标签"
              required
            />
          </div>
  
          <!-- 金额 -->
          <div class="form-group">
            <label for="amount">约稿金额</label>
            <input
              id="amount"
              v-model="formData.amount_of_money"
              type="number"
              min="0"
              step="0.01"
              placeholder="请输入金额"
              required
            />
          </div>
  
          <!-- 封面图片 -->
          <div class="form-group">
            <label>封面图片</label>
            <input
              type="file"
              accept="image/*"
              @change="handleFileUpload"
              required
            />
            <div v-if="previewImage" class="image-preview">
              <img :src="previewImage" alt="封面预览" />
            </div>
          </div>
  
          <!-- 提交按钮 -->
          <div class="form-actions">
            <button type="submit" :disabled="submitting">
              {{ submitting ? '提交中...' : '创建方案' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useStore } from '@assets/model/store'
  import { BaseApi } from '@/base_api'
  
  const router = useRouter()
  const store = useStore()
  const api = new BaseApi()
  
  const formData = ref({
    title: '',
    work_type: '',
    age_classification: '',
    introduce: '',
    tags: '',
    amount_of_money: 0
  })
  
  const previewImage = ref(null)
  const selectedFile = ref(null)
  const submitting = ref(false)
  
  // 处理文件上传
  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      selectedFile.value = file
      previewImage.value = URL.createObjectURL(file)
    }
  }
  
 // 提交表单
const submitForm = async () => {
  if (!selectedFile.value) {
    alert('请上传封面图片')
    return
  }

  submitting.value = true
  
  try {
    const form = new FormData()
    form.append('file', selectedFile.value)
    form.append('data', JSON.stringify(formData.value))

    // 获取用户token
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const response = await fetch('https://www.sunyuanling.com/api/api/AddFunc', {
      method: 'POST',
      body: form,
      headers: {
        'Authorization': `token ${token}`
      }
    })

    const result = await response.json()

    if (response.ok) {
      alert('方案创建成功')
      router.push('/my-functions')
    } else {
      throw new Error(result.msg || '创建失败')
    }
  } catch (error) {
    console.error('创建方案出错:', error)
    alert(error.message || '创建过程中出现错误，请稍后重试')
  } finally {
    submitting.value = false
  }
}
  </script>
  
  <style scoped>
  .create_func {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .form-container {
    background: #fff;
    border-radius: 8px;
    padding: 25px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  h2 {
    text-align: center;
    margin-bottom: 25px;
    color: #333;
  }
  
  .func-form {
    display: grid;
    gap: 20px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .form-group label {
    font-weight: 600;
    color: #555;
  }
  
  input, select, textarea {
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  
  textarea {
    min-height: 120px;
    resize: vertical;
  }
  
  .image-preview {
    margin-top: 10px;
  }
  
  .image-preview img {
    max-width: 200px;
    max-height: 200px;
    border-radius: 4px;
    border: 1px solid #eee;
  }
  
  .form-actions {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
  
  button {
    padding: 12px 25px;
    background-color: #4a6bff;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover:not(:disabled) {
    background-color: #3a5bef;
  }
  
  button:disabled {
    background-color: #a0b0ff;
    cursor: not-allowed;
  }
  </style>