<template>
  <div class="comment" v-if="comment_info && user">
    <div class="user_box" @click="to_usercenter(comment_info.user.user_id)">
      <div class="user_avatar">
        <img
          alt="头像"
          :src="'https://www.sunyuanling.com/server/static/image/avatar_thumbnail/' + (comment_info.user.avatar||'default.jpg')"
        />
      </div>
      <div class="username" @click="go_to_other_usercenter(comment_info.user.id)">
        <span>{{ comment_info.user.username }}</span>
      </div>
    </div>
    <div class="comment_box">
      <div class="comment_content">
        <div class="reply_user" v-if="comment_info.reply_user" @click="to_usercenter(comment_info.reply_user.user_id)">
          {{
            comment_info.reply_user ? '@'+comment_info.reply_user.username+':' : null
          }}
        </div>
        <div v-html="restore_html(comment_info.content)"></div>
      </div>
      <div class="comment_info">
        <span class="send_time">
          {{api.formatTimeAgo(comment_info.create_time) }}
        </span>
        <div class="comment_interaction">
          <div class="btn" @click="comment_like(comment_info.comment_id)">
            <span
              >{{
                comment_info.like_count ? comment_info.like_count : 0
              }}
              点赞</span
            >
            <img
              :src="comment_info.is_like?'https://www.sunyuanling.com/server/static/svg/已点赞.svg':'https://www.sunyuanling.com/server/static/svg/点赞.svg'"
              alt="点赞"
              class="icon"
            />
          </div>
          <div class="btn" @click="set_comment_index()">
            <span>回复</span>
            <img
              src="https://www.sunyuanling.com/server/static/svg/留言.svg"
              alt="回复"
              class="icon"
            />
          </div>
        </div>
      </div>
      <transition name="fade">
        <div v-if="input_show" class="comment_input">
          <input_index @content="get_comment_content"></input_index>
        </div>
      </transition>
    </div>
  </div>
</template>
  

<script setup>
import { ref, defineProps, watch, computed, defineEmits } from "vue";
import { useRouter } from "vue-router";
import input_index from "./input_box/input_index.vue";
import {useCommentStore} from './store'
import { like_comment } from "./ts/operate_comment";
import { BaseApi } from "@/base_api";
const api=new BaseApi();

const commentStore = useCommentStore();
const router = useRouter();
//const store = useStore();

const props = defineProps({
  user: {
    type: Object,
    default: () => {
      return {
        username: "test",
        avatar: "default.png",
        user_id: "1",
      };
    },
  },
  comment_info: {
    type: Object,
    default: () => {
      return {
        comment_id: "1",
        content: "test",
        create_time: "2021-01-01",
        user_id: "1",
        like_count: 0,
        is_like: true,
      };
    },
  },
  comment_index: {
    type: Array,
    default: () => {
      return [];
    },
  },
  total: {
    type: Number,
    default: 0,
  },
  limit:{
    type: Number,
    default: 3,
  },
  offset: {
    type: Number,
    default: 0,
  },
  index: {
    type: Number,
    default: 0,
  }
});

const emit = defineEmits(["send_comment"]);

let comment_content = ref();

let user =ref(props.comment_info.user);

let comment_info = ref(props.comment_info);

function get_comment_content(e) {
  let send_user_info=props.comment_info.user;
  comment_content.value = e;
  e.username = send_user_info.username;
  e.user_id = send_user_info.user_id;
  e.avatar = send_user_info.avatar;
  emit("send_comment", e);
}

// 控制展开与收起逻辑
function set_comment_index() {
  // 判断当前索引是否相等以及是否已展开
  if (
    JSON.stringify(now_comment_index.value) ===
    JSON.stringify(props.comment_index)
  ) {
    input_show.value = !input_show.value; // 切换展开/收起
    //更新索引
    if (input_show.value) {
      //store.commit("set_comment_index", props.comment_index); // 更新索引
      commentStore.set_comment_index(props.comment_index); // 更新索引
    }
  } else {
    //store.commit("set_comment_index", props.comment_index); // 更新索引
    commentStore.set_comment_index(props.comment_index); // 更新索引
    input_show.value = true; // 强制展开
  }
}

let now_comment_index = computed(() => commentStore.$state.comment_index);

let input_show = ref(false);
watch(now_comment_index, () => {
  if (
    JSON.stringify(now_comment_index.value) ===
    JSON.stringify(props.comment_index)
  ) {
    input_show.value = true;
  } else {
    input_show.value = false;
  }
});

// 还原HTML
function restore_html(html_text, customStyles = {}) {
  if (!html_text) return "";
  // 默认样式
  const defaultStyles = {
    display: "inline-block",
    width: "16px",
    height: "16px",
    "object-fit": "cover",
    "border-radius": "5px",
    "margin-right": "2px",
    "margin-left": "2px",
    ...customStyles, // 支持动态样式
  };

  // 构建style字符串
  const imgStyle = Object.entries(defaultStyles)
    .map(([key, value]) => `${key}: ${value}`)
    .join("; ");

  // 用正则匹配$$表情包$$占位符并替换为对应的img标签
  let regex = /\$\$ ([^$$]+) \$\$/g;

  return html_text.replace(regex, (match, emojiName) => {
    return `<img src="https://www.sunyuanling.com/server/static/emoji/${emojiName}" alt="${emojiName}" class="emoji" style="${imgStyle}" />`;
  });
}

//其他用户中心跳转
function go_to_other_usercenter(id){
  router.push('/other_user_center'+`?user_id=${id}`)
}


//评论点赞预留接口
async function comment_like(id){
    console.log('评论点赞预留接口：'+id)
    //comment_info.value.is_like = !comment_info.value.is_like;
    let res=await like_comment(id);
    if(res.code==200){
      comment_info.value.is_like=!comment_info.value.is_like
      if(comment_info.value.is_like){
        commentStore.set_comment_global_msg('点赞成功')
        comment_info.value.like_count+=1
      }
      else{
        commentStore.set_comment_global_msg('取消点赞')
        comment_info.value.like_count-=1
      }
    }
    else{
      console.log(res.msg)
    }
}
</script>

<style scoped>
.icon {
  width: 25px;
  height: 25px;
  object-fit: cover;
  display: inline-block;
}
.comment {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 10px;
  transition: all 0.2s;
}
.user_box {
  display: flex;
  flex-direction: row;
  gap: 10px;
  width: fit-content;
  height: 35px;
  align-items: center;
  background-color: rgba(233, 233, 233, 1);
  padding: 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s;
}
.user_box:hover {
  opacity: 0.8;
  transform: scale(1.05);
  background-color: rgba(244, 244, 244, 1);
}
.user_avatar {
  width: 30px;
  height: 30px;
  display: flex;
}
.user_avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}
.username {
  font-size: 17px;
  font-weight: 550;
  font-family: "微软雅黑";
}
.comment_box {
  display: flex;
  flex-direction: column;
  gap: 5px;
  background-color: rgba(233, 233, 233, 1);
  padding: 5px;
  width: calc(100% - 10px);
  height: fit-content;
  border-radius: 5px;
  transition: all 0.2s;
}
.comment_content {
  font-size: 16px;
  font-family: "微软雅黑";
  /*行间距*/
  line-height: 3px;
  text-align: left;
  margin-top: 5px;
  display: flex;
}
.reply_user{
    cursor: pointer;
    color: rgba(0,150,250,1);
    transition: all 0.2s;
}
.reply_user:hover{
    text-decoration-line: underline;
    opacity: 0.8;
}
.comment_info {
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
}
.comment_interaction {
  display: flex;
  flex-direction: row;
  gap: 5px;
  margin-left: 10px;
  align-items: center;
}
.btn {
  display: flex;
  flex-direction: row;
  gap: 3px;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
  padding: 5px;
}
.btn:hover {
  opacity: 0.8;
  background-color: rgba(133, 133, 233, 1);
  border-radius: 5px;
  transform: scale(1.02);
  color: rgb(233, 233, 245);
}
.comment_input {
  transition: all 0.2s;
}
/* Transition 动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>