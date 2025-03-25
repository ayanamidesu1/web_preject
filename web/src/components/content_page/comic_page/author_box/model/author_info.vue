<template>
  <div class="author_info_page" v-if="props.author_id && author_info">
    <div class="content">
      <div class="author_info" @click="jump_to_other_user_center(author_info.userid, author_info)">
        <div class="author_avatar">
          <img :src="'https://www.sunyuanling.com/image/avatar_thumbnail/' + author_info.user_avatar">
        </div>
        <div class="author_name">
          <span>{{ author_info.username }}</span>
        </div>
        <div class="author_follow" :class="follow_status === '已关注' ? 'off_follow' : 'on_follow'" @click="follow_author">
          <div class="follow_btn">
            <span>{{ follow_status }}</span>
          </div>
        </div>
      </div>
      
      <div class="others_work">
        <div class="others_work_title">其他作品</div>
        <scroll_box :msg_list="author_other_work_list_path" @chose_item="get_choose_item"></scroll_box>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, onMounted, defineEmits, watch } from 'vue';
import * as cookies from "@/assets/js/cookies.js";
import scroll_box from './scroll_box_bottom.vue';
import { useStore } from 'vuex';

const store = useStore();
const props = defineProps({
  author_id: {
    type: String,
    default: '10086'
  }
});

const author_info = ref(null);
const follow_info = ref([]);
const follow_status = ref('关注');
const author_other_work_list_path = ref([]);
const token = cookies.get_cookie("token");
const emit = defineEmits(['chose_item']);

watch(() => props.author_id, async () => {
  await fetchAuthorData();
});

async function fetchData(url, data) {
  try {
    const response = await fetch(url, {
      method: 'post',
      headers: { 'Content-Type': 'application/json','Authorization': 'Bearer ' + localStorage.getItem('token') },
      body: JSON.stringify(data),
    });
    if (response.ok) {
      return await response.json();
    } else {
      console.error(`HTTP error: ${response.status}`);
      return { status: 'error', message: 'Request failed' };
    }
  } catch (error) {
    console.error(`Fetch error: ${error}`);
    return { status: 'error', message: 'Fetch error' };
  }
}

async function fetchAuthorData() {
  const [authorInfo, followInfo, authorWork] = await Promise.all([
    fetchData('https://www.sunyuanling.com/api/GetUserInfo/GetAllUserInfo/', { userid: props.author_id }),
    fetchData('https://www.sunyuanling.com/api/GetUserInfo/GetUserFollow/', { token: token }),
    fetchData('https://www.sunyuanling.com/api/GetUserInfo/GetUserWorkList/', { userid: props.author_id }),
  ]);

  if (authorInfo.status === 'success') {
    author_info.value = authorInfo.data[0];
  } else {
    console.error(authorInfo.message);
  }

  if (followInfo.status === 'success') {
    follow_info.value = followInfo.data;
    is_follow();
  } else {
    console.error(followInfo.message);
  }

  if (authorWork.status === 'success') {
    console.log(authorWork.data.comic)
    author_other_work_list_path.value = authorWork.data.comic.map(item => ({
      item_path: 'https://www.sunyuanling.com/image/comic/thumbnail/' + item.content_file_list.split(/[,，]/)[0],
      work_id: item.id
    }));
    console.log(author_other_work_list_path.value)
  } else {
    console.error(authorWork.message);
  }
}

function is_follow() {
  const isFollowing = follow_info.value.some(item => item.follow_user_id === props.author_id);
  follow_status.value = isFollowing ? '已关注' : '关注';
}

async function follow_author() {
  const data = await fetchData('https://www.sunyuanling.com/api/GetUserInfo/UserAddFollow/', {
    token: token,
    target_id: author_info.value.userid,
    target_username: author_info.value.username
  });
  if (data.status === 'success') {
    follow_status.value = follow_status.value === '已关注' ? '关注' : '已关注';
    alert(data.message);
  } else {
    alert(data.message);
  }
}

function get_choose_item(item) {
  emit('chose_item', { work_id: item.work_id });
}

function jump_to_other_user_center(userid, item) {
  store.commit('SET_OTHER_USERID', userid);
  store.commit('SET_SINGLE_PAGE_STATUS', { key: 'other_user_center_page', value: true });
}

onMounted(() => {
  fetchAuthorData();
});
</script>

<style scoped>
.author_info_page {
  display: flex;
  width: 100%;
  height: auto;
  flex-direction: column;
}

.content {
  display: flex;
  width: 100%;
  height: auto;
  flex-direction: column;
}

.author_info {
  width: 100%;
  height: 50px;
  padding: 5px 0px;
  display: flex;
  flex-direction: row;
  gap: 10px;
  cursor: pointer;
}

.author_avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  overflow: hidden;
}

.author_avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.author_name {
  width: auto;
  height: 50px;
  display: flex;
  align-items: center;
  font-size: 1em;
}

.author_follow {
  width: 70%;
  height: auto;
  padding: 5px 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  color: rgba(255, 255, 255, 1);
  margin-top: 10px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  max-width: 100px;
}

.author_follow:hover {
  transition: all 0.3 ease-in-out;
  opacity: 0.8;
}

.on_follow {
  background-color: rgba(0, 150, 250, 0.8);
}

.off_follow {
  background-color: rgba(133, 133, 133, 1);
}

.others_work {
  width: 100%;
  margin-right: 5px;
  padding: 5px;
  height: auto;
}
</style>