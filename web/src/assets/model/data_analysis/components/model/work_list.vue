<template>
    <div class="work_list">
      <div class="content">
          <div class="category">
              <h3>插画</h3>
              <div class="item" v-for="(item, index) in ill_list" :key="index">
                  <div class="item_img" @click="choose_item({'work_id': item.Illustration_id, 'work_type': 'ill'})">
                      <img :src="'https://www.sunyuanling.com/image/thumbnail/' + item.content_file_list.split(/[,，]/)[0]">
                      <div class="page_count">
                          <span>{{ item.content_file_list.split(/[,，]/).length }}</span>
                      </div>
                      <div class="age_tag" v-if="item.age_classification >= 18">
                          <span>R-{{ item.age_classification }}</span>
                      </div>
                  </div>
                  <div class="work_info">
                      <div class="work_name">
                          {{ item.name }}
                      </div>
                  </div>
              </div>
          </div>
  
          <div class="category">
              <h3>漫画</h3>
              <div class="item" v-for="(item, index) in comic_list" :key="index">
                  <div class="item_img" @click="choose_item({'work_id': item.id, 'work_type': 'comic'})">
                      <img :src="'https://www.sunyuanling.com/image/comic/thumbnail/' + item.content_file_list.split(/[,，]/)[0]">
                      <div class="page_count">
                          <span>{{ item.content_file_list.split(/[,，]/).length }}</span>
                      </div>
                      <div class="age_tag" v-if="item.age_classification >= 18">
                          <span>R-{{ item.age_classification }}</span>
                      </div>
                  </div>
                  <div class="work_info">
                      <div class="work_name">
                          {{ item.work_name }}
                      </div>
                  </div>
              </div>
          </div>
  
          <div class="category">
              <h3>小说</h3>
              <div class="item" v-for="(item, index) in novel_list" :key="index">
                  <div class="work_cover">
                      <img :src="'https://www.sunyuanling.com/image/novel/thumbnail/' + item.work_cover"
                          @click="choose_item({'work_id': item.work_id, 'work_type': 'novel'})">
                      <div class="age_tag" v-if="item.age_classification >= 18">
                          {{ item.age_classification }}
                      </div>
                      <div class="work_status">
                          <span>{{ item.work_status }}</span>
                      </div>
                  </div>
                  <div class="work_info">
                      <span>{{ item.work_name }}</span>
                  </div>
              </div>
          </div>
      </div>
    </div>
  </template>
  

<script setup>
import {ref,defineProps,watch,defineEmits}  from 'vue'

const props=defineProps({
  work_list:{
    type:Object,
    default:()=>{
        return {}
    }
  }
})
let ill_list=ref(props.work_list.ill)
let comic_list=ref(props.work_list.comic)
let novel_list=ref(props.work_list.novel)

const emit=defineEmits(['choose_item'])

function choose_item(item){
    emit('choose_item',item)
    console.log(item)
}

watch(()=>props.work_list,()=>{
    ill_list.value=props.work_list.ill
    comic_list.value=props.work_list.comic
    novel_list.value=props.work_list.novel
})
</script>

<style scoped>
.work_list {
  display: flex;
  flex-direction: column;
  padding: 16px;
  width: 100%;
  height: auto;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 16px; /* 设定分类之间的间距 */
}

h3 {
  margin-bottom: 12px;
  font-size: 1.25rem;
  font-weight: bold;
}

.category {
  display: flex;
  flex-wrap: wrap; /* 启用换行 */
  gap: 16px; /* 作品之间的间距 */
}

.item {
  display: flex;
  flex-direction: column;
  width: 200px; /* 固定宽度 */
  max-height: 300px; /* 最大高度 */
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  box-sizing: border-box; /* 包括边框和内边距在内的宽度 */
}

.item_img,.work_cover {
  display: flex;
  flex-direction: column;
  cursor: pointer;
  position: relative;
  flex-shrink: 0; /* 防止图片缩小 */
}

.item_img img {
  width: 200px; /* 固定宽度 */
  height: auto; /* 高度自动 */
  max-height: 200px; /* 图片最大高度 */
  object-fit: cover;
  border-radius: 5px;
}
.work_cover img{
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 5px;
}

.page_count {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
}

.age_tag {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255, 0, 0, 0.8);
  color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
}

.work_info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 8px;
  width: 100%; /* 使工作信息区域填满宽度 */
  box-sizing: border-box; /* 包括边框和内边距在内的宽度 */
}

.work_name {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 4px;
}

.work_status {
  font-size: 0.875rem;
  color: #666;
}
</style>

