<template>
  <div class="content_index_page">
    <ill_index v-if="ill_index_show"/>
    <comic_index v-if="comic_index_show" />
    <novel_index v-if="novel_index_show"/>
    <img_content_page v-if="img_content_page_show"/>
  </div>
</template>
<script setup>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted,computed } from 'vue';
import { useStore } from 'vuex';
import ill_index from './ill_page/ill_index.vue';
import comic_index from './comic_page/comic_index.vue';
import novel_index from './novel_page/novel_index.vue';
import img_content_page from './img_content_page/img_content_page.vue';
const store = useStore()
let ill_index_show=computed(()=>store.getters.ill_page)
let comic_index_show=computed(()=>store.getters.comic_page)
let novel_index_show=computed(()=>store.getters.novel_page)
let img_content_page_show=computed(()=>store.getters.img_content_page)
</script>

<style scoped>
  
</style>