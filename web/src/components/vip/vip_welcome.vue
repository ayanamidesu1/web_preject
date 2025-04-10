<template>
    <div class="vip-welcome-page">
      <!-- 头部区域 -->
      <header class="vip-header">
        <div class="header-content">
          <span class="vip-badge">VIP 专属</span>
          <h1>解锁插画星球完整体验</h1>
          <p class="subtitle">数据分析、小说畅读、历史回溯，尽在VIP会员</p>
          <router-link to="/vip_pay" class="btn">立即开通</router-link>
        </div>
      </header>
  
      <!-- 会员特权区域 -->
      <section class="benefits-section">
        <h2 class="section-title">VIP会员尊享特权</h2>
        <div class="benefits-grid">
          <div class="benefit-card">
            <div class="benefit-icon">📊</div>
            <h3 class="benefit-title">高级数据分析</h3>
            <p>获取作品详细阅读数据、用户行为分析，助您优化创作方向</p>
          </div>
          <div class="benefit-card">
            <div class="benefit-icon">📚</div>
            <h3 class="benefit-title">衍生小说畅读</h3>
            <p>无限制阅读插画衍生的精品小说内容，沉浸式体验故事世界</p>
          </div>
          <div class="benefit-card">
            <div class="benefit-icon">⏳</div>
            <h3 class="benefit-title">历史消息回溯</h3>
            <p>永久保存您的互动记录，随时回溯社区精彩内容</p>
          </div>
        </div>
      </section>
  
      <!-- 用户评价区域 -->
      <section class="testimonials">
        <h2 class="section-title">VIP会员怎么说</h2>
        <div class="testimonial-grid">
          <div class="testimonial-card">
            <p class="testimonial-text">VIP的数据分析功能让我的作品曝光量提升了3倍，太值了！</p>
            <div class="testimonial-author">
              <img src="https://www.sunyuanling.com/server/static/image/avatar_thumbnail/65014220_p0.jpg" alt="用户头像" class="author-avatar">
              <div>
                <div class="author-name">林小画</div>
                <div class="author-title">插画师 | 2年VIP会员</div>
              </div>
            </div>
          </div>
          <div class="testimonial-card">
            <p class="testimonial-text">衍生小说内容质量超高，为我的创作提供了无数灵感。</p>
            <div class="testimonial-author">
              <img src="https://www.sunyuanling.com/server/static/image/avatar_thumbnail/97255797_p0.jpg" alt="用户头像" class="author-avatar">
              <div>
                <div class="author-name">创意马克</div>
                <div class="author-title">故事板艺术家 | 1年VIP会员</div>
              </div>
            </div>
          </div>
          <div class="testimonial-card">
            <p class="testimonial-text">历史回溯功能让我找回了3年前喜欢的作品，感动！</p>
            <div class="testimonial-author">
              <img src="https://www.sunyuanling.com/server/static/image/avatar_thumbnail/94552901_p0 (1).jpg" alt="用户头像" class="author-avatar">
              <div>
                <div class="author-name">怀旧小米</div>
                <div class="author-title">资深用户 | 永久VIP会员</div>
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- 底部行动号召 -->
      <section class="cta-section">
        <h2>准备好提升您的创作体验了吗？</h2>
        <button @click="goToPayment('yearly')" class="btn">立即成为VIP会员</button>
      </section>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  // 跳转到支付页面
  const goToPayment = (planType) => {
    router.push('/vip_pay')
  }
  </script>
  
  <style scoped>
  /* 这里保持与之前相同的CSS样式，略作调整以适应组件作用域 */
  .vip-welcome-page {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background-color: #F8F5F2;
    color: #292F36;
    line-height: 1.6;
  }
  
  .vip-header {
    background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
    color: white;
    padding: 80px 0 60px;
    text-align: center;
    border-radius: 0 0 20px 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    position: relative;
    overflow: hidden;
  }
  
  .header-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .vip-badge {
    background-color: #FFE66D;
    color: #292F36;
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.9rem;
    margin-bottom: 20px;
  }
  
  h1 {
    font-size: 3rem;
    margin-bottom: 10px;
    font-weight: 800;
  }
  
  .subtitle {
    font-size: 1.5rem;
    margin-bottom: 30px;
    font-weight: 300;
  }
  
  .btn {
    display: inline-block;
    padding: 12px 30px;
    background: #FF6B6B;
    color: white;
    border-radius: 30px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    font-size: 1rem;
  }
  
  .btn:hover {
    background: #ff5252;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255,107,107,0.3);
  }
  
  .btn-outline {
    background: transparent;
    border: 2px solid #FF6B6B;
    color: #FF6B6B;
  }
  
  .btn-outline:hover {
    background: #FF6B6B;
    color: white;
  }
  
  .benefits-section, .pricing-section, .testimonials, .cta-section {
    padding: 60px 20px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .section-title {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 50px;
    color: #FF6B6B;
    position: relative;
  }
  
  .section-title::after {
    content: "";
    display: block;
    width: 80px;
    height: 4px;
    background: #4ECDC4;
    margin: 15px auto;
  }
  
  .benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
  }
  
  .benefit-card {
    background: white;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .benefit-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
  }
  
  .benefit-icon {
    font-size: 2.5rem;
    color: #FF6B6B;
    margin-bottom: 20px;
  }
  
  .benefit-title {
    font-size: 1.3rem;
    margin-bottom: 15px;
    font-weight: 600;
  }
  
  .pricing-cards {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 30px;
    margin-top: 40px;
  }
  
  .pricing-card {
    background: white;
    border-radius: 15px;
    padding: 40px;
    width: 100%;
    max-width: 300px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.08);
    border: 2px solid #eee;
    transition: all 0.3s ease;
  }
  
  .pricing-card.popular {
    border: 2px solid #FF6B6B;
    position: relative;
    transform: scale(1.05);
  }
  
  .popular-badge {
    position: absolute;
    top: -15px;
    right: 20px;
    background: #FF6B6B;
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;
  }
  
  .price {
    font-size: 3rem;
    font-weight: 700;
    color: #292F36;
    margin: 20px 0;
  }
  
  .price span {
    font-size: 1rem;
    color: #777;
  }
  
  .period {
    color: #777;
    margin-bottom: 30px;
  }
  
  .testimonial-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
  }
  
  .testimonial-card {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  }
  
  .testimonial-text {
    font-style: italic;
    margin-bottom: 20px;
    position: relative;
  }
  
  .testimonial-text::before {
    content: "“ ";
    font-size: 4rem;
    color: #4ECDC4;
    opacity: 0.2;
    position: absolute;
    top: -20px;
    left: -10px;
  }
  
  .testimonial-author {
    display: flex;
    align-items: center;
  }
  
  .author-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 15px;
  }
  
  .author-name {
    font-weight: 600;
  }
  
  .author-title {
    font-size: 0.8rem;
    color: #777;
  }
  
  .cta-section {
    text-align: center;
    padding: 80px 20px;
    background: linear-gradient(to right, #FF6B6B, #4ECDC4);
    color: white;
    border-radius: 20px 20px 0 0;
    margin-top: 60px;
  }
  
  .cta-section h2 {
    font-size: 2.5rem;
    margin-bottom: 30px;
  }
  
  @media (max-width: 768px) {
    h1 {
      font-size: 2.2rem;
    }
    
    .subtitle {
      font-size: 1.2rem;
    }
    
    .pricing-cards {
      flex-direction: column;
      align-items: center;
    }
    
    .pricing-card.popular {
      transform: none;
    }
  }
  </style>