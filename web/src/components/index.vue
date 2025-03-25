<template>
  <div class="tag_box">
    <scroll_box :msg_type="'tags'" :msg_list="tags_list.data" v-if="shouldShowScrollBox"></scroll_box>
  </div>
  <div class="switch_page">
    <span :class="{'active': page_show === 0}" @click="choosePage(0)">插画</span>
    <span :class="{'active': page_show === 1}" @click="choosePage(1)">漫画</span>
    <span :class="{'active': page_show === 2}" @click="choosePage(2)">小说</span>
  </div>
  <illustration_page v-if="page_show === 0"></illustration_page>
  <cartoon_page v-if="page_show === 1"></cartoon_page>
  <novel_page v-if="page_show === 2"></novel_page>
</template>
<script setup>
import { onMounted, ref, computed, watch } from 'vue';
import work_tags from './work_tags/work_tags.vue';
import illustration_page from './Illustration_page/Illustration_page.vue';
import cartoon_page from './cartoon/cartoon_page.vue';
import novel_page from './novel_page/novel_page.vue';
import scroll_box from './models/scroll_box.vue';
import { useStore } from 'vuex';
import { get_user_follow_work_tags } from '@/assets/js/get_userinfo';
import * as cookies from '@/assets/js/cookies';

const store = useStore();
const pageIndex = computed(() => store.getters.indexPage);
const page_show = ref(pageIndex.value);

const tags_list = ref({
  data: []
});

const shouldShowScrollBox = computed(() => {
  return tags_list.value.data.length > 0 && tags_list.value!== null && tags_list.value!== undefined;
});

function choosePage(index) {
  store.commit('SET_INDEXPAGE', index);
  store.commit('SET_PAGESTATUS');
  page_show.value = index;
}

watch(() => store.getters.indexPage, (newValue) => {
  page_show.value = newValue;
});

onMounted(async () => {
  let tagsData = await get_user_follow_work_tags(cookies.get_cookie('token'));
  tags_list.value = tagsData;
});
</script>
<style scoped>
.switch_page {
  display: flex;
  width: 80%;
  margin: 0 auto;
  margin-top: 20px;
}

.switch_page > span {
  margin-left: 10px;
  padding: 5px;
  margin: 0;
  font-size: 18px;
  cursor: pointer;
  font-weight: bold;
}

.switch_page > span.active {
  background-color: rgba(233, 233, 233, 1);
  border-bottom: 3px solid rgba(0, 150, 250, 1);
}

/* 图像抗锯齿处理 */
img {
  image-rendering: -moz-crisp-edges;
  image-rendering: crisp-edges;
  -ms-interpolation-mode: nearest-neighbor;
  image-rendering: smooth;
}

.tag_box {
  width: 80%;
  margin: 5px auto;
  display: flex;
  height: 60px;
}
</style>
