<template>
    <div class="novel_index" v-if="work_id">
        <novel_content_page :work_id="work_id"  :key="work_id"></novel_content_page>
         <comment_box :item="{work_type:'novel',work_id:work_id}"></comment_box>
        <h3>推荐小说作品</h3>
        <div class="recommend_page">
          <novel_recommend  :work_type="'novel'"></novel_recommend>
        </div>
      </div>
</template>

<script setup>
import { ref, watch, onMounted ,defineProps,computed} from 'vue';
import { useStore } from 'vuex';
import novel_content_page from './novel_components/novel_content_page.vue';
import go_back from '../go_back.vue';
import novel_recommend from '@/assets/model/recommend_page/modle/index.vue'
import comment_box from '@assets/model/comment_box/comment_box.vue';
import { useRouter } from 'vue-router';
const router= useRouter()

const store = useStore();

const work_id = computed(()=>{
  return router.currentRoute.value.query.id
})

// 组件挂载时设置 work_id
onMounted(() => {
  //work_id.value = store.getters.work_id;
});

</script>


<style scoped>
.novel_index {
    width: 80%;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 20px;
}
</style>