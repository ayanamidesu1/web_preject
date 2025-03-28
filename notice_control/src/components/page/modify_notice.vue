<template>
  <div class="modify_notice">
    <div class="content">
      <div class="title">修改公告</div>
      <div class="search_box">
        <div class="search_input">
          <input placeholder="搜索公告" v-model="searchQuery" @input="filterNotices">
          <img src="https://www.sunyuanling.com/assets/search.svg" class="icon">
        </div>
      </div>
      <div class="item_box">
        <div class="item" v-for="(item, index) in notice_info" :key="index">
          <div class="notice_title">
            标题：<input v-model="item.title" />
          </div>
          <div class="notice_content">
            内容：<textarea v-model="item.content"></textarea>
          </div>
          <div class="notice_info">
            <span>用户名：{{ item.author_name }}</span>
            发布时间<input type="datetime-local" v-model="item.publish_time" />
            截止时间<input type="datetime-local" v-model="item.expire_time" />
            公告状态
            <select v-model="item.status" style="width:90%;">
              <option value="draft">草稿</option>
              <option value="published">发布</option>
              <option value="expired">过期</option>
            </select>
            重要级别<input v-model="item.priority" />
            公告类别<input v-model="item.category" />
          </div>
          <div class="attachment_url">
            附件地址：<input v-model="item.attachment_url" />
          </div>
          <div class="is_important">
            是否重要：<input type="checkbox" v-model="item.is_important" :checked="item.is_important==1"  />
          </div>
          <div class="edit_btn">
            <div class="sure" @click="updateNotice(item)">
              <span>确定</span>
              <img src="https://www.sunyuanling.com/assets/correct.svg" class="icon">
            </div>
            <div class="close" @click="cancelEdit(item)">
              <span>取消</span>
              <img src="https://www.sunyuanling.com/assets/close.svg" class="icon">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import * as cookies from '../../../../model/cookies.js';

const token = cookies.get_cookie('token');
let notice_info = ref([]);
const searchQuery = ref('');
const originalNoticeInfo = ref([]);

const get_notice_info = async () => {
  try {
    const res = await fetch('https://www.sunyuanling.com/api/notice_control/NoticeOperations/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        operate_type: 'search',
        token: localStorage.getItem('token'),
      }),
    });

    if (res.ok) {
      const data = await res.json();
      if (data.status === 'success') {
        notice_info.value = data.data;
        originalNoticeInfo.value = JSON.parse(JSON.stringify(data.data));
      } else {
        console.log(data.message);
      }
    } else {
      console.log('请求失败');
    }
  } catch (err) {
    console.log(err);
  }
};

const updateNotice = async (item) => {
  try {
    const res = await fetch('https://www.sunyuanling.com/api/notice_control/NoticeOperations/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        operate_type: 'update',
        token: localStorage.getItem('token'),
        id: item.id,
        title: item.title,
        content: item.content,
        publish_time: item.publish_time,
        expire_time: item.expire_time,
        category: item.category,
        attachment_url: item.attachment_url,
        status: item.status,
        priority: item.priority,
        is_important: item.is_important,
      }),
    });

    if (res.ok) {
      const data = await res.json();
      if (data.status === 'success') {
        alert('公告更新成功');
      } else {
        alert('公告更新失败');
      }
    } else {
      alert('请求失败');
    }
  } catch (err) {
    console.log(err);
  }
};

const cancelEdit = (item) => {
  const original = originalNoticeInfo.value.find((o) => o.id === item.id);
  Object.assign(item, original);
};

const filterNotices = () => {
  notice_info.value = originalNoticeInfo.value.filter((item) =>
    item.title.includes(searchQuery.value)
  );
};

// eslint-disable-next-line no-unused-vars
const toggleImportance = (item) => {
  if(item.is_important==0)
{
  item.is_important = false;
}
else
{
  item.is_important = true;
}
};

onMounted(() => {
  get_notice_info();
});
</script>

<style scoped>
.modify_notice {
  padding: 20px;
  font-family: Arial, sans-serif;
  width: 100%;
}

.content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.search_box {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.search_input {
  display: flex;
  align-items: center;
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
}

.search_input input {
  border: none;
  background: none;
  outline: none;
  width: 90%;
  padding: 5px;
}

.icon {
  width: 20px;
  height: 20px;
}

.item_box {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.item {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.notice_title input,
.notice_content textarea,
.notice_info input,
.attachment_url input {
  width: 90%;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  margin-top: 5px;
  margin-bottom: 15px;
}

.notice_info {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.notice_content textarea {
  resize: none;
  height: 100px;
}

.edit_btn {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.edit_btn div {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.edit_btn img {
  margin-left: 5px;
}
</style>
