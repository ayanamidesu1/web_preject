<template>
  <div class="novel_page">
    <div class="content">
      <div class="sort_fun_box">
        排序方法
      </div>
      <div class="popular_box">
        推荐作品
      </div>
      <div class="title">
        <span>作品</span>
        <div class="work_count" v-if="data">
          <span>{{ data.length }}</span>
        </div>
      </div>
      <div class="item_box">
        <div class="item" v-for="(item, index) in data" :key="index">
          <div class="novel_cover" @click="jump_to_page(item.work_id)">
            <img :src="'https://www.sunyuanling.com/image/novel/thumbnail/'+item.work_cover">
          </div>
          <div class="novel_info">
            <div class="novel_title">
              <span >{{item.work_name}}</span>
            </div>
            <div class="author_info">
              <div class="author_avatar">
                <img :src="item.avatar">
              </div>
              <div class="author_name">
                <span>{{item.belong_to_username}}</span>
              </div>
            </div>
            <div class="tags">
               <span style="font-size:16px;font-weight:bold;color:red;margin-right:5px;" v-if="item.age_classification>16">R-{{ item.age_classification }}</span>
              <span style="color:rgba(0,150,250,1);font-size:16px;font-weight:bold;margin-right:5px;"
              v-for="(tag_item,tag_index) in item.work_tags.split(/[,，]/)" :key="tag_index">#{{ tag_item }}</span>
            </div>
            <div class="author_say">
              {{item.author_say}}
            </div>
            <div class="read_info"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted, defineEmits, defineProps } from 'vue';
export default {
  name: 'novel_page',
}
</script>

<script setup>
import { useStore } from 'vuex'
const store = new useStore()
let novel_data = defineProps({
  novel_data: {
    type: Object,
    default: () => {
      return {}
    }
  }
})
let data = ref(novel_data.novel_data)
const emit=defineEmits(['work_count'])
watch(() => novel_data.novel_data,async (newValue, oldValue) => {
  data.value = newValue;
  await set_avatar();
  emit('work_count',{'type':'novel','count':data.value.length})
})
onMounted(async () => {
  data.value = novel_data.novel_data;
  await set_avatar();
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
  data.value[i].avatar=await get_author_avatar(data.value[i].belong_to_userid)
}
}
//带参跳转
function jump_to_page(id)
{
  console.log(id)
  //window.location.href='https://localhost:3002/?work_id='+id+'&type=novel';
  store.commit('SET_CONTENT_PAGE', {
    key: 'novel_page',
    value: true
  })
  store.commit('SET_SINGLE_PAGE_STATUS',{key:'content_index_page',value:true})
  store.commit('SET_WORK_ID',id)
  store.commit('SET_WORK_TYPE','novel')
}
</script>

<style scoped>
.novel_page {
  width: 80%;
  height: auto;
  display: flex;
  flex-direction: column;
  margin: 5px auto;
  margin-bottom: auto;
}

.content {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  margin: 5px 10% auto auto;
}

.title {
  display: flex;
  width: auto;
  height: auto;
  align-items: center;
  padding: 5px;
  font-size: 20px;
  font-weight: bold;
  padding: 5px 10px;
}
.work_count {
  display: flex;
  margin-left: 5px;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  padding: 3px 5px;
  color: white;
}
.item_box{
  display: flex;
  width: 100%;
  height: auto;
  flex-wrap: wrap;
}
.item{
  width:45%;
  height:200px;
  padding: 5px;
  display: flex;
  position: relative;
  overflow: hidden;
  margin:10px;
}
.icon{
  width:25px;
  height: 25px;
}
.novel_info{
  width:auto;
  height: 200px;
  padding: 5px;
  margin-left: 5px;
  display: flex;
  flex-direction: column;
  flex: 1;
  justify-content: space-around;
}
.author_info{
  display: flex;
  width: 100%;
  height: auto;
  padding: 5px;
  align-items: center;
}
.author_avatar{
  width: 35px;
  height: 35px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 5px;
}
.author_avatar img{
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}
.novel_cover{
  width:150px;
  height: 200px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
.novel_cover img{
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 5px;
}
.novel_title{
  font-size: 16px;
  font-weight: bold;
}
</style>