<template>
  <div class="order-page">
    <h2 class="page-title">订单管理</h2>

    <!-- 筛选条件 -->
    <div class="filter-section">
      <div class="filter-group">
        <label class="filter-label">时间范围：</label>
        <div class="date-range">
          <input
            type="datetime-local"
            v-model="filter.start_time"
            class="filter-input"
          />
          <span class="range-separator">至</span>
          <input
            type="datetime-local"
            v-model="filter.end_time"
            class="filter-input"
          />
        </div>
      </div>

      <div class="filter-group">
        <label class="filter-label">订单状态：</label>
        <select v-model="filter.status" class="filter-select">
          <option value="">全部</option>
          <option value="0">取消</option>
          <option value="1">完成</option>
          <option value="2">进行中</option>
          <option value="3">收到但未开始</option>
          <option value="4">待确认</option>
          <option value="5">已拒绝</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="filter-label">支付类型：</label>
        <select v-model="filter.type" class="filter-select">
          <option value="">全部</option>
          <option value="VIP">VIP充值</option>
          <option value="recharge">余额充值</option>
          <option value="com_an_article">约稿</option>
          <option value="complete_article">完成稿件收入</option>
        </select>
      </div>
      <div class="filter-group">
        <label class="filter-label">金额流向用户ID：</label>
        <input type="text" v-model="filter.target_user_id" />
      </div>
      <div class="filter-group">
        <label class="filter-label">订单发起用户：</label>
        <input type="text" v-model="filter.user_id" />
      </div>

      <div class="filter-actions">
        <button @click="resetFilters" class="btn btn-reset">重置</button>
        <button @click="applyFilters" class="btn btn-apply">搜索</button>
      </div>
    </div>

    <!-- 订单列表 - Grid布局 -->
    <div class="order-grid">
      <!-- 表头 -->
      <div class="grid-header">
        <div class="grid-cell">订单ID</div>
        <div class="grid-cell">类型</div>
        <div class="grid-cell">金额</div>
        <div class="grid-cell">用户ID</div>
        <div class="grid-cell">时间</div>
        <div class="grid-cell">状态</div>
        <div class="grid-cell">目标用户</div>
      </div>

      <!-- 数据行 -->
      <div v-for="order in data" :key="order.id" class="grid-row">
        <div class="grid-cell">{{ order.id }}</div>
        <div class="grid-cell">{{ getTypeName(order.type) }}</div>
        <div class="grid-cell">{{ formatCurrency(order.amount_of_money) }}</div>
        <div class="grid-cell">{{ order.user_id }}</div>
        <div class="grid-cell">{{ formatTime(order.time) }}</div>
        <div class="grid-cell">
          <select
            v-model="order.status"
            @change="onStatusChange(order)"
            class="status-select"
          >
            <option value="0">取消</option>
            <option value="1">完成</option>
            <option value="2">进行中</option>
            <option value="3">收到但未开始</option>
            <option value="4">待确认</option>
            <option value="5">已拒绝</option>
          </select>
        </div>
        <div class="grid-cell">
          {{ order.target_user_id }}
        </div>
      </div>

      <!-- 无数据提示 -->
      <div v-if="!data" class="no-data">暂无订单数据</div>
    </div>

    <!-- 分页组件 -->
    <page
      :total="total"
      :pageSize="limit"
      @page-change="get_more($event)"
      class="pagination"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { BaseApi } from "@/base_api";
import page from "../page.vue";

const api = new BaseApi();
const limit = ref(5);
const offset = ref(0);
const total = ref(0);
const data = ref();
const filter = ref({
  start_time: "",
  end_time: "",
  status: "",
  type: "",
  user_id: "",
});

// 获取订单列表
async function get_order_list() {
  try {
    const params = {
      limit: limit.value,
      offset: offset.value,
      filter: {
        time_range:
          filter.value.start_time && filter.value.end_time
            ? [filter.value.start_time, filter.value.end_time]
            : [],
        status: filter.value.status,
        type: filter.value.type,
        user_id: filter.value.user_id,
      },
    };

    const res = await api.post("admin_control/GetOrderList", params);

    if (res.status === 200) {
      data.value = res.result.data;
      total.value = res.result.total;
    } else {
      console.error("获取订单列表失败:", res);
    }
  } catch (error) {
    console.error("请求出错:", error);
  }
}

// 应用筛选条件
function applyFilters() {
  offset.value = 0; // 重置到第一页
  get_order_list();
}

// 重置筛选条件
function resetFilters() {
  filter.value = {
    start_time: "",
    end_time: "",
    status: "",
    type: "",
    user_id: "",
    target_user_id: "",
  };
  applyFilters();
}

// 状态变更处理
async function onStatusChange(order) {
  console.log("订单状态变更:", order.id, "新状态:", order.status);
  let res = await api.post("admin_control/UpdateOrderStatus", {
    order_id: order.id,
    status: order.status,
  });
  if (res.status == 200) {
    alert("订单状态更新成功");
  } else {
    console.log(res);
    alert("订单状态更新失败");
  }
  // 这里可以添加API调用更新状态
}

// 显示订单详情
function showOrderDetail(order) {
  console.log("查看订单详情:", order.id);
  // 这里可以跳转到详情页或显示弹窗
}

// 辅助函数 - 获取类型名称
function getTypeName(type) {
  const typeMap = {
    VIP: "VIP充值",
    recharge: "余额充值",
    com_an_article: "约稿",
    complete_article: "完成稿件",
  };
  return typeMap[type] || type;
}

// 辅助函数 - 格式化时间
function formatTime(timestamp) {
  if (!timestamp) return "-";
  const date = new Date(timestamp);
  return date.toLocaleString();
}

// 辅助函数 - 格式化金额
function formatCurrency(amount) {
  return parseFloat(amount).toFixed(2);
}

// 分页处理
function get_more(page) {
  offset.value = (page - 1) * limit.value;
  get_order_list();
}

// 初始化加载
onMounted(() => {
  get_order_list();
});
</script>

<style scoped>
.order-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

/* 筛选区域样式 */
.filter-section {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  flex-direction: column;
  display: flex;
  gap: 10px;
}

.filter-group {
  display: flex;
  align-items: center;
}

.filter-label {
  min-width: 80px;
  margin-right: 10px;
  font-weight: bold;
}

.filter-input,
.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex: 1;
}

.date-range {
  display: flex;
  align-items: center;
}

.range-separator {
  margin: 0 10px;
}

.filter-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  grid-column: 1 / -1;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-reset {
  background: #f0f0f0;
  color: #666;
}

.btn-apply {
  background: #409eff;
  color: white;
}

/* 订单网格样式 */
.order-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.grid-header {
  display: contents;
}

.grid-header > .grid-cell {
  background: #f8f8f8;
  font-weight: bold;
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #eee;
}

.grid-row {
  display: contents;
}

.grid-row:nth-child(even) > .grid-cell {
  background: #f9f9f9;
}

.grid-cell {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
}

.btn-detail {
  padding: 6px 12px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-detail:hover {
  background: #e0e0e0;
}

.no-data {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  color: #999;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>