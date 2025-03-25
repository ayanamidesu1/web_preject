<script setup>
import { ref, defineProps, onMounted } from 'vue'
import send_msg_box from './model/send_msg_box.vue';
import msg_box from './model/msg_box/msg_box.vue';
import { get_comment, add_comment } from '../../../assets/js/get_comment';
let props = defineProps({
  work_type: {
    type: String,
    default: 'ill'
  },
  work_id: {
    type: [String,Number],
    default: 1
  },
  token: {
    type: String,
    default: ''
  },
  user_avatar_path: {
    type: String,
    default: 'work_like.svg'
  }
})
//接收评论消息
let limit = ref(5)
let offset = ref(0)
async function receive_msg(msg) {
  msg_info.value.content = msg
  if (send_ready_ok_status.value) {
    await add_comment(props.work_id, props.work_type, token, msg_info.value.send_userid,
      msg_info.value.is_root_comment, msg_info.value.content, msg_info.value.main_userid,
      msg_info.value.main_comment_id, msg_info.value.reply_comment_id)

  }
  send_ready_ok_status.value = false
}
//获取服务器评论消息
let comment_list = ref()
onMounted(async () => {
  comment_list.value = await get_comment(String(props.work_id), props.work_type, props.token)
})
//获取更多评论
async function get_more_comment() {
  limit.value += 3;
  //offset.value+=3;
  comment_list.value = await get_comment(String(props.work_id), props.work_type, props.token, limit.value, offset.value)
}
let token = 'sunyuanling'
//组建发送的消息结构
let msg_info = ref({
  work_id: props.work_id,
  work_type: props.work_type,
  token: token,
  send_userid: '',
  is_root_comment: 1,
  content: '',
  main_userid: 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb',
  main_comment_id: 0,
  reply_comment_id: 0,
  limit: limit.value,
  offset: offset.value
})
let sub_reply_comment = ref()
let sub_msg_ready_ok_status = ref(false)
async function get_sub_msg_ready_ok_status(status) {
  sub_msg_ready_ok_status.value = status
  await add_comment(props.work_id, props.work_type, token, '', sub_reply_comment.value.is_root_comment,
    sub_reply_comment.value.content, sub_reply_comment.value.main_userid, sub_reply_comment.value.main_comment_id,
    sub_reply_comment.value.reply_comment_id
  )
}
function get_sub_reply_comment(item) {
  sub_reply_comment.value = item
}
let send_ready_ok_status = ref(false)
async function get_send_ready_ok_status(status) {
  send_ready_ok_status.value = status
  await add_comment(props.work_id, props.work_type, token, msg_info.value.send_userid,
    msg_info.value.is_root_comment, msg_info.value.content, msg_info.value.main_userid,
    msg_info.value.main_comment_id, msg_info.value.reply_comment_id)
}
</script>

<template>
  <div class="index">
    <div class="title">
      <span>评论</span>
    </div>
    <div class="content">
      <send_msg_box @send_msg="receive_msg" :user_avatar_path="user_avatar_path" :msg_info="msg_info"
        @send_ready_ok="get_send_ready_ok_status"></send_msg_box>
      <msg_box :comments="comment_list" @get_more_comment="get_more_comment()" :work_id="work_id" :work_type="work_type"
        :token="token" :user_avatar_path="user_avatar_path" @send_reply_msg="get_sub_reply_comment"
        @sub_msg_ready_ok="get_sub_msg_ready_ok_status" v-if="comment_list"></msg_box>
    </div>
  </div>
</template>

<style scoped>
.index {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-top: 1px solid rgba(133, 133, 133, 1);
}
</style>
