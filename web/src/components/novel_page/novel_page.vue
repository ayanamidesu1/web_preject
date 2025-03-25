<template>
  <div class="novel_page">
    <h3>已关注用户作品</h3>
    <div class="novel_list">
      <div class="novel_item" v-for="(item,index) in novel_info_list" :key="index">
        <div class="novel_cover" @click="open_novel_page(item.work_id)">
          <img :src="'https://www.sunyuanling.com/image/novel/thumbnail/'+item.work_cover">
        </div>
        <div class="novel_info">
          <div class="novel_state mt">
            <span>{{item.work_status}}</span>
          </div>
          <div class="novel_title  mt">
            <span>{{item.work_name}}</span>
          </div>
          <div class="novel_userinfo  mt" @click="jump_to_other_user_center(item.belong_to_userid,item)">
            <div class="novel_useravatar">
              <img :src="'https://www.sunyuanling.com/image/'+item.belong_to_avatar">
            </div>
            <div class="novel_username">
              <span>{{item.belong_to_username}}</span>
            </div>
          </div>
          <div class="novel_tags  mt">
            <span style="margin-right: 5px" class="age_tag" v-if="item.age_classification>17">R-{{item.age_classification}}</span>
            <span class="tags" v-for="(tags,index) in item.work_tags.split(/[,，]/)" :key="index">#{{tags}}</span>
          </div>
          <div class="novel_read_data  mt">
            <div class="word_count">
              <span>{{word_count}}字</span>
            </div>
            <div class="read_time">
              <span>{{read_time}}分钟</span>
            </div>
            <div class="like_count">
              <span>{{like_count}}人喜欢</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <h4>推荐的小说作品</h4>
    <div class="recommend_page" style="max-height: 1200px; overflow:hidden;">
      <recommendation_novel :token="token" :work_type="'novel'"></recommendation_novel>
    </div>
    <h4>小说排行榜</h4>
    <ranking></ranking>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted ,computed} from 'vue';
import recommendation_novel from './recommendation_novel.vue';
import ranking from './ranking.vue';
export default {
  name: 'novel_page',
  components:{recommendation_novel,ranking},
}
</script>

<script setup>
import * as cookies from '../../../../model/cookies.js'
import { useStore } from 'vuex';
const store=useStore();
let token=computed(()=>store.getters.token)
//进入指定用户的用户中心
function jump_to_other_user_center(userid,item)
{
  store.commit('SET_OTHER_USERID',userid)
  store.commit('SET_SINGLE_PAGE_STATUS',{'key':'other_user_center_page','value':true})
  console.log(userid)
}
let word_count=ref('1111');
let read_time=ref('12');
let like_count=ref('45');
let userinfo=ref(JSON.parse(cookies.get_cookie('userinfo')))

//获取用户关注的用户的小说信息
let novel_info_list=ref([])

async function get_novel_list(){
  try{
    const res=await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserFollowNovel/',{
      method:'post',
      headers:{
        'Content-Type':'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token'),
      },
      body:JSON.stringify({
        userid:userinfo.value.userid,
      })
    })
    if(res.ok)
    {
      const data=await res.json()
      console.log(data)
      novel_info_list.value=data.data
      for(let i=0;i<novel_info_list.value.length;i++)
    {
      novel_info_list.value[i].belong_to_avatar=await get_author_avatar(novel_info_list.value[i].belong_to_userid)
    }
    }
    else{
      console.log('服务器错误')
    }
  }
  catch(e)
  {
    console.log(e)
  }
}
async function get_author_avatar(userid) {
  try {
    const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetAllUserInfo/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token'),
      },
      body: JSON.stringify({
        userid: userid,
        token: null,
      })
    })
    if (res.ok) {
      const data = await res.json()
      if (data.status == 'success') {
        return data.data[0].user_avatar;
      }
    }
    else {
      console.log(res.status)
    }
  }
  catch (error) {
    console.log(error)
  }
}
onMounted(()=>{
  get_novel_list()
})

//打开小说作品详情页并设置work_id参数
function open_novel_page(id)
{
  store.commit('SET_WORK_ID',id)
  store.commit('SET_CONTENT_PAGE',{key:'novel_page',value:true})
  store.commit('SET_SINGLE_PAGE_STATUS',{key:'content_index_page',value:true})
}
</script>

<style scoped>
.mt{
  margin-top: 5px;
}
  .novel_page {
  display: flex;
  flex-direction: column;
  width: 80%;
  height: auto;
  margin:0 auto;
  margin-top: 20px;
  }
  .novel_list{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin-top: 20px;
    width: 100%;
    height: auto;
  }
 .novel_item{
    display: flex;
    width:45%;
    height: auto;
    min-width: 350px;
    min-height: 230px;
    margin-top: 20px;
    align-items: center;
    padding-top: 10px;
    padding-bottom: 10px;
 }
 .novel_cover{
  display: flex;
  width:30%;
  height: 100%;
  max-height: 200px;
  border-radius: 15px;
  overflow: hidden;
  justify-content: center;
  align-items: center;
  cursor: pointer;
 }
 .novel_cover img{
  width: 100%;
  height: 100%;
  object-fit: cover;
  max-height: 200px;
 }
 .novel_info{
  display: flex;
  flex-direction: column;
  width: 70%;
  height: 100%;
  padding: 5px;
  justify-content: space-around;
  padding: 10px;
 }
 .novel_userinfo{
  display: flex;
  width: 100%;
  height: 35px;
  align-items: center;
  cursor: pointer;
 }
 .novel_useravatar{
  display: flex;
  width:35px;
  height: 35px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 10px;
 }
 .novel_useravatar img{
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.novel_read_data{
  display: flex;
  justify-content: space-between;
}
.novel_title{
  font-size: 18px;
  font-weight: bold;
}
.age_tag{
  font-size: 18px;
  color: red;
  font-weight: bold;
}
.tags{
  cursor: pointer;
  font-size: 16px;
  color: rgba(0, 174, 255,1);
  margin-left:8px;
  margin-top: 5px;
}
</style>