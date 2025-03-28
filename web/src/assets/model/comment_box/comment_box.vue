<template>
  <div class="comment_box">
    评论区
    <user_box></user_box>
    <div class="comment_list">
      <div
        class="comment_item"
        v-for="(item, index) in comment_list"
        :key="index"
      >
        <div class="main_reply" v-if="item.is_main" :key="item.comment_id">
          <comment
            :user="item.user"
            :comment_info="item"
            :comment_index="[index, null]"
            @send_comment="add_sub_reply"
            :total="main_comment_total"
            :limit="limit"
            :offset="offset"
            :index="index"
          ></comment>
          <div
            class="reply_list"
            v-if="item.reply_list && item.reply_list.length > 0"
            :class="{ is_sub_reply: !is_reply(item) }"
            :key="item.temp_key"
          >
            <div
              class="reply_item"
              v-for="(reply_item, reply_index) in item.reply_list"
              :key="reply_index"
            >
              <comment
                :user="reply_item.user"
                :comment_info="reply_item"
                :comment_index="[index, reply_index]"
                @send_comment="add_sub_reply"
              ></comment>
              <div class="show_more" v-if="reply_index>=(item.reply_limit+item.reply_offset-1)"
                @click="get_more_reply_comment(item.comment_id,item.reply_offset,item.reply_limit)">
                <span>查看更多{{ item.reply_total-item.reply_limit>0?item.reply_total-item.reply_limit:0 }}条回复</span>
              </div>
            </div>
          </div>
          <div class="show_more" v-if="index >= (limit + offset - 1)" @click="get_more_main_comment()">
            <span>查看更多</span>
          </div>
        </div>
      </div>
    </div>
    <float_msg></float_msg>
  </div>
</template>


<script setup>
import { ref, defineProps, computed, watch, onMounted } from "vue";
import user_box from "./user_box.vue";
import comment from "./comment.vue";
//导入uuid生成库
import { v4 as uuidv4 } from "uuid";
import { useCommentStore } from "./store";
import float_msg from "./float_msg.vue";
import { debounce } from "lodash";
import { add_comment, get_comment,get_more_reply } from "./ts/operate_comment";
import {useStore} from '@assets/model/store/index'
const store = useStore();

//const store = useStore();
const commentStore = useCommentStore();

let user = computed(()=>{
  return store.$state.user;
})

const props = defineProps({
  //传入作品信息,work_id,work_type
  item: Object,
});
console.log(props.item);
//主评论索引
let comment_index = computed(() => commentStore.$state.comment_index);

//主评论总数，limit，offset
let main_comment_total = computed(() => commentStore.main_comment_info.total);
let limit = computed(() => commentStore.main_comment_info.limit);
let offset = computed(() => commentStore.main_comment_info.offset);

function is_reply(item) {
  if (item.reply_list) {
    if (item.reply_list[0].is_main == 0) {
      console.log("is_sub_reply");
      return false;
    } else {
      return true;
    }
  } else {
    return false;
  }
}

let comment_list = ref([]);

//增加主评论
watch(
  () => commentStore.main_reply,
  debounce((newVal) => {
    console.log(newVal);
    add_main_reply(newVal);
  }, 300) // 设置 300ms 的防抖时间
);
async function add_main_reply(reply) {
  console.log(reply);
  if (!reply || !reply.content || reply.content.trim() === "") {
    //commentStore.set_comment_global_msg("评论不能为空");
    return;
  }
  let comment = {
    content: reply.content,
    is_main: true,
    reply_comment_id: null,
    reply_work_id: props.item.work_id,
    reply_work_type: props.item.work_type,
    reply_user_id: null,
  };
  const res = await add_comment(comment);
  let new_comment_id = "";
  if (res.code == 200) {
    commentStore.set_main_reply("新增主评论成功");
    new_comment_id = res.data.comment_id;
  } else {
    commentStore.set_main_reply(res.msg);
    return;
  }
  let new_comment = {
    temp_key: uuidv4(), // 唯一的temp_key
    comment_id: new_comment_id|| uuidv4(), // 唯一的comment_id
    content: reply.content, // 评论内容
    create_time: new Date().toISOString(), // 当前时间
    user_id: user.value.userid, // 当前用户ID
    like_count: 0,
    is_like: false,
    is_main: true, // 标记为主评论
    reply_comment_id: null, // 父评论ID
    reply_work_id: 1, // work_id
    reply_work_type: "forum", // work_type
    user: {
      username: user.value.username,
      avatar: user.value.user_avatar,
      user_id: user.value.userid,
    },
    reply_list: [], // 子评论列表
    reply_limit: 3,
    reply_offset: 0,
    reply_total: 0,
    main_reply_total: 0,
  };
  comment_list.value.unshift(new_comment);
}
//增加子评论
async function add_sub_reply(reply) {
  if (!reply || !reply.content || reply.content.trim() === "") {
    commentStore.set_comment_global_msg("评论不能为空");
    return;
  }
  let parent_comment = comment_list.value[comment_index.value[0]];
  let comment = {
    content: reply.content,
    is_main: false,
    reply_comment_id: parent_comment.comment_id,
    reply_work_id: props.item.work_id,
    reply_work_type: props.item.work_type,
    reply_user_id: reply.user_id,
  };
  const res = await add_comment(comment);
  let new_comment_id = "";
  if (res.code == 200) {
    commentStore.set_comment_global_msg("新增子评论成功");
    new_comment_id = res.data.comment_id;
  } else {
    commentStore.set_comment_global_msg(res.msg);
    return;
  }
  console.log(reply);
  let username = user.username;
  let avatar = user.avatar;
  let user_id = user.id;
  //查找父评论
  console.log(comment_index.value);
  //构建子评论并插入栈顶
  const new_reply = {
    temp_key: uuidv4(), // 唯一的temp_key
    comment_id: new_comment_id || uuidv4(), // 唯一的comment_id
    content: reply.content, // 子评论内容
    create_time: new Date().toISOString(), // 当前时间
    user_id: user.value.userid, // 当前用户ID
    like_count: 0,
    is_like: false,
    is_main: false, // 标记为子评论
    reply_comment_id: parent_comment.comment_id, // 回复的父评论ID
    reply_work_id: parent_comment.reply_work_id, // 父评论的work_id
    reply_work_type: parent_comment.reply_work_type, // 父评论的work_type
    user: {
      username: user.value.username,
      avatar: user.value.user_avatar,
      user_id: user.value.userid,
    },
    reply_user: {
      username: reply.username,
      avatar: reply.avatar,
      user_id: reply.user_id,
    },
  };
  parent_comment.reply_list.unshift(new_reply); // 将子评论插入到父评论的reply_list中
  parent_comment.reply_total++; // 增加父评论的reply_total
  parent_comment.main_reply_total++; // 增加父评论的main_reply_total
  console.log(comment_list.value);
  commentStore.set_comment_global_msg("新增子评论成功");
}

//请求更多主评论
async function get_more_main_comment() {
  // 1. 检查 main_comment_info 是否已经初始化
  if (!commentStore.main_comment_info) {
    console.error('main_comment_info 未初始化');
    return;
  }

  // 2. 计算新的偏移量
  let temp_offset = commentStore.main_comment_info.offset + commentStore.main_comment_info.limit;

  // 3. 检查必需参数是否存在
  if (!props.item.work_id || !props.item.work_type) {
    console.error('缺少必要参数 work_id 或 work_type');
    return;
  }

  try {
    // 4. 发起请求
    let res = await get_comment(props.item.work_id, props.item.work_type, commentStore.main_comment_info.limit, temp_offset);

    if (res.code === 200) {
      // 更新评论信息
      commentStore.set_main_comment_info(parseInt(res.data.total), temp_offset, commentStore.main_comment_info.limit);

      // 将新评论追加到已有列表
      comment_list.value.push(...(res.data.comments || []));

      console.log(res.data);
    } else {
      console.error('获取评论失败:', res.msg);
    }
  } catch (error) {
    console.error('请求主评论时发生错误:', error);
  }
}


//加载更多子评论
async function get_more_reply_comment(comment_id,offset,limit){
  try{
    console.log(comment_id,offset,limit);
    let temp_offset=offset+limit;
    let res=await get_more_reply(comment_id,limit,temp_offset);
    if(res.code==200){
      //查找对应ID的主评论
      let parent_comment = comment_list.value.find((comment) => comment.comment_id === comment_id);
      if (!parent_comment) {
        console.error('未找到对应的父评论');
        return;
      }
      //压入reply_list的栈低
      parent_comment.reply_list.push(...res.data);
      parent_comment.reply_total=parseInt(res.total);
      parent_comment.reply_offset=temp_offset;
      parent_comment.reply_total=parseInt(res.total);
      //console.log(res.data);
      console.log(comment_list.value);
    }
    else{
      console.log(res.msg);
    }
  }
  catch(e)
  {
    console.log(e);
  }
}

onMounted(async function () {
  let res = await get_comment(props.item.work_id, props.item.work_type);
  if (res.code == 200) {
    comment_list.value = res.data.comments;
    commentStore.set_main_comment_info(parseInt(res.data.total), 0, 3);
    console.log(res.data);
  } else {
    console.log(res.msg);
  }
});
</script>

<style scoped>
.comment_box {
  width: 100%;
  height: fit-content;
  display: flex;
  flex-direction: column;
  gap: 5px;
  background-color: rgba(233, 233, 233, 0.5);
  padding: 5px;
  border-radius: 5px;
}
.is_sub_reply {
  margin-left: 30px;
}
.show_more {
  display: flex; /* 居中 */
  justify-content: center;
  align-items: center;
  width: fit-content; /* 适配容器宽度 */
  min-width: 100px;
  margin: 10px 0; /* 上下留白 */
  padding: 10px 20px; /* 内边距 */
  background-color: #f0f0f0; /* 背景颜色 */
  border: 1px solid #ddd; /* 边框 */
  border-radius: 5px; /* 圆角 */
  color: #333; /* 字体颜色 */
  font-size: 14px; /* 字体大小 */
  cursor: pointer; /* 鼠标样式 */
  transition: background-color 0.3s, color 0.3s, box-shadow 0.3s; /* 动画效果 */
}

.show_more:hover {
  background-color: #e0e0e0; /* 悬停时背景颜色 */
  color: #000; /* 悬停时字体颜色 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* 悬停时阴影 */
}

.show_more:active {
  background-color: #d0d0d0; /* 点击时背景颜色 */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1); /* 点击时内阴影 */
}
</style>