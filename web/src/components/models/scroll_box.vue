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
        <div class="item" v-if="props.msg_type === 'image'" @click="chose_item('custom_cover')">
          <div class="image_item">
            <img class="icon" src="https://www.sunyuanling.com/assets/add.svg">
          </div>
        </div>
        <div class="item" v-for="(item, index) in props.msg_list" :key="index">
          <div v-if="props.msg_type === 'tags'" class="tags_item" ref="tags_item" @click="chose_item(item)">
            <span>{{ item }}</span>
          </div>
          <div v-if="props.msg_type === 'image'" class="image_item" @click="chose_item(item, index)">
            <img :src="item" class="image">
            <div class="select_box" ref="select_box">
              <img :src="select_svg" class="icon" ref="select_icon" style="display: none;">
            </div>
          </div>
        </div>
      </div>
      <input class="select_cover" type="file" ref="select_cover" id="select_cover" style="display: none;"
       accept="image/*" @change="upload_choose_cover_file">
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, defineEmits,watch } from 'vue';

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
let select_cover=ref(null)
const set_tag_color = () => {
  if (tags_item.value) {
    tags_item.value.forEach((item, index) => {
      item.style.backgroundColor = colorArr.value[index % colorArr.value.length];
    });
  }
};

const emit = defineEmits(['chose_item','choose_cover_file','clear_cover_file']);
let select_svg = ref('https://www.sunyuanling.com/assets/select_correct.svg')
let select_box = ref(null)
let select_icon = ref(null)
const chose_item = (item, index) => {

  if (item != 'custom_cover') {
    emit('chose_item', 'template_' + (index + 1));
    emit('clear_cover_file',true)
    //设置指定索引元素为内部阴影
    select_box.value[index].style.boxShadow = 'inset 0px 0px 10px 0px rgba(0, 150, 250, 1)';
    select_icon.value[index].style.display = '';
    //遍历其他位置元素，去除所有内部阴影和select_icon的src值
    for (let i = 0; i < select_box.value.length; i++) {
      if (i != index) {
        select_box.value[i].style.boxShadow = 'none';
        select_icon.value[i].style.display = 'none';
      }
    }
  }
  else{
    //模拟点击
    select_cover.value.click();
    emit('chose_item','custom_cover')
  }
};
function upload_choose_cover_file(e)
{
  let file=e.target.files[0];
  if(file.type.indexOf('image')==-1)
  {
    alert('请选择图片文件');
    return;
  }
  if(file.size>1024*1024*35)
  {
    alert('请选择小于35M的图片');
    return;
  }
  if(file)
  {
    emit('choose_cover_file',file)
    console.log('文件传递父组件')
    console.log(file)
  }
}

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

onMounted(() => {
  set_tag_color();
});
watch(() => props.msg_list, (newList) => {
  // 更新 tags_item 引用
  tags_item.value = list.value.querySelectorAll('.tags_item');
  set_tag_color();
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
  max-height: 220px;
  flex-direction: column;
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
  padding: 5px;
  background-color: rgba(233, 233, 233, 1);
  border-radius: 10px;
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
  height: 200px;
  display: flex;
  align-items: center;
  gap: 10px;
  overflow-x: auto;
  scrollbar-width: none;
  white-space: nowrap;
  transition: transform 0.3s ease;
}

.item {
  width: auto;
  height: 200px;
  display: flex;
  align-items: center;
}

.custom_cover {
  width: auto;
  height: 200px;
  display: flex;
  align-items: center;
}

.tags_item {
  width: auto;
  height: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 1);
  cursor: pointer;
  padding: 10px 20px;
  border-radius: 15px;
}

.image_item {
  width: auto;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 15px;
  min-width: 150px;
  min-height: 75px;
  max-height: 200px;
  max-width: 100px;
  margin: 0px 10px;
  position: relative;
}

.image_item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 15px;
}

.select_box {
  position: absolute;
  right: 5px;
  bottom: 5px;
  background-color: rgb(255, 255, 255);
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.select_box img {
  width: 20px;
  height: 20px;
  object-fit: cover;
}
</style>
