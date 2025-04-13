<template>
  <div class="receiver-request-container">
    <h2 class="section-title">收到的约稿申请</h2>
    
    <div class="filter-controls">
      <div class="filter-tabs">
        <button 
          class="filter-tab" 
          :class="{ active: filter_type === 'all' }" 
          @click="changeFilter('all')"
        >
          全部
        </button>
        <button 
          class="filter-tab" 
          :class="{ active: filter_type === 'cancel' }" 
          @click="changeFilter('cancel')"
        >
          已取消
        </button>
      </div>
      
      <div class="filter-options">
        <div class="filter-group">
          <label>筛选</label>
          <select 
            v-model="status_filter" 
            @change="fetchData"
            class="filter-select"
          >        
            <option value="all">所有状态</option>
            <option value="5">已拒绝</option>
            <option value="4">等待委托人确定</option>
            <option value="3">待处理</option>
            <option value="1">已处理</option>
            <option value="2">创作中</option>
            <option value="0">已完成</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>排序</label>
          <select 
            v-model="sort_by" 
            @change="fetchData"
            class="filter-select"
          >
            <option value="time_desc">最新</option>
            <option value="amount_desc">按金额从高到低排序</option>
            <option value="time_asc">按截稿日期从早到晚排序</option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- 订单列表展示 -->
    <div class="order-list">
      <div 
        v-for="order in order_list" 
        :key="order.id" 
        class="order-card"
        :class="getStatusClass(order.status)"
      >
        <div class="order-header">
          <span class="order-id">订单ID: #{{ order.id }}</span>
          <span class="order-amount">¥{{ order.amount_of_money }}</span>
          <span class="order-status">{{ getStatusText(order.status) }}</span>
        </div>
        <div class="order-body">
          <p class="order-field">
            <span class="field-label">工作类型:</span>
            <span class="field-value">{{ order.work_type || '未指定' }}</span>
          </p>
          <p class="order-field">
            <span class="field-label">工作介绍:</span>
            <span class="field-value">{{ order.work_introduce || '无介绍' }}</span>
          </p>
          <p class="order-field">
            <span class="field-label">创建时间:</span>
            <span class="field-value">{{ formatTime(order.time) }}</span>
          </p>
          <div class="order-field" v-if="order.status==3">
            <span class="field-label">操作：</span>
            <div class="field-value">
              <span class="accept" @click="accept_order(order.id,'agree')">接受</span>
              <span class="reject" @click="accept_order(order.id,'refuse')">拒绝</span>
            </div>
          </div>
          <div class="order-field">
            <div class="show_details" @click="show_order_details(order.id)">
              <span>查看详情</span>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="order_list.length === 0" class="empty-state">
        <img src="https://www.sunyuanling.com/server/static/svg/暂无订单.svg" alt="无订单" class="empty-icon">
        <p>暂无约稿申请</p>
      </div>
    </div>
    
    <!-- 分页控制 -->
    <div class="pagination" v-if="total > limit">
      <button 
        class="pagination-button" 
        @click="prevPage" 
        :disabled="offset === 0"
      >
        &lt; 上一页
      </button>
      <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
      <button 
        class="pagination-button" 
        @click="nextPage" 
        :disabled="offset + limit >= total"
      >
        下一页 &gt;
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router';
import { useStore } from '@assets/model/store';
import { BaseApi } from '@/base_api';

const router = useRouter();
const store = useStore();
const api = new BaseApi();

// 响应式数据
const order_list = ref([])
const filter_type = ref('all')
const status_filter = ref('all')
const sort_by = ref('time_desc')
const limit = ref(10)
const offset = ref(0)
const total = ref(0)

// 计算属性
const currentPage = computed(() => Math.floor(offset.value / limit.value) + 1)
const totalPages = computed(() => Math.ceil(total.value / limit.value))

// 状态文本映射
const statusTextMap = {
  0: '已取消',
  1: '已完成',
  2: '创作中',
  3: '待处理',
  4:'待确认',
  5:'已拒绝'
}

// 状态样式类映射
const statusClassMap = {
  0: 'cancelled',
  1: 'completed',
  2: 'in-progress',
  3: 'pending'
}

// 获取状态文本
const getStatusText = (status) => {
  return statusTextMap[status] || '未知状态'
}

// 获取状态对应的CSS类
const getStatusClass = (status) => {
  return statusClassMap[status] || ''
}

// 格式化时间
const formatTime = (time) => {
  return new Date(time).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 改变筛选类型
const changeFilter = (type) => {
  filter_type.value = type
  offset.value = 0 // 重置分页
  fetchData()
}

// 上一页
const prevPage = () => {
  if (offset.value > 0) {
    offset.value -= limit.value
    fetchData()
  }
}

// 下一页
const nextPage = () => {
  if (offset.value + limit.value < total.value) {
    offset.value += limit.value
    fetchData()
  }
}

// 获取数据
const fetchData = async () => {
  try {
    const response = await api.post('api/GetReceiverList', {
      limit: limit.value,
      offset: offset.value,
      filter_type: filter_type.value,
      status_filter: status_filter.value,
      sort_by: sort_by.value
    })
    
    if (response.status === 200) {
      order_list.value = response.result.data
      total.value = response.result.total
    } else {
      console.error('获取数据失败:', response.result)
    }
  } catch (error) {
    console.error('请求错误:', error)
  }
}

//是否接受约稿
async function accept_order(id,type){
  try{
    let res=await api.post('api/ComAnArticleOperate',{
      operate_type: type,
      order_id: id
    })
    if(res.status===200){
      alert('操作成功')
      await fetchData()
    }else{
      alert('操作失败')
    }
  }catch(e){
    console.log(e)
  }
}

//调整订单详情
function show_order_details(id){
  router.push(`/order_details?id=${id}`)
}

// 初始化加载数据
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.receiver-request-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.filter-controls {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 16px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
}

.filter-tab {
  padding: 8px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: #fff;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-tab:hover {
  border-color: #1890ff;
  color: #1890ff;
}

.filter-tab.active {
  background: #1890ff;
  color: #fff;
  border-color: #1890ff;
}

.filter-options {
  display: flex;
  gap: 16px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  color: #666;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: #fff;
  min-width: 180px;
  transition: all 0.3s;
}

.filter-select:focus {
  border-color: #1890ff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.order-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.order-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f5f5f5;
}

.order-id {
  font-size: 14px;
  color: #666;
}

.order-amount {
  font-weight: 600;
  color: #ff4d4f;
}

.order-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.order-body {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}

.order-field {
  display: flex;
  gap: 8px;
  margin: 0;
  font-size: 14px;
}

.field-label {
  color: #888;
  min-width: 80px;
}

.field-value {
  color: #333;
  word-break: break-word;
}
.accept{
  color: #fff;
  background-color: #409EFF;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
  margin-right: 10px;
}
.reject{
  color: #fff;
  background-color: #F56C6C;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
}
.show_details{
  color: #409EFF;
  cursor: pointer;
  margin-right: 10px;
  font-size: 16px;
  margin-top: 10px;
  margin-bottom: 10px;
  display: inline-block;
  border-bottom: 1px dashed #409EFF;
  transition: all 0.3s ease;
  &:hover{
    border-bottom: 1px solid #409EFF;
  }
}
/* 状态样式 */
.order-card.pending .order-status {
  background-color: #faad14;
  color: #fff;
}

.order-card.in-progress .order-status {
  background-color: #1890ff;
  color: #fff;
}

.order-card.completed .order-status {
  background-color: #52c41a;
  color: #fff;
}

.order-card.cancelled .order-status {
  background-color: #f5f5f5;
  color: #999;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #999;
}

.empty-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 16px;
  opacity: 0.6;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
}

.pagination-button {
  padding: 8px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination-button:hover:not(:disabled) {
  border-color: #1890ff;
  color: #1890ff;
}

.pagination-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #666;
}

@media (max-width: 768px) {
  .filter-controls {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-options {
    width: 100%;
    flex-direction: column;
  }
  
  .filter-select {
    width: 100%;
  }
}
</style>