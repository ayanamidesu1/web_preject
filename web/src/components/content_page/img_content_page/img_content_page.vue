<template>
    <div class="img_content_page" @click="close_page_click">
        <div class="img_box">
            <img :src="props.item_path" ref="img_content_page_img">
        </div>
    </div>
  </template>
  
  <script setup>
  // eslint-disable-next-line no-unused-vars
  import { ref, watch, onMounted, defineProps,defineEmits } from 'vue';
  import { useStore } from 'vuex';
  
  const store = useStore();
  
  const props = defineProps({
    item_path: {
      type: String,
      default: ''
    }
  });
 
  const item_path = ref(props.item_path);
  let emit=defineEmits(['close_img_content_page']);
  
  watch(() => props.item_path, (newValue) => {
    item_path.value = newValue;
  });
  
  onMounted(() => {
    item_path.value = store.getters.item_path;
  });
  
  const img_content_page_img = ref(null);
  
  function close_page_click() {
    emit('close_img_content_page',false)
    if (img_content_page_img.value) {
      // img_content_page_img.value.click();
    } else {
      console.warn('img_content_page_img.value is null');
    }
  }
  </script>
  
  <style scoped>
  .img_content_page {
    width: auto;
    height: auto;
    background-color: rgba(0, 0, 0, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 985;
    position: fixed;
    top: 0;
    left: 0;
    min-height: 100vh;
    min-width: 100vw;
    cursor: zoom-out;
    pointer-events: auto; /* 保证这个层本身是可以接收点击事件的 */
    overflow: auto;
    box-sizing: border-box;
  }
  .img_box{
    width: auto;
    height: auto;
    display: flex;
    overflow: auto;
    position: absolute;
    top: 0px;
    left: 0px;
    margin: auto;
  }
  .img_box img {
    width: auto;
    height: auto;
    object-fit: cover;
    pointer-events: none; /* 禁止 img 本身接收点击事件，确保点击事件传递到 .img_content_page */
    overflow: auto;
  }
  </style>
  