// src/main.ts
import { createApp } from 'vue';
import App from './App.vue';
import VueLazyload from 'vue-lazyload';
import store from './components/store.js';
import { RootState, Mutation } from './components/store.d';
import {router} from '@assets/model/router/index.js'
//使用pinia
import { createPinia } from 'pinia'
const pinia = createPinia()


// 设置延迟执行的时间
const DEBOUNCE_TIME = 50;

const app = createApp(App);
app.use(router);
app.use(pinia);

app.use(VueLazyload, {
  preLoad: 1.3,
  error: 'https://www.sunyuanling.com/assets/default_avatar.svg',
  loading: 'https://www.sunyuanling.com/assets/下载加载.mp4',
  attempt: 1,
});

// 订阅器，用于监听页面状态的变化
store.subscribe((mutation: Mutation, state: RootState) => {
  if (mutation.type === 'SET_PAGESTATUS' || 
      mutation.type === 'SET_CONTENT_PAGE' || 
      mutation.type === 'SET_SINGLE_PAGE_STATUS' ||
      mutation.type === 'SET_INDEX_PAGE'
  ) {
    if (state.pushTimer) {
      clearTimeout(state.pushTimer); // 清除之前的定时器
    }
    state.pushTimer = setTimeout(() => {
      state.pushTimer = null;
      store.commit('PUSH_PAGE_STATE'); // 在页面状态改变时记录状态
    }, DEBOUNCE_TIME);
  }
});

app.use(store);
app.mount('#app');
