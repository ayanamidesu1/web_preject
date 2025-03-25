<template>
    <div class="root">
      <div class="root_page">
        <div class="title mt mb">
          <h1>注册账号</h1>
        </div>
        <div class="content mt mb">
          <div class="username mt mb">
            <input v-model="username" type="text" placeholder="用户名">
          </div>
          <div class="password mt mb">
            <input v-model="password" type="password" placeholder="密码">
          </div>
          <div class="user_avatar mt mb">
            <div class="avatar mt mb">
              <img :src="avatarPreview" class="preview" v-show="avatarPreview">
              <label for="avatarInput" class="choose_avatar mt">选择头像</label>
              <input 
                type="file" 
                id="avatarInput" 
                accept="image/*" 
                style="display: none;"
                @change="handleAvatarChange"
              >
            </div>
          </div>
          <span class="tips mt mb">头像的选择最好是一比一</span>
          <div class="email mt mb">
            <input v-model="email" type="text" placeholder="邮箱">
          </div>
          <div class="phone mt mb">
            <input v-model="phone" type="text" placeholder="手机号">
          </div>
          <div class="sex mt mb">
            <select v-model="sex">
              <option value="男">男</option>
              <option value="女">女</option>
            </select>
          </div>
          <input type="submit" value="注册" class="submit_btn mt" @click="register">
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const username = ref('');
  const password = ref('');
  const email = ref('');
  const phone = ref('');
  const sex = ref('男');
  const avatarFile = ref(null);
  const avatarPreview = ref(null);
  
  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      avatarFile.value = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        avatarPreview.value = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  };
  
  const setUserAvatar = async () => {
    if (!avatarFile.value) return;
  
    const formData = new FormData();
    formData.append('avatar', avatarFile.value);
  
    try {
      const res = await fetch('https://127.0.0.1:4434/UploadFile', {
        method: 'POST',
        body: formData,
      });
      return await res.json();
    } catch (error) {
      console.error('头像上传失败:', error);
      throw error;
    }
  };
  
  const setUserInfo = async (filename) => {
    const userInfo = {
      username: username.value,
      password: password.value,
      email: email.value,
      phone: phone.value,
      sex: sex.value,
      filename: filename
    };
  
    try {
      const res = await fetch('https://127.0.0.1:4434/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userInfo)
      });
      const data = await res.json();
      
      if (data.status === "success") {
        alert("注册成功");
        window.location.href = "/";
      } else {
        alert(data.message || "注册失败");
      }
    } catch (error) {
      console.error('注册请求失败:', error);
      alert("注册失败");
    }
  };
  
  const register = async () => {
    if (!avatarFile.value) {
      alert("请选择头像");
      return;
    }
  
    try {
      // 先上传头像
      const avatarRes = await setUserAvatar();
      if (avatarRes?.filename) {
        // 提交用户信息（携带文件名）
        await setUserInfo(avatarRes.filename);
      }
    } catch (error) {
      console.error('注册流程错误:', error);
    }
  };
  </script>

<style scoped>
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

.root{
    display: flex;
    padding: 0px;
    margin: 0px;
    justify-content: center;
    align-items: center;
    width: 100vw;
    height: 100vh;
    background-image: linear-gradient(90deg, #fa86f4, #e0e8ef, #48a6f8);
    background-size: 250% 100%;
    /* 让渐变背景可以移动 */
    animation: gradient 3s ease infinite;
    /* 应用动画，并设置动画时间、缓动函数和循环次数 */
    background-color: #48a6f8;
}

.root_page {
    display: flex;
    flex-direction: column;
    width: auto;
    min-width: 350px;
    padding: 10px;
    height: auto;
    margin: auto;
    align-self: center;
    background-color: rgba(245, 245, 245, 0.8);
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
}

.mt {
    margin-top: 10px;
}

.mb {
    margin-bottom: 5px;
}

.content {
    display: flex;
    flex-direction: column;
    width: 98%;
    height: 100%;
    justify-content: center;
}

input {
    width: 100%;
    height: 100%;
    border-radius: 5px;
    margin-left: auto;
    margin-right: auto;
    align-self: center;
    border: 1px solid rgba(0, 0, 0, 0.2);
}

.username,
.password,
.email,
.phone {
    display: flex;
    width: 100%;
    height: 30px;
    justify-content: center;
    margin-left: auto;
    margin-right: auto;
}

.user_avatar {
    display: flex;
    width: 100%;
    height: 150px;
    position: relative;
}

.preview {
    width: 100px;
    height: 100px;
    overflow: hidden;
    border-radius: 50%;
    object-fit: cover;
}

.avatar {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.choose_avatar {
    display: flex;
    width: 50%;
    height: 35px;
    background-color: rgba(0, 150, 250, 1);
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    opacity: 0.8;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
}

.choose_avatar:hover {
    opacity: 1;
    cursor: pointer;
    transition: 0.2s;
}

.submit_btn {
    display: flex;
    margin-left: auto;
    margin-right: auto;
    height: 35px;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 150, 250, 1);
    border-radius: 10px;
    opacity: 0.8;
    font-size: 18px;
    font-weight: bold;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
    ;
}

.submit_btn:hover {
    opacity: 1;
    cursor: pointer;
    transition: 0.2s;
}

</style>