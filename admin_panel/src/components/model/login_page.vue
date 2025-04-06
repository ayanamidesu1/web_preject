<template>
    <div class="login_page">
        <div class="login_container">
            <div class="title">管理面板登录</div>
            <div class="login_form">
                <div class="form_group">
                    <label for="username">管理员用户ID</label>
                    <input v-model="username" id="username" type="text" placeholder="请输入管理员用户ID" />
                </div>
                <div class="form_group">
                    <label for="password">管理员密码</label>
                    <input v-model="password" id="password" type="password" placeholder="请输入管理员密码" />
                </div>
                <div class="login_btn">
                    <button @click="handleLogin">登录</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { admin_login } from './js/login.js'

const username = ref('');
const password = ref('');

const handleLogin = async () => {
    // 登录处理逻辑待定
    let result = await admin_login(null, username.value, password.value)
    localStorage.setItem('token', result.token);
    console.log(result)
    console.log(`用户名: ${username.value}, 密码: ${password.value}`);
    if (result.code==200){
        window.location.href='/'
    }
    else{
        console.warn('登录失败，请检查用户名和密码')
        console.log(result)
    }
};
</script>

<style scoped>
.login_page {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100vw;
    height: 100vh;
    background-color: #f4f4f4;
    position: fixed;
    top: 0px;
    left: 0px;
    z-index: 100;
}

.login_container {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    width: 360px;
}

.title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
}

.login_form {
    display: flex;
    flex-direction: column;
}

.form_group {
    margin-bottom: 1rem;
}

.form_group label {
    display: block;
    font-size: 14px;
    margin-bottom: 0.5rem;
}

.form_group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

.login_btn {
    display: flex;
    justify-content: center;
}

.login_btn button {
    padding: 0.75rem 1.5rem;
    font-size: 16px;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.login_btn button:hover {
    background-color: #0056b3;
}
</style>