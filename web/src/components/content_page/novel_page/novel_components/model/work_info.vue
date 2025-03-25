<template>
  <div class="work_info" v-if="work_info && author_info.length != 0">
    <div class="content">
      <div class="work_info_item">
        <div class="work_cover">
          <img :src="'https://www.sunyuanling.com/image/novel/' + work_info[0].work_cover">
        </div>
        <div class="author_info">
          <div class="info">
            <div class="title">
              <span style="font-size: 24px; font-weight:bold;">{{ work_info[0].work_name }}</span>
            </div>
            <div class="author_name" style="display: flex;gap:10px;">
              <span>作者：<b>{{ author_info.username }}</b></span>
              <span style="font-size: 18px;font-weight:bold;color:rgb(133,133,133);">
                最后更新时间：{{ work_info[(work_info.length - 1)].create_time }}</span>
            </div>
            <div class="most_new_chapter">
              <div class="title">
                <span style="color: rgb(133,133,133);">最新章节：{{ work_info[(work_info.length - 1)].title }}</span>
              </div>
            </div>
            <div class="work_status">
              <span>{{ work_info[0].work_status }}·{{ (work_info[0].is_vip_work == 1 ? 'VIP作品' : '免费作品') }}</span>
            </div>
            <div class="brief_introduction">
              <span style="font-size: 14px;color:rgb(133,133,133);">{{ work_info[0].brief_introduction }}</span>
            </div>
            <div class="work_data">
              <span>{{ (Math.round((word_count / 10000) * 100) / 100).toFixed(2) }}&nbsp;<b>万字</b></span>
              <span><img class="icon" src="https://www.sunyuanling.com/assets/show.svg">{{ work_info_dict.watch_count
                }}观看</span>
              <span @click="add_like_work($event,work_info[0].work_id)" style="cursor: pointer;"><img class="icon"
                  :src="is_like_svg">
                {{ work_info_dict.like_count }}点赞</span>
              <span @click="add_collect_work($event,work_info[0].work_id)" style="cursor: pointer;"><img class="icon"
                  :src="is_collect_svg">
                {{ work_info_dict.collect_count }}收藏</span>
            </div>
          </div>
        </div>
        <div class="author_box">
          <div class="author_avatar">
            <img :src="'https://www.sunyuanling.com/image/avatar_thumbnail/' + author_info.user_avatar">
          </div>
          <div class="author_name">
            <span>{{ author_info.username }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <float_msg_box v-if="float_msg_box_show" :message="float_msg_box_msg"
    :mouse_position="{ 'x': float_msg_box_x, 'y': float_msg_box_y }"></float_msg_box>
</template>

<script setup>
// eslint-disable-next-line no-unused-vars
import { ref, defineProps, onMounted, computed } from 'vue'
import { watch_work, like_work, collect_work } from '@/assets/js/interaction.js'
import * as cookies from '@/assets/js/cookies.js'
import float_msg_box from '@/assets/model/float_msg_box.vue';
import { useStore } from 'vuex'
const store = useStore()

let token = cookies.get_cookie('token')
let float_msg_box_show = ref(false)
let float_msg_box_msg = ref('')
let float_msg_box_x = ref()
let float_msg_box_y = ref()

onMounted(async () => {
  await watch_work(props.work_info[0].belong_to_series_id, token, 'novel', props.work_info[0].work_name)
  console.log(props.work_info)
})

let props = defineProps({
  work_info: {
    type: Array,
    default: () => {
      return null
    }
  },
  author_info: {
    type: Object,
    default: () => {
      return null
    }
  },
  word_count: {
    type: [Number, String],
    default: 0
  },
  work_info_dict: {
    type: Object,
    default: () => {
      return null
    }
  },
})

let is_like_svg = computed(() => props.work_info_dict.is_like ? 'https://www.sunyuanling.com/assets/work_like.svg'
  : 'https://www.sunyuanling.com/assets/no_work_like.svg')
let is_collect_svg = computed(() => props.work_info_dict.is_collect ? 'https://www.sunyuanling.com/assets/love.svg'
  : 'https://www.sunyuanling.com/assets/no_love.svg')

let work_info_dict = ref(props.work_info_dict)
async function add_like_work(event,work_id) {
  work_info_dict.value.is_like = !work_info_dict.value.is_like
  let data = await like_work(work_id, 'add', token, 'novel', props.work_info[0].work_name)

  if (data == 1) {
    
    float_msg_box_msg.value = '感谢达令的点赞！'
    float_msg_box_show.value=true
    //获取点击位置鼠标的坐标
    float_msg_box_x.value = event.clientX
    float_msg_box_y.value = event.clientY
    setTimeout(()=>{
      float_msg_box_show.value=false
    },1500)
    
   store.commit('set_cursor_msg','感谢达令的点赞！')
  }
  else{
    float_msg_box_msg.value='伦家有什么地方做的不好吗？'
    store.commit('set_cursor_msg','伦家有什么地方做的不好吗？')
  }
}
async function add_collect_work(event,work_id) {
  work_info_dict.value.is_collect = !work_info_dict.value.is_collect
  let data = await collect_work(work_id, 'add', token, 'novel', props.work_info[0].work_name)
  if (data == 1) {
    float_msg_box_msg.value = '感谢达令的收藏！'
    float_msg_box_show.value=true
    //获取点击位置鼠标的坐标
    float_msg_box_x.value = event.clientX
    float_msg_box_y.value = event.clientY
    setTimeout(()=>{
      float_msg_box_show.value=false
    },1500)
   store.commit('set_cursor_msg','感谢达令的收藏！')
  }
  else{
    float_msg_box_msg.value='伦家有什么地方做的不好吗？'
    store.commit('set_cursor_msg','伦家有什么地方做的不好吗？')
  }
}
</script>

<style scoped>
.work_info {
  width: 100%;
  height: auto;
  display: flex;
  border-radius: 10px;
  box-shadow: 5px -3px 10px rgba(0, 0, 0, 0.5);
  padding: 5px;
  min-width: 100px;
  min-height: 30px;
  flex-direction: column;
}

.content {
  width: 98%;
  height: auto;
  display: flex;
  border-radius: 10px;
  box-shadow: 5px -3px 10px rgba(0, 0, 0, 0.5);
  padding: 5px;
  min-width: 100px;
  min-height: 30px;
  flex-direction: column;
  margin: 0px auto;
}

.work_info_item {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.work_cover {
  width: 20%;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.work_cover img {
  width: 100%;
  height: auto;
  border-radius: 10px;
  object-fit: cover;
}

.author_info {
  width: 70%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-left: 10px;
}

.info {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.author_box {
  width: 25%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
  align-items: center;
}

.author_avatar {
  width: 80px;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.author_avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.work_data {
  width: auto;
  padding: 5px 0px;
  display: flex;
  gap: 10px;
}

.icon {
  width: 15px;
  height: 15px;
  object-fit: cover;
  align-self: center;
  margin: auto 2px;
}
</style>