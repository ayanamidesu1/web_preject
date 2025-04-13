<template>
  <div class="func-container">
    <!-- 方案列表区域 -->
    <div class="func-list-container">
      <h3 class="list-title">我的约稿方案</h3>
      
      <!-- 方案列表 -->
      <div 
        class="func-list"
        v-infinite-scroll="loadMore"
        :infinite-scroll-disabled="loading"
        :infinite-scroll-distance="100"
      >
        <div 
          class="func-card"
          v-for="(item, index) in func_list"
          :key="index"
          @click="viewFuncDetail(item.func_id)"
        >
          <div class="func-header">
            <span class="func-type-badge" :class="getTypeClass(item.work_type)">
              {{ getTypeName(item.work_type) }}
            </span>
            <span class="func-price">{{ formatPrice(item.amount_of_money) }}</span>
          </div>
          <div class="func-content">
            <h4 class="func-title">{{ item.title || '未命名方案' }}</h4>
            <p class="func-desc">{{ truncateDescription(item.introduce) }}</p>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-indicator">
          <div class="spinner"></div>
          <span>加载中...</span>
        </div>

        <!-- 无数据提示 -->
        <div v-if="!loading && func_list.length === 0" class="empty-tips">
          <img src="https://www.sunyuanling.com/server/static/svg/方案.svg" alt="无方案">
          <p>暂无约稿方案，快去创建一个吧~</p>
        </div>
      </div>
    </div>

    <!-- 新建按钮 -->
    <button class="create-func-btn" @click="create_func">
      <i class="icon-plus"></i> 新建方案
    </button>

    <!-- 操作提示 -->
    <div class="operation-tips">
      <div class="tips-header">
        <i class="icon-info"></i>
        <span>约稿提示</span>
      </div>
      <p>约稿方案说明及约稿内容现已支持自动翻译为简体、繁体中文。在日本时间12月12日11:30后公开、更新的内容支持本更新。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { BaseApi } from "@/base_api";
import { useStore } from "@assets/model/store";
import infiniteScroll from 'vue-infinite-scroll'

// 在 <script setup> 中
const vInfiniteScroll = infiniteScroll

const router = useRouter();
const api = new BaseApi();
const store = useStore();

// 数据状态
const func_list = ref([]);
const loading = ref(false);
const hasMore = ref(true);
const limit = 10;
let offset = 0;

// 获取方案列表
const get_func_list = async () => {
  if (loading.value || !hasMore.value) return;
  
  loading.value = true;
  try {
    const res = await api.post("api/GetFuncList", {
      limit,
      offset,
      user_id: store.$state.user?.userid || null
    });

    if (res.status === 200) {
      const newData = res.result.data || [];
      func_list.value = [...func_list.value, ...newData];
      hasMore.value = newData.length >= limit;
      offset += limit;
    }
  } catch (e) {
    console.error("获取方案列表失败:", e);
  } finally {
    loading.value = false;
  }
};

// 滚动加载更多
const loadMore = () => {
  if (hasMore.value) {
    get_func_list();
  }
};

// 工具函数
const formatPrice = (num) => {
  return Number(num || 0).toFixed(2) + '￥';
};

const getTypeName = (type) => {
  const types = {
    illustration: '插画',
    comic: '漫画',
    novel: '小说'
  };
  return types[type] || '其他';
};

const getTypeClass = (type) => {
  return `type-${type}`;
};

const truncateDescription = (text) => {
  return text?.length > 50 ? text.substring(0, 50) + '...' : text || '暂无描述';
};

const formatTime = (timeStr) => {
  if (!timeStr) return '';
  try {
    const date = new Date(timeStr);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    }).replace(/\//g, '-');
  } catch {
    return timeStr;
  }
};

// 页面跳转
const create_func = () => router.push("/create_func");
const viewFuncDetail = (funcId) => router.push(`/func/${funcId}`);

// 初始化加载
onMounted(() => {
  get_func_list();
});
</script>

<style scoped>
/* 样式部分保持不变，与之前相同 */
.func-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.func-list-container {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.list-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.func-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  padding-bottom: 20px;
}

.func-card {
  background: #fff;
  border-radius: 8px;
  border: 1px solid #eee;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.func-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.func-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.func-type-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.type-illustration {
  background: #e6f7ff;
  color: #1890ff;
}

.type-comic {
  background: #f6ffed;
  color: #52c41a;
}

.type-novel {
  background: #fff2e8;
  color: #fa8c16;
}

.func-price {
  font-size: 16px;
  font-weight: 600;
  color: #ff4d4f;
}

.func-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.func-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 12px;
  min-height: 42px;
}

.func-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #999;
}

.func-status {
  padding: 2px 6px;
  border-radius: 3px;
}

.status-active {
  background: #f6ffed;
  color: #52c41a;
}

.status-draft {
  background: #fff2e8;
  color: #fa8c16;
}

.create-func-btn {
  align-self: flex-end;
  padding: 10px 20px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.create-func-btn:hover {
  background: #40a9ff;
}

.operation-tips {
  background: #f6f6f6;
  border-radius: 8px;
  padding: 16px;
  font-size: 14px;
  line-height: 1.6;
  color: #666;
}

.tips-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.tips-header i {
  margin-right: 8px;
}

.loading-indicator {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #1890ff;
  animation: spin 1s linear infinite;
  margin-bottom: 8px;
}

.empty-tips {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 0;
  color: #999;
}

.empty-tips img {
  width: 120px;
  margin-bottom: 16px;
  opacity: 0.6;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>