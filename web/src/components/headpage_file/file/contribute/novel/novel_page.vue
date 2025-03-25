<template>
  <div class="novel_page">
    <div class="page_title">
      小说投稿
    </div>
    <div class="content">
      <span>投稿形式</span>
      <div class="work_typeof">
        <input type="radio" value="系列作品" name="novel_typeof" ref="novel_typeof">
        <label for="">系列作品</label>
        <input type="radio" value="单篇完结作品" name="novel_typeof" ref="novel_typeof">
        <label for="">单篇完结作品</label>
        <div class="contribute_tips" style="margin-top: 10px;color:rgba(77,77,77,0.9);font-size:14px;">
          <span>若是连载作品，或是类似短篇小说集等分多个篇章叙述的作品，还请选为系列作品进行投稿。
            在新建系列后才能投稿系列作品。</span>
        </div>
      </div>
      <div class="work_series">
        <re_select :select_title="select_title" :select_list="select_list" @select-item="get_select_item"></re_select>
      </div>
      <div class="work_item">
        <div class="work_title">
          <input type="text" placeholder="作品标题" v-model="work_title" maxlength="100">
          <span style="position:absolute;right:2px;color:rgba(77,77,77,0.6)">{{ work_title_len }}/100</span>
        </div>
        <div class="work_content">
          <auto_textarea v-model="work_content" :maxlength="300000" :rows="5" placeholder="请输入正文内容..." :fontsize="14"
            :lineheight="1.6"></auto_textarea>
          <span style="position:absolute;right:0px;top:100%;color:rgba(77,77,77,0.6);">{{ work_content_len
            }}/300000</span>
        </div>
      </div>
      <div class="btn_box">
        <div class="sure_btn" @click="upload_chapter()">
          <span>确定</span>
        </div>
      </div>
    </div>
    <create_new_series v-if="create_new_series_show" @close_create_new_series="close_create_new_series">
    </create_new_series>
    <div class="hr" style="border-top:1px solid rgba(77,77,77,0.3);margin-top:50px;
    height:1px;width:90%;margin-left:auto;margin-right:auto;">
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted,computed } from 'vue';
export default {
  name: 'novel_page',
}
</script>

<script setup>
import re_select from '../../../../models/select.vue'
import auto_textarea from '../../../../models/auto_textarea.vue'
import create_new_series from './create_new_series.vue';
import * as cookies from '@/assets/js/cookies'
import {useStore} from 'vuex'
const store=useStore()

let token = cookies.get_cookie('token');
token=computed(()=>store.getters.token)
token=token.value
let select_title = ref('新建系列')
let select_list = ref([
  '新建系列',
  '作品系列一'
])
let novel_typeof=ref(null)
let select_item = ref();
let work_content = ref('')
let work_content_len = ref(work_content.value.length);
let work_title = ref('');
let work_title_len = ref(work_title.value.length);
let create_new_series_show = ref(false)
watch(work_title, () => {
  work_title_len.value = work_title.value.length
})
watch(work_content, () => {
  work_content_len.value = work_content.value.length
})
function get_select_item(item) {
  select_item.value = item
  console.log(item)
}
function open_create_new_series() {
  if (select_item.value == '新建系列') {
    create_new_series_show.value = true
  }
  else {
    create_new_series_show.value = false
  }
}
watch(select_item, (newValue) => {
  open_create_new_series()
})
function close_create_new_series() {
  create_new_series_show.value = false
}
async function get_user_series_list() {
  let temp = [];
  select_list.value = ['新建系列']
  try {
    let res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserWorkSeries/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify({
        token: token,
      })
    });
    if (!res.ok) {
      console.error('HTTP error:', res.status);
      return;
    }
    const data = await res.json();
    if (data.status === 'success') {
      temp = data.data;
      const workSeries = temp.map(item => item.work_series).filter(Boolean);
      select_list.value = [...new Set([...select_list.value, ...workSeries])];
    } else {
      alert(data.message);
    }
  } catch (e) {
    console.error('Fetch error:', e);
  }
}
onMounted(async () => {
  await get_user_series_list()
})
//章节上传
async function upload_chapter() {
  let temp=work_content.value.replace(/\n/g, '\\n')
  try {
    const res = await fetch('https://www.sunyuanling.com/api/novel/UploadNewChapter/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify({
        token: token,
        series_name: select_item.value,
        chapter_name: work_title.value,
        content: temp,
        is_series:novel_typeof.value.value
      })
    })
    if (res.ok) {
      const data = await res.json()
      if (data.status == 'success') {
        alert(data.message)
      }
      else {
        alert(data.message)
      }
    }
    else {
      console.log('服务器错误')
    }
  }
  catch (e) {
    console.log(e)
  }
}
</script>

<style scoped>
.btn_box {
  display: flex;
  width: auto;
  height: auto;
  padding: 10px 20px;
  flex-direction: column;
}

.sure_btn {
  width: 100%;
  display: flex;
  height: 100%;
  justify-content: center;
  align-items: center;
  padding: 5px 10px;
  border-radius: 15px;
  background-color: rgba(0, 150, 250, 1);
  cursor: pointer;
  color: white;
}

.sure_btn:hover {
  opacity: 0.8;
  transition: all 0.3s ease-in-out;
}

.novel_page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.page_title {
  width: 100%;
  height: auto;
  min-height: 35px;
  display: flex;
  justify-content: center;
  margin: 0px 5px auto auto;
  font-size: 18px;
  font-weight: bold;
  background-color: #f5f5f5;
  align-items: center;
  padding: 5px 10px;

}

.content {
  width: 80%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-self: center;
  gap: 10px;
}

.work_typeof {
  width: 100%;
  height: auto;
  gap: 10px;
}

.work_series {
  width: 300px;
  height: auto;
  display: flex;
  z-index: 3;
}

.work_item {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.work_title {
  width: 100%;
  height: 30px;
  display: flex;
  align-items: center;
  border: 1px solid rgba(133, 133, 133, 1);
  padding: 2px;
  border-radius: 5px;
  position: relative;
}

.work_title input {
  width: 100%;
  height: 100%;
  border-radius: 5px;
  border: none;
}

.work_content {
  width: 100%;
  height: auto;
  border: 1px solid rgba(133, 133, 133, 1);
  padding: 5px;
  border-radius: 5px;
  position: relative;
}
</style>