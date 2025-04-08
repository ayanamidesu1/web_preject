<template>
  <div class="comic_control">
    <h1>插画审核</h1>
    <div class="control_box" v-if="work_info_list">
      <div class="search_box">
        <span>搜索：</span>
        <input type="text" placeholder="请输入搜索内容" v-model="search_key">
        <button>搜索</button>
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
      <div class="item" v-for="(item, index) in work_list" :key="index">
        <div class="comic_cover">
          <img :src="'https://www.sunyuanling.com/server/static/image/comic/thumbnail/' + item.content_file_list.split(/[,，]/)[0]"
            alt="漫画作品封面">
          <span @click="show_comic(item)" class="show_comic_content_btn">查看详情</span>
        </div>
        <div class="comic_info">
          <div class="info_item">
            <span>标题：</span>
            <span>{{ item.work_name }}</span>
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
            <button @click="update_work_status(1, item.id,item.userid)">通过</button>
            <button @click="update_work_status(0, item.id,item.userid)">不通过</button>
          </div>
        </div>
      </div>
      <div class="scroll_tag" ref="scroll_tag" style="width:1px;height:1px;overflow:hidden;"></div>
      <div class="loading" v-if="loading">
        <span>加载中……</span>
      </div>
    </div>
    <div class="show_comic_content" v-if="show_comic_content">
      <div class="close">
        <button @click="show_comic_content = false">
          <img src="https://www.sunyuanling.com/assets/close.svg" alt="关闭" class="icon">
        </button>
      </div>
      <div class="comic_img" v-for="(item, index) in comic_list" :key="index">
        <img :src="'https://www.sunyuanling.com/server/static/image/comic/' + item" alt="作品">
      </div>
    </div>
  </div>
 
</template>


<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { get_comic_worklist } from './js/get_work_list'
import { search_comic_work } from './js/search_work'
import { update_comic_work_status } from './js/update_work'
import { useStore } from '@/model/store/store'

const store = useStore()

const work_info_list = ref()
const limit = ref(5)
const offset = ref(0)
const total = ref(0)
const work_list = ref([])
const search_key = ref('')
const show_comic_content = ref(false)
const work_status = ref('all')
const comic_list = ref([])
const loading = ref(false)


function show_comic(item) {
  comic_list.value = item.content_file_list.split(/[,，]/)
  show_comic_content.value = true
}

//获取漫画作品列表

async function get_comic_list() {
  work_info_list.value = await get_comic_worklist(limit.value, offset.value)
  console.log(work_info_list.value)
  total.value = work_info_list.value.data.total
  work_list.value = [...work_list.value, ...work_info_list.value.data.work_list]
}

onMounted(async () => {
  await get_comic_list()
})

//搜索实现
async function search_comic(search_key, work_status = 'all') {
  work_info_list.value = await search_comic_work(search_key, work_status, limit.value, offset.value)
  work_list.value = work_info_list.value.data.work_list
  total.value = work_info_list.value.data.total
  console.log(work_list.value)
}
watch([search_key, work_status], async () => {
  await search_comic(search_key.value, work_status.value)
})

//更新作品状态
async function update_work_status(work_status, work_id,user_id) {
  let data = await update_comic_work_status(work_status, work_id)
  if (data.status == 'success') {
    alert('修改成功'),
    await get_comic_list()
    send_comic_review_msg(user_id, work_id, work_status)
  }
  else {
    alert(data.message)
  }
  await get_comic_list()
}

//向目标用于发送审核消息
async function send_comic_review_msg(user_id, work_id, work_status) {
  const msg = {
    target_user_id: user_id,
    content: {
      work_id: work_id,
      work_status: work_status,
      work_type: "comic",
      msg_type: "comic_review",
      msg: work_status == 1 ? "作品审核通过" : "作品审核未通过",
    },
    type: "review_msg",
  };

  try {
    // 直接发送对象，无需手动序列化
    if (store.$state.ws?.readyState === WebSocket.OPEN) {
      store.$state.ws.send(JSON.stringify(msg));
      console.log("审核消息发送成功", msg);
    } else {
      console.error("WebSocket 连接未就绪");
      // 可选：重连机制或消息队列
    }
  } catch (error) {
    console.error("消息发送失败:", error);
  }
}

let scroll_tag = ref(null)
const obsserver = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting && total.value > work_list.value.length) {
    loading.value = true
    offset.value += limit.value
    await get_comic_list()
    loading.value = false
  }
}, {
  root: null,
  rootMargin: '400px',
  threshold: 0
},100)
onMounted(async () => {
  obsserver.observe(scroll_tag.value)
})
onUnmounted(() => {
  obsserver.disconnect()
})

</script>

<style scoped>
.comic_control {
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

.comic_cover {
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

.comic_cover img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 15px;
}

.comic_info {
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

.show_comic_content {
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

.comic_img {
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

.comic_img img {
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

.show_comic_content_btn {
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

.show_comic_content_btn:hover {
  background-color: rgb(0, 150, 250);
  opacity: 0.8;
  color: white;
  transition: all 0.2s ease-in-out;
  transform: scale(1.02);
  transform: translateY(-1px);
}
</style>