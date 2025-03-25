<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import { ref,defineProps ,onMounted} from 'vue'
import { get_rank_list } from './model/js/get_ranklist';
import scroll_box from './model/scroll_box.vue';
import scroll_box_comic from './model/scroll_box_comic.vue';
import scroll_box_novel from './model/scroll_box_novel.vue';
const props=defineProps({
  msg: String,
  work_type:{
    type:String,
    default:'ill'
  }
})
let rank_list=ref()

onMounted(async ()=>{
  rank_list.value=await get_rank_list(props.work_type,localStorage.getItem('token'))
  console.log(rank_list.value)
})
</script>

<template>
<div class="root">
  <scroll_box :msg_list="rank_list" v-if="work_type=='ill'&&rank_list"></scroll_box>
  <scroll_box_comic :msg_list="rank_list" v-if="work_type=='comic'&&rank_list"></scroll_box_comic>
  <scroll_box_novel :msg_list="rank_list" v-if="work_type=='novel'&&rank_list"></scroll_box_novel>
</div>
</template>

<style scoped>

</style>
