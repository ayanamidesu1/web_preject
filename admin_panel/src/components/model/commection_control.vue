<template>
  <div class="comment_page">
    <h1>评论管理</h1>
    <div class="content" v-if="comment_list.length > 0">
      <div class="search_box">
        搜索评论：
        <span>作品ID：</span>
        <input type="text" placeholder="作品ID" v-model="work_id">
        <span>作品类型：</span>
        <select v-model="work_type">
          <option value="all">全部</option>
          <option value="ill">插画</option>
          <option value="comic">漫画</option>
          <option value="novel">小说</option>
        </select>
        <span>评论ID：</span>
        <input type="text" placeholder="评论ID" v-model="comment_id">
        <span>发送者ID：</span>
        <input type="text" placeholder="发送者ID" v-model="send_userid">
        <span>被回复者ID：</span>
        <input type="text" placeholder="被回复者ID" v-model="main_userid">
        <div class="search_btn">
          <span @click="search_comment_list()">搜索</span>
          <span @click="delete_comment_f()">批量删除</span>
        </div>
      </div>
      <div class="item_list">
        <div class="item" v-for="(item, index) in comment_list" :key="index">
          <div class="user_info">
            <div class="user_avatar">
              <img :src="getAvatarUrl(item.user_avatar)" alt="用户头像" />
            </div>
            <div class="user_name">
              <span>{{ item.username }}</span>
            </div>
            <div class="comment_id">
              <span>评论ID：{{ item.comment_id }}</span>
            </div>
          </div>
          <div class="work_info">
            <span>作品名称：</span>
            <span>{{ item.work_type == 'ill' ? item.work_data.name : item.work_data.work_name }}</span>
            <span>作品类型：</span>
            <span>{{ item.work_type == 'ill' ? '插画' : item.work_type == 'comic' ? '漫画' : '小说' }}</span>
          </div>
          <div class="comment_content">
            <span>{{ item.content }}</span>
          </div>
          <div class="edit_box">
            <div class="delete_btn">
              <span>删除评论</span>
              <div class="multiple_choice">
                <input type="checkbox" :value="item.comment_id" v-model="multiple_choice">
              </div>
            </div>
            <div class="edit_box">
              <textarea placeholder="请输入修改后的评论内容" v-model="edit_comment_text"></textarea>
              <div class="edit_btn">
                <span @click=" update_comment_f(item.comment_id)">确认修改</span>
              </div>
            </div>
          </div>
        </div>
        <div class="check_point" ref="check_point" style="width:1px;height:1px;display:block;"></div>
        <div class="loding" v-if="is_loding">
          <span>加载中……</span>
        </div>
      </div>
    </div>
    <div v-else>
      <p>暂无评论</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { get_comment_list } from './js/get_work_list'
import { search_comment } from './js/search_work';
import { delete_comment } from './js/update_work';
import { update_comment } from './js/update_work';

const comment_list = ref([])
const limit = ref(5)
const offset = ref(0)
const total = ref(0)
const check_point = ref(null)
const is_loding = ref(false)
let edit_comment_text = ref('')
let multiple_choice = ref([])

let work_id = ref('')
let work_type = ref('')
let comment_id = ref('')
let send_userid = ref('')
let main_userid = ref('')

async function search_comment_list() {
  const response = await search_comment(999, 0, comment_id.value, work_id.value, work_type.value, send_userid.value, main_userid.value)
  console.log(response.data.rows)
  comment_list.value = await response.data.rows
}

//批量删除评论
async function delete_comment_f() {
  let res = await delete_comment(multiple_choice.value)
  if (res.status == 'success') {
    alert('删除成功')
    await get_comment_info_list()
  }
  else {
    alert(res.message)
  }
}

//更新评论内容
async function update_comment_f(comment_id) {
  let res = await update_comment(comment_id, edit_comment_text.value)
  if (res.status == 'success') {
    alert('更新成功')
    await get_comment_info_list()
  }
  else {
    alert(res.message)
  }
}

// IntersectionObserver 回调函数
const observer = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting && comment_list.value.length < total.value) {
    is_loding.value = true
    offset.value += limit.value
    await get_comment_info_list()
    is_loding.value = false
  }
}, {
  root: null,
  rootMargin: '400px',
  threshold: 0
})

const getAvatarUrl = (avatar) => `https://www.sunyuanling.com/server/static/image/avatar_thumbnail/${avatar}`

const getWorkName = (item) => {
  if (item.work_type === 'ill') {
    return item.work_data.name
  }
  return item.work_data.work_name
}

const getWorkType = (workType) => {
  return workType === 'ill' ? '插画' : workType === 'comic' ? '漫画' : '小说'
}

// 获取评论列表
async function get_comment_info_list() {
  const response = await get_comment_list(limit.value, offset.value)
  if (response && response.data) {
    comment_list.value = [...comment_list.value, ...response.data.comment_list]
    total.value = response.data.total
  }
}

onMounted(async () => {
  await get_comment_info_list()
  await nextTick()  // 确保 DOM 元素已经渲染
  if (check_point.value) {
    observer.observe(check_point.value)
  }
})

onUnmounted(() => {
  observer.disconnect()
})

</script>

<style scoped>
.comment_page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background-color: #f9f9f9;
}

h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.search_box {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
  width: 90%;
}

.search_input {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.search_input input {
  flex-grow: 1;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search_btn {
  width: auto;
  display: flex;
  flex-direction: row;
  gap: 10px;
  align-items: center;
  justify-content: flex-end;
}

.search_btn span {
  background-color: #007bff;
  color: white;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.search_btn span:hover {
  background-color: #0056b3;
}

.item_list {
  width: 85%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
}

.user_info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user_avatar img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.user_name {
  font-size: 16px;
  font-weight: bold;
}

.comment_id {
  font-size: 12px;
  color: #666;
  margin-left: auto;
}

.work_info {
  margin-top: 10px;
  font-size: 14px;
  color: #333;
  display: flex;
  gap: 10px;
}

.comment_content {
  margin-top: 10px;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
}

.edit_box {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

textarea {
  width: auto;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: vertical;
}

.delete_btn {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.edit_btn span,
.delete_btn span {
  background-color: #28a745;
  color: white;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.edit_btn span:hover,
.delete_btn span:hover {
  background-color: #218838;
}

.loding {
  text-align: center;
  font-size: 14px;
  color: #666;
}

@media (max-width: 768px) {
  .search_box {
    flex-direction: column;
  }

  .user_info {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
