<template>
  <div class="user_search_result" v-if="user_info">
    <div class="user_info">
      <div class="avatar">
        <img
          :src="
            api.s_base_url + 'image/avatar_thumbnail/' + user_info.user_avatar
          "
          alt="用户头像"
        />
      </div>
      <div class="user_name">
        <span>{{ user_info.username }}</span>
      </div>
      <div class="follow" :class="{is_follow:user_info.follow_status}" @click="follow_user(user_info.userid)">
        <span>{{ user_info.follow_status ? "已关注" : "关注" }}</span>
      </div>
    </div>
    <div class="select_work">
      <div
        class="work_cover"
        v-for="(value, key, index) in work_info"
        :key="index"
      >
        <div class="img" v-if="key == 'ill' || key == 'comic'">
          <div class="img_container" v-for="(item, i) in value" :key="i">
            <img
              :src="
                api.s_base_url +
                'image/content_thumbnail/' +
                item.content_file_list.split(/[\[,\，\]]/).filter(Boolean)[0]
              "
              alt="作品封面"
              @click="to_work_detail(item.work_id, key)"
            />
          </div>
        </div>
        <div class="img" v-if="key == 'novel'">
          <div class="img_container" v-for="(item, i) in value" :key="i">
            <img
              :src="
                api.s_base_url + 'image/content_thumbnail/' + item.work_cover
              "
              alt="作品封面"
              @click="to_work_detail(item.work_id, key)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, defineProps, onMounted, computed, defineEmits } from "vue";
import { useRouter } from "vue-router";
import { BaseApi } from "@/base_api";
const router = useRouter();
const api = new BaseApi();
let user_info = ref();
let work_info = ref({});
const props = defineProps({
  userid: {
    type: String,
    default: "",
  },
});
const emit = defineEmits(["close"]);
//获取用户信息
async function get_user_info(id) {
  let res = await api.post("GetUserInfo/GetUserInfoById", {
    user_id: id,
  });
  if (res.status == 200) {
    return res.result.data;
  } else {
    console.log("获取用户信息失败", res.result);
  }
}
//获取前三个用户的精选作品
async function get_select_work(id, type) {
  try {
    if (type == "ill") {
      let res = await api.post("get_work_info/GetIllInfo/", {
        work_id: id,
      });
      if (res.status == 200) {
        return res.result.data[0] || {};
      } else {
        console.log("获取插画信息失败", res.result);
      }
    }
    if (type == "comic") {
      let res = await api.post("get_work_info/GetComicinfo/", {
        work_id: id,
      });
      if (res.status == 200) {
        return res.result.data[0] || {};
      } else {
        console.log("获取漫画信息失败", res.result);
      }
    }
    if (type == "novel") {
      let res = await api.post("get_work_info/GetNovelInfo/", {
        work_id: id,
      });
      if (res.status == 200) {
        return res.result.data[0] || {};
      } else {
        console.log("获取小说信息失败", res.result);
      }
    }
  } catch (err) {
    console.log("获取用户精选作品失败", err);
  }
}
//关注用户
async function follow_user(user_id) {
    let res=await api.add_follow(user_id);
    user_info.value.follow_status = !user_info.value.follow_status;
}

//跳转内容详情页
function to_work_detail(id, type) {
  if (type == "ill") {
    router.push(`/ill_content?id=${id}`);
  }
  if (type == "comic") {
    router.push(`/comic_content?id=${id}`);
  }
  if (type == "novel") {
    router.push(`/novel_content?id=${id}`);
  }
  emit("close");
}

onMounted(async () => {
  user_info.value = await get_user_info(props.userid);
  user_info.value["follow_status"] = await api.get_follow_status(props.userid);
  if (user_info.value.select_work != null) {
    user_info.value.select_work = JSON.parse(user_info.value.select_work);

    let totalCount = 0; // 记录总共已获取的作品数
    work_info.value = {}; // 初始化作品信息对象

    // 遍历字典键和值
    for (let [key, value] of Object.entries(user_info.value.select_work)) {
      if (totalCount >= 3) break; // 如果已达到 3 个作品，提前结束循环

      work_info.value[key] = [];

      for (let i = 0; i < user_info.value.select_work[key].length; i++) {
        if (totalCount >= 3) break; // 如果已达到 3 个作品，停止获取

        work_info.value[key].push(
          await get_select_work(user_info.value.select_work[key][i], key)
        );
        totalCount++; // 记录已获取的作品数量
      }
    }
  }
});
</script>

<style scoped>
.user_search_result {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.user_info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
}

.avatar img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user_name {
  font-size: 1.1em;
  font-weight: 600;
  color: #333;
}

.select_work {
  display: flex;
  gap: 5px;
}

.work_cover {
  display: contents; /* 解除容器层级限制 */
}
.img {
  display: flex;
  gap: 5px;
}
.img_container {
  position: relative;
  width: 100%;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.img_container:hover {
  transform: translateY(-2px);
  cursor: pointer;
}

.img_container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center center;
  max-height: 200px;
  max-width: 150px;
  min-height: 200px;
  min-width: 150px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .select_work {
    gap: 5px;
  }

  .img_container {
    height: 150px;
  }
}
.follow{
    cursor: pointer;
    padding: 5px 10px;
    background-color: rgb(0, 150, 250);
    font-size: 18x;
    color: white;
    border-radius: 5px;
    transition: all 0.3s;
}
.follow:hover{
    opacity: 0.8;
    transform: scale(1.05);
}
.is_follow{
    background-color: rgb(133,133,133);
    color: white;
}
</style>