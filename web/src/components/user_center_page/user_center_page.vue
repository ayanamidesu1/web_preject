<template>
<div class="user_center_page" v-if="user_info">
  <div class="content">
    <user_background :user_back_img="'https://www.sunyuanling.com/image/content_thumbnail/'+user_info.user_back_img" :token="token"></user_background>
    <user_info_box :user_info="user_info" :token="token"></user_info_box>
    <user_select_box :user_info="user_info" :token="token"></user_select_box>
  </div>
</div>
<go_back></go_back>
</template>
<script setup>
import {defineProps,ref,onMounted} from 'vue';
import { get_userinfo } from './user_center_model/js/get_userinfo.js';
import user_background from './user_center_model/model/user_background.vue';
import user_info_box from './user_center_model/model/user_info_box/user_info.vue' 
import user_select_box from './user_center_model/model/user_select_box/user_select_box.vue';
import go_back from './user_center_model/go_back.vue'
const props=defineProps({
  userid:{
    type:String,
    default:''
  },
  token:{
    type:String,
    default:'sunyuanling'
  }
})
let user_info=ref()
onMounted(async()=>{
  user_info.value=await get_userinfo(props.token)
  user_info.value=user_info.value[0]
  console.log(user_info.value)
})
</script>

<style scoped>

</style>
