<template>
    <go_back></go_back>
  <div class="br_his_index_page">
    <div class="content" >
        <h1>浏览历史</h1>
        <span>默认只保留一千条浏览记录，需要更多请联系管理员</span>
        <div class="item_list" v-if="history_info_list">
          <div class="switch_type">
            <div class="switch_item">
              <span @click="page_type='ill'" :class="page_type=='ill'?'switch_item_chose':''">插画</span>
              <span @click="page_type='comic'" :class="page_type=='comic'?'switch_item_chose':''">漫画</span>
              <span @click="page_type='novel'" :class="page_type=='novel'?'switch_item_chose':''">小说</span>
            </div>
            <div class="item">
               <ill_page v-if="page_type=='ill'" :ill_item="ill_work_list"></ill_page>
               <comic_page v-if="page_type=='comic'" :comic_item="comic_work_list"></comic_page>
               <novel_page v-if="page_type=='novel'" :novel_item="novel_work_list"></novel_page>
            </div>
          </div>
        </div>
    </div>
  </div>
</template>
<script setup>
import {ref,onMounted,computed} from 'vue'
import { useStore } from 'vuex';
import go_back from './go_back.vue'
import { get_history } from './js/get_history';
import ill_page from './ill_page.vue'
import comic_page from './comic_page.vue'
import novel_page from './novel_page.vue'

const history_info_list=ref()
const ill_work_list=ref([])
const comic_work_list=ref([])
const novel_work_list=ref([])
let page_type=ref('ill')


async function classify_work(){
  console.log(history_info_list.value)
  for(let item of history_info_list.value){
    if(item.type=='ill'){
      ill_work_list.value.push(item)
    }
    if(item.type=='comic'){
      comic_work_list.value.push(item)
    }
    if(item.type=='novel'){
      novel_work_list.value.push(item)
    }
  }
}

onMounted(async()=>{
  history_info_list.value=await get_history()
  history_info_list.value=history_info_list.value.data
  await classify_work()
})

const store = useStore()

</script>

<style scoped>
.br_his_index_page{
  width:85vw;
  height: auto;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap:10px;
}
.content{
  width:100%;
  height: auto;
  display: flex;
  gap:10px;
  flex-direction: column;
}
.switch_item{
  width:auto;
  height: auto;
  display: flex;
  flex-direction: row;
  gap:10px;
}
.switch_item span{
  cursor: pointer;
  padding: 5px 10px;
  display: flex;
}
.switch_item span:hover{
  opacity: 0.8;
  transform: scale(1.01);
  transform: translateY(-1px);
  transition: all 0.2s;
}
.switch_item_chose{
  background-color: rgba(0,150,250,1);
  color:white;
  border-radius: 5px;
}
</style>