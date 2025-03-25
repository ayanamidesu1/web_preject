<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import { ref,defineProps } from 'vue'
import ill_contribute_page from './model/ill_contribute_page.vue';
import comic_contribute_page from './model/comic_contribute_page.vue';
import novel_contribute_page from './model/novel_contribute_page.vue';
import go_back from '../../go_back.vue';

const props=defineProps({
  userid:{
    type:String,
    default:''
  }
})

let userinfo=ref({})
let work_content=ref({})
let page_index=ref(0)

</script>

<template>
  <div class="contribute_control">
    <div class="title">投稿状态管理</div>
    <div class="content">
      <div class="choose_item">
        <span @click="page_index=0" :class="page_index==0?'is_choose_item':''">插画投稿</span>
        <span @click="page_index=1" :class="page_index==1?'is_choose_item':''">漫画投稿</span>
        <span @click="page_index=2" :class="page_index==2?'is_choose_item':''">小说投稿</span>
      </div>
      <div class="page_item">
        <ill_contribute_page v-if="page_index==0"></ill_contribute_page>
        <comic_contribute_page v-if="page_index==1"></comic_contribute_page>
        <novel_contribute_page v-if="page_index==2"></novel_contribute_page>
      </div>
    </div>
  </div>
  <go_back></go_back>
</template>

<style scoped>
.contribute_control{
  width:85vw;
  height: auto;
  display: flex;
  flex-direction: column;
  gap:10px;
  margin:10px auto;
}
.title{
  width:100%;
  height: auto;
  display: flex;
  font-weight: bold;
  font-size:24px;
}
.content{
  width:100%;
  height:100%;
  display: flex;
  flex-direction: column;
  gap:10px;
}
.choose_item{
  width:auto;
  display: flex;
  height: auto;
  gap:10px;
  cursor: pointer;
  transition: all 0.2s;
  padding: 5px 10px;
}
.choose_item span{
  padding:5px 10px;
}
.choose_item span:hover{
  transform: scale(1.05);
  transform: translateY(-2px);
  border-radius: 5px;
  transition: all 0.2s ease-in-out;
}
.is_choose_item{
  color:white;
  background-color:rgba(0,150,250,1);
  transform: scale(1.05);
  transform: translateY(-2px);
  border-radius: 5px;
  transition: all 0.2s ease-in-out;
}
</style>
