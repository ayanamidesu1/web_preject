<script setup>
import { ref, defineProps, onMounted } from 'vue'
import work_info from './model/work_info.vue';
import directory_page from './model/directory_page.vue';
import { get_workinfo, get_novel_content } from './model/js/get_workinfo';
import novel_content_page from './model/novel_content_model/novel_content.vue';


let props = defineProps({
  work_id: {
    type: [String,Number],
    default: '10'
  },
  token: {
    type: String,
    default: ''
  }
})
let data = ref()
let author_info = ref()
let work_list = ref()
let word_count = ref()
let novel_content = ref()
let work_title = ref('')
let novel_brief_introduction_page=ref(true)
let novel_content_page_show = ref(false)
let chapter_index=ref(0)


onMounted(async () => {
  data.value = await get_workinfo(props.token, props.work_id)
  author_info.value = data.value.author_info
  work_list.value = data.value.work_list
  word_count.value = data.value.word_count
  console.log(props)
})
async function get_chapter(item) {
  novel_content.value = await get_novel_content('sunyuanling', item.belong_to_series_id, item.title)
  work_title.value = item.title
  chapter_index.value=item.index
  novel_brief_introduction_page.value = false
  novel_content_page_show.value = true
}



</script>

<template>
  <div class="novel_conteng_page" v-if="data">
    <div class="novel_brief_introduction" v-if="novel_brief_introduction_page">
      <div class="work_info">
        <work_info :work_info="work_list" :author_info="author_info" :word_count="word_count" :work_info_dict="data"></work_info>
      </div>
      <div class="directory_page">
        <directory_page :work_info="work_list" @get_chapter="get_chapter"></directory_page>
      </div>
    </div>
    <div class="novel_content" v-if="novel_content_page_show">
      <novel_content_page :content="novel_content" :title="work_title" :work_info="work_list" 
      :chapter_index="chapter_index"></novel_content_page>
    </div>
  </div>
  <div class="wait" v-else-if="!data">
    <div class="wait_text">
      <p>正在加载中</p>
    </div>
  </div>
</template>

<style scoped>
.novel_conteng_page {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.directory_page{
  margin-top:20px;
}
</style>
