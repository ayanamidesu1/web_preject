<template>
  <div class="send_msg_box">
    <div class="user_avatar">
        <img class="avatar_img" :src="'https://www.sunyuanling.com/image/avatar_thumbnail/'+user_avatar_path">
    </div>
    <auto_textarea v-model="content"></auto_textarea>
    <div class="send_btn" @click="send_msg">
        <span>发送</span>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, toRefs, watch, onMounted, onUnmounted ,defineProps,defineEmits} from 'vue';
import auto_textarea from './auto_textarea.vue'
const props =defineProps({
    user_avatar_path:{
        type:String,
        default:'work_like.svg'
    },
    msg_info:{
      type:Object,
      default:()=>{
        return {
          work_id:'',
          work_type:'',
          token:'',
          send_userid:'',
          is_root_comment:'',
          content:'',
          main_userid:'',
          main_comment_id:'',
          reply_comment_id:''
        }
      }
    }
    
})
const emit=defineEmits(['send_msg','msg_info','send_ready_ok'])
let content=ref('')
//发送消息
 const  send_msg=async ()=>{
    emit('send_msg',content.value)
    emit('msg_info',props.msg_info)
    emit('send_ready_ok',true)
    content.value=''
}
watch(content,()=>{
  if(content.value!=''&&content.value){
    emit('send_msg',content.value)
    emit('msg_info',props.msg_info)
  }
})
</script>

<style scoped>
  .send_msg_box{
    display: flex;
    flex-direction: row;
    gap: 10px;
    width: 100%;
    height: 100%;
    align-items: center;
  }
  .user_avatar{
    width: 50px;
    height: 50px;
    display: flex;
    overflow: hidden;
    min-width: 50px;
    min-height: 50px;
  }
  .user_avatar img{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
  }
  .send_btn{
    width: auto;
    height: auto;
    display: flex;
    padding: 5px 10px;
    min-width: 40px;
    cursor: pointer;
    background-color: rgba(0,150,255,1);
    border-radius: 10px;
    color: white;
    align-items: center;
    justify-content: center;
    font-weight: bold;
  }
  .send_btn:hover{
    opacity: 0.8;
    transition: all 0.3s ease-in-out;
  }
</style>