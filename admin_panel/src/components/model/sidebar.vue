<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="sidebar">
    <div class="content">
        <div class="item">
            <span :class="{is_active:now_page==0}" @click="switch_page('/',0)">用户管理</span>
            <span :class="{is_active:now_page==1}" @click="switch_page('/ill',1)">插画作品审核</span>
            <span :class="{is_active:now_page==2}" @click="switch_page('/comic',2)">漫画作品审核</span>
            <span :class="{is_active:now_page==3}" @click="switch_page('/novel',3)">小说作品审核</span>
            <span :class="{is_active:now_page==4}" @click="switch_page('/comment',4)">评论管理</span>
        </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
const router=useRouter()
let now_page=ref(0)
function switch_page(page_name,index){
  now_page.value=index;
  router.push(page_name)
}

</script>

<style scoped>
  .sidebar{
    width:150px;
    height: fit-content;
    background-color:rgba(100, 100, 100, 0.5);
    display: flex;
    flex-direction: column;
    border-radius: 10px;
    position:sticky;
    top:0;
    z-index:5;
  }
  .content{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .item{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }
  .item span{
    width:100%;
    height: auto;
    margin: 5px ;
    padding:5px 0px;
    cursor: pointer;
    font-size: 18px;
    color: white;
    font-weight: bold;
    align-items: center;
    display: flex;
    justify-content: center;
  }
  .item span:hover{
    background-color: rgba(133,133,133,1);
    border-radius: 10px;
    transition: all 0.2s ease-in-out;
    transform: scale(1.05);
    transform: translateY(-2px);
  }
  .is_active{
    background-color: rgba(133,133,133,1);
    border-radius: 10px;
    transition: all 0.2s ease-in-out;
    transform: scale(1.05);
    transform: translateY(-2px);
  }
</style>