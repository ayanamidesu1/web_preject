import { createApp } from 'vue'
import { createPinia } from 'pinia'  // 导入createPinia
import App from './App.vue'
import { router } from './model/router'
import ElementPlus from 'element-plus'

const app = createApp(App)

// 创建Pinia实例并安装
const pinia = createPinia()
app.use(pinia)
app.use(ElementPlus)

// 安装路由
app.use(router)

app.mount('#app')