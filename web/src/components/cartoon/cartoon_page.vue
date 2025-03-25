<template>
  <div class="cartoon_page">
    <h3>已关注用户作品</h3>
    <scroll_box :msg_list="comic_list" v-if="comic_list" @chose_item="open_comic_page"></scroll_box>
    <h4>推荐作品</h4>
    <div class="recommend_page" style="max-height: 900px; overflow:hidden;">
      <recommendation_cartoon :token="token" :work_type="'comic'"></recommendation_cartoon>
    </div>
      <h4>排行榜</h4>
      <ranking></ranking>
  </div>

</template>

<script>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted,computed } from 'vue';
import recommendation_cartoon from './recommendation_cartoon.vue';
import ranking from './ranking.vue';
export default {
  name: 'cartoon_page',
  components:{recommendation_cartoon,ranking,},
}
</script>
<script setup>
import * as cookies from '../../../../model/cookies.js'
import { useStore } from 'vuex';
import scroll_box from './model/scroll_box.vue';
const store = useStore()
let userinfo=ref(JSON.parse(cookies.get_cookie('userinfo')))
console.log(userinfo.value)
let comic_list=ref([])

let token = computed(() => store.getters.token);
//获取用户关注的漫画作品列表
async function get_comic_list(){
  try{
    const res=await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserFollowToComic/',{
      method:'post',
      headers:{
        'Content-Type':'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token'),
      },
      body:JSON.stringify({
        userid:userinfo.value.userid,
      })
    })
    const data=await res.json()
    if(res.ok)
    {
      console.log(data)
      comic_list.value=data.data
      console.log(comic_list.value)
      for(let i=0;i<comic_list.value.length;i++)
      {
        comic_list.value[i].belong_to_avatar=await get_author_avatar(comic_list.value[i].belong_to_userid)
      }
    }
    else{
      console.log('服务器错误')
    }
  }
  catch(e){
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
  get_comic_list()

})

//滚动函数
// eslint-disable-next-line no-unused-vars
function scrollTabs(scrollAmount) {
  const tags = document.querySelector('.cartoon_list');
  const animationDuration = 0.2 * 1000; // 0.5秒转为毫秒
  const fps = 24; // 帧率
  const frameDuration = animationDuration / fps; // 每帧持续时间
  const framesCount = Math.ceil(animationDuration / frameDuration); // 总帧数
  let count = 0;

  function animateScroll() {
    if (count < framesCount) {
      tags.scrollLeft += scrollAmount / framesCount;
      count++;
      requestAnimationFrame(animateScroll);
    }
  }

  animateScroll();
}
//带参跳转
function open_comic_page(id)
{
  store.commit('SET_CONTENT_PAGE',{key:'comic_page',value:true})
  store.commit('SET_SINGLE_PAGE_STATUS',{key:'content_index_page',value:true})
  store.commit('SET_WORK_ID',id)
}
</script>

<style scoped>
.cartoon_page {
  display: flex;
  flex-direction: column;
  width: 80%;
  height: auto;
  margin: 0 auto;
  margin-top: 20px;
  position: relative;
  gap: 20px;
}



</style>