<template>
  <div class="send-request-container">
    <h2 class="section-title">发送的约稿申请</h2>
    
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
            <option value="1">已完成</option>
            <option value="2">创作中</option>
            <option value="0">已取消</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>排序</label>
          <select 
            v-model="sort_by" 
            @click="fetchData"
            class="filter-select"
          >
            <option value="time_desc">最新</option>
            <option value="amount_desc">金额从高到低</option>
            <option value="time_asc">截稿日期从早到晚</option>
            <option value="target_user">按接稿人排序</option>
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
          <span class="order-amount">¥{{ formatAmount(order.amount_of_money) }}</span>
          <span class="order-status">{{ getStatusText(order.status) }}</span>
        </div>
        
        <div class="order-body">
          <div class="order-field">
            <span class="field-label">接稿人:</span>
            <span class="field-value">{{ order.target_user_id || '未指定' }}</span>
          </div>
          <div class="order-field">
            <span class="field-label">工作类型:</span>
            <span class="field-value">{{ order.work_type || '未指定' }}</span>
          </div>
          <div class="order-field">
            <span class="field-label">工作介绍:</span>
            <span class="field-value multiline">{{ order.work_introduce || '无介绍' }}</span>
          </div>
          <div class="order-field">
            <span class="field-label">创建时间:</span>
            <span class="field-value">{{ formatTime(order.time) }}</span>
          </div>
        </div>
        
        <div class="order-actions">
          <button 
            v-if="order.status === 3" 
            @click="cancelOrder(order.id)"
            class="action-button cancel-button"
          >
            取消约稿
          </button>
          <button 
            @click="viewOrderDetail(order.id)"
            class="action-button detail-button"
          >
            查看详情
          </button>
        </div>
      </div>
      
      <div v-if="order_list.length === 0" class="empty-state">
        <img src="https://www.sunyuanling.com/server/static/svg/暂无订单.svg" alt="无订单" class="empty-icon">
        <p>暂无发送的约稿申请</p>
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
import { useRouter } from 'vue-router'
import { BaseApi } from '@/base_api'

const router = useRouter()
const api = new BaseApi()

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

// 格式化金额
const formatAmount = (amount) => {
  return parseFloat(amount).toFixed(2)
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

// 取消约稿
const cancelOrder = async (orderId) => {
  try {
    const response = await api.post('api/CancelOrder', { order_id: orderId })
    if (response.status === 200) {
      fetchData() // 刷新数据
    }
  } catch (error) {
    console.error('取消约稿失败:', error)
  }
}

// 查看订单详情
const viewOrderDetail = (orderId) => {
  router.push(`/order/detail/${orderId}`)
}

// 获取数据
const fetchData = async () => {
  try {
    const response = await api.post('api/GetSendList', {
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
      console.error('获取数据失败:', response)
    }
  } catch (error) {
    console.error('请求错误:', error)
  }
}

// 初始化加载数据
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.send-request-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.section-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.filter-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.filter-tabs {
  display: flex;
  gap: 10px;
}

.filter-tab {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-tab:hover {
  border-color: #409eff;
  color: #409eff;
}

.filter-tab.active {
  background: #409eff;
  color: white;
  border-color: #409eff;
}

.filter-options {
  display: flex;
  gap: 15px;
  align-items: center;
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
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 150px;
}

.order-list {
  display: grid;
  gap: 15px;
}

.order-card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.order-card:hover {
  transform: translateY(-2px);
}

.order-card.cancelled {
  opacity: 0.7;
  background: #f9f9f9;
}

.order-card.completed {
  border-left: 4px solid #67c23a;
}

.order-card.in-progress {
  border-left: 4px solid #e6a23c;
}

.order-card.pending {
  border-left: 4px solid #409eff;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.order-id {
  font-size: 14px;
  color: #999;
}

.order-amount {
  font-weight: bold;
  color: #f56c6c;
}

.order-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  background: #f0f0f0;
}

.order-body {
  display: grid;
  gap: 8px;
}

.order-field {
  display: flex;
  gap: 8px;
}

.field-label {
  color: #666;
  min-width: 80px;
  text-align: right;
}

.field-value {
  flex: 1;
}

.multiline {
  white-space: pre-line;
  line-height: 1.5;
}

.order-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.action-button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.detail-button {
  background: #409eff;
  color: white;
}

.detail-button:hover {
  background: #66b1ff;
}

.cancel-button {
  background: #f56c6c;
  color: white;
}

.cancel-button:hover {
  background: #f78989;
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
  width: 150px;
  height: 150px;
  margin-bottom: 20px;
  opacity: 0.6;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.pagination-button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-button:hover:not(:disabled) {
  border-color: #409eff;
  color: #409eff;
}

.pagination-button:disabled {
  opacity: 0.5;
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
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .filter-select {
    width: 100%;
  }
  
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .order-field {
    flex-direction: column;
    gap: 4px;
  }
  
  .field-label {
    text-align: left;
  }
}
</style>