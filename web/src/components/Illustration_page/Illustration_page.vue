<template>
  <div class="illustration_page">
    <scroll_box_1 :msg_type="'tags'" :msg_list="tags_list.data" v-if="tags_list.data.length>0" style="max-height:100px;"></scroll_box_1>
    <h3>用户关注的作品</h3>
    <scroll_box v-if="follow_illustrations_list" :msg_list="follow_illustrations_list" @chose_item="go_to_illustration_page"></scroll_box>
    <h4>推荐的作品</h4>
    <div style="max-height: 900px; overflow:hidden;"><recommendation :token="token" :work_type="'ill'" v-if="token"></recommendation></div>
    <h4>排行榜</h4>
    <ranking></ranking>
  </div>
</template>

<script setup>
import { useStore } from '@/assets/model/store/index';
import scroll_box from './model/scroll_box.vue'
import scroll_box_1 from '../models/scroll_box.vue';
import { ref, reactive, toRefs, watch, onMounted, onUnmounted,computed } from 'vue';
import recommendation from './recommendation.vue';
import ranking from './ranking.vue';
import { get_user_follow_work_tags } from '@/assets/js/get_userinfo';
const store = useStore()

const tags_list = ref({
  data: []
});



let user_info = computed(()=>{
  return store.$state.user
})
let token = computed(() =>{
  return localStorage.getItem('token')
});

//获取用户关注用户的插画作品列表
let follow_illustrations_list = ref([])
async function get_follow_illustrations_list() {
  try {
    const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserFollowToIll/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization':'token '+localStorage.getItem('token')
      },
      body: JSON.stringify({
        userid: user_info.value.userid,
      })
    })
    const data = await res.json()
    console.log(data)
    if (data.status == 'success') {
      follow_illustrations_list.value = data.data;
      for (let i = 0; i < follow_illustrations_list.value.length; i++) {
        follow_illustrations_list.value[i].belong_to_user_avatar = await get_author_avatar(follow_illustrations_list.value[i].belong_to_user_id)
      }
      return data.data;
    }
    else {
      console.log(data.message)
    }
  }
  catch (error) {
    console.log(error)
  }
}
//根据ID获取用户作者头像
async function get_author_avatar(userid) {
  try {
    const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetAllUserInfo/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization':'token '+localStorage.getItem('token')
      },
      body: JSON.stringify({
        userid: userid,
        token: null,
      })
    })
    if (res.ok) {
      const data = await res.json()
      if (data.status == 'success') {
        return data.data[0].user_avatar;
      }
    }
    else {
      console.log(res.status)
    }
  }
  catch (error) {
    console.log(error)
  }
}
onMounted(async () => {
  get_follow_illustrations_list()
  let tagsData = await get_user_follow_work_tags(null);
  tags_list.value = tagsData;
})

//插画作品的带参跳转
function go_to_illustration_page(id) {
  store.commit('SET_CONTENT_PAGE', {
    key: 'ill_page',
    value: true
  })
  store.commit('SET_SINGLE_PAGE_STATUS',{key:'content_index_page',value:true})
  store.commit('SET_WORK_ID',id)
  store.commit('SET_WORK_TYPE','ill')
}

//模拟横向滚动效果
function scrollTabs(scrollAmount) {
  const tags = document.querySelector('.follow_list');
  const animationDuration = 0.2 * 1000; // 0.5秒转为毫秒
  const fps = 24; // 帧率
  const frameDuration = animationDuration / fps; // 每帧持续时间
  const framesCount = Math.ceil(animationDuration / frameDuration); // 总帧数
  let count = 0;
  function animateScroll() {
    if (count < framesCount) {
      tags.scrollLeft += scrollAmount / framesCount;
      count++;
      requestAnimationFrame(animateScroll);
    }
  }
  animateScroll();
}

</script>

<style scoped>
.illustration_page {
  width: 80%;
  height: auto;
  min-height: 400px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  position: relative;
}
.illustration_page::-webkit-scrollbar{
  display: none;
}

.follow_list {
  display: flex;
  width: 100%;
  height: 250px;
  margin-top: 10px;
  overflow-x: auto;
  scrollbar-width: none;
  white-space: nowrap;
}

.follow_work {
  display: flex;
  flex-direction: column;
  width: 150px;
  min-width: 150px;
  height: 100%;
  margin-right: 20px;
  margin-left: 10px;
  position: relative;
}

.left_btn {
  display: flex;
  position: absolute;
  left: 0px;
  height: 230px;
  width: 60px;
  opacity: 0;
  align-items: center;
}

.left_btn svg,
.right_btn svg {
  width: 40px;
  height: 40px;
  object-fit: cover;
}

.left_btn img,
.right_btn img {
  width: 40px;
  height: 40px;
  object-fit: cover;
}

.left_btn:hover {
  opacity: 1;
  cursor: pointer;
  transition: all 0.3s ease;
  /*从左到右白色到透明渐变*/
  background: linear-gradient(to right, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0));
}

.right_btn {
  display: flex;
  position: absolute;
  right: 0px;
  height: 230px;
  width: 60px;
  opacity: 0;
  align-items: center;
}

.right_btn svg {
  position: absolute;
  right: 0px;
}

.right_btn:hover {
  opacity: 1;
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 1));
}

.follow_work_item {
  display: flex;
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 80%;
  border-radius: 10px;
  cursor: pointer;
}

.follow_work_item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.age_tag {
  display: flex;
  position: absolute;
  left: 5px;
  top: 5px;
  font-size: 12px;
  color: white;
  background-color: red;
  border-radius: 5px;
  padding: 2px;
  font-weight: bold;
  z-index: 2;
}

.page_count {
  display: flex;
  position: absolute;
  right: 5px;
  top: 5px;
  min-height: 25px;
  min-width: 35px;
  font-size: 14px;
  font-weight: bold;
  color: white;
  background-color: rgba(129, 128, 128, 0.8);
  border-radius: 5px;
  padding: 2px;
  align-items: center;
  z-index: 2;
}

.page_count svg {
  width: 16px;
  height: 16px;
  margin-right: 2px;
  object-fit: cover;
  fill: rgba(244, 244, 244, 1)
}

.page_count img {
  width: 25px;
  height: 25px;
  margin-right: 2px;
  object-fit: cover;
}

.like {
  display: flex;
  position: absolute;
  right: 5px;
  bottom: 5px;
  z-index: 2;
}

.like svg {
  width: 30px;
  height: 30px;
  object-fit: cover;
}

.like img {
  width: 30px;
  height: 30px;
  object-fit: cover;
}

.userinfo {
  display: flex;
  width: 100%;
  flex-flow: 1;
  align-items: center;
}

.work_name {
  width: 100%;
  margin-top: 5px;
}

.user_avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 5px;
  margin-top: 5px;
}

.user_avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>