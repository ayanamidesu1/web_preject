<template>
  <div class="search_page_index" @wheel="onWheel">
    <div class="close_btn" @click="close_btn_click()">
      <img class="icon" src="https://www.sunyuanling.com/assets/close.svg" alt="close_btn">
    </div>
    <div class="content">
      <div class="head_box">

        <scroll_box :msg_list="tag_list" v-if="tag_list"></scroll_box>
      </div>
      <div class="choose_search_target_page">
        <div class="choose_ill_page" ref="choose_ill_page" @click="switch_page(0)">
          <span>插画</span>
          <span class="count_result">{{ill_count}}</span>
        </div>
        <div class="choose_comic_page" ref="choose_comic_page" @click="switch_page(1)">
          <span>漫画</span>
          <span class="count_result">{{comic_count}}</span>
        </div>
        <div class="choose_novel_page" ref="choose_novel_page" @click="switch_page(2)">
          <span>小说</span>
          <span class="count_result">{{novel_count}}</span>
        </div>
        <div class="choose_user_page" ref="choose_user_page" @click="switch_page(3)">
          <span>用户</span>
          <span class="count_result">{{user_count}}</span>
        </div>
      </div>
      <ill_page :ill_data="ill_list" v-show="ill_page_show" @work_count="set_work_count"></ill_page>
      <comic_page :comic_data='comic_list' v-show="comic_page_show" @work_count="set_work_count"></comic_page>
      <novel_page :novel_data="novel_list" v-show="novel_page_show" @work_count="set_work_count"></novel_page>
      <user_page :user_data="userinfo_list" v-show="user_page_show" @work_count="set_work_count"></user_page>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted, defineProps, defineEmits, defineExpose } from 'vue';
// eslint-disable-next-line no-unused-vars
import * as cookies from '../../../../../../model/cookies.js'
import ill_page from './page/ill_page.vue'
import comic_page from './page/comic_page.vue'
import novel_page from './page/novel_page.vue'
import user_page from './page/user_page.vue'
import scroll_box from './model/scroll_box.vue'
export default {
  name: 'search_page_index',
  components: {
    ill_page,
    comic_page,
    novel_page,
    user_page,
  }
}

</script>

<script setup>
let props = defineProps({
  search_item: {
    type: String,
    default: '德丽莎'
  }
})
let search_data = ref(props.search_item)
let ill_list = ref([])
let comic_list = ref([])
let novel_list = ref([])
let userinfo_list = ref([])
let tag_list = ref()
let tag_background_color_list = ['rgb(129, 126, 200)', 'rgb(126, 172, 200)', 'rgb(200, 126, 176)', 'rgb(200, 126, 152)',
  'rgb(200, 146, 126)'
  , 'rgb(126, 178, 200)', 'rgb(200, 173, 126)', 'rgb(126, 171, 200)', 'rgb(194, 200, 126)'
]
let search_result_cover = ref('https://www.sunyuanling.com/image/thumbnail/120282888_p0.jpg')

let ill_page_show = ref(true)
let comic_page_show = ref(false)
let novel_page_show = ref(false)
let user_page_show = ref(false)
let choose_ill_page = ref(null)
let choose_comic_page = ref(null)
let choose_novel_page = ref(null)
let choose_user_page = ref(null)
//切换搜索结果页面
function switch_page(index) {
  switch (index) {
    case 0:
      ill_page_show.value = true;
      choose_ill_page.value.style.borderTop = '4px solid rgb(0,250,250)';
      comic_page_show.value = false;
      choose_comic_page.value.style.borderTop = '';
      novel_page_show.value = false;
      choose_novel_page.value.style.borderTop = '';
      user_page_show.value = false;
      choose_user_page.value.style.borderTop = '';
      break;
    case 1:
      ill_page_show.value = false;
      choose_ill_page.value.style.borderTop = '';
      comic_page_show.value = true;
      choose_comic_page.value.style.borderTop = '4px solid rgb(0,250,250)';
      novel_page_show.value = false;
      choose_novel_page.value.style.borderTop = '';
      user_page_show.value = false;
      choose_user_page.value.style.borderTop = '';
      break;
    case 2:
      ill_page_show.value = false;
      choose_ill_page.value.style.borderTop = '';
      comic_page_show.value = false;
      choose_comic_page.value.style.borderTop = '';
      novel_page_show.value = true;
      choose_novel_page.value.style.borderTop = '4px solid rgb(0,250,250)';
      user_page_show.value = false;
      choose_user_page.value.style.borderTop = '';
      break;
    case 3:
      ill_page_show.value = false;
      choose_ill_page.value.style.borderTop = '';
      comic_page_show.value = false;
      choose_comic_page.value.style.borderTop = '';
      novel_page_show.value = false;
      choose_novel_page.value.style.borderTop = '';
      user_page_show.value = true;
      choose_user_page.value.style.borderTop = '4px solid rgb(0,250,250)'
      break;
  }
}
onMounted(() => {
  switch_page(0);
})

watch(() => props.search_item, async (new_value, old_value) => {
  search_data.value = await get_search_data(new_value)
  categorize_data(search_data.value)
  set_tag_list(search_data.value)
  console.log(tag_list.value)
}
)
function categorize_data(data) {
  ill_list.value = [];
  comic_list.value = [];
  novel_list.value = [];
  userinfo_list.value = [];
  if (data == null) {
    return
  }
  else {
    data.forEach(item => {
      if (item.type === 'ill') {
        ill_list.value.push(item);
      } else if (item.type === 'comic') {
        comic_list.value.push(item);
      } else if (item.type === 'novel') {
        novel_list.value.push(item);
      }
      if (item.type === 'user') {
        userinfo_list.value.push(item);
      }
    });
  }
}
// 设置标签
function set_tag_list(data) {
  if (data == null) {
    tag_list.value = [];
    return;
  }
  let all_tags = data.flatMap(item => {
    if (item.work_tags && typeof item.work_tags === 'string') {
      return item.work_tags.split(/[,，]/).map(tag => tag.trim());
    } else {
      console.warn('Expected a string for work_tags but got:', item.work_tags);
      return [];
    }
  });
  tag_list.value = [...new Set(all_tags)];
}


let close_msg = defineEmits(['close_msg'])
function close_btn_click() {
  close_msg('close_msg', false)
}

async function get_search_data(data) {
  search_data.value = null
  try {
    const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetSearch/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify({
        'search_key': data
      })
    })
    if (res.ok) {
      const data = await res.json()
      if (data.status == 'success') {
        console.log(data.data)
        return data.data
      }
      else {
        console.log(data.message)
        return []
      }
    }
  } catch (error) {
    console.log(error)
    return []
  }
}
//阻止滚动事件传播
function onWheel(event) {
  event.stopPropagation();
}
defineExpose({
  get_search_data
})
//获取子页面的搜索结果数据
let ill_count=ref()
let comic_count=ref()
let novel_count=ref()
let user_count=ref()
function set_work_count(item)
{
  let type=item.type;
  let count=item.count;
  switch(type)
  {
    case 'ill':
      ill_count.value=count
      break;
    case 'comic':
      comic_count.value=count
      break;
    case 'novel':
      novel_count.value=count
      break;
    case 'user':
      user_count.value=count
   
  }
}

</script>

<style scoped>
.choose_ill_page,
.choose_comic_page,
.choose_novel_page,
.choose_user_page {
  display: flex;
  width: auto;
  height: 100%;
  padding: 5px 10px;
  align-items: center;
  margin-bottom: 30px;
  cursor: default;
  cursor: pointer;
}

/*倒序*/
.search_page_index {
  position: fixed;
  top: 65px;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 15;
  background-color: rgba(255, 255, 255, 1);
  overflow: auto;
}

.close_btn {
  display: flex;
  width: 35px;
  height: 35px;
  align-items: center;
  justify-content: center;
  position: absolute;
  right: 30px;
}

.close_btn:hover {
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  transition: all 0.3s ease-in-out;
}

.icon {
  width: 25px;
  height: 25px;
}

.content {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  margin-top: 30px;
}

.head_box {
  display: flex;
  width: 80%;
  height: 80px;
  align-items: center;
  margin: 10px auto;
}

.search_result_cover {
  width: 100%;
  height: 100%;
  display: flex;
}

.search_result_cover image {
  width: 200px;
  height: 200px;
  object-fit: cover;
}

.tag_list {
  width: 100%;
  height: 50px;
  display: flex;
  position: relative;
  margin-left: auto;
  margin-right: auto;
}

.btn_box {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  position: absolute;
  left: 0;
  opacity: 0;
}

.btn_box:hover {
  cursor: pointer;
  opacity: 1;
  transition: all 0.3s ease-in-out;
}

.left_btn,
.right_btn {
  width: 45px;
  height: 100%;
  position: absolute;
  align-items: center;
  display: block;
  justify-content: center;
}

.left_btn {
  left: 0;
}

.left_btn:hover {
  cursor: pointer;
  background-color: rgba(255, 255, 255, 0.5);
  transition: all 0.3s ease-in-out;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0));
  opacity: 1;
}

.right_btn {
  right: 0;
}

.right_btn:hover {
  cursor: pointer;
  background-color: rgba(255, 255, 255, 0.5);
  transition: all 0.3s ease-in-out;
  background: linear-gradient(to left, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0));
  opacity: 1;
}

.choose_search_target_page {
  width: 80%;
  display: flex;
  height: 35px;
  align-items: center;
  margin: 0px auto;
}
.count_result{
  width: auto;
  height: auto;
  padding: 3px;
  margin-left: 5px;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 5px;
  color: white;
}
</style>