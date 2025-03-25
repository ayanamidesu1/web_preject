<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="root_page" v-if="!loading">
      <div class="cursor_action"
        :style="{ top: cursor_top + 'px', left: cursor_left + 'px', opacity: cursor_apactiy, transform: `translateY(${cursor_add}px)` }">
        <img src="https://www.sunyuanling.com/assets/cat.svg" class="icon">
        <span>喵喵喵~</span>
      </div>
      <float_msg_box></float_msg_box>
      <float_hand></float_hand>
      <header_box v-if="load_reading"></header_box>
      <index v-if="load_reading&&index_page_show"></index>
      <div class="loading" v-if="!load_reading">
        <img class="icon" src="https://www.sunyuanling.com/image/loading.gif">
      </div>
      <upload_page v-if="upload_page_show" />
      <content_index_page v-if="content_index_page_show"/>
      <user_center_page :token="token" v-if="user_center_page_show"></user_center_page>
      <other_user_center_page v-if="other_user_center_page_show" :userid="other_userid"></other_user_center_page>
      <data_analysis :token="token" v-if="data_analysis_page"/>
      <work_contribute v-if="work_contribute_page"></work_contribute>
      <br_his_index_page v-if="br_his_page"></br_his_index_page>

    </div>
    <div v-else class="loading">
      <img class="icon" src="https://www.sunyuanling.com/image/loading.gif">
      <p>正在加载...</p>
    </div>
  </template>
  
  <script setup>
  import * as cookies from '../assets/js/cookies';
  import { ref, computed, onMounted } from 'vue';
  import { useStore } from 'vuex';
  import index from './index.vue';
  import header_box from './headpage_file/header_box.vue';
  import upload_page from './headpage_file/file/contribute/index.vue';
  import content_index_page from './content_page/content_index_page.vue';
  import user_center_page from './user_center_page/user_center_page.vue';
  import other_user_center_page from './other_user_center_page/user_center_page.vue';
  import data_analysis from '@/assets/model/data_analysis/components/root.vue';
  import work_contribute from '@/assets/model/work_contribute_review/components/root.vue';
  import br_his_index_page from './browse_history_page/br_his_index_page.vue';
  import float_msg_box from '../assets/model/float_msg_box.vue'
  import float_hand from '../assets/model/float_hand.vue'
  
  const store = useStore();
  const cursor_top = ref(0);
  const cursor_left = ref(0);
  const cursor_apactiy = ref(0);
  const cursor_add = ref(0);
  const load_reading = ref(false);
  const loading = ref(true); // Initialize with true to block page loading
  const upload_page_show = computed(() => store.getters.upload_work);
  const index_page_show = computed(() => store.getters.index_page);
  const content_index_page_show = computed(() => store.getters.content_index_page);
  const user_center_page_show = computed(() => store.getters.user_center_page);
  const token = computed(() => store.getters.token);
  const other_user_center_page_show = computed(() => store.getters.other_user_center_page);
  const other_userid = computed(() => store.getters.other_userid);
  const data_analysis_page = computed(() => store.getters.data_analysis_page);
  const work_contribute_page=computed(()=>store.getters.work_contribute_page);
  const br_his_page=computed(()=>store.getters.br_his_page);
  
  // 读取URL参数设置cookie并清除URL中的token参数
  function setTokenFromURL() {
    const url = new URL(window.location.href);
    const token = url.searchParams.get('token');
  
    if (token && (localStorage.getItem('token') !== token)) {
      //cookies.set_cookie('token', token, { secure: true, 'max-age': 3600, path: '/', HttpOnly: true });
      localStorage.setItem('token', token);
      
      // 移除 URL 中的所有参数，只保留基本路径
      const newUrl = url.origin + url.pathname;
      
      // 替换当前历史记录
      window.history.replaceState({}, document.title, newUrl);
    }
  }
  
  async function get_userinfo() {
    try {
      const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetAllUserInfo/', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token') }`
        },
        body: JSON.stringify({
          userid: null,
          token: localStorage.getItem('token')
        })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.status === 'success') {
          cookies.set_cookie('userinfo', JSON.stringify(data.data[0]), { secure: true, 'max-age': 3600, path: '/', HttpOnly: true });
          localStorage.setItem('userinfo',JSON.stringify(data.data[0]))
          load_reading.value = true;
        } else {
          console.log('用户未登录');
          window.location.href = 'https://localhost:3000';
        }
      } else {
        console.log('网络错误');
        cookies.clearAllCookies();
        window.location.href = 'https://localhost:3000';
      }
    } catch (err) {
      console.log('获取用户信息失败:', err);
      cookies.clearAllCookies();
      window.location.href = 'https://localhost:3000';
    }
  }
  
  async function load_login() {
    try {
      const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/Login/', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          userid: null,
          token: localStorage.getItem('token')
        })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.status === 'success') {
          //cookies.set_cookie('token', data.token, { secure: true, 'max-age': 3600, path: '/', HttpOnly: true });
          localStorage.setItem('token', data.token);
          store.commit('SET_TOKEN', data.token);
        }
      }
    } catch (err) {
      console.log('登录验证失败:', err);
    }
  }
  
  onMounted(async () => {
    setTokenFromURL();
    await get_userinfo();
    await load_login();
    loading.value = false; // Set loading to false after initialization
  });
  </script>
  
  <style scoped>
  .cursor_action {
    position: fixed;
    color: #f889fc;
    opacity: 0;
    width: 90px;
    z-index: 100;
    pointer-events: none;
  }
  
  .cursor_action svg img {
    width: 20px;
    height: 20px;
    object-fit: cover;
  }
  
  .icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
  }
  
  .loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: #fff;
  }
  </style>
  