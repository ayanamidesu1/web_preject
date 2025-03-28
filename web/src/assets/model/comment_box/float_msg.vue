<template>
    <div class="float_msg_box">
        <div class="content" :class="show_status ? 'msg_show' : 'msg_hide'">
            <div class="msg">{{ msg }}</div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted,onBeforeUnmount } from 'vue'
import { useCommentStore } from './store';

//const router = useRouter()
const commentStore = useCommentStore()
const show_status = ref(false)
let timeoutId = null

// 计算属性监听全局消息
let msg = computed(() => commentStore.comment_global_msg)

watch(msg, (newVal) => {
  if (newVal) {
    show_status.value = true
    if (timeoutId) clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      show_status.value = false
      //store.commit('set_global_msg', '')
      commentStore.set_comment_global_msg('')
    }, 2000)
  }
})

// 清除定时器
onBeforeUnmount(() => {
  if (timeoutId) clearTimeout(timeoutId)
  //store.commit('set_global_msg', '')
  commentStore.set_comment_global_msg('')
})

</script>

<style scoped>
.float_msg_box {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    z-index: 9999;
    /*鼠标点击操作可穿透*/
    pointer-events: none;
}

.content {
    position: absolute;
    left: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;
    border-radius: 15px;
    font-size: 18px;
    font-weight: bold;
    transition: all 0.5s ease-in-out;
    opacity: 0;
    box-shadow: 0px 0px 10px rgba(0, 150, 250, 1);
    background-color: rgba(255, 255, 255, 1);
}

.msg_show {
    top: 20vh;
    transform: translateY(-50%);
    opacity: 1;
}

.msg_hide {
    top: -50px;
    transform: translateY(-50%);
    opacity: 0;
}
</style>