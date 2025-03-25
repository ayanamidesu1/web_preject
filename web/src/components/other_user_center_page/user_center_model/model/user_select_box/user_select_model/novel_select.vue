<template>
  <div class="ill_select" v-if="all_work_list">
    <div class="header">
      <h2 class="title">小说作品标签
        <div class="work_count_box">
          <span>{{ all_work_list.length }}</span>
        </div>
      </h2>
    </div>
    <scroll_box_copy :msg_list="work_tags" :msg_type="'tags'" v-if="work_tags.length > 0" />
    <div class="work_item_list">
      <div class="work_item" v-for="(item, index) in all_work_list" :key="index">
        <img :src="'https://www.sunyuanling.com/image/novel/thumbnail/' + item.work_cover" alt="Work Thumbnail"
          class="thumbnail" @click="chose_item({ 'work_type': 'novel', 'work_id': item.work_id })">
        <span class="work_name">{{ item.work_name }}</span>
      </div>
    </div>
  </div>
  <div class="if_all_none" v-else>
    <span>这里空空如也什么也没有</span>
  </div>
</template>

<script setup>
import { ref, defineProps, onMounted, defineEmits } from 'vue'
// eslint-disable-next-line no-unused-vars
import { get_workinfo, get_user_all_worklist } from '../../../js/get_workinfo'
import scroll_box_copy from './model/scroll_box_copy.vue';
import { useStore } from 'vuex'
const store = useStore()

const props = defineProps({
  user_info: {
    type: Object,
    default: () => ({})
  },
  token: {
    type: String,
    default: ''
  },
  userid:{
    type: String,
    default: ''
  }
})

// eslint-disable-next-line no-unused-vars
const emit = defineEmits(['choose_item'])

function chose_item(item) {
  store.commit('SET_CONTENT_PAGE', {
    key: 'novel_page',
    value: true
  })
  store.commit('SET_SINGLE_PAGE_STATUS', { key: 'content_index_page', value: true })
  store.commit('SET_WORK_ID', item.work_id)
  store.commit('SET_WORK_TYPE', item.work_type)
}

const work_tags = ref([]);
const all_work_list = ref([]);


function set_work_tags() {
  const tagsSet = new Set(); // 使用 Set 来避免重复的标签
  console.log(all_work_list.value.work_tags)
  all_work_list.value.forEach(work => {
    const tags = work.work_tags.split(/[,，]/);
    tags.forEach(tag => tagsSet.add(tag.trim())); // 去除可能的空白字符
  });

  work_tags.value = Array.from(tagsSet); // 转换回数组
  console.log(work_tags.value);
}

onMounted(async () => {
  //await set_select_work(select_work.value);
  all_work_list.value = await get_user_all_worklist(props.token,props.userid);
  all_work_list.value = all_work_list.value.novel || [];
  console.log(all_work_list.value);
  set_work_tags();
});
</script>

<style scoped>
.ill_select {
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.title {
  font-size: 1.5rem;
  color: #333;
  position: relative;
  display: flex;
  width: auto
}

.work_count_box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 35px;
  height: 35px;
  min-width: 35px;
  min-height: 35px;
  background-color: #f0f0f0;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 1rem;
  color: #333;
  position: absolute;
  right: -80px;
}

.work_item_list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.work_item {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 200px;
  text-align: center;
}

.work_item img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  cursor: pointer;

}

.thumbnail {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.work_name {
  margin-top: 10px;
  font-size: 1rem;
  color: #555;
}
.if_all_none {
  text-align: center;
  font-size: 18px;
  color: #888;
}
</style>
