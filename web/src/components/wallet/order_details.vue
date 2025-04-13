<template>
  <div class="order-details-container">
    <div class="header">
      <h2 class="title">订单详情</h2>
      <span class="order-id">订单ID: #{{ order_info.id }}</span>
    </div>

    <div class="order-content">
      <!-- 基本信息 -->
      <div class="section">
        <h3 class="section-title">基本信息</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">订单类型:</span>
            <span class="value">{{ getOrderType(order_info.type) }}</span>
          </div>
          <div class="info-item">
            <span class="label">订单状态:</span>
            <span
              class="value status-badge"
              :class="getStatusClass(order_info.status)"
            >
              {{ getStatusText(order_info.status) }}
            </span>
          </div>
          <div class="info-item">
            <span class="label">金额:</span>
            <span class="value amount"
              >¥{{ formatAmount(order_info.amount_of_money) }}</span
            >
          </div>
          <div class="info-item">
            <span class="label">创建时间:</span>
            <span class="value">{{ formatTime(order_info.time) }}</span>
          </div>
          <div class="info-item">
            <span class="label">委托方:</span>
            <span class="value">{{ order_info.user_id }}</span>
          </div>
          <div class="info-item">
            <span class="label">接稿方:</span>
            <span class="value">{{
              order_info.target_user_id || "未指定"
            }}</span>
          </div>
          <div class="info-item">
            <span class="label">年龄分类:</span>
            <span class="value">{{
              order_info.age_classification || "未指定"
            }}</span>
          </div>
        </div>
      </div>

      <!-- 作品信息 -->
      <div class="section">
        <h3 class="section-title">作品信息</h3>
        <div class="work-info">
          <div class="info-item">
            <span class="label">作品类型:</span>
            <span class="value">{{ order_info.work_type || "未指定" }}</span>
          </div>
          <div class="info-item full-width">
            <span class="label">作品介绍:</span>
            <div class="value work-introduce">
              {{ order_info.work_introduce || "无介绍" }}
            </div>
          </div>
        </div>
      </div>

      <!-- 备注信息 -->
      <div class="section" v-if="order_info.back">
        <h3 class="section-title">备注</h3>
        <div class="back-content">{{ order_info.back }}</div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button v-if="canCancel" @click="cancelOrder" class="btn cancel-btn">
          取消订单
        </button>
        <button
          v-if="canConfirm"
          @click="confirmCompletion"
          class="btn confirm-btn"
        >
          确认完成
        </button>
        <button
          v-if="canReject"
          @click="rejectCompletion"
          class="btn reject-btn"
        >
          拒绝完成
        </button>
        <button @click="goBack" class="btn back-btn">返回</button>
      </div>
    </div>
  </div>
</template>
  
  <script setup>
import { ref, onMounted, computed } from "vue";
import { useStore } from "@assets/model/store";
import { BaseApi } from "@/base_api";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useStore();
const api = new BaseApi();
const order_info = ref({});

// 计算订单ID
const order_id = computed(() => {
  return router.currentRoute.value.query.id;
});

// 状态文本映射
const statusTextMap = {
  0: "已取消",
  1: "已完成",
  2: "进行中",
  3: "待处理",
  4: "等待确认",
  5: "已拒绝",
};

// 状态样式类映射
const statusClassMap = {
  0: "cancelled",
  1: "completed",
  2: "in-progress",
  3: "pending",
  4: "waiting-confirm",
  5: "rejected",
};

// 订单类型映射
const orderTypeMap = {
  VIP: "VIP充值",
  recharge: "余额充值",
  com_an_article: "约稿",
  complete_article: "完成稿件收入",
};

// 获取状态文本
const getStatusText = (status) => {
  return statusTextMap[status] || "未知状态";
};

// 获取状态对应的CSS类
const getStatusClass = (status) => {
  return statusClassMap[status] || "";
};

// 获取订单类型文本
const getOrderType = (type) => {
  return orderTypeMap[type] || type;
};

// 格式化金额
const formatAmount = (amount) => {
  return parseFloat(amount).toFixed(2);
};

// 格式化时间
const formatTime = (time) => {
  if (!time) return "";
  return new Date(time).toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};

// 是否可以取消订单
const canCancel = computed(() => {
  return [3, 4].includes(order_info.value.status);
});

// 是否可以确认完成
const canConfirm = computed(() => {
  return (
    order_info.value.status === 4 && store.user.id === order_info.value.user_id
  );
});

// 是否可以拒绝完成
const canReject = computed(() => {
  return (
    order_info.value.status === 4 && store.user.id === order_info.value.user_id
  );
});

// 获取订单信息
const get_order_info = async (id) => {
  try {
    const res = await api.post("api/GetOrderInfoById", {
      order_id: id,
    });
    if (res.status === 200) {
      return res.result.data;
    } else {
      alert("获取订单信息失败");
      return {};
    }
  } catch (error) {
    console.error("获取订单信息出错:", error);
    return {};
  }
};

// 取消订单
const cancelOrder = async () => {
  if (!confirm("确定要取消此订单吗？")) return;

  try {
    const res = await api.post("api/CancelOrder", {
      order_id: order_id.value,
    });
    if (res.status === 200) {
      alert("订单已取消");
      order_info.value = await get_order_info(order_id.value);
    } else {
      alert("取消订单失败");
    }
  } catch (error) {
    console.error("取消订单出错:", error);
  }
};

// 确认完成
const confirmCompletion = async () => {
  if (!confirm("确认此订单已完成？")) return;

  try {
    const res = await api.post("api/ConfirmOrderCompletion", {
      order_id: order_id.value,
    });
    if (res.status === 200) {
      alert("订单已完成确认");
      order_info.value = await get_order_info(order_id.value);
    } else {
      alert("确认完成失败");
    }
  } catch (error) {
    console.error("确认完成出错:", error);
  }
};

// 拒绝完成
const rejectCompletion = async () => {
  if (!confirm("拒绝此订单的完成状态？")) return;

  try {
    const res = await api.post("api/RejectOrderCompletion", {
      order_id: order_id.value,
    });
    if (res.status === 200) {
      alert("已拒绝订单完成状态");
      order_info.value = await get_order_info(order_id.value);
    } else {
      alert("拒绝完成失败");
    }
  } catch (error) {
    console.error("拒绝完成出错:", error);
  }
};

// 返回上一页
const goBack = () => {
  router.go(-1);
};

// 初始化加载数据
onMounted(async () => {
  order_info.value = await get_order_info(order_id.value);
});
</script>
  
  <style scoped>
.order-details-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.title {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.order-id {
  font-size: 14px;
  color: #999;
}

.section {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f5f5f5;
}

.section:last-child {
  border-bottom: none;
}

.section-title {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
  padding-left: 10px;
  border-left: 4px solid #409eff;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.info-item {
  display: flex;
  align-items: center;
}

.full-width {
  grid-column: 1 / -1;
}

.label {
  min-width: 80px;
  color: #666;
  font-weight: bold;
}

.value {
  color: #333;
}

.amount {
  color: #f56c6c;
  font-weight: bold;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status-badge.cancelled {
  background: #fef0f0;
  color: #f56c6c;
}

.status-badge.completed {
  background: #f0f9eb;
  color: #67c23a;
}

.status-badge.in-progress {
  background: #fdf6ec;
  color: #e6a23c;
}

.status-badge.pending {
  background: #ecf5ff;
  color: #409eff;
}

.status-badge.waiting-confirm {
  background: #f4f4f5;
  color: #909399;
}

.status-badge.rejected {
  background: #fef0f0;
  color: #f56c6c;
}

.work-introduce {
  white-space: pre-line;
  line-height: 1.6;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 4px;
  margin-top: 5px;
}

.back-content {
  white-space: pre-line;
  line-height: 1.6;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 30px;
  justify-content: center;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.cancel-btn {
  background: #f56c6c;
  color: white;
}

.cancel-btn:hover {
  background: #f78989;
}

.confirm-btn {
  background: #67c23a;
  color: white;
}

.confirm-btn:hover {
  background: #85ce61;
}

.reject-btn {
  background: #e6a23c;
  color: white;
}

.reject-btn:hover {
  background: #ebb563;
}

.back-btn {
  background: #909399;
  color: white;
}

.back-btn:hover {
  background: #a6a9ad;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>