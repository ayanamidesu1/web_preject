<template>
  <div class="serach_img">
    <div class="title">
        <span></span>
        <h3>搜索图片</h3>
        <div class="close_btn" @click="close_page">
            <img class="icon" src="https://www.sunyuanling.com/assets/close.svg" alt="退出" style="width: 25px;height:25px;object-fit: cover">
        </div>
    </div>
    <div class="content">
        <img :src="'https://www.sunyuanling.com/server/static/image/'+img_src" alt="搜索图片">
    </div>
  </div>
</template>

<script setup>
import {ref,defineProps,defineEmits} from 'vue'

const props=defineProps({
    img_src:String
})

const emit=defineEmits(['close_page'])

function close_page(){
    emit('close_page')
}
</script>

<style scoped>
.serach_img{
    width: 100vw;
    height: 100vh;
    position: fixed;
    top:0;
    left: 0;
    z-index: 6;
    display: flex;
    background-color: rgba(0, 0, 0, 0.5);
    align-items: center;
    justify-content: center;
    overflow: auto;
}
.title{
    width:98%;
    height: 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: absolute;
    top:0;
    left: 0;
    background-color: rgba(233,233,233,1);
}
.title img{
    width:25px;
    height: 25px;
    object-fit: cover;
}
.close_btn{
    width:35px;
    height: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}
.close_btn:hover{
    background-color: rgba(0, 0, 0, 0.1);
    transition: all 0.2s;
    transform: scale(1.05);
    transform: translateY(-2px);
    border-radius: 50%;
}
.close_btn img{
    width:25px;
    height: 25px;
    object-fit: cover;
}
.icon{
    width:25px;
    height: 25px;
    object-fit: cover;
}
.content{
    width:100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.content img{
    width: auto;
    height: auto;
    object-fit: cover;
    max-width:800px;
    max-height: 800px;
}
</style>