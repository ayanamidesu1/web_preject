<template>
  <div class="review_msg">
    <div class="content" v-if="is_ready">
      <div class="ill_item" v-if="msg.work_type == 'ill'">
        <div class="title">插画审核消息</div>
        <div class="work_info" v-if="work_info">
          <span
            >作品名称：{{ work_info.name }}&nbsp;作品ID：{{
              work_info.work_id
            }}</span
          >
          <span
            >消息：{{ msg.msg }}&nbsp;审核状态：{{
              msg.work_status == 0 ? "未通过" : "审核通过"
            }}</span
          >
          <span>作品类型：{{ msg.work_type }}</span>
          <img
            :src="
              'https://www.sunyuanling.com/server/static/image/thumbnail/' +get_cover(work_info.content_file_list)            "
            width="100px"
            height="100px"
            alt="插画作品封面"
          />
        </div>
      </div>
      <div class="comic_item" v-if="msg.work_type == 'comic'">
        <div class="title">漫画审核消息</div>
        <div class="work_info" v-if="work_info">
            <span>作品名称：{{work_info.work_name}}&nbsp;作品ID：{{work_info.work_id}}</span>
            <span>消息：{{ msg.msg }}&nbsp;审核状态：{{
              msg.work_status == 0 ? "未通过" : "审核通过"
            }}</span
          >
          <span>作品类型：{{ msg.work_type }}</span>
          <img
            :src="
              'https://www.sunyuanling.com/server/static/image/comic/thumbnail/' +get_cover(work_info.content_file_list)            "
            width="100px"
            height="100px"
            alt="漫画作品封面"
          />
        </div>
      </div>
      <div class="novel_item" v-if="msg.work_type == 'novel'">
        <div class="title">小说审核消息</div>
        <div class="work_info" v-if="work_info">
          <span>作品名称：{{work_info.work_name}}&nbsp;作品连载状态：{{work_info.work_status}}</span>
          <span>作品ID：{{work_info.work_id}}</span>
          <span>消息：{{ msg.msg }}&nbsp;审核状态：{{
            msg.work_status == 0 ? "未通过" : "审核通过"
          }}</span>
          <span>作品类型：{{ msg.work_type }}</span>
          <img :src="'https://www.sunyuanling.com/server/static/image/novel/thumbnail/'+work_info.work_cover" width="100px" height="100px" alt="小说作品封面" />
        </div>
        <div
          class="chapter_list"
          v-if="
            msg.work_type == 'novel' &&
            msg.chapter_id &&
            msg.chapter_id.length > 0
          "
        >
        <span>消息：{{ msg.msg }}&nbsp;审核状态：{{
          msg.work_status == 0 ? "未通过" : "审核通过"
        }}</span
      >
      <div style="display:flex;flex-direction:column;gap:8px;" v-if="work_info.chapter_info.length > 0">
        <span>作品类型：{{ msg.work_type }}</span>
          通过审核的章节列表：<span
            v-for="(item, index) in msg.chapter_id"
            :key="index"
            >章节ID：{{ item }}&nbsp;章节名称：{{work_info.chapter_info[index].title}}</span>
      </div>
        </div>
      </div>
      <span>{{api.formatTimeAgo(time)}}</span>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, defineProps } from "vue";
import { BaseApi } from "@/base_api";
import { useRouter } from "vue-router";
import base_api from "@assets/model/comment_box/ts/base_api";

let is_ready = ref(false);
const api = new BaseApi();
const props = defineProps({
  msg: {
    type: Object,
    default: () => {
      return {
        work_id: 3,
        work_status: 1,
        work_type: "ill",
        msg_type: "ill_review",
        msg: "作品审核通过",
      };
    },
  },
  time:{
    type:String,
  }
});

let work_info = ref({
  chapter_info: [],
});

//获取封面
function get_cover(files) {
  try {
    let cover_url = "";
    if (files && files.length > 0) {
      cover_url = files.split(/[,，]/)[0];
    }
    return cover_url;
  } catch (e) {
    console.warn("获取封面失败", e);
    return "";
  }
}

//获取插画信息
async function get_ill_info() {
  let data = await api.post("get_work_info/GetIllInfo/", {
    work_id: props.msg.work_id,
  });
  if (data.status == 200) {
    work_info.value = data.result.data[0];
  } else {
    console.warn("获取插画信息失败", data);
  }
}
//获取漫画信息
async function get_comic_info() {
  let data = await api.post("get_work_info/GetComicinfo/", {
    work_id: props.msg.work_id,
  });
  if (data.status == 200) {
    work_info.value = data.result.data[0];
  } else {
    console.warn("获取漫画信息失败", data);
  }
}
//获取小说信息
async function get_novel_info() {
  let data = await api.post("get_work_info/GetNovelInfo/", {
    work_id: props.msg.work_id,
  });
  if (data.status == 200) {
    work_info.value = data.result.data[0];
  } else {
    console.warn("获取小说信息失败", data);
  }
}
//获取章节作品的章节信息
async function get_chat_info(work_id, chapter_id) {
  let data = await api.post("get_work_info/GetChapterInfo", {
    work_id: work_id,
    chapter_id: chapter_id,
  });
  if (data.status == 200) {
    return data.result.data;
  } else {
    console.warn("获取章节信息失败", data);
  }
}
onMounted(async () => {
  if (props.msg.work_type == "ill") {
    console.log("获取插画信息");
    get_ill_info();
    is_ready.value = true;
    return;
  } else if (props.msg.work_type == "comic") {
    console.log("获取漫画信息");
    get_comic_info();
    is_ready.value = true;
    return;
  } else if (props.msg.work_type == "novel") {
    console.log("获取小说信息");
    get_novel_info();
    if (props.msg.chapter_id && props.msg.chapter_id.length > 0) {
      console.log("获取章节信息");
      let temp_arr = [];
      for (let i = 0; i < props.msg.chapter_id.length; i++) {
        let res = await get_chat_info(
          props.msg.work_id,
          props.msg.chapter_id[i]
        );
        console.log("章节信息", res);
        temp_arr.push(res);
      }
      work_info.value.chapter_info = temp_arr;
    }
    is_ready.value = true;
    return;
  } else {
    console.warn("未知作品类型", props.msg.work_type);
  }
});
</script>

<style scoped>
.review_msg {
  width: calc(100% - 50px);
  min-width: 300px;
  padding: 10px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.content {
  display: grid;
  gap: 24px;
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a1a;
  padding-bottom: 8px;
  border-bottom: 2px solid #f0f0f0;
  margin-bottom: 16px;
}

.work_info {
  display: grid;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.work_info > span {
  display: flex;
  gap: 8px;
  font-size: 0.9rem;
  color: #4a4a4a;
  line-height: 1.5;
}

.work_info img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #eee;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.chapter_list {
  display: grid;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 16px;
}

.chapter_list > span {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #fff;
  border-radius: 6px;
  border: 1px solid #eee;
  font-size: 0.85rem;
  margin: 4px 0;
}

/* 审核状态样式 */
.status-tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-approved {
  background: #e6f4ea;
  color: #0d6832;
}

.status-rejected {
  background: #fde8e8;
  color: #c5221f;
}

/* 时间样式 */
.time {
  font-size: 0.8rem;
  color: #8c8c8c;
  text-align: right;
  margin-top: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .review_msg {
    padding: 12px;
    margin: 12px;
  }

  .work_info > span {
    flex-direction: column;
    gap: 4px;
  }

  .chapter_list > span {
    flex-wrap: wrap;
  }
}

/* 加载动画 */
@keyframes loading {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

.loading-placeholder {
  animation: loading 1.5s ease-in-out infinite;
  background: #f0f0f0;
  border-radius: 8px;
  min-height: 120px;
}
</style>