<template>
  <div class="novel_control">
    <h1>小说审核</h1>
    <div class="search_box">
      <span>搜索：</span>
      <input type="text" placeholder="请输入小说名/ID" v-model="novel_work_search_key">
      <div class="search_btn"><span>搜索</span></div>
      <div class="novel_work_status">
        <span>小说状态：</span>
        <select v-model="novel_work_search_status">
          <option value="all">全部</option>
          <option value="1">已上架</option>
          <option value="0">未上架</option>
          <option value="2">未审核</option>
        </select>
      </div>
    </div>
    <div class="content">
      <div class="item" v-for="(item, index) in novel_work_list" :key="index">
        <div class="novel_cover">
          <img :src="'https://www.sunyuanling.com/server/static/image/novel/thumbnail/' + item.work_cover" alt="小说作品封面">
          <div class="show_novel_work_content" @click="show_novel_content_page(item.work_id)">
            <span>查看小说详情</span>
          </div>
        </div>
        <div class="novel_work_info">
          <div class="info_item">
            <span>名称：</span>
            <span>{{ item.work_name }}</span>
          </div>
          <div class="info_item">
            <span>作者：</span>
            <span>{{ item.username }}</span>
          </div>
          <div class="info_item">
            <span>简介：</span>
            <span>{{ item.brief_introduction }}</span>
          </div>
          <div class="info_item">
            <span>作品类型：</span>
            <span>{{ item.category }}</span>
          </div>
          <div class="info_item">
            <span>年龄分级：</span>
            <span>{{ item.age_classification }}</span>
          </div>
          <div class="info_item">
            <span>作品状态：</span>
            <span>{{ item.work_status }}</span>
          </div>
          <div class="info_item">
            <span>作品字数：</span>
            <span>{{ item.novel_word_count }}</span>
          </div>
          <div class="info_item">
            <span>作品上架状态：</span>
            <span>{{ item.work_approved == 1 ? '已上架' : item.work_approved == 0 ? '未上架' : '未审核' }}</span>
          </div>
          <div class="novel_work_control">
            <span class="novel_work_control_btn" @click="update_work_status(1, item.work_id)">上架</span>
            <span class="novel_work_control_btn" @click="update_work_status(0, item.work_id)">下架</span>
          </div>
        </div>
      </div>
      <div class="check_points" ref="check_points" style="display: none; width:1px;height:1px;"></div>
      <div class="loding" v-if="is_loding">
        加载中……
      </div>
    </div>
  </div>
  <div class="show_novel_content_page" v-if="show_novel_content_page_show">
    <div class="close" @click="show_novel_content_page_show = false">
      <div class="close_btn">
        <img src="https://www.sunyuanling.com/assets/close.svg" alt="退出">
      </div>
    </div>
    <div class="novel_content_page" v-if="content_info_list">
      <div class="novel_info">
        <div class="content_novel_cover">
          <img :src="'https://www.sunyuanling.com/server/static/image/novel/thumbnail/' + title_list[0].work_cover" alt="小说封面">
        </div>

        <div class="novel_info_item_box">
          <div class="info_item_box">
            <span>作品名称：{{ title_list[0].work_name }}</span>
            <span>作品类型：{{ title_list[0].is_series }}</span>
            <span>作者：{{ title_list[0].username }}</span>
            <span>作品字数：{{ content_info_list.total_word_count }}</span>
          </div>
        </div>
      </div>
      <div class="novel_info_item_control">
        <div class="novel_info_item_control_search">
          <span>搜索：</span>
          <input type="text" placeholder="请输入章节名/ID" v-model="chapter_search_key">
          <span style="width:auto;height:auto;padding:5px 10px;background-color:rgba(0,150,250);
          color:white;border-radius:5px;cursor:pointer;" @click="search_chapter">搜索</span>
        </div>
        <div class="chapter_status">
          <span>章节审核状态：</span>
          <select v-model="selectedStatus">
            <option value="all">全部</option>
            <option value="1">通过</option>
            <option value="0">未通过</option>
            <option value="2">未审核</option>
          </select>
        </div>
        <div class="novel_info_item_control_all">
          <span>批量操作</span>
          <select v-model="selectAll">
            <option value="all">全选</option>
            <option value="all_none">取消全选</option>
          </select>
        </div>
        <div class="novel_info_item_control_btn">
          <span @click="update_novel_chapter_status_list(1)">批量通过</span>
          <span @click="update_novel_chapter_status_list(0)">批量未通过</span>
        </div>
      </div>
      <div class="title_list">
        <div class="title_item" v-for="(item, index) in filteredTitles" :key="index">
          <span>章节名称：&nbsp;{{ item.title }}</span>
          <span>章节审核状态：&nbsp;
            <span
              :class="item.chapter_approved == 1 ? 'chapter_is_pass' : (item.chapter_approved == 0 ? 'chapter_not_pass' : 'chapter_none_pass')">
              {{ item.chapter_approved == 1 ? '通过' : item.chapter_approved == 0 ? '未通过' : '未审核' }}</span>
          </span>
          <div class="read_content" @click="set_red_box_content(item.content)">
            阅读章节
          </div>
          选择该节：<input type="checkbox" v-model="choose_chapter_list" :value="item">
        </div>
        <div class="read_box" v-if="read_box_show">
          <div class="close" @click="read_box_show = false" style="right: 50px;top:50px;">
            <img src="https://www.sunyuanling.com/assets/close.svg" alt="关闭">
          </div>
          <span v-html="read_box_content"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { get_novel_work_list, get_novel_work_content_list } from './js/get_work_list'
import { ref, onMounted, watch, onUnmounted, computed } from 'vue'
import { search_novel_work } from './js/search_work'
import { update_novel_work_status, update_novel_chapter_status } from './js/update_work'

const novel_info_list = ref([])
const novel_work_list = ref([])
const limit = ref(10)
const offset = ref(0)
const total = ref(0)
const show_novel_content_page_show = ref(false)
const content_info_list = ref()
const title_list = ref([])
const read_box_content = ref(`测试{\n}测试`)
const read_box_show = ref(false)
const choose_chapter_list = ref([])
const selectedStatus = ref('all')  // 筛选状态
const selectAll = ref('all_none')  // 全选状态
const chapter_search_key = ref()
let novel_work_search_key = ref()
let novel_work_search_status = ref('all')
let check_points = ref(null)
let is_loding=ref(false)

//滚动加载实现
const observer =new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting && total.value >= novel_info_list.value.length) {
    is_loding.value=true
    offset.value += limit.value
    await get_novel_work_list(limit.value, offset.value)
    is_loding.value=false
  }
},{
  root:null,
  rootMargin:'400px',
  threshold: 0
},100)

//监听多选状态
watch(choose_chapter_list, (newVal) => {
  console.log(newVal)
})

//批量更新章节状态
async function update_novel_chapter_status_list(status) {
  let work_id = choose_chapter_list.value[0].belong_to_series_id
  let chapter_id = choose_chapter_list.value.map(item => item.id)
  //确定数组长度大于等于1
  if (chapter_id.length >= 1) {
    let res = await update_novel_chapter_status(status, work_id, chapter_id)
    if (res.status == 'success') {
      alert('更新成功')
    }
    else {
      alert(res.message)
    }
  }
  else {
    console.log('请选择章节')
  }

}

// 过滤章节列表
const filteredTitles = computed(() => {
  if (selectedStatus.value === 'all') {
    return title_list.value
  }
  return title_list.value.filter(item => item.chapter_approved == selectedStatus.value)
})

// 全选/取消全选功能
watch(selectAll, (newVal) => {
  if (newVal === 'all') {
    choose_chapter_list.value = [...filteredTitles.value]
  } else {
    choose_chapter_list.value = []
  }
})

//前端搜索实现
watch(chapter_search_key, (newVal) => {
  if (newVal) {
    title_list.value = title_list.value.filter(item => item.title.includes(newVal) || item.id.toString().includes(newVal))
  } else {
    title_list.value = content_info_list.value.work_list
  }
})

//搜索小说作品实现
watch([novel_work_search_key, novel_work_search_status], async (newVal) => {
  console.log(newVal)
  await search_novel_work_list()
  if (novel_work_search_key.value == '' || novel_work_search_key.value == null && novel_work_search_status.value == 'all') {
    await get_novel_work()
  }
})

//设置阅读内容
function set_red_box_content(item) {
  read_box_content.value = item.replace(/\\n/g, '<br>')
  read_box_show.value = true
}

//获取小说作品列表
async function get_novel_work() {
  const res = await get_novel_work_list(limit.value, offset.value)
  if (res.status == 'success') {
    novel_info_list.value = res.data
    total.value = novel_info_list.value.total
    console.log(novel_info_list.value)
    novel_work_list.value = [...novel_work_list.value, ...novel_info_list.value.work_list]
  }
  else {
    console.log(res.message)
  }
}

//搜索小说作品
async function search_novel_work_list() {
  const res = await search_novel_work(novel_work_search_key.value, novel_work_search_status.value, 999, 0)
  if (res.status == 'success') {
    novel_info_list.value = res.data
    total.value = novel_info_list.value.total
    console.log(novel_info_list.value)
    novel_work_list.value = novel_info_list.value.work_list
  }
  else {
    console.log(res.message)
  }
}

//获取指定ID的小说章节列表
async function get_title_list(work_id) {
  let res = await get_novel_work_content_list(work_id, 9999999, 0)
  if (res.status == 'success') {
    content_info_list.value = res.data
    console.log(content_info_list.value)
    title_list.value = content_info_list.value.work_list
  }
}

//更新小说状态
async function update_work_status(status, work_id) {
  let res = await update_novel_work_status(status, work_id)
  if (res.status == 'success') {
    await get_novel_work()
    alert('更新成功')
  }
  else {
    alert(res.message)
  }
}

async function show_novel_content_page(work_id) {
  show_novel_content_page_show.value = true
  await get_title_list(work_id)
}

onMounted(async () => {
  await get_novel_work()
  observer.observe(check_points.value)
})
onUnmounted(() => {
  observer.disconnect()
})

</script>

<style scoped>
.novel_control {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search_box {
  width: 100%;
  height: 80px;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 20px;
}

.content {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.item {
  width: 90%;
  height: auto;
  display: flex;
  flex-direction: row;
  max-height: 350px;
  background-color: rgb(190, 190, 190);
  border-radius: 10px;
  padding: 10px;
}

.novel_cover {
  width: 25%;
  max-width: 30%;
  margin-right: 10px;
  height: auto;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.novel_cover img {
  width: 100%;
  height: auto;
  max-height: 80%;
  object-fit: cover;
  border-radius: 10px;
}

.show_novel_work_content {
  width: 75%;
  height: auto;
  display: flex;
  background-color: rgb(0, 150, 250);
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  padding: 5px 10px;
  border-radius: 10px;
  font-weight: bold;
}

.show_novel_work_content:hover {
  cursor: pointer;
  opacity: 0.8;
  transition: all 0.2s;
  transform: scale(1.03);
  transform: translateY(-1px);
}

.novel_work_info {
  width: auto;
  height: auto;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 10px;
}

.info_item {
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: 10px;
  word-wrap: break-word;
}

.novel_work_control {
  width: 100%;
  height: auto;
  display: flex;
  gap: 20px;
}

.novel_work_control_btn {
  width: auto;
  height: auto;
  padding: 5px 15px;
  cursor: pointer;
  background-color: rgb(241, 150, 89);
  border-radius: 10px;
  color: white;
  font-weight: bold;
}

.novel_work_control_btn:hover {
  opacity: 0.8;
  transition: all 0.2s;
  transform: scale(1.03);
  transform: translateY(-1px);
}

.novel_work_control_btn:active {
  opacity: 0.6;
  transition: all 0.2s;
  transform: scale(1.01);
  transform: translateY(1px);
}

.novel_work_control_btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transition: all 0.2s;
  transform: scale(1);
}

.show_novel_content_page {
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  z-index: 5;
  gap: 20px;
  justify-content: center;
  align-items: center;
}

.close {
  width: 35px;
  height: 35px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 6;
  position: fixed;
  top: 30px;
  right: 30px;
  background-color: rgba(211, 211, 211, 1);
  border-radius: 15px;
}

.close:hover {
  cursor: pointer;
  opacity: 0.8;
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  transition: all 0.2s;
  transform: scale(1.05);
  transform: translateY(-1px);
}

.close img {
  width: 25px;
  height: 25px;
  object-fit: cover;
}

.novel_content_page {
  width: 90%;
  height: 90%;
  max-height: 90%;
  overflow-y: auto;
  display: flex;
  background-color: rgba(233, 233, 233, 1);
  flex-direction: column;
}

.novel_info {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  gap: 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}

.info_item_box {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
}

.read_box {
  width: 100vw;
  height: 98vh;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  justify-content: center;
  align-items: center;
  z-index: 7;
  background-color: rgba(0, 0, 0, 0.5);
  overflow-y: auto;
  max-height: 100vh;
}

.read_box span {
  background-color: white;
  width: 80%;
  height: auto;
  margin: auto;
  max-height: 80%;
  overflow-y: auto;
}

.novel_info_item_control {
  width: 100%;
  height: auto;
  max-height: 150px;
  display: flex;
  gap: 10px;
  margin-top: 5px;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.novel_info_item_control_search {
  width: auto;
  display: flex;
  gap: 10px;
  align-items: center;
}

.novel_info_item_control_search input {
  width: auto;
  height: 25px;
  border-radius: 5px;
  background-color: rgba(0, 150, 250, 0.2);
  border: 1px solid rgba(211, 211, 211, 1);
}

.novel_info_item_control_btn {
  width: auto;
  display: flex;
  gap: 10px;
}

.novel_info_item_control_btn span {
  width: auto;
  height: auto;
  padding: 5px 10px;
  background-color: rgba(0, 150, 250);
  color: white;
  border-radius: 10px;
  cursor: pointer;
}

.title_item {
  width: 100%;
  height: auto;
  display: flex;
  gap: 10px;
  justify-content: flex-start;
  align-items: center;
}

.read_content {
  width: auto;
  height: auto;
  padding: 5px 10px;
  background-color: rgba(0, 150, 250, 0.2);
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.read_content:hover {
  opacity: 0.8;
  transition: all 0.2s;
  transform: scale(1.03);
  transform: translateY(-1px);
}

.title_list {
  display: flex;
  gap: 10px;
  flex-direction: column;
}

.chapter_is_pass {
  color: green;
}

.chapter_not_pass {
  color: red;
}

.chapter_none_pass {
  color: yellow;
}
</style>
