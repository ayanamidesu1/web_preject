<template>
  <div class="scroll_box">
    <div class="scroll_box_content">
      <div class="btn_box">
        <div class="left_btn" @click="scrollLeft">
          <img :src="props.left_btn" class="icon">
        </div>
        <div class="right_btn" @click="scrollRight">
          <img :src="props.right_btn" class="icon">
        </div>
      </div>
      <div class="list" ref="list">
        <div class="item" v-for="(item, index) in props.msg_list" :key="index">
          <div v-if="props.msg_type === 'image'" class="image_item" @click="chose_item(item.work_info.work_id)">
            <div class="ranking">
              {{ index+1 }}
            </div>
            <img :src="'https://www.sunyuanling.com/image/novel/thumbnail/' + item.work_info.work_cover"
              class="image">
            <div class="age_tag" v-if="item.work_info.age_classification >= 17">R-{{ item.work_info.age_classification }}</div>
          </div>
          <div class="work_info">
            <span>{{ item.work_info.work_name }}</span>
            <div class="brief_introduction">{{item.work_info.brief_introduction}}</div>
            <div class="work_status">
              <span>{{item.work_info.category}}·{{item.work_info.is_vip_work==1?'VIP作品':'免费作品'}}·{{item.work_info.work_status}}</span>
            </div>
            <div class="user_info" @click="jump_to_other_user_center(item.author_info.author_id,item)">
              <div class="user_avatar">
                <img :src="'https://www.sunyuanling.com/image/avatar_thumbnail/' + item.author_info.author_avatar">
              </div>
              <div class="username">
                <span>{{ item.author_info.author_username }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, defineEmits } from 'vue';
import { useStore } from 'vuex';
const store = useStore();

const props = defineProps({
  left_btn: {
    type: String,
    default: 'https://www.sunyuanling.com/assets/left.svg'
  },
  right_btn: {
    type: String,
    default: 'https://www.sunyuanling.com/assets/right.svg'
  },
  msg_type: {
    type: String,
    default: 'image'
  },
  msg_list: {
    type: Array,
    default: () => []
  },
  animationDuration: {
    type: Number,
    default: 500 // Default animation duration in ms
  },
  scrollDistance: {
    type: Number,
    default: 400 // Default scroll distance in px
  }
});

const colorArr = ref([
  'rgb(126, 183, 200)', 'rgb(126, 186, 200)', 'rgb(157, 200, 126)', 'rgb(200, 126, 170)', 'rgb(200, 126, 146)',
  'rgb(126, 129, 200)', 'rgb(167, 126, 200)', 'rgb(200, 170, 126)', 'rgb(126, 200, 167)', 'rgb(126, 200, 129)'
]);

const tags_item = ref(null);
const list = ref(null);

const set_tag_color = () => {
  if (tags_item.value) {
    tags_item.value.forEach((item, index) => {
      item.style.backgroundColor = colorArr.value[index % colorArr.value.length];
    });
  }
};

const emit = defineEmits(['chose_item']);
const chose_item = (item) => {
  emit('chose_item', item);
  store.commit('SET_CONTENT_PAGE', {
    key: 'novel_page',
    value: true
  })
  store.commit('SET_SINGLE_PAGE_STATUS',{key:'content_index_page',value:true})
  store.commit('SET_WORK_ID',item)
  store.commit('SET_WORK_TYPE','novel')
};

// Easing function for smooth animation
const easeInOutQuad = (t) => {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
};

const smoothScroll = (distance, duration) => {
  const start = list.value.scrollLeft;
  const startTime = performance.now();

  const animateScroll = (currentTime) => {
    const elapsedTime = currentTime - startTime;
    const progress = Math.min(elapsedTime / duration, 1);
    const ease = easeInOutQuad(progress);

    list.value.scrollLeft = start + distance * ease;

    if (progress < 1) {
      requestAnimationFrame(animateScroll);
    }
  };

  requestAnimationFrame(animateScroll);
};

const scrollLeft = () => {
  smoothScroll(-props.scrollDistance, props.animationDuration);
};

const scrollRight = () => {
  smoothScroll(props.scrollDistance, props.animationDuration);
};

//用户详情页跳转
function jump_to_other_user_center(userid,item)
{
  store.commit('SET_OTHER_USERID',userid)
  store.commit('SET_SINGLE_PAGE_STATUS',{'key':'other_user_center_page','value':true})
  console.log(userid)
}

onMounted(() => {
  set_tag_color();
  console.log(props)
});
</script>

<style scoped>
.scroll_box {
  width: 100%;
  height: 100%;
  min-height: 30px;
  min-width: 50px;
  display: flex;
  align-items: center;
  max-height: 300px;
  position: relative; /* 将 position 移到父容器以控制 btn_box 的位置 */
}
/*禁用横向滚动条显示*/
.scroll_box::-webkit-scrollbar {
  display: none;
}

.scroll_box_content {
  display: flex;
  width: 100%;
  height: 100%;
  align-items: center;
  white-space: nowrap;
  overflow: hidden;
}

.btn_box {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  position: absolute;
  top: 0;
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
  z-index: 5;
  pointer-events: none;
}

.scroll_box:hover .btn_box {
  opacity: 1;
}

.left_btn,
.right_btn {
  width: 60px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: absolute;
  pointer-events: auto;
}

.left_btn {
  left: 0;
  background: linear-gradient(to right, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0));
}

.right_btn {
  right: 0;
  background: linear-gradient(to left, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0));
}

.icon {
  width: 25px;
  height: 25px;
}

.list {
  display: flex;
  gap: 10px;
  white-space: nowrap;
  overflow-x: auto;
  scrollbar-width: none;
}
.left::-webkit-scrollbar{
  height: 0px;
  display: none;
  width: 0px;
}

.item {
  min-height: 200px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.image_item {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 15px;
  min-width: 150px;
  max-width: 280px;
  max-height: 200px;
  margin: 0 10px;
  position: relative;
  width: 150px;
  height: 200px;
}

.image_item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 15px;
}

.age_tag,
.page_count {
  position: absolute;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  color: white;
  z-index: 2;
  padding: 2px 4px;
}

.age_tag {
  width: 40px;
  height: 20px;
  left: 5px;
  top: 5px;
  background-color: rgba(255, 0, 0, 1);
  font-size: 12px;
}

.page_count {
  width: auto;
  height: auto;
  display: flex;
  gap: 5px;
  right: 0;
  top: 5px;
  background-color: rgba(87, 85, 85, 0.8);
  font-size: 16px;
  margin-right: 5px;
}

.page_count img {
  width: 25px;
  height: 25px;
}

.user_info {
  display: flex;
  align-items: center;
  width: 100%;
  cursor: pointer;
}

.user_avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  overflow: hidden;
}

.user_avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.username {
  display: flex;
  align-items: center;
}
.work_info{
  width: 200px;
  height: auto;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  gap: 10px;
}
.brief_introduction{
  width: 200px;
  height: 60px;
  max-height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  font-size: 14px;
  line-height: 20px;
  white-space: pre-wrap;
}
.ranking{
  display: flex;
  width: 25px;
  height: 25px;
  position:absolute;
  border-radius: 50%;
  color: white;
  font-size: 12px;
  justify-content: center;
  align-items: center;
  background-color: rgb(255, 195, 65);
  z-index: 2;
  bottom: 5px;
  right: 5px;
}
</style>
