<template>
    <div class="header_page">
      <div class="content">
        <div class="user_item">
          <div class="username">
            <span>欢迎管理员：{{username}}</span>
          </div>
          <div class="user_avatar">
            <img src="https://www.sunyuanling.com/server/static/image/avatar_thumbnail/65014220_p0.jpg" alt="User Avatar">
          </div>
        </div>
        <div class="logout" @click="logout">
          <div class="logout_btn">
            <span>退出登录</span>
            <img class="icon" src="https://www.sunyuanling.com/assets/logout.svg" alt="Logout Icon">
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  let username = ref('admin');
  </script>
  
  <style scoped>
  .header_page {
    width: 100%;
    height: 60px; 
    display: flex;
    justify-content: space-between; 
    align-items: center; 
    background-color: #f4f4f4; 
    padding: 0 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); 
    z-index:5;
  }
  
  .content {
    display: flex;
    width: 100%;
    justify-content: space-between; 
    align-items: center;
  }
  
  .user_item {
    display: flex;
    align-items: center;
  }
  
  .username {
    margin-right: 15px; 
    font-size: 16px;
    color: #333; 
  }
  
  .user_avatar img {
    width: 40px; 
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .logout {
    cursor: pointer; 
    display: flex;
    align-items: center;
    width: auto;
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    padding:5px 10px;
    border-radius: 5px;
  }
  .logout:hover{
    background-color: rgba(233,233,233,1);
    transform: scale(1.05);
    transition: all 0.2s ease-in-out;
    transform: translateY(-2px);
  }
  
  .logout_btn {
    display: flex;
    align-items: center;
    font-size: 14px;
    color: #000000; 
  }
  
  .icon {
    width: 20px; 
    height: 20px;
    margin-left: 8px;
    object-fit: cover;
  }
  </style>
  