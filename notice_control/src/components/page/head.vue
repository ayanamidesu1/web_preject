<template>
  <div class="notice_head">
    <div class="title">
      公告管理
    </div>
    <div class="time">
      {{ time }}
    </div>
    <div class="user_box" v-if="user_info" @mouseover="showDropdown" @mouseleave="hideDropdown">
      <span>{{ user_info.username }}</span>
      <div class="user_avatar" @click="drop_down">
        <img :src="'https://www.sunyuanling.com/server/static/image/avatar_thumbnail/' + user_info.user_avatar">
      </div>
      <div class="drop_down_svg">
        <img :src="temp_svg" class="icon">
      </div>
      <div class="drop_down" v-if="drop_down_show" @click="hideDropdown">
        <div class="drop_down_item">
          <span id="username">
            {{ user_info.username }}
          </span>
        </div>
        <div class="drop_down_item">
          <div class="user_avatar">
            <img :src="'https://www.sunyuanling.com/server/static/image/avatar_thumbnail/' + user_info.user_avatar">
          </div>
        </div>
        <div class="drop_down_item" @click="logout">
          <span>退出登录</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted } from 'vue';
import * as cookies from '../../../../model/cookies.js'
export default {
  name: 'notice_head',
}
</script>

<script setup>
let time = ref();
let drop_down_show = ref(false);
let drop_svg = ref('https://www.sunyuanling.com/assets/drop_down.svg');
let drop_up_svg = ref('https://www.sunyuanling.com/assets/drop_up.svg');
let temp_svg = ref('https://www.sunyuanling.com/assets/drop_down.svg');

function updatetime() {
  setInterval(() => {
    time.value = new Date().toLocaleString();
  }, 500)
}

onMounted(() => {
  time.value = new Date().toLocaleString();
  updatetime();
})

function showDropdown() {
  drop_down_show.value = true;
  temp_svg.value = drop_up_svg.value;
}

function hideDropdown() {
  drop_down_show.value = false;
  temp_svg.value = drop_svg.value;
}

// 设置用户信息
let user_info = ref(JSON.parse(cookies.get_storage('user_info')))
// 退出登录
function logout() {
  cookies.clearAllCookies();
  cookies.clearAllLocalStorage();
  setTimeout(() => {
    window.location.href = '/'
  }, 1000)
  window.location.reload()
}
</script>

<style scoped>
.icon {
  width: 25px;
  height: 25px;
}

.notice_head {
  display: flex;
  width: 95vw;
  height: 60px;
  margin: 0px auto;
  justify-content: space-between;
  align-items: center;
}

.user_box {
  display: flex;
  align-items: center;
  width: auto;
  height: auto;
  padding: 5px;
  position: relative;
}

.user_avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 5px auto;
  margin-left: 5px;
}

.user_avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.drop_down_svg {
  cursor: pointer;
}

.drop_down {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 60px;
  justify-content: space-around;
  gap: 10px;
  padding: 10px 10px;
  background-color: rgba(133, 133, 133, 0.5);
  min-width: 100px;
  border-radius: 10px;
  transition: all 0.3s ease-in-out;
  opacity: 0;
  visibility: hidden;
}

.drop_down_item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: auto;
  max-height: 50px;
  border-bottom: 1px solid rgba(255, 255, 188, 1);
  cursor: pointer;
}

.drop_down_item:hover {
  background-color: rgba(133, 133, 133, 0.8);
  transition: all 0.3s ease-in-out;
  border-radius: 5px;
}

.user_box:hover .drop_down {
  opacity: 1;
  visibility: visible;
}
</style>
