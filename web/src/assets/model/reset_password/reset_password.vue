<template>
  <div class="back">
    <div class="root_page">
      <div class="title">
        <h1>重置密码</h1>
      </div>
      <div class="content w">
        <form @submit.prevent="handleSubmit">
          <div class="username">
            <input
              v-model="formData.username"
              type="text"
              placeholder="请输入用户名"
              class="mt mb w"
            />
          </div>
          <div class="password w">
            <input
              v-model="formData.password"
              type="password"
              placeholder="请输入密码"
              class="mb w"
            />
          </div>
          <div class="surepassword w">
            <input
              v-model="formData.again_password"
              type="password"
              placeholder="请再次输入密码"
              class="mb w"
            />
          </div>
          <div class="phone w">
            <input
              v-model="formData.phone"
              type="text"
              placeholder="请输入手机号"
              class="mb w"
            />
          </div>
          <div class="email w">
            <input
              v-model="formData.email"
              type="text"
              placeholder="请输入邮箱"
              class="mb w"
            />
          </div>
          <button type="submit" class="submit w">
            <span>提交</span>
          </button>
        </form>
      </div>
      <div class="footer">
        <router-link to="/"><span>返回主页</span></router-link>
        <router-link to="/login"><span>返回登录</span></router-link>
      </div>
    </div>
  </div>
</template>
  
  <script setup>
import { ref } from "vue";
import { BaseApi } from "@/base_api";
const api=new BaseApi();

const formData = ref({
  username: "",
  password: "",
  again_password: "",
  phone: "",
  email: "",
});

const validateForm = () => {
  if (formData.value.password !== formData.value.again_password) {
    alert("两次密码不一致");
    return false;
  }
  if (Object.values(formData.value).some((value) => value === "")) {
    alert("请输入完整信息");
    return false;
  }
  return true;
};

const handleSubmit = async () => {
  if (!validateForm()) return;

  try {
    const res=await api.post('GetUserInfo/ResetPassword',
        {
          username: formData.value.username,
          password: formData.value.password,
          phone: formData.value.phone,
          email: formData.value.email,
        }
    )
    if(res.status==200){
        alert("重置密码成功");
    }
    else{
        alert(res.result.msg)
    }
  } catch (err) {
    console.error(err);
    alert("请求失败，请稍后重试");
  }
};
</script>
  
  <style scoped>
/* 保持原有样式不变 */
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
  display: flex;
  padding: 0px;
  margin: 0px;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
  background-image: linear-gradient(90deg, #fa86f4, #e0e8ef, #48a6f8);
  background-size: 250% 100%;
  animation: gradient 3s ease infinite;
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
  margin-left: auto;
  margin-right: auto;
  width: 100%;
}

.w {
  width: 100%;
}

input {
  width: 100%;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  height: 30px;
}

.submit {
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  height: 40px;
  border-radius: 10px;
  background-color: rgba(0, 150, 250, 1);
  opacity: 0.8;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 20px;
  font-weight: bold;
  border: none;
  cursor: pointer;
}

.submit:hover {
  opacity: 1;
  transition: 0.2s;
}
.footer{
    display: flex;
    flex-direction: row;
    gap:10px;
    align-self: center;
    margin-top: 10px;
}
.footer span:hover{
    color: rgba(0, 150, 250, 1);
    transition: 0.2s;
    text-decoration: underline;
}
</style>