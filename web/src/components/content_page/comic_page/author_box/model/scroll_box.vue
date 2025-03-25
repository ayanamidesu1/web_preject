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
        <div class="item" v-for="(item, index) in msg_list" :key="index">
          <div v-if="props.msg_type === 'tags'" class="tags_item" ref="tags_item" @click="chose_item(item)">
            <span>{{ item }}</span>
          </div>
          <div v-if="props.msg_type === 'image'" class="image_item"
            @click="chose_item({ 'item': item, 'work_id': item.work_id })">
            <img :src="item.item_path" class="image">
            <div class="work_count" v-if="item.work_count>1">
              <img :src="props.page_count_svg" class="icon">
              <span>{{item.work_count}}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, defineEmits, watch } from 'vue';

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
  },
  page_count_svg: {
    type: String,
    default: 'https://www.sunyuanling.com/assets/page_count.svg'
  },
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
let msg_list = ref(props.msg_list);
watch(() => props.msg_list, () => {
  msg_list.value = props.msg_list;
})

const emit = defineEmits(['chose_item']);
const chose_item = (item) => {
  emit('chose_item', item);
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

onMounted(async () => {
  set_tag_color();
  msg_list.value = props.msg_list;
  for (let i = 0; i < props.msg_list.length; i++) {
    msg_list.value[i].work_count = await get_work_info(props.msg_list[i].work_id);
  }
});
//通过ID请求作品详情，并获取数量
async function get_work_info(work_id) {
  try {
    const res = await fetch('https://www.sunyuanling.com/api/get_work_info/GetComicinfo/',
      {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify({
          work_id: work_id
        })
      }
    )
    if (res.ok) {
      const data = await res.json();
      if (data.status == 'success') {
        return data.data[0].content_file_list.split(/[,，]/).length;
      }
    }
  }
  catch (e) {
    console.log(e);
  }
}
</script>

<style scoped>
.scroll_box {
  width: 100%;
  height: 100%;
  min-height: 30px;
  min-width: 50px;
  display: flex;
  align-items: center;
  max-height: 200px;
  margin-top: 5px;
}

.scroll_box_content {
  display: flex;
  width: 100%;
  height: 100%;
  align-items: center;
  overflow-x: auto;
  scrollbar-width: none;
  white-space: nowrap;
  transition: transform 0.3s ease;
  position: relative;
}

.btn_box {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  position: absolute;
  left: 0;
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
  /* Enable pointer events only for the buttons */
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
  object-fit: cover;
}

.list {
  width: auto;
  height: 100%;
  display: flex;
  align-items: center;
  overflow-x: auto;
  scrollbar-width: none;
  white-space: nowrap;
  transition: transform 0.3s ease;
  gap: 10px;
}

.item {
  width: auto;
  height: 100%;
  display: flex;
  align-items: center;
  max-width: 100px;
}

.tags_item {
  width: auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 1);
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 10px;
}

.image_item {
  width: auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 10px;
  min-width: 100px;
  min-height: 100px;
  max-height: 100px;
  max-width: 200px;
  position: relative;
}

.image_item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 15px;
}
.work_count{
  width: auto;
  height: auto;
  padding: 3px;
  display: flex;
  flex-direction: row;
  align-items: center;
  position: absolute;
  top:5px;
  right: 5px;
  z-index: 10;
  gap:3px;
  background-color: rgba(133,133,133,0.8);
  border-radius: 10px;
  color: white;
}
.work_count img{
  width: 20px;
  height: 20px;
  object-fit: cover;
}
</style>
