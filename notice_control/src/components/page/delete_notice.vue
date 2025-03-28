<template>
  <div class="delete_notice">
    <div class="content">
      <div class="title">
        <span>删除公告</span>
      </div>
      <div class="delete_item">
        <div class="item" v-for="(item, index) in notice_info" :key="index">
          <div class="notice_title">
            <span>{{ item.title }}</span>
          </div>
          <div class="notice_content">
            <span>{{ item.content }}</span>
            <div class="date_info">
              <span>发布时间：{{ item.publish_time }}</span>
              <span>过期时间：{{ item.expire_time }}</span>
              <span>最后修改时间：{{ item.last_modified_time }}</span>
              <span>状态：{{ item.status }}</span>
            </div>
            <div class="notice_info">
              <span>优先级：{{ item.priority }}</span>
              <span>公告类别：{{ item.category }}</span>
              <span>附件地址：{{ item.attachment_url }}</span>
              <span>是否为重要公告：{{ item.is_important }}</span>
            </div>
          </div>
          <div class="delete_btn" @click="delete_notice(item.id)">
            <img class="icon" src="https://www.sunyuanling.com/assets/close.svg">
          </div>
        </div>
        <div class="page">
          <div class="up_page" @click="prevPage">
            <img class="icon" src="https://www.sunyuanling.com/assets/left.svg">
          </div>
          <div class="page_num">{{ page }}</div>
          <div class="all_page">/{{ totalPages }}</div>
          <div class="down_page" @click="nextPage">
            <img class="icon" src="https://www.sunyuanling.com/assets/right.svg">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import * as cookies from '../../../../model/cookies.js';

let token = cookies.get_cookie('token');
let page = ref(1);
let per_page = ref(10);
let notice_info = ref([]);
let total_count = ref(0);
let totalPages = ref(0);

async function get_notice_info() {
  try {
    const res = await fetch('https://www.sunyuanling.com/api/notice_control/NoticeOperations/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        operate_type: 'search',
        token: localStorage.getItem('token'),
        page: page.value,
        per_page: per_page.value
      })
    });
    if (res.ok) {
      const data = await res.json();
      if (data.status == 'success') {
        notice_info.value = data.data;
        total_count.value = data.total_count;
        page.value = data.page;
        per_page.value = data.per_page;
        totalPages.value = Math.ceil(total_count.value / per_page.value);
      }
    }
  } catch (err) {
    console.log(err);
  }
}

async function delete_notice(id) {
  //确定操作弹窗
  if (!confirm('确定删除该公告吗？')) {
    return;
  }
  try {
    const res = await fetch('https://www.sunyuanling.com/api/notice_control/NoticeOperations/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        operate_type: 'delete',
        id: id,
        token: localStorage.getItem('token')
      })
    });
    if (res.ok) {
      const data = await res.json();
      if (data.status == 'success') {
        alert('删除成功');
        await get_notice_info();
      } else {
        alert('删除失败');
      }
    }
  } catch (err) {
    console.log(err);
  }
}

function prevPage() {
  if (page.value > 1) {
    page.value -= 1;
    get_notice_info();
  }
}

function nextPage() {
  if (page.value < totalPages.value) {
    page.value += 1;
    get_notice_info();
  }
}

onMounted(async () => {
  await get_notice_info();
});
</script>

<style scoped>
.delete_notice {
  display: flex;
  width: 100%;
  flex: 1;
  flex-direction: column;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 5px;
}

.content {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 800px;
  margin: auto;
}

.title span {
  font-size: 24px;
  font-weight: bold;
}

.delete_item {
  margin-top: 20px;
  display: flex;
  width: 100%;
  flex-direction: column;
}

.item {
  background: #fff;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-around;
  flex-direction: column;
  width: 100%;
  position: relative;
}

.notice_title span {
  font-size: 18px;
  font-weight: bold;
}

.notice_content {
  margin-top: 10px;
}

.date_info,
.notice_info {
  margin-top: 10px;
  margin-bottom: 30px;
}

.date_info span,
.notice_info span {
  display: block;
  margin-bottom: 5px;
}

.delete_btn {
  display: inline-block;
  margin-top: 10px;
  cursor: pointer;
  position: absolute;
  bottom: 10px;
  right: 10px;
}

.page {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.page .icon {
  width: 25px;
  height: 25px;
  cursor: pointer;
}

.page_num,
.all_page {
  margin: 0 10px;
}

.icon {
  width: 25px;
  height: 25px;
  object-fit: cover;
}
</style>
