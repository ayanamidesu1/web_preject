<template>
  <div class="directory_page">
    <div class="content">
      <div class="close_box">
        <span></span>
        <span>目录</span>
        <div class="close_btn" @click="close_page()">
          <img src="https://www.sunyuanling.com/assets/close.svg" class="icon">
        </div>
      </div>
      <div class="item_box">
        <div class="item" v-for="(item, index) in work_info" :key="index">
          <div class="item_content" @click="get_chapter(item.belong_to_series_id, item.title, index)">
            {{ item.title }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  work_info: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['get_chapter','close_page']);

// 获取章节向上传递
function get_chapter(belong_to_series_id, title, index) {
  emit('get_chapter', { 'belong_to_series_id': belong_to_series_id, 'title': title, 'index': index });
  return { belong_to_series_id, title, index };
}
function close_page() {
  emit('close_page');
}
</script>

<style scoped>
.directory_page {
  width: 60vw;
  height: auto;
  display: flex;
  border-radius: 10px;
  box-shadow: 5px -3px 10px rgba(0, 0, 0, 0.5);
  min-width: 100px;
  min-height: 30px;
  background-color: rgb(253, 253, 253);
  position: absolute;
  right: 120%;
  flex-direction: column;
  box-sizing: border-box;
}

.content {
  width: 100%;
  height: auto;
  display: flex;
  border-radius: 10px;
  box-shadow: 5px -3px 10px rgba(0, 0, 0, 0.5);
  min-width: 100px;
  min-height: 30px;
  flex-direction: column;
}

.item_box {
  width: 100%;
  height: auto;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.item {
  width: 30%;
  height: auto;
  padding: 5px;
  border-radius: 10px;
  cursor: pointer;
  max-width: 30%;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.item:hover {
  transition: all 0.3s ease-in-out;
  background-color: #e0e0e0;
  transform: translateY(-2px);
}

.item_content {
  width: 100%;
  height: auto;
  overflow: hidden;
  display: flex;
  align-items: center;
  white-space: nowrap;
  text-overflow: ellipsis;
  justify-content: flex-start;
}

.icon {
  width: 25px;
  height: 25px;
  object-fit: cover;
}

.close_box {
  width: 100%;
  height: auto;
  display: flex;
  justify-content: space-between;
  position: relative;
  font-size: 18px;
  font-weight: bold;
}

.close_btn {
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 10px;
  margin-top: 5px;
}

.close_btn:hover {
  background-color: rgba(0, 0, 0, 0.5);
  transition: all 0.3s ease-in-out;
  cursor: pointer;
  transform: translateY(-2px);
}
</style>
