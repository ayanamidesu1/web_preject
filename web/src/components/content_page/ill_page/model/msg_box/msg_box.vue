<template>
  <div class="comments-section">
    <!-- 渲染主评论 -->
    <div v-for="item in visibleMainComments" :key="item.comment_id" class="msg_box">
      <div class="content" :class="item.is_main ? '' : 'is_reply'">
        <div class="user_info">
          <div class="avatar">
            <img :src="'https://www.sunyuanling.com/image/avatar_thumbnail/' + item.user_avatar" alt="avatar">
          </div>
        </div>
        <div class="msg_content">
          <div class="username" @click="enter_user_home(item.userid)">
            <span>{{ item.username }}</span>
          </div>
          <div class="msg_text">
            <span>{{ item.msg_content }}</span>
          </div>
          <div class="msg_time">
            <span>{{ item.time }}</span>
            <div class="like" @click="like_comment(item.comment_id,'like',props.token,props.work_type,props.work_id)">
              <img class="icon" 
              :src="item.user_is_like_comment[0]? 'https://www.sunyuanling.com/assets/is_hand_like.svg':
              'https://www.sunyuanling.com/assets/hand_like.svg'"
              style="width: 15px;height:15px;">
            </div>
            <div class="like_count">
              <span>{{item.like_comment_count}}</span>
            </div>
           
            <span class="reply_btn" @click="toggleReplyBox(item.comment_id, true)">回复</span>
          </div>
          <div class="reply_box" v-if="replyBoxVisible[item.comment_id]">
            <send_msg_box :user_avatar_path="props.user_avatar_path" @send_msg="handleSendMsg" :msg_info="{
              work_id:props.work_id,
              work_type:props.work_type,
              token:props.token,
              is_root_comment:0,
              content:msg_content,
              main_userid:item.userid,
              main_comment_id:item.comment_id,
              reply_comment_id:item.comment_id
            }" @msg_info="get_msg_info" @send_ready_ok="get_send_ready_ok_status"></send_msg_box>
          </div>
          <!-- 渲染子评论 -->
          <div v-if="item.replies.length > 0">
            <div v-for="reply in visibleReplies(item.replies)" :key="reply.comment_id" class="msg_box is_reply">
              <div class="content">
                <div class="user_info">
                  <div class="avatar">
                    <img :src="'https://www.sunyuanling.com/image/avatar_thumbnail/' + reply.user_avatar" alt="avatar">
                  </div>
                </div>
                <div class="msg_content">
                  <div class="username" @click="enter_user_home(reply.userid)">
                    <span>{{ reply.username }}</span>
                  </div>
                  <div class="msg_text">
                    <span style="margin-right: 10px;color:rgba(0,150,250,1);cursor:pointer;">@{{reply.reply_username}}</span>
                    <span>{{ reply.msg_content }}</span>
                  </div>
                  <div class="msg_time">
                    <span>{{ reply.time }}</span>
                    <div class="like" @click="like_comment(reply.comment_id,'like',props.token,props.work_type,props.work_id)">
                      <img class="icon" 
                      :src="reply.user_is_like_comment? 'https://www.sunyuanling.com/assets/is_hand_like.svg':
                      'https://www.sunyuanling.com/assets/hand_like.svg'"
                      style="width: 15px;height:15px;">
                    </div>
                    <div class="like_count">
                      <span>{{reply.like_comment_count}}</span>
                    </div>
                    <span class="reply_btn" @click="toggleReplyBox(reply.comment_id, false)">回复</span>
                  </div>
                  <div class="reply_box" v-if="replyBoxVisible[reply.comment_id]">
                    <send_msg_box :user_avatar_path="props.user_avatar_path" @send_msg="handleSendMsg" 
                    :msg_info="{
                      work_id:props.work_id,
                      work_type:props.work_type,
                      token:props.token,
                      is_root_comment:0,
                      content:msg_content,
                      main_userid:item.userid,
                      main_comment_id:item.comment_id,
                      reply_comment_id:reply.comment_id
                    }" @msg_info="get_msg_info" @send_ready_ok="get_send_ready_ok_status"></send_msg_box>
                  </div>
                </div>
              </div>
            </div>
            <!-- 显示查看更多子评论按钮 -->
            <div class="show_more_sub_comment" v-if="item.replies.length > subCommentMax">
              <span @click="addSubCommentMax">查看更多</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 显示查看更多主评论按钮 -->
    <div class="show_more_root_comment" v-if="comments.length >= maxRootComment" @click="addMaxRootComment">
      <span >查看更多</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps,defineEmits, watch } from 'vue';
import send_msg_box from '../send_msg_box.vue';
import {like_comment} from '../../../../../assets/js/get_comment'

import { useStore } from 'vuex';
const store = useStore();
//进入指定用户的用户中心
function jump_to_other_user_center(userid,item)
{
  store.commit('SET_OTHER_USERID',userid)
  store.commit('SET_SINGLE_PAGE_STATUS',{'key':'other_user_center_page','value':true})
  console.log(userid)
  console.log(item)
}

const props = defineProps({
  comments: {
    type: Array,
    default: () => []
  },
  work_id:{
    type: String,
    default: '1'
  },
  work_type:{
    type: String,
    default: 'ill'
  },
  token:{
    type:String,
    default: ''
  },
  user_avatar_path: {
    type: String,
    default: 'work_like.svg'
  },
});
let emit=defineEmits(['get_more_comment','send_reply_msg','sub_msg_ready_ok'])
function get_more_comment(){
  emit('get_more_comment')
}
const replyBoxVisible = ref({}); // 用于跟踪哪个评论的回复框是可见的
let msg_content=ref('')
let msg_info=ref({
  content:'',
  is_root_comment:0,
  main_comment_id:0,
  main_userid:'',
  reply_comment_id:0,
  token:'',
  work_id:'',
  work_type:''
})
let send_ready_ok_status=ref(false)
function get_send_ready_ok_status(item)
{
  send_ready_ok_status.value=item
  emit('sub_msg_ready_ok',send_ready_ok_status.value)
}

function get_msg_info(item)
{
  let temp=msg_info.value
  let temp_content=temp.content
  //删除item中的content
  delete item.content
  msg_info.value=item
  msg_info.value.content=temp_content
}

// 切换回复框的可见性
function toggleReplyBox(commentId, isMain) {
  // 展开前先隐藏所有回复框
  Object.keys(replyBoxVisible.value).forEach(key => {
    replyBoxVisible.value[key] = false;
  });
  
  // 如果是主评论，先隐藏所有子评论的回复框
  if (isMain) {
    Object.keys(replyBoxVisible.value).forEach(key => {
      if (key !== commentId) {
        replyBoxVisible.value[key] = false;
      }
    });
  }

  // 切换当前评论的回复框状态
  replyBoxVisible.value[commentId] = !replyBoxVisible.value[commentId];
}

// 处理发送消息的逻辑
function handleSendMsg(item) {
  // 处理发送消息的逻辑，并可能更新评论列表
  msg_content.value=item
  msg_info.value.content=item
  emit('send_reply_msg',msg_info.value)
}
watch(msg_content,()=>{
  
})

// 最大渲染主评论数量
const maxRootComment = ref(1);
// 最大渲染子评论数量
const subCommentMax = ref(1);

// 增加渲染主评论数量
function addMaxRootComment() {
  maxRootComment.value += 3;
  get_more_comment();
}

// 增加渲染子评论数量
function addSubCommentMax() {
  subCommentMax.value += 3;
}

// 获取可见的主评论
const visibleMainComments = computed(() => {
  return props.comments.slice(0, maxRootComment.value);
});

// 获取可见的子评论
function visibleReplies(replies) {
  return replies.slice(0, subCommentMax.value);
}
//通过评论ID进入用户主页接口准备
function enter_user_home(userid) {
  console.log(userid)
  jump_to_other_user_center(userid,'')
}
</script>
  
  <style scoped>
  /* 添加你的样式 */
  .is_reply {
    margin-left: 50px;
  }
  
  .comments-section {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .msg_box {
    display: flex;
    flex-direction: row;
    gap: 10px;
    width: 100%;
    height: 100%;
    align-items: center;
    overflow: hidden;
  }
  
  .content {
    display: flex;
    flex-direction: row;
    gap: 10px;
    width: 100%;
    height: 100%;
  }
  
  .user_info {
    display: flex;
    width: 50px;
    height: 50px;
    align-items: center;
    justify-content: center;
  }
  
  .avatar {
    width: 50px;
    height: 50px;
  }
  
  .avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .msg_content {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 100%;
    height: 100%;
    align-items: flex-start;
  }
  
  .username {
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
  }
  
  .msg_text {
    font-size: 14px;
  }
  
  .msg_time {
    font-size: 12px;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 15px;
    width: auto;
  }
  
  .reply_box {
    display: flex;
    width: 100%;
    height: 100%;
    min-width: 150px;
  }
  
  .reply_btn {
    display: flex;
    width: auto;
    height: auto;
    padding: 5px;
    cursor: pointer;
    color: rgba(0,150,250,1);
  }
  
  .reply_btn:hover {
    opacity: 0.6;
    transition: all 0.3s;
  }
  .show_more_root_comment{
    display: flex;
    width: 90%;
    height: auto;

    padding: 5px 10px;
    background-color: rgba(133,133,133,1);
    cursor: pointer;
    border-radius: 10px;
    align-items: center;
    justify-content: center;
    margin: 5px auto;
  }
  .show_more_root_comment:hover{
    opacity: 0.6;
    transition: all 0.3s;
  }
  .show_more_sub_comment{
    display: flex;
    width: auto;
    height: auto;
    max-width: 80px;
    padding: 5px 10px;
    background-color: rgb(87, 230, 255);
    cursor: pointer;
    border-radius: 10px;
    align-items: center;
    justify-content: center;
    margin-left: 50px;
  }
  .show_more_sub_comment:hover{
    opacity: 0.6;
    transition: all 0.3s;
  }
  </style>
  