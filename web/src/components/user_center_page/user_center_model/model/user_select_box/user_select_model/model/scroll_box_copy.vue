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
          <div v-if="props.msg_type === 'tags' && item!='' &&item" class="tags_item" ref="tags_items" @click="chose_item(item)">
            <span>{{ item }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, defineEmits,nextTick } from 'vue';

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
    type: [Array, Object],
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

const list = ref(null);
const tags_items = ref([]);

const set_tag_color = () => {
  tags_items.value.forEach((item, index) => {
    item.style.backgroundColor = colorArr.value[index % colorArr.value.length];
  });
};

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

onMounted(() => {
  tags_items.value = document.querySelectorAll('.tags_item');
  nextTick(()=>{
    set_tag_color();
  })
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
  max-height: 200px;
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

.left_btn, .right_btn {
  width: 60px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: absolute;
  pointer-events: auto; /* Enable pointer events only for the buttons */
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

.tags_item {
  width: auto;
  height: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgb(0, 0, 0);
  cursor: pointer;
  padding: 10px 20px;
  border-radius: 15px;
  background-color: rgb(214, 156, 156);
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
  max-height: 100px;
  max-width: 200px;
  margin: 0px 10px;
}

.image_item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 15px;
}
</style>
