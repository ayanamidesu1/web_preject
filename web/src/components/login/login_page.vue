<!-- eslint-disable no-useless-catch -->
<template>
    <div class="back">
        
        <div class="login_page">
            <h1>登录</h1>
            <div class="username_input">
                <input placeholder="用户名/用户ID/邮箱/手机号" type="text" v-model="username_in" ref="username">
            </div>
            <div class="user_password">
                <input placeholder="密码" type="password" v-model="password_in" ref="password">
            </div>
            <div class="more_box">
                <div class="register_btn">
                    <span>没有账号？<span class="register_btn_text" @click="register">&nbsp;注册~</span></span>
                    
                </div>
                <div class="reset_password_btn">
                    <span class="reset_password_btn_text">忘记密码？</span>
                </div>
            </div>
            <div class="login_btn" @click="login"><span>登录</span></div>
        </div>
    </div>
</template>

<script setup lang="ts">   
// eslint-disable-next-line no-unused-vars
import {ref,} from 'vue';
let username_in = ref('');  
let password_in = ref('');  
let get_message = ref('');
//登录
async function login(){
    if(username_in.value == '' || password_in.value == ''){
        alert('请输入用户名和密码');
        return;
    }
    try{
        let res=await fetch('https://www.sunyuanling.com/api/login/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            
            },
            body:JSON.stringify({
                login_key:username_in.value,
                password:password_in.value
            })
        })
        let data=await res.json();
        console.log(data);
        if(data.code == 200){
            alert('登录成功');
            localStorage.setItem('token',data.token);
            window.location.href='/'
        }
    }   
    catch(e)
    {
        console.log(e);
    }
}


//注册跳转
function register(){
        window.location.href="/register"
    }
</script>

<style  scoped>
.register_btn_text:hover{
    cursor: pointer;
    color: rgba(0,150,250,0.8);
    transition:0.2s;
}
.reset_password_btn_text:hover{
    cursor: pointer;
    color: rgba(0,150,250,0.8);
    transition:0.2s;
}
.more_box{
    display: flex;
    justify-content: space-between;
    width:80%;
    height: 30px;
    margin-top:5px;
    margin-bottom: 5px;
}

@keyframes gradient {  
    0% {  
        background-position: 0% 50%;  
    }  
    50% {  
        background-position: 100% 50%;  
    }  
    100% {  
        background-position: 0% 50%;  
    }  
}  
  
.back {  
    /* 你的原始样式 */  
    background-color: #c0c8cf; /* 作为备用的背景颜色，或者渐变开始的颜色 */  
    height: 100vh;  
    width: 100vw;  
    display: flex;  
    justify-content: center;  
    align-items: center;  
    color: #fff;  
    border-radius: 15px;  
    padding: 5px;  
  
    /* 添加渐变背景 */  
    background-image: linear-gradient(90deg, #9fbcd4, #e0e8ef, #71b2eb);  
    background-size: 250% 100%; /* 让渐变背景可以移动 */  
    animation: gradient 3s ease infinite; /* 应用动画，并设置动画时间、缓动函数和循环次数 */  
}
.login_page{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width:100%;
    height: 100%;
}
.username_input,.user_password{
    width:80%;
    height: 40px;
    margin-top:20px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    background-color: #e0e8ef;
}
.login_btn{
    width:80%;
    height: 50px;
    margin-top:50px;
    background-color: #2a98f8;
    border-radius: 15px;
    padding: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 18px;
    font-weight: bold;
}
.login_btn:hover{
    cursor: pointer;
    opacity: 0.8;
    transition: 0.2s;
}
input{
    border:1px solid rgba(0,0,0,0.2);
    border-radius: 10px;
    background: transparent;
    width:100%;
    height: 100%;
}

</style>