<template>
  <div class="index">
    <div class="choose_page">
      <div class="close_btn" @click="close_upload_page()">
        <img class="icon" src="https://www.sunyuanling.com/assets/close.svg">
      </div>
      <span @click="type = 'ill'" class="choose_page_item" :class="{ select: type === 'ill' }">
        <img class="icon" src="https://www.sunyuanling.com/assets/photo.svg">
        插画</span>
      <span @click="type = 'comic'" class="choose_page_item" :class="{ select: type === 'comic' }">
        <img class="icon" src="https://www.sunyuanling.com/assets/comic.svg">
        漫画</span>
      <span @click="type = 'novel'" class="choose_page_item" :class="{ select: type === 'novel' }">
        <img class="icon" src="https://www.sunyuanling.com/assets/novel.svg">
        小说</span>
    </div>
    <ill_page v-if="type == 'ill'"></ill_page>
    <comic_page v-else-if="type == 'comic'"></comic_page>
    <novel_page v-else-if="type == 'novel'"></novel_page>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted, defineEmits } from 'vue';
import ill_page from './ill/ill_page.vue';
import comic_page from './comic/comic_page.vue';
import novel_page from './novel/novel_page.vue';
import { useStore } from 'vuex'
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'index',
  components: {
    ill_page, comic_page, novel_page
  }
}
</script>

<script setup>
const store = useStore()
let type = ref();
function close_upload_page() {
  store.commit('SET_SINGLE_PAGE_STATUS', { key: 'upload_work', value: false })
}
watch(() => store.getters.upload_work_type, (newValue) => {
  type.value = newValue;
  console.log(newValue)
})
onMounted(() => {
  type.value = store.getters.upload_work_type;
})
</script>

<style scoped>
.icon {
  width: 25px;
  height: 25px;
  object-fit: cover;
}
.select {
  background-color: rgba(200, 200, 200, 1);
  border-bottom: 3px solid rgba(0, 150, 250, 1);
  transition: all 0.2s ease-in-out;
  margin-bottom: 5px;
}
.index {
  width: 100vw;
  min-height: 90vh;
  height: 100%;
  display: flex;
  background-color: rgba(255, 255, 255, 1);
  top: 65px;
  left: 0px;
  flex-direction: column
}

.choose_page {
  width: 100%;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(107, 107, 107, 1);
  margin: 0px auto;
  position: relative;
  color:rgba(233,233,233,1);
  font-size: 16px;
  font-weight: bold;
  overflow: hidden;
}
.close_btn{
  width:30px;
  height: 30px;
  position: absolute;
  left: 10px;
  margin:auto;
  justify-content: center;
  align-items: center;
  display: flex;
}
.close_btn:hover{
  cursor: pointer;
  background-color:rgba(188,188,188,1);
  border-radius: 50%;
  transition:all 0.3s ease-in-out;
}
.choose_page_item {
  width: auto;
  height: 85%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: auto 10px;
  padding: 2px 20px;
  cursor: pointer;
  gap: 10px;
}
.choose_page_item:hover{
  background-color: rgba(200,200,200,1);
  transition: all 0.3s ease-in-out;
}
</style>
