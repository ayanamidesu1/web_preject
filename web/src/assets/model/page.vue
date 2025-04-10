<template>
    <div class="pagination-container">
      <!-- 导航按钮组 -->
      <div class="nav-buttons">
        <button
          class="pagination-btn"
          :class="{ disabled: nowPage === 1 }"
          @click="jumpToFirst"
        >
          首页
        </button>
        <button
          class="pagination-btn"
          :class="{ disabled: nowPage === 1 }"
          @click="prevPage"
        >
          上一页
        </button>
      </div>
  
      <!-- 页码显示 -->
      <div class="page-indicator">
        <span class="current-page">{{ nowPage }}</span>
        <span class="separator">/</span>
        <span class="total-pages">{{ totalPages }}</span>
      </div>
  
      <!-- 跳转控制 -->
      <div class="page-control">
        <input
          v-model.number="inputPage"
          type="number"
          class="page-input"
          :min="1"
          :max="totalPages"
          placeholder="页数"
          @keyup.enter="handleJump"
        />
        <button class="pagination-btn" @click="handleJump">跳转</button>
      </div>
  
      <!-- 导航按钮组 -->
      <div class="nav-buttons">
        <button
          class="pagination-btn"
          :class="{ disabled: nowPage >= totalPages }"
          @click="nextPage"
        >
          下一页
        </button>
        <button
          class="pagination-btn"
          :class="{ disabled: nowPage >= totalPages }"
          @click="jumpToLast"
        >
          尾页
        </button>
      </div>
    </div>
  </template>
    
    <script setup>
  import { ref, computed, watch } from "vue";
  
  const props = defineProps({
    total: { type: Number, required: true },
    //总条数
    pageSize: { type: Number, default: 10 },
    //每页条数
    current: { type: Number, default: 1 },
    //当前页码
  });
  
  const emit = defineEmits(["page-change"]);
  
  const nowPage = ref(props.current);
  const inputPage = ref("");
  
  // 计算总页数
  const totalPages = computed(() => Math.ceil(props.total / props.pageSize) || 1);
  
  // 页码变化观察
  watch(
    () => props.current,
    (newVal) => {
      nowPage.value = newVal;
    }
  );
  
  // 通用跳转方法
  const jumpPage = (page) => {
    const validPage = Math.max(1, Math.min(page, totalPages.value));
    if (validPage !== nowPage.value) {
      nowPage.value = validPage;
      emit("page-change", validPage);
    }
  };
  
  // 导航方法
  const prevPage = () => jumpPage(nowPage.value - 1);
  const nextPage = () => jumpPage(nowPage.value + 1);
  const jumpToFirst = () => jumpPage(1);
  const jumpToLast = () => jumpPage(totalPages.value);
  
  // 处理跳转输入
  const handleJump = () => {
    if (!inputPage.value) return;
    const page = parseInt(inputPage.value);
    if (page > 0 && page <= totalPages.value) {
      jumpPage(page);
      inputPage.value = "";
    }
  };
  </script>
    
    <style scoped>
  .pagination-container {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 16px;
    background: #f8f9fa;
    border-radius: 8px;
  }
  
  .nav-buttons {
    display: flex;
    gap: 8px;
  }
  
  .page-indicator {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 14px;
    color: #606266;
  }
  
  .current-page {
    font-weight: 500;
    color: #409eff;
  }
  
  .page-control {
    display: flex;
    gap: 8px;
    align-items: center;
  }
  
  .page-input {
    width: 60px;
    padding: 6px 8px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    text-align: center;
    transition: border-color 0.3s;
  }
  
  .page-input:focus {
    border-color: #409eff;
    outline: none;
  }
  
  .pagination-btn {
    padding: 6px 12px;
    background: #ffffff;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    color: #606266;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .pagination-btn:hover:not(.disabled) {
    color: #409eff;
    border-color: #c6e2ff;
    background-color: #ecf5ff;
  }
  
  .pagination-btn.disabled {
    color: #c0c4cc;
    cursor: not-allowed;
    background-color: #f5f7fa;
    border-color: #e4e7ed;
  }
  </style>