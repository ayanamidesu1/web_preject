<template>
<div class="user_center_page" v-if="user_info">
  <div class="content">
    <user_background 
    :user_back_img="'https://www.sunyuanling.com/server/static/image/content_thumbnail/'+(user_info.user_back_img?user_info.user_back_img:'20240525174916_f4f4acc7280f4eabb9fc1712929c3ccc.png')" 
    :token="token"></user_background>
    <user_info_box :user_info="user_info" :token="token"></user_info_box>
    <user_select_box :user_info="user_info" :token="token" :userid="user_id"></user_select_box>
  </div>
</div>
</template>
<script setup>
import {defineProps,ref,onMounted,computed} from 'vue';
import { get_userinfo } from './user_center_model/js/get_userinfo.js';
import user_background from './user_center_model/model/user_background.vue';
import user_info_box from './user_center_model/model/user_info_box/user_info.vue' 
import user_select_box from './user_center_model/model/user_select_box/user_select_box.vue';
import go_back from './user_center_model/go_back.vue'
import {useRouter} from 'vue-router'
const router=useRouter()
const props=defineProps({
  userid:{
    type:String,
    default:'10086'
  },
  token:{
    type:String,
    default:''
  }
})
let user_id=computed(()=>{
  return router.currentRoute.value.query.id
})
let user_info=ref()
onMounted(async()=>{
  user_info.value=await get_userinfo(null,user_id.value)
  user_info.value=user_info.value[0]
  console.log(user_info.value)
})
</script>

<style scoped>

</style>
