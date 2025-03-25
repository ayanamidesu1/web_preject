<template>
  <div class="ill_select">
    <div class="header">
      <h2 class="title">插画作品标签
        <div class="work_count_box">
          <span>{{ all_work_list.length }}</span>
        </div>
      </h2>
    </div>
    <scroll_box_copy :msg_list="work_tags" :msg_type="'tags'" v-if="work_tags.length > 0" />
    <div class="work_item_list">
      <div class="work_item" v-for="(item, index) in all_work_list" :key="index">
        <img :src="'https://www.sunyuanling.com/image/thumbnail/' + item.content_file_list.split(/[，,]/)[0]"
          alt="Work Thumbnail" class="thumbnail"
          @click="chose_item({ 'work_type': 'ill', 'work_id': item.Illustration_id })">
        <span class="work_name">{{ item.name }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, onMounted, defineEmits } from 'vue'
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
  }
})

const emit = defineEmits(['choose_item'])

function chose_item(item) {
  store.commit('SET_CONTENT_PAGE', {
    key: 'ill_page',
    value: true
  })
  store.commit('SET_SINGLE_PAGE_STATUS', { key: 'content_index_page', value: true })
  store.commit('SET_WORK_ID', item.work_id)
  store.commit('SET_WORK_TYPE', item.work_type)
}

const select_work = ref(JSON.parse(props.user_info.select_work).ill || []);
const ill_work_list = ref([]);
const work_tags = ref([]);
const all_work_list = ref([]);

async function set_select_work(select_work) {
  const temp_dict = select_work.map(work_id => ({
    work_id,
    work_type: 'ill'
  }));

  ill_work_list.value = await get_workinfo(props.token, temp_dict);
  console.log(ill_work_list.value);
}

function set_work_tags() {
  const tagsSet = new Set(); // 使用 Set 来避免重复的标签

  all_work_list.value.forEach(work => {
    const tags = work.work_tags.split(/[,，]/);
    tags.forEach(tag => tagsSet.add(tag.trim())); // 去除可能的空白字符
  });

  work_tags.value = Array.from(tagsSet); // 转换回数组
  console.log(work_tags.value);
}

onMounted(async () => {
  await set_select_work(select_work.value);
  all_work_list.value = await get_user_all_worklist(props.token);
  all_work_list.value = all_work_list.value.ill || [];
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
</style>
