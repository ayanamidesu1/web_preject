<template>
  <div class="card-password-manager">
    <!-- 搜索筛选区域 -->
    <div class="filter-section">
      <div class="filter-group">
        <label>卡密搜索：</label>
        <input
          type="text"
          v-model="filter.card_key"
          placeholder="输入卡密"
          @keyup.enter="handleFilter"
        />
      </div>

      <div class="filter-group">
        <label>过期时间：</label>
        <div class="date-range-picker">
          <input
            type="datetime-local"
            v-model="dateRange.start"
            @change="updateDateRange"
          />
          <span>至</span>
          <input
            type="datetime-local"
            v-model="dateRange.end"
            @change="updateDateRange"
          />
        </div>
      </div>

      <div class="filter-group">
        <label>使用状态：</label>
        <select v-model="filter.use_status" @change="handleFilter">
          <option :value="null">全部</option>
          <option :value="0">未使用</option>
          <option :value="1">已使用</option>
        </select>
      </div>

      <div class="filter-group">
        <label>价格范围：</label>
        <div class="price-range">
          <input
            type="number"
            v-model.number="filter.price.min"
            placeholder="最低价"
            min="0"
            step="0.01"
            @change="handleFilter"
          />
          <span>-</span>
          <input
            type="number"
            v-model.number="filter.price.max"
            placeholder="最高价"
            min="0"
            step="0.01"
            @change="handleFilter"
          />
        </div>
      </div>

      <div class="filter-group">
        <label>
          <input
            type="checkbox"
            v-model="filter.is_expire"
            @change="handleFilter"
          />
          仅显示过期卡密
        </label>
      </div>

      <div class="filter-actions">
        <button @click="handleFilter">搜索</button>
        <button @click="resetFilter">重置</button>
      </div>
    </div>

    <!-- 卡密列表 -->
    <div class="card-list">
      <div class="list-header">
        <div class="header-item" v-for="(col, index) in columns" :key="index">
          {{ col.label }}
        </div>
      </div>

      <div class="list-body">
        <div class="list-row" v-for="(item, index) in data" :key="item.id">
          <div class="list-cell">{{ item.id }}</div>
          <div class="list-cell">{{ item.card_key }}</div>
          <div class="list-cell">{{ formatDateTime(item.duration) }}</div>
          <div class="list-cell">{{ getStatusText(item.use_status) }}</div>
          <div class="list-cell">{{ formatDateTime(item.create_time) }}</div>
          <div class="list-cell">{{ formatPrice(item.price) }}</div>
        </div>

        <div class="empty-state" v-if="!data || data.length === 0">
          暂无数据
        </div>
      </div>
    </div>

    <!-- 保持您原有的分页组件 -->
    <page
      :total="total"
      :offset="offset"
      @page-change="add_more($event)"
    ></page>
  </div>
</template>
  
  <script setup>
import { ref, computed, onMounted } from "vue";
import { useStore } from "@/model/store/store";
import { BaseApi } from "@/base_api";
import page from "@/components/model/page.vue";

const store = useStore();
const api = new BaseApi();

// 保持您原有的分页相关逻辑
let limit = ref(10);
let offset = ref(0);
let total = ref(0);
let data = ref([]);

// 筛选条件
let filter = ref({
  date_range: null,
  use_status: null,
  price: {
    min: null,
    max: null,
  },
  card_key: null,
  is_expire: null,
});

// 日期范围选择器数据
let dateRange = ref({
  start: "",
  end: "",
});

// 表格列配置
const columns = ref([
  { label: "ID", prop: "id" },
  { label: "卡密", prop: "card_key" },
  { label: "过期时间", prop: "duration" },
  { label: "使用状态", prop: "use_status" },
  { label: "创建时间", prop: "create_time" },
  { label: "价格", prop: "price" },
]);

// 保持您原有的分页方法
async function add_more(e) {
  //目标页面
  let target_offset = (e - 1) * limit.value;
  if (target_offset >= total.value) {
    target_offset = total.value - limit.value;
  }
  if (target_offset < 0) {
    target_offset = 0;
  }
  offset.value = target_offset;
  await get_card_list();
}

// 获取卡密列表
async function get_card_list() {
  try {
    // 准备请求参数
    const params = {
      limit: limit.value,
      offset: offset.value,
      filter: {
        ...filter.value,
        date_range:
          dateRange.value.start && dateRange.value.end
            ? [
                dateRange.value.start.replace("T", " "),
                dateRange.value.end.replace("T", " "),
              ]
            : null,
        price_range: {
          // 添加price_range参数
          min:
            filter.value.price.min !== null
              ? parseFloat(filter.value.price.min)
              : 0,
          max:
            filter.value.price.max !== null
              ? parseFloat(filter.value.price.max)
              : 10000,
        },
      },
    };

    let res = await api.post("admin_control/FilterCardPassword", params);
    if (res.status == 200) {
      data.value = res.result.data;
      total.value = res.result.total;
    } else {
      console.error("获取卡密列表失败:", res);
    }
  } catch (error) {
    console.error("请求出错:", error);
  }
}

// 处理筛选
function handleFilter() {
  offset.value = 0; // 重置分页
  get_card_list();
}

// 重置筛选
function resetFilter() {
  filter.value = {
    date_range: null,
    use_status: null,
    price: {
      min: null,
      max: null,
    },
    card_key: null,
    is_expire: null,
  };
  dateRange.value = {
    start: "",
    end: "",
  };
  handleFilter();
}

// 更新日期范围函数需要修改
function updateDateRange() {
  if (dateRange.value.start && dateRange.value.end) {
    // 将本地日期时间格式转换为API需要的格式
    filter.value.date_range = [
      dateRange.value.start.replace("T", " "),
      dateRange.value.end.replace("T", " "),
    ];
  } else {
    filter.value.date_range = null;
  }
}

// 格式化日期时间
function formatDateTime(datetime) {
  if (!datetime) return "-";
  return new Date(datetime).toLocaleString();
}

// 格式化价格
function formatPrice(price) {
  if (price === null || price === undefined) return "-";
  return parseFloat(price).toFixed(2);
}

// 获取状态文本
function getStatusText(status) {
  switch (status) {
    case 0:
      return "未使用";
    case 1:
      return "已使用";
    default:
      return "-";
  }
}

onMounted(async () => {
  await get_card_list();
});
</script>
  
  <style scoped>
.card-password-manager {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
  text-align: center;
}

.filter-section {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.filter-group {
  display: inline-block;
  margin-right: 15px;
  margin-bottom: 10px;
}

.filter-group label {
  margin-right: 8px;
  font-weight: bold;
}

.date-range-picker {
  display: inline-flex;
  align-items: center;
}

.date-range-picker span {
  margin: 0 5px;
}

.price-range {
  display: inline-flex;
  align-items: center;
}

.price-range span {
  margin: 0 5px;
}

.filter-actions {
  display: inline-block;
}

.filter-actions button {
  margin-right: 10px;
  padding: 5px 15px;
  cursor: pointer;
}

.card-list {
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  max-height: 90vh;
  overflow-y: auto;
}

.list-header {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  background: #f0f0f0;
  font-weight: bold;
  padding: 10px;
}

.header-item {
  padding: 5px;
  text-align: center;
}

.list-body {
  min-height: 200px;
}

.list-row {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  border-bottom: 1px solid #eee;
  padding: 10px;
  align-items: center;
}

.list-row:hover {
  background-color: #f9f9f9;
}

.list-cell {
  padding: 5px;
  text-align: center;
  word-break: break-all;
}

.empty-state {
  text-align: center;
  padding: 50px;
  color: #999;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}
</style>