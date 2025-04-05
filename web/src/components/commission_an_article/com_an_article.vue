<template>
  <div class="com_an_article">
    <h2>约稿管理</h2>
    <div class="menu_item">
        <span :class="page_index===0? 'is_active':''" @click="page_index=0">收到的约稿申请</span>
        <span :class="page_index===1? 'is_active':''" @click="page_index=1">发送的约稿申请</span>
    </div>
    <div class="item">
        <div class="content">
            <receiver_request v-if="page_index===0"></receiver_request>
            <send_request v-if="page_index===1"></send_request>
        </div>
        <div class="right_box">
            <func_page></func_page>
        </div>
    </div>
    
  </div>
</template>


<script setup>
import { ref } from 'vue'
import receiver_request from './sub_page/receiver_request.vue';
import send_request from './sub_page/send_request.vue';
import func_page from './sub_page/func_page.vue';
let page_index=ref(0)

</script>

<style scoped>
.com_an_article{
    width: 90%;
    display: flex;
    flex-direction: column;
    margin: 10px auto;
    padding: 10px;
    border-radius: 10px;
    background-color: rgb(248, 244, 248);
    height: 100%;
    min-height: calc(100vh - 100px);
    overflow: auto;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    gap:10px;
}
.menu_item{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    width: fit-content;
    gap: 10px;
}
.menu_item span{
    color: #797777;
    cursor: pointer;
    padding: 5px 10px;
    font-weight: bold;
    transition: all 0.2s ease-in-out;
}
.menu_item span.is_active{
    border-top: 3px solid rgb(0,150,250);
    color: #000;
    transform: scale(1.05);
}
.item{
    display: grid;
    grid-template-columns: minmax(400px,70%) minmax(200px,25%);
    gap:10px;
    height: 100%;
    min-height: 100%;
    padding: 10px;
    min-height: 400px;
}
.item .content{
    overflow: auto;
    height: 100%;
    min-height: 100%;
    display: flex;
    flex-direction: column;
    gap:10px;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    box-shadow: 2px 0 3px rgba(0, 0, 0, 0.2);
    background-color: rgb(255, 255, 255);
}
.item .right_box{
    overflow: auto;
    height: 100%;
    min-height: 100%;
    display: flex;
    flex-direction: column;
    gap:10px;
    padding: 10px;
   
}
</style>