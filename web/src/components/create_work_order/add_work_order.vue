<template>
  <div class="content">
    <div class="create_func">
      <div class="form-container">
        <h2>新建约稿方案</h2>
        <form @submit.prevent="add_order" class="func-form">
          <!-- 方案标题 -->
          <div class="form-group">
            <label for="title">方案标题</label>
            <input id="title" v-model="formData.title" type="text" placeholder="请输入方案标题" required />
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
            <textarea id="introduce" v-model="formData.introduce" placeholder="请详细描述约稿要求" required></textarea>
          </div>

          <!-- 标签 -->
          <div class="form-group">
            <label for="tags">标签</label>
            <input id="tags" v-model="formData.tags" type="text" placeholder="用逗号分隔多个标签" required />
          </div>

          <!-- 金额 -->
          <div class="form-group">
            <label for="amount">约稿金额</label>
            <input id="amount" v-model="formData.amount_of_money" type="number" min="0" step="0.01" placeholder="请输入金额"
              required />
          </div>
          <div class="form-group">
            <label for="tags">备注</label>
            <input id="back" type="text" v-model="formData.back" placeholder="请输入约稿备注"></input>
          </div>

          <!-- 封面图片 -->
          <div class="form-group">
            <label>封面图片</label>
            <div v-if="previewImage" class="image-preview">
              <img :src="previewImage" alt="封面预览" />
            </div>
          </div>

          <!-- 提交按钮 -->
          <div class="form-actions">
            <button type="submit" :disabled="submitting">
              {{ submitting ? '提交中...' : '提交订单' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    <div class="func_list">
      用户方案列表
      <func_list :user_id="user_id" v-if="user_id" @choose_item="fillFormFromFunc"></func_list>
    </div>
  </div>
</template>

<script setup>
import { ref,onMounted,computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '@assets/model/store'
import { BaseApi } from '@/base_api'
import func_list from './func_list.vue'

const router = useRouter()
const store = useStore()
const api = new BaseApi()
const is_ready=ref(false)
const user_id=computed(()=>{
  return router.currentRoute.value.query.id
})

const formData = ref({
  title: '',
  work_type: '',
  age_classification: '',
  introduce: '',
  tags: '',
  amount_of_money: 0.00,
  back:''
})

const previewImage = ref(null)
const selectedFile = ref(null)
const submitting = ref(false)

// 提交表单
const add_order=async ()=>{
  try{
    let res=await api.post('api/AddOrder',{
      work_type:formData.value.work_type=='illustration'?'ill':formData.value.work_type,
      amount_of_money:formData.value.amount_of_money,
      target_user_id:user_id.value,
      work_introduce:formData.value.introduce,
      age_classification:formData.value.age_classification
    })
    if(res.status==200){
      alert('约稿消息发送成功，请注意查看约稿中心的约稿状态')
    }
    else{
      console.log(res)
    }
  }
  catch(e){
    console.log(e)
    submitting.value=false
  }
}

const fillFormFromFunc = (item) => {
  formData.value = {
    title: item.title || '',
    work_type: item.work_type || '',
    age_classification: item.age_classification || '',
    introduce: item.introduce || '',
    tags: item.tags || '',
    amount_of_money: Number(item.amount_of_money) || 0
  }

  // 设置封面图预览，但不允许直接替换上传文件
  previewImage.value = getCoverUrl(item.cover)
  selectedFile.value = null // 代表未修改
}
const getCoverUrl = (fileName) => {
    // 根据你项目封面图路径调整此处
    return `https://www.sunyuanling.com/server/static/image/${fileName}`
}

</script>

<style scoped>
.content {
  display: grid;
  grid-template-columns: minmax(500px, 1fr) minmax(200px, 300px);
  width: 90%;
  margin: 0 auto;
  padding: 20px;
}

.create_func {
  width: calc(100% - 40px);
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

input,
select,
textarea {
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