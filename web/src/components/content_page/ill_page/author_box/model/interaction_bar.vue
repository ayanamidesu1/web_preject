<script setup>
// eslint-disable-next-line no-unused-vars
import { ref, defineProps, defineEmits, watch, onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

let interaction_bar = ref(null)
let props = defineProps({
  like_svg: {
    type: String,
    default: 'https://www.sunyuanling.com/assets/like.svg'
  },
  is_like_svg: {
    type: String,
    default: 'https://www.sunyuanling.com/assets/is_like.svg'
  },
  collect: {
    type: String,
    default: 'https://www.sunyuanling.com/assets/no_work_like.svg'
  },
  is_collect: {
    type: String,
    default: 'https://www.sunyuanling.com/assets/work_like.svg'
  },
  share_svg: {
    type: String,
    default: 'https://www.sunyuanling.com/assets/share.svg'
  },
  like_status: {
    type: Boolean,
    default: false
  },
  collect_status: {
    type: Boolean,
    default: false
  }
})

let emit = defineEmits(['like_status', 'collect_status'])
let localState = ref({
  like_svg: props.like_svg,
  is_like_svg: props.is_like_svg,
  collect: props.collect,
  is_collect: props.is_collect,
  share_svg: props.share_svg,
  like_status: props.like_status,
  collect_status: props.collect_status
})

let debounce = ref({ like: false, collect: false }) // 添加中间量

function like_status() {
  if (!debounce.value.like) {
    debounce.value.like = true
    let new_status = !localState.value.like_status
    emit('like_status', new_status)
    if(new_status){
      store.commit('set_cursor_msg','非常感谢主人的临幸呢，看看其他作品吧~也许还会有喜欢的哦~')
    }
    else{
      store.commit('set_cursor_msg','呜~主人不爱我了————')
    }
    localState.value.like_status = new_status
    setTimeout(() => { debounce.value.like = false }, 50) // 50ms的延迟
  }
}

function collect_status() {
  if (!debounce.value.collect) {
    debounce.value.collect = true
    let new_status = !localState.value.collect_status
    emit('collect_status', new_status)
    if(new_status){
      store.commit('set_cursor_msg','感谢主人的收藏呢~，要看看其他的作品吗？')
    }
    else{
      store.commit('set_cursor_msg','我会努力改进的！')
    }
    localState.value.collect_status = new_status
    setTimeout(() => { debounce.value.collect = false }, 50) // 50ms的延迟
  }
}

watch(() => props, (newProps) => {
  localState.value = { ...newProps }
}, { deep: true })

onMounted(() => {
  localState.value = { ...props }
})
</script>

<template>
  <div class="interaction_bar" ref="interaction_bar">
    <div class="content">
      <div class="item">
        <div class="like" @click="like_status">
          <img :src="localState.like_status ? localState.is_like_svg : localState.like_svg" class="icon">
        </div>
        <div class="collect" @click="collect_status">
          <img :src="localState.collect_status ? localState.is_collect : localState.collect" class="icon">
        </div>
        <div class="share">
          <img :src="localState.share_svg" class="icon">
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.interaction_bar {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  min-width: 150px;
}

.content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  position: relative;
  justify-content: flex-end;
  align-items: flex-end;
}

.item {
  width: auto;
  height: auto;
  gap: 15px;
  display: flex;
  flex-direction: row;
}

.icon {
  width: 25px;
  height: 25px;
  object-fit: cover;
}

.like,
.collect,
.share {
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.like:hover,
.collect:hover,
.share:hover {
  background-color: rgba(133, 133, 133, 0.5);
  cursor: pointer;
  border-radius: 50%;
  overflow: hidden;
  transition: all 0.3s ease-in-out;
}
</style>
