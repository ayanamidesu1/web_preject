<template>
  <div class="comic_page">
    <div class="content">
      <div class="sort_fun_box">
        排序方式
      </div>
      <div class="popular_works">
        热门作品
      </div>
      <div class="title">
        <span>作品</span>
        <div class="work_count" v-if="data">
          <span>{{data.length}}</span>
        </div>
      </div>
      <div class="comic_box" v-if="data">
        <div class="comic_item" v-for="(item,index) in data" :key="index">
          <div class="age_classification" v-if="item.age_classification>16">
            <span>R-{{item.age_classification}}</span>
          </div>
          <div class="page_count">
            <img class="icon" src="https://www.sunyuanling.com/assets/page_count.svg">
            <span>{{item.content_file_list.split(/[,，]/).length}}</span>
          </div>
          <div class="comic_cover" @click="jump_to_page(item.id)">
            <img :src="'https://www.sunyuanling.com/image/comic/thumbnail/'+item.content_file_list.split(/[,，]/)[0]">
          </div>
          <div class="comic_title">
            <span>{{item.work_name}}</span>
          </div>
          <div class="author_info">
            <div class="author_avatar">
              <img class="author_avatar_img" :src="item.avatar">
            </div>
            <div class="author_name">
              <span>{{item.belong_to_user}}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted,defineEmits,defineProps } from 'vue';
export default {
  name: 'comic_page',
}
</script>

<script setup>
import {useStore} from 'vuex'
const store = new useStore()
let comic_data=defineProps({
    comic_data:{
        type:Object,
        default(){
            return {}
        }
    }
})
let data=ref(comic_data.comic_data)
const emit=defineEmits(['work_count'])
watch(()=>comic_data.comic_data,async (newValue,oldValue)=>{
    data.value=newValue;
    await set_avatar()
    emit('work_count',{'type':'comic','count':data.value.length})
})
onMounted(async ()=>{
  data.value=comic_data.comic_data;
  await set_avatar()
})
//请求作者头像
async function get_author_avatar(userid){
  const res=await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetAllUserInfo/',{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    },
    body:JSON.stringify({
      userid:userid
    })
  })
  if(res.ok)
  {
    const data=await res.json()
    if (data.status=='success')
  {
    return 'https://www.sunyuanling.com/image/avatar_thumbnail/'+data.data[0].user_avatar
  }
  }
}
//设置头像
async function set_avatar()
{
  for(let i=0;i<data.value.length;i++)
{
  data.value[i].avatar=await  get_author_avatar(data.value[i].belong_to_userid)
}
}
//带参跳转
function jump_to_page(id)
{
  console.log(id)
  //window.location.href='https://localhost:3002/?id='+id+'&work_type=comic'
  store.commit('SET_CONTENT_PAGE', {
    key: 'comic_page',
    value: true
  })
  store.commit('SET_SINGLE_PAGE_STATUS',{key:'content_index_page',value:true})
  store.commit('SET_WORK_ID',id)
  store.commit('SET_WORK_TYPE','comic')
}
</script>

<style scoped>
  .comic_page{
    width: 80%;
    height: auto;
    margin: 5px  auto;
    display: flex;
    flex-direction: column;
    padding: 5px;
    margin-bottom: 10%;
  }
  .content{
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    margin: 5px 10% auto auto;
  }
  .comic_box{
    width: 100%;
    height: auto;
    display: flex;
    flex-wrap: wrap;
  }
  .comic_item{
    width:210px;
    max-height: 300px;
    margin:10px 10px;
    border-radius: 10px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    position: relative;
  }
  .age_classification{
    position: absolute;
    left: 5px;
    top:5px;
    width: auto;
    height: auto;
    padding: 3px 5px;
    background-color: red;
    color: white;
    border-radius: 5px;
    font-size: 14px;
    font-weight: bold;
    z-index: 5;
    display: flex;
    align-items: center;
  }
  .icon{
    width: 25px;
    height: 25px;
    object-fit: cover;
  }
  .page_count{
    position: absolute;
    right: 15px;
    top:5px;
    width: auto;
    height: auto;
    padding: 3px 5px;
    background-color: rgba(0,0,0,0.5);
    color: white;
    border-radius: 5px;
    font-size: 14px;
    font-weight: bold;
    z-index: 5;
    display: flex;
    align-items: center;
  }
  .comic_cover{
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 10px;
    cursor: pointer;
  }
  .comic_cover img{
    width: 100%;
    height: 100%;
    border-radius: 10px;
    object-fit: cover;
  }
  .comic_title{
    font-size: 16px;
    font-weight: bold;
    margin: 5px;
  }
  .author_info{
    display: flex;
    width: 100%;
    height: auto;
    align-items: center;
    padding: 5px;
  }
  .author_avatar_img{
    width:35px;
    height: 35px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 10px;
  }
  .author_name{
    font-size: 14px;
  }
  .title{
    display: flex;
    width: auto;
    height: auto;
    align-items: center;
    padding: 5px;
    font-size: 20px;
    font-weight: bold;
    padding: 5px 10px;
  }
  .work_count{
    display: flex;
    margin-left: 5px;
    background-color: rgba(0,0,0,0.5);
    border-radius: 10px;
    padding: 3px 5px;
    color: white;
  }
</style>