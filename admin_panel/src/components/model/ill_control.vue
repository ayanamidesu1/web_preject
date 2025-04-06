<template>
  <div class="ill_control" v-if="work_list_info">
    <h1>插画审核</h1>
    <div class="control_box" ref="content">
      <div class="search_box">
        <span>搜索：</span>
        <input type="text" placeholder="请输入搜索内容" v-model="search_key">
        <button @click="performSearch">搜索</button>
      </div>
      <div class="work_status">
        <label>作品状态：</label>
        <select v-model="work_status">
          <option value="all">全部</option>
          <option value="1">已通过</option>
          <option value="0">未通过</option>
          <option value="2">待审核</option>
        </select>
      </div>
    </div>
    <div class="content">
      <div class="item" v-for="(item, index) in ill_worklist" :key="index">
        <div class="ill_cover">
          <img :src="'https://www.sunyuanling.com/server/static/image/thumbnail/' + item.content_file_list.split(/[,，]/)[0]"
            alt="插画作品封面">
          <span @click="show_ill(item)" class="show_ill_content_btn">查看详情</span>
        </div>
        <div class="ill_info">
          <div class="info_item">
            <span>标题：</span>
            <span>{{ item.name }}</span>
          </div>
          <div class="info_item">
            <span>作者：</span>
            <span>{{ item.username }}</span>
          </div>
          <div class="info_item">
            <span>作品标签：</span>
            <span v-for="(tag_item, index) in item.work_tags.split(/[,，]/)" :key="index">
              {{ tag_item }}
            </span>
          </div>
          <div class="info_item">
            <span>作品简介：</span>
            <span>{{ item.brief_introduction }}</span>
          </div>
          <div class="info_item">
            <span>作品年龄分级：</span>
            <span>{{ item.age_classification }}</span>
          </div>
          <div class="info_item">
            <span>作品状态：</span>
            <span>{{ item.work_approved == 1 ? '已通过' : item.work_approved == 0 ? '未通过' : '待审核' }}</span>
          </div>
          <div class="work_action">
            <button @click="update_work_status(1, item.Illustration_id)">通过</button>
            <button @click="update_work_status(0, item.Illustration_id)">不通过</button>
          </div>
        </div>
      </div>
      <div class="scroll_tag" ref="scroll_tag" style="width:1px;height:1px;overflow:hidden;"></div>
      <div class="loading" v-if="loading">
        <span>加载中……</span>
      </div>
    </div>
    <div class="show_ill_content" v-if="show_ill_content">
      <div class="close">
        <button @click="show_ill_content = false">
          <img src="https://www.sunyuanling.com/assets/close.svg" alt="关闭" class="icon">
        </button>
      </div>
      <div class="ill_img" v-for="(item, index) in ill_list" :key="index">
        <img :src="'https://www.sunyuanling.com/server/static/image/' + item" alt="作品">
      </div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { get_ill_worklist } from './js/get_work_list'
import { search_ill_work } from './js/search_work'
import { update_ill_work_status } from './js/update_work'

const ill_worklist = ref([])
const work_list_info = ref()
const limit = ref(5)
const offset = ref(0)
const total = ref(0)
const show_ill_content = ref(false)
const ill_list = ref([])
const search_key = ref('')
const work_status = ref('all')
const loading = ref(false)

function show_ill(item) {
  ill_list.value = item.content_file_list.split(/[,，]/)
  show_ill_content.value = true
}

// 获取作品列表
async function get_worklist() {
  let response = await get_ill_worklist(limit.value, offset.value)
  console.log(response)
  work_list_info.value = response
  if (offset.value == 0) {
    ill_worklist.value = response.data.work_list
  } else {
    ill_worklist.value = [...ill_worklist.value, ...response.data.work_list]
  }
  total.value = response.data.total
}

// 搜索实现
async function search_ill() {
  offset.value = 0 // 重置偏移量
  let response = await search_ill_work(search_key.value, work_status.value, limit.value, offset.value)
  ill_worklist.value = response.data.work_list
  total.value = response.data.total
}

watch([search_key, work_status], async () => {
  await search_ill()
})

function performSearch() {
  search_ill()
}

// 更新作品状态
async function update_work_status(work_status, work_id) {
  let data = await update_ill_work_status(work_status, work_id)
  if (data.status === 'success') {
    alert('修改成功')
    offset.value = 0 // 重置偏移量
    await get_worklist()
  } else {
    alert(data.message)
  }
}

// 滚动加载
let scroll_tag = ref(null)
let content = ref(null)
const observer = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting && !loading.value && ill_worklist.value.length < total.value) {
    loading.value = true;
    offset.value += limit.value; // 增加偏移量
    await get_worklist(); // 加载更多内容
    loading.value = false;
  }
}, {
  root: null,
  rootMargin: '400px',
  threshold: 0
});
//const observer=null
onMounted(async () => {
  await get_worklist();


  observer.observe(scroll_tag.value);
})

onUnmounted(() => {
  observer.disconnect();
})
</script>


<style scoped>
.ill_control {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
}

.content {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.item {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 20px;
  gap: 10px;
  max-height: 350px;
  overflow-y: auto;
}

.ill_cover {
  width: 200px;
  height: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.ill_cover img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 15px;
}

.ill_info {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 5px;
  justify-content: space-around;
  flex: 1;
}

.info_item {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #838383;
}

.info_item span:nth-child(1) {
  font-weight: bold;
  color: #333;
}

.show_ill_content {
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 20px;
  overflow-y: auto;
  z-index: 5;
  padding: 50px;
  overflow-x: auto;
}

.ill_img {
  width: auto;
  height: auto;
  max-width: 80%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin: 10px;
}

.ill_img img {
  width: auto;
  height: auto;
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.close {
  width: 35px;
  height: 35px;
  position: fixed;
  right: 30px;
  top: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 6;
}

.close button {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border: none;
  background-color: rgba(255, 255, 255, 0.8);
}

.close button:hover {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  transition: all 0.2s ease-in-out;
  transform: scale(1.05);
  transform: translateY(-2px);
}

.close button img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.control_box {
  width: 100%;
  height: 50px;
  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: center;
}

.search_box {
  width: 70%;
  height: 40px;
  display: flex;
  flex-direction: row;
  gap: 10px;
  align-items: center;
}

.search_box input {
  width: 80%;
  height: 100%;
  border-radius: 10px;
  border: 1px solid rgb(133, 133, 133);
}

.work_action {
  width: 150px;
  height: 50px;
  display: flex;
  flex-direction: row;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
}

.work_action button {
  width: 75px;
  height: 40px;
  border: 1px solid rgb(133, 133, 133);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.work_action button:hover {
  background-color: rgb(133, 133, 133);
  color: white;
  transition: all 0.2s ease-in-out;
}

.show_ill_content_btn {
  width: 100px;
  height: 40px;
  cursor: pointer;
  background-color: rgba(0, 150, 250);
  border-radius: 10px;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}

.show_ill_content_btn:hover {
  background-color: rgb(0, 150, 250);
  opacity: 0.8;
  color: white;
  transition: all 0.2s ease-in-out;
  transform: scale(1.02);
  transform: translateY(-1px);
}
</style>