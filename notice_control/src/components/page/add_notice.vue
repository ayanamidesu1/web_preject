<template>
  <div class="add_notice">
    <div class="content">
      <div class="title">
        <span>新增公告</span>
      </div>
      <div class="add_item">
        <div class="notice_title">
          公告标题：<input type="text" v-model="title">
        </div>
        <div class="notice_content">
          公告内容：<textarea v-model="content"></textarea>
        </div>
        <div class="publish_time">
          发布时间：<input type="text" v-model="publish_time" readonly>
        </div>
        <div class="expire_time">
          过期时间：<input type="date" v-model="expire_time">
        </div>
        <div class="notice_status">
          公告状态：
          <select v-model="status">
            <option value="draft">草稿</option>
            <option value="publish">发布</option>
            <option value="expire">过期</option>
          </select>
        </div>
        <div class="attachment">
          附件连接：<input type="text" v-model="attachment">
        </div>
        <div class="is_important">
          是否重要：
          <select v-model="is_important">
            <option value="1">是</option>
            <option value="0">否</option>
          </select>
        </div>
        <div class="submit" @click="add_notice()">
          <span>提交</span>
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
  name: 'add_notice',
}
</script>

<script setup>
let now_time = ref(new Date().toLocaleString());
let title = ref('');
let content = ref('');
let author_id = ref('');
let author_name = ref('');
let create_time = ref(now_time.value);
let publish_time = ref(new Date().toISOString().split('T')[0]);
let expire_time = ref('');
let status = ref('draft');
let attachment = ref('');
let is_important = ref('0');
// eslint-disable-next-line no-unused-vars
let la_modifiy_time = ref('');
let token = ref(cookies.get_cookie('token'));
let type = ref('add');

async function add_notice() {
  try {
    const res = await fetch('https://www.sunyuanling.com/api/notice_control/NoticeOperations/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: title.value,
        content: content.value,
        author_id: author_id.value,
        author_name: author_name.value,
        create_time: create_time.value,
        publish_time: publish_time.value,
        expire_time:expire_time.value,
        category:'默认',
        attachment_url:attachment.value,
        status:status.value,
        is_important:is_important.value,
        operate_type: type.value,
        token:localStorage.getItem('token').value,
      })
    })
    if (res.ok) {
      const data = await res.json();
      if (data.status == 'success') {
        alert('添加成功');
        console.log(data.message);
      }
      else {
        alert('添加失败');
        console.log(data.message);
      }
    }
    else {
      console.log('网络错误');
    }
  }
  catch (error) {
    console.log(error);
  }
}

onMounted(() => {
  publish_time.value = new Date().toISOString().split('T')[0];
});
</script>

<style scoped>
.add_notice {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.content {
  width: 600px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.add_item {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.notice_title,
.notice_content,
.publish_time,
.expire_time,
.notice_status,
.attachment,
.is_important {
  display: flex;
  flex-direction: column;
}

.notice_title input,
.notice_content textarea,
.publish_time input,
.expire_time input,
.notice_status select,
.attachment input,
.is_important select {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-top: 5px;
}

.notice_content textarea {
  height: 100px;
  resize: vertical;
}

.submit {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  width: auto;
  height: auto;
  padding: 10px 20px;
  background-color: rgba(0, 150, 250, 1);
  border-radius: 10px;
  color: rgba(255, 255, 255, 1);
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: bold;
}

.submit:hover {
  background-color: rgba(0, 100, 200, 1);
  transition: all 0.3s;
}
</style>
