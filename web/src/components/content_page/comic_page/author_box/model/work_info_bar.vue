<script setup>
// eslint-disable-next-line no-unused-vars
import { defineProps,ref,onMounted } from 'vue'
import {get_comic_workinfo} from '@/assets/js/get_work_info'

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  title: {
    type: String,
    default: '作品标题'
  },
  brief_introduction: {
    type: String,
    default: '作品简介'
  },
  age_classification: {
    type: String,
    default:'18'
  },
  tags: {
    type: Array,
    default: () => ['标签一']
  },
  work_data: {
    type: Object,
    default: () => ({
      'like': '100',
      'collect': '100',
      'watch': '100'
    })
  },
  work_create_time: {
    type: String,
    default: '2024年7月26日13:08:38'
  },
  work_id:{
    default:'123'
  }
})

const work_info = ref(null)
const work_tags = ref([])

onMounted(async () => {
  try {
    const data = await get_comic_workinfo(props.work_id)
    work_info.value = data
    console.log(work_info.value)
    // 检查数据是否存在并更新标签
    if (work_info.value && work_info.value.data && work_info.value.data.length > 0) {
      work_tags.value = work_info.value.data[0].work_tags.split(/[,，]/)
    }
    console.log(work_info.value)
  } catch (error) {
    console.error('获取作品信息失败:', error)
  }
})
</script>

<template>
  <div class="work_info_bar">
    <div class="content">
      <div class="title">
        <span>{{ title }}</span>
      </div>
      <div class="brief_introduction">
        <span>{{ brief_introduction }}</span>
      </div>
      <div class="tags_box">
        <span class="age_classification" v-if="age_classification !== '16'">
          <span>R-{{ age_classification }}</span>
        </span>
        <div class="tag_item">
          <div class="tag" v-for="(item, index) in work_tags" :key="index">
            <span>#&nbsp;{{ item }}</span>
          </div>
        </div>
      </div>
      <div class="work_data" style="color:rgba(133,133,133,1)">
        <div class="work_data_item">
          <img src="https://www.sunyuanling.com/assets/like.svg" class="icon">
          <span>{{ work_data.like }}</span>
        </div>
        <div class="work_data_item">
          <img src="https://www.sunyuanling.com/assets/work_like.svg" class="icon" style="width:25px;height:25px;">
          <span>{{ work_data.collect }}</span>
        </div>
        <div class="work_data_item">
          <img src="https://www.sunyuanling.com/assets/show.svg" class="icon">
          <span>{{ work_data.watch }}</span>
        </div>
      </div>
      <div class="work_create_time">
        <span>{{ work_create_time }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.work_info_bar{
  display: flex;
  width: 100%;
  height: auto;
  flex-direction: column;
  min-width: 100px;
  min-height: 50px;
  margin: 5px 0px;
  padding-left: 20px;
}
.content{
  display: flex;
  width: 100%;
  height: 100%;
  flex-direction: column;
  gap:10px;
}
.title{
  width: auto;
  height: auto;
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
}
.brief_introduction{
  display: flex;
  width: 100%;
  height: auto;
}
.tags_box{
  display: flex;
  width: 100%;
  height: auto;
  gap: 5px;
}
.age_classification{
  display: flex;
  font-size: 16px;
  font-weight: bold;
  color:white;
  background-color: red;
  border-radius: 10px;
  padding: 5px;
  width: auto;
  height: auto;
  max-height: 26px;
}
.tag_item{
  display: flex;
  width: auto;
  height: auto;
  padding: 5px;
  color: rgba(0,150,250,1);
}
.icon{
  width: 20px;
  height: 20px;
  object-fit: cover;
}
.work_data{
  width: auto;
  height: auto;
  padding: 5px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.work_data_item{
  width: auto;
  height: auto;
  display: flex;
  align-items: center;
  gap: 5px;
}
.work_create_time{
  width: auto;
  height: auto;
  color: rgba(133,133,133,1);
  font-size: 14px;
}
</style>
