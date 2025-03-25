<template>
  <div class="directory_page">
    <div class="content">
      <div class="item_box">
        <div class="item" v-for="(item,index) in work_info" :key="index">
            <div class="item_content" @click="get_chapter(item.belong_to_series_id,item.title,index)">{{item.title}}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref ,defineProps,defineEmits} from 'vue'
let props=defineProps({
  work_info:{
    type:Array,
    default:()=>{
      return[]
    }
  },
})
let emit=defineEmits(['get_chapter'])
//获取章节向上传递
function get_chapter(belong_to_series_id,title,index)
{ 
  emit('get_chapter',{'belong_to_series_id':belong_to_series_id,'title':title,index:index})
  return {belong_to_series_id,title}
}
</script>

<style scoped>
  .directory_page{
    width: 100%;
    height: auto;
    display: flex;
    border-radius: 10px;
    box-shadow: 5px -3px 10px rgba(0, 0, 0, 0.5);
    padding: 5px;
    min-width: 100px;
    min-height: 30px;
  }
  .content{
    width: 100%;
    height: auto;
    display: flex;
    border-radius: 10px;
    box-shadow: 5px -3px 10px rgba(0, 0, 0, 0.5);
    padding: 5px;
    min-width: 100px;
    min-height: 30px;
  }
  .item_box{
    width: 100%;
    height: auto;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  .item{
    width: 30%;
    height: auto;
    padding: 5px 10px;
    border-radius: 10px;
    cursor: pointer;
  }
  .item:hover{
    background-color: rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease-in-out;
  }
</style>