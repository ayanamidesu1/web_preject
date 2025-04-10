<template>
  <div class="wallet-container">
    <!-- 主页面 -->
    <div class="wallet-header" v-if="wallet_info">
      <h2>我的钱包</h2>
      <button class="recharge-btn" @click="openRechargeModal">充值</button>
    </div>

    <div class="wallet-content">
      <!-- 余额卡片 -->
      <div class="balance-card">
        <div class="balance-title">账户余额</div>
        <div class="balance-amount" v-if="wallet_info.data">
          ¥ {{ formatBalance(wallet_info.data.balance) }}
        </div>
      </div>

      <!-- 交易记录 -->
      <div class="transaction-section">
        <h3 class="section-title">
          交易记录 <span class="record-count">(共 {{ total }} 条)</span>
        </h3>

        <div class="transaction-table">
          <div class="table-header">
            <div class="col-time">交易时间</div>
            <div class="col-type">类型</div>
            <div class="col-amount">金额</div>
            <div class="col-status">状态</div>
          </div>

          <div v-if="loading" class="loading-row">加载中...</div>

          <template v-else>
            <div v-for="tx in transactions" :key="tx.id" class="table-row">
              <div class="col-time">{{ baseApi.formatTimeAgo(tx.time) }}</div>
              <div class="col-type">
                {{
                  tx.type === "vip"
                    ? "VIP购买"
                    : tx.type === "recharge"
                    ? "余额充值"
                    : tx.type=='com_an_article'?"约稿":
                    tx.type=='complete_article'?"约稿完成":tx.type
                }}
              </div>
              <div
                class="col-amount"
                :class="{
                  income: tx.type === 'recharge',
                  expense: tx.type !== 'recharge',
                }"
              >
                {{ tx.type === "recharge" ? "+" : "-" }}{{ tx.amount_of_money }}
              </div>
              <div
                class="col-status"
                :class="{
                  'status-success': tx.status === 1,
                  'status-failed': tx.status === 3,
                  'status-pending': tx.status === 2,
                }"
              >
                {{
                  tx.status == 0
                    ? "取消"
                    : tx.status === 1
                    ? "已完成"
                    : tx.status === 2
                    ? "处理中"
                    : tx.status === 3
                    ? "收到但未开始"
                    : "未知状态"
                }}
              </div>
            </div>

            <div v-if="transactions.length === 0" class="empty-row">
              暂无交易记录
            </div>
          </template>
        </div>

        <!-- 分页组件（保持原有） -->
        <div class="page">
          <page
            :total="total"
            :pageSize="limit"
            @page-change="load_more_order($event)"
          />
        </div>
      </div>
    </div>

    <!-- 充值模态框 -->
    <div v-if="showRechargeModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>账户充值</h3>
          <button class="close-btn" @click="closeRechargeModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="cardPassword">充值卡密</label>
            <input
              id="cardPassword"
              v-model="rechargeForm.cardPassword"
              type="text"
              placeholder="请输入32位充值卡密"
              class="form-input"
              @keyup.enter="handleRecharge"
            />
          </div>
          <div class="recharge-tips">
            <p><strong>充值说明：</strong></p>
            <ul>
              <li>卡密为32位数字字母组合</li>
              <li>充值成功后余额即时到账</li>
              <li>如有问题请联系客服</li>
            </ul>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeRechargeModal">取消</button>
          <button
            class="confirm-btn"
            @click="handleRecharge"
            :disabled="recharging"
          >
            <span v-if="recharging">处理中...</span>
            <span v-else>确认充值</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { BaseApi } from "@/base_api";
import page from "@/assets/model/page.vue";

const baseApi = new BaseApi();
const wallet_info = ref({ balance: 0 });
const transactions = ref([]);
const showRechargeModal = ref(false);
const recharging = ref(false);
const loading = ref(false);
let limit = ref(10);
let offset = ref(0);
let total = ref(0);

// 充值表单
const rechargeForm = ref({
  cardPassword: "",
});

// 格式化余额显示
const formatBalance = (balance) => {
  return Number(balance || 0).toFixed(2);
};

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return `${date.getFullYear()}-${(date.getMonth() + 1)
    .toString()
    .padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")}`;
};

// 状态样式
const statusClass = (status) => {
  switch (status) {
    case "成功":
      return "status-success";
    case "失败":
      return "status-failed";
    case "处理中":
      return "status-pending";
    default:
      return "";
  }
};

// 加载钱包信息
const loadWalletInfo = async () => {
  loading.value = true;
  try {
    const response = await baseApi.post("api/getWalletInfo", {});
    if (response.status === 200) {
      wallet_info.value = response.result;
    }
  } catch (error) {
    console.error("获取钱包信息失败:", error);
  } finally {
    loading.value = false;
  }
};

// 加载交易记录
const loadTransactions = async () => {
  try {
    const response = await baseApi.post("api/GetSelfOrder", {
      limit: limit.value,
      offset: offset.value,
    });
    if (response.status === 200) {
      transactions.value = response.result.data || [];
      total.value = response.result.total;
    }
  } catch (error) {
    console.error("加载交易记录失败:", error);
  }
};
//加载更多交易记录
function load_more_order(page_change) {
  const target_offset = (page_change - 1) * limit.value; // 修正页码计算
  if (target_offset >= 0 && target_offset < total.value) {
    offset.value = target_offset;
    loadTransactions();
  } else {
    console.warn(
      `无效的页码: ${page_change}, 最大页码: ${Math.ceil(
        total.value / limit.value
      )}`
    );
  }
}

// 打开充值模态框
const openRechargeModal = () => {
  rechargeForm.value.cardPassword = "";
  showRechargeModal.value = true;
};

// 关闭充值模态框
const closeRechargeModal = () => {
  showRechargeModal.value = false;
};

// 处理充值
const handleRecharge = async () => {
  if (!rechargeForm.value.cardPassword) {
    alert("请输入充值卡密");
    return;
  }

  recharging.value = true;
  try {
    const response = await baseApi.post("api/Recharge", {
      card_password: rechargeForm.value.cardPassword,
    });

    if (response.status === 200) {
      alert("充值成功");
      closeRechargeModal();
      await loadWalletInfo();
      await loadTransactions();
    } else {
      console.error("充值失败:", response);
      alert(`充值失败：${response.result.msg}`);
    }
  } catch (error) {
    alert("网络错误，请稍后重试");
    console.error("充值失败:", error);
  } finally {
    recharging.value = false;
  }
};

// 初始化加载
onMounted(() => {
  loadWalletInfo();
  loadTransactions();
});
</script>

<style scoped>
/* 新增的表格样式 */
.transaction-table {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1fr;
  padding: 12px 15px;
}

.table-header {
  background-color: #f5f7fa;
  font-weight: bold;
}

.table-row {
  border-bottom: 1px solid #eee;
}

.table-row:hover {
  background-color: #f9f9f9;
}

.col-amount.income {
  color: #67c23a;
  font-weight: bold;
}

.col-amount.expense {
  color: #f56c6c;
  font-weight: bold;
}
.status-close {
  color: #909399;
}
.status-success {
  color: #67c23a;
}

.status-failed {
  color: #f56c6c;
}
/*进行中*/
.status-loading {
  color: #ebf55e;
}
.status-pending {
  color: #e6a23c;
}

.loading-row,
.empty-row {
  text-align: center;
  padding: 20px;
  color: #999;
}

.record-count {
  font-size: 14px;
  color: #999;
  font-weight: normal;
}

.balance-update {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

/* 基础样式 */
.wallet-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Helvetica Neue", Arial, sans-serif;
}

.wallet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.wallet-header h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

/* 按钮样式 */
.recharge-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.recharge-btn:hover {
  background-color: #45a049;
}

/* 余额卡片 */
.balance-card {
  background: linear-gradient(135deg, #4a6bff, #6a8cff);
  color: white;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.balance-title {
  font-size: 16px;
  margin-bottom: 10px;
  opacity: 0.9;
}

.balance-amount {
  font-size: 32px;
  font-weight: bold;
}

/* 交易记录 */
.transaction-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section-title {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 18px;
}

.transaction-list {
  max-height: 400px;
  overflow-y: auto;
}

.transaction-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
}

.transaction-item:last-child {
  border-bottom: none;
}

.tx-time {
  color: #666;
  font-size: 14px;
  width: 120px;
}

.tx-details {
  flex: 1;
  padding: 0 15px;
}

.tx-type {
  color: #333;
}

.tx-amount {
  font-weight: bold;
  margin-left: 10px;
}

.income {
  color: #4caf50;
}

.expense {
  color: #f44336;
}

.tx-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
}

.status-success {
  background-color: #e8f5e9;
  color: #4caf50;
}

.status-failed {
  background-color: #ffebee;
  color: #f44336;
}

.status-pending {
  background-color: #fff8e1;
  color: #ffa000;
}

.empty-tips {
  text-align: center;
  padding: 20px;
  color: #999;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  animation: modalFadeIn 0.3s;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #4a6bff;
  box-shadow: 0 0 0 2px rgba(74, 107, 255, 0.2);
}

.recharge-tips {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
  color: #555;
  font-size: 14px;
}

.recharge-tips p {
  margin-top: 0;
  margin-bottom: 10px;
}

.recharge-tips ul {
  padding-left: 20px;
  margin: 0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 15px 20px;
  border-top: 1px solid #eee;
}

.cancel-btn,
.confirm-btn {
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-left: 10px;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.cancel-btn:hover {
  background-color: #e9e9e9;
}

.confirm-btn {
  background-color: #4a6bff;
  color: white;
  border: none;
}

.confirm-btn:hover:not(:disabled) {
  background-color: #3a5bef;
}

.confirm-btn:disabled {
  background-color: #a0b0ff;
  cursor: not-allowed;
}

/* 加载动画 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4a6bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>