<template>
  <div class="pay-container">
    <!-- 头部标题 -->
    <div class="title-section">
      <span class="subtitle">每天只需{{ base_price }}元起</span>
      <h3 class="main-title">加入ILLWeb会员</h3>
    </div>

    <!-- 套餐选择 -->
    <div class="plan-section">
      <h4 class="section-title">选择套餐</h4>
      <div class="plan-grid">
        <div
          v-for="(plan, index) in func_list"
          :key="index"
          class="plan-card"
          :class="{ active: selectedPlanIndex === index }"
          @click="selectPlan(index)"
        >
          <div class="plan-duration">{{ plan.title }}</div>
          <div class="plan-price">¥{{ plan.price.toFixed(2) }}</div>
          <div v-if="plan.off < 1" class="plan-discount">
            省{{ ((1 - plan.off) * 100).toFixed(2) }}%
          </div>
        </div>
      </div>
    </div>

    <!-- 价格汇总 -->
    <div class="summary-section">
      <div class="summary-row">
        <span>套餐价格：</span>
        <span>¥{{ selectedPlan.price.toFixed(2) }}</span>
      </div>
      <div class="summary-row total">
        <span>总价：</span>
        <span class="total-price">¥{{ selectedPlan.price.toFixed(2) }}</span>
      </div>
    </div>

    <!-- 支付方式 -->
    <div class="payment-section">
      <h4 class="section-title">支付方式</h4>
      <div class="payment-methods">
        <div
          class="payment-method"
          :class="{ active: paymentMethod === 'balance' }"
          @click="paymentMethod = 'balance'"
        >
          <div class="method-icon">
            <img
              src="https://www.sunyuanling.com/server/static/svg/钱包.svg"
              alt="钱包"
              width="24"
              height="24"
            />
          </div>
          <div class="method-info">
            <div class="method-name">余额支付</div>
            <input v-model="pay_password" placeholder="请输入支付密码" type="password">
          </div>
        </div>
        <div class="payment-method disabled">
          <div class="method-icon">
            <img
              src="https://www.sunyuanling.com/server/static/svg/支付宝.svg"
              alt="支付宝"
              width="24"
              height="24"
            />
          </div>
          <div class="method-name">支付宝</div>
          <div class="method-tip">即将上线</div>
        </div>
        <div class="payment-method disabled">
          <div class="method-icon">
            <img
              src="https://www.sunyuanling.com/server/static/svg/微信.svg"
              alt="微信"
              width="24"
              height="24"
            />
          </div>
          <div class="method-name">微信支付</div>
          <div class="method-tip">即将上线</div>
        </div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="action-section">
      <button class="pay-btn" :disabled="isPaying" @click="handlePayment">
        {{ isPaying ? "支付中..." : "立即开通" }}
      </button>
    </div>
  </div>
</template>
  
  <script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { BaseApi } from "@/base_api";

const api = new BaseApi();
const router = useRouter();

// 基础数据
const base_price = ref(0.5);
const day_count = ref(30);
const isPaying = ref(false);
const paymentMethod = ref("balance"); // 当前仅支持余额支付
const selectedPlanIndex = ref(2); // 默认选择一个月套餐
let pay_password=ref()// 支付密码

// 套餐列表
const func_list = ref([
  {
    title: "一天",
    vip_type:'1d',
    price: 0.5,
    off: 0,
  },
  {
    title: "一周",
    vip_type:'1w',
    price: base_price.value * 7 * 0.98,
    off: 0.98,
  },
  {
    title: "一个月",
    vip_type:'1m',
    price: base_price.value * 30 * 0.9,
    off: 0.9,
  },
  {
    title: "三个月",
    vip_type:'3m',
    price: base_price.value * 90 * 0.8,
    off: 0.8,
  },
  {
    title: "半年",
    vip_type:'6m',
    price: base_price.value * 180 * 0.7,
    off: 0.7,
  },
  {
    title: "一年",
    vip_type:'1y',
    price: base_price.value * 365 * 0.5,
    off: 0.5,
  },
]);

// 计算属性
const selectedPlan = computed(() => func_list.value[selectedPlanIndex.value]);

// 方法
const selectPlan = (index) => {
  selectedPlanIndex.value = index;
};

const handlePayment = async () => {
  if (isPaying.value) return;

  isPaying.value = true;

  try {
    // 调用支付接口
    const response = await api.post("api/pay", {
      plan: selectedPlan.value.title,
      duration: selectedPlan.value.title,
      amount: selectedPlan.value.price,
      paymentMethod: paymentMethod.value,
      type:'vip',
      back:selectedPlan.value.vip_type,
      pay_password:pay_password.value
    });

    // 根据后端返回结果处理
    if (response.status == 200) {
      // 支付成功
      alert("开通成功！");
      router.push("/");
    } else if (response.status === 410) {
      // 余额不足，跳转充值页面
      alert("余额不足，请充值");
      //router.push("/recharge?redirect=/member/subscribe");
    }
    else if(response.status === 411){
        //支付账户未初始化
        alert("支付账户未初始化，请先初始化支付账户并设置支付密码");
        router.push('/init_pay_account')
    } 
    else {
      // 其他错误
      console.log("支付失败:", response);
      alert(response.result || "开通失败，请稍后重试");
    }
  } catch (error) {
    console.error("支付失败:", error);
    alert("开通失败，请稍后重试");
  } finally {
    isPaying.value = false;
  }
};

// 初始化
onMounted(() => {
  // 可以在这里初始化数据
});
</script>
  
  <style scoped>
.pay-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Helvetica Neue", Arial, sans-serif;
  color: #333;
}

.title-section {
  text-align: center;
  margin-bottom: 30px;
}

.subtitle {
  display: block;
  font-size: 16px;
  color: #666;
  margin-bottom: 5px;
}

.main-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  color: #222;
}

.section-title {
  font-size: 18px;
  font-weight: 500;
  margin: 20px 0 15px;
  color: #444;
}

.plan-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.plan-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.plan-card:hover {
  border-color: #4a90e2;
}

.plan-card.active {
  border-color: #4a90e2;
  background-color: #f0f7ff;
}

.plan-duration {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 5px;
}

.plan-price {
  font-size: 18px;
  font-weight: 600;
  color: #ff6b6b;
  margin-bottom: 5px;
}

.plan-discount {
  font-size: 12px;
  color: #fff;
  background-color: #ff6b6b;
  border-radius: 10px;
  padding: 2px 8px;
  display: inline-block;
}

.summary-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  margin: 20px 0;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 15px;
}

.summary-row.total {
  border-top: 1px solid #eee;
  padding-top: 10px;
  margin-top: 10px;
  font-weight: 600;
}

.total-price {
  color: #ff6b6b;
  font-size: 18px;
}

.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.payment-method {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.payment-method:hover:not(.disabled) {
  border-color: #4a90e2;
}

.payment-method.active {
  border-color: #4a90e2;
  background-color: #f0f7ff;
}

.payment-method.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  position: relative;
}

.method-icon img {
  font-size: 24px;
  margin-right: 15px;
    width: 24px;
    height: 24px;
    object-fit: contain;
}
.method-info input{
  width: calc(100% - 20px);
  margin: 5px auto;
  border: 1px solid rgb(233,233,233);
  background-color: rgb(255, 255, 255);
  border-radius: 5px;
  padding: 5px;
}
.method-name {
  font-weight: 500;
}

.method-tip {
  margin-left: auto;
  font-size: 12px;
  color: #999;
}

.action-section {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

.pay-btn {
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 30px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  width: 100%;
  max-width: 300px;
}

.pay-btn:hover:not(:disabled) {
  background-color: #3a7bc8;
}

.pay-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .plan-grid {
    grid-template-columns: 1fr;
  }

  .pay-btn {
    max-width: none;
  }
}
</style>