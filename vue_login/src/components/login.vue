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
import { useRouter } from 'vue-router';
let username_in = ref('');  
let password_in = ref('');  
let get_message = ref('');
  
function login() {  
    if (username_in.value === '') {  
        alert('用户名不能为空');  
        return;  
    }  
    if (password_in.value === '') {  
        alert('密码不能为空');  
        return;  
    }  
  
    connServer()  
        .then(data => {  
            if (data.status === 'success') {  
                console.log(data.data)
                //cookies.set_cookie('userinfo',JSON.stringify(data.data))
                //console.log(JSON.parse(cookies.get_cookie('userinfo')))
                //window.location.href='https://www.sunyuanling.com/index_page/dist/index.html'+'?token='+data.token;
                window.location.href='https://localhost:3002/'+"?token="+data.token
                return;
            } else {  
                // 登录失败的处理逻辑  
                alert('登录失败: ' + data.message);  
            }  
        })  
        .catch(error => {  
            // 请求失败的处理逻辑  
            console.error('请求失败:', error);  
            alert('登录失败，请检查您的网络连接或稍后重试');  
        });  
}  
  

// 连接服务器  
async function connServer() {  
    // eslint-disable-next-line no-useless-catch
    try {  
        
        const response = await fetch('https://www.sunyuanling.com/api/GetUserInfo/Login/', {  
            method: 'POST',  
            headers: {  
                'Content-Type': 'application/json',
                  
            },  
            body: JSON.stringify({  
                username: username_in.value,  
                password: password_in.value,
                login_type:'front_end'
            })  
        });
  
        if (!response.ok) {  
            throw new Error('请求失败: ' + response.status);  
        }  

        const data = await response.json(); // 将响应数据解析为 JSON 格式
        get_message.value = data; // 存储响应数据
        console.log(data)
        return data; // 返回解析后的数据
    } catch (error) {  
        // 这里可以抛出错误或返回某种失败状态  
        throw error;  
    }  
    
} 
//注册跳转
function register(){
        window.location.href="https://127.0.0.1:4434/register"
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
    height: 50vh;  
    width: 50vw;  
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