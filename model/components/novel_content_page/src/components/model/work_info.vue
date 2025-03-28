<template>
  <div class="work_info" v-if="work_info && author_info.length != 0">
    <div class="content">
      <div class="work_info_item">
        <div class="work_cover">
          <img :src="'https://www.sunyuanling.com/server/static/image/novel/' + work_info[0].work_cover">
        </div>
        <div class="author_info">
          <div class="info">
            <div class="title">
              <span style="font-size: 24px; font-weight:bold;">{{work_info[0].title}}</span>
            </div>
            <div class="author_name" style="display: flex;gap:10px;">
              <span>作者：<b>{{author_info.username}}</b></span>
              <span style="font-size: 18px;font-weight:bold;color:rgb(133,133,133);">
                最后更新时间：{{work_info[(work_info.length-1)].create_time}}</span>
            </div>
            <div class="most_new_chapter">
              <div class="title">
                <span style="color: rgb(133,133,133);">最新章节：{{work_info[(work_info.length-1)].title}}</span>
              </div>
            </div>
            <div class="work_status">
              <span>{{work_info[0].work_status}}·{{(work_info[0].is_vip_work==1?'VIP作品':'免费作品')}}</span>
            </div>
            <div class="brief_introduction">
              <span style="font-size: 14px;color:rgb(133,133,133);">{{work_info[0].brief_introduction}}</span>
            </div>
            <div class="work_data">
              <span>{{ (Math.round((word_count / 10000) * 100) / 100).toFixed(2) }}&nbsp;<b>万字</b></span>
              <span>点赞</span>
              <span>收藏</span>
            </div>
          </div>
        </div>
        <div class="author_box">
            <div class="author_avatar">
              <img :src="'https://www.sunyuanling.com/server/static/image/avatar_thumbnail/'+author_info.user_avatar">
            </div>
            <div class="author_name">
              <span>{{author_info.username}}</span>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue'
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
  }
})

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
  margin:0px auto;
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
.author_box{
  width: 25%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
  align-items: center;
}
.author_avatar{
  width: 80px;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.author_avatar img{
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}
.work_data{
  width: auto;
  padding: 5px 0px;
  display: flex;
  gap: 10px;
}
</style>