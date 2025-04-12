<template>
  <div class="send_msg_index">
    <div class="content">
        <span>发送消息</span>
        <div class="menu">
          <span @click="change_page(0)" :class="{is_active:page_index==0}" class="menu_item">向置顶用户发送消息</span>
          <span @click="change_page(1)" :class="{is_active:page_index==1}" class="menu_item">查询卡密</span>
        </div>
        <div class="item">
          <send_box v-if="page_index===0"></send_box>
          <search_box v-if="page_index===1"></search_box>
        </div>
    </div>
  </div>
</template>


<script setup>
import { ref,onMounted } from 'vue'
import { useStore } from '@/model/store/store';
import { BaseApi } from '@/base_api';
import send_box from './send_box.vue';
import search_box from './search_box.vue';

const store = useStore();
const api= new BaseApi();

const page_index=ref(0)
function change_page(index){
  page_index.value=index
}

</script>

<style scoped>
.send_msg_index{
  width: 100%;
  display: flex;
  flex-direction: column;
  gap:10px;
}
.content{
  width: 100%;
  display: flex;
  flex-direction: column;
  gap:10px;
}
.menu{
  width: fit-content;
  display: flex;
  gap:10px;
}
.menu_item{
  cursor: pointer;
  padding: 5px 10px;
  background-color: rgb(114, 112, 112);
  border-radius: 5px;
  color: white;
  font-weight: bold;
  transition: all 0.2s;
}
.is_active{
  background-color: rgb(0,150,250);
  color: white;
  transform: scale(1.05);
}
</style>