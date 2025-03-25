<template>
    <div class="float_hand">
        <div class="flost_box" ref="float_box" :style="bubbleStyle">
            <div class="cursor" ref="cursor">
                <img src="https://www.sunyuanling.com/assets/cat.svg" class="icon">
                <span>喵~</span>
            </div>
            <div class="msg_box" ref="msgBox" :class="showBubble ? 'msg_box_show' : 'msg_box_hidden'">
                <div class="msg">{{ currentMessage }}</div>
            </div>
        </div>
        <div class="star_container">
            <div v-for="(star, index) in stars" :key="index" class="star" :style="star.style"></div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

// 获取 store 中的消息
const cursor_msg = computed(() => store.getters.cursor_msg)
const float_box = ref(null)
let star_box_status = ref(false)

// 管理当前显示的消息
const currentMessage = ref('')
const showBubble = ref(false)
let bubbleTimeout = null
const stars = ref([])  // 存储生成的星星
const starContainer = ref(null)

// 鼠标位置
const mouseX = ref(0)
const mouseY = ref(0)

// 默认点击的冒泡文字
const defaultBubbleText = '喵~'

// 节流函数
function throttle(func, delay) {
    let lastCall = 0
    return function (...args) {
        const now = new Date().getTime()
        if (now - lastCall < delay) return
        lastCall = now
        func(...args)
    }
}

// 监听鼠标移动事件，更新鼠标位置
function updateMousePosition(event) {
    mouseX.value = event.clientX
    mouseY.value = event.clientY
}

// 监听鼠标点击事件，触发默认冒泡和星星效果
onMounted(() => {
    window.addEventListener('mousemove', throttle(updateMousePosition, 16)) // 节流处理
    window.addEventListener('click', () => {
        if (cursor_msg.value === '喵~' || cursor_msg.value === '') {
            triggerBubble(defaultBubbleText)
        } else {
            triggerBubble(cursor_msg.value)
        }
        createStars()  // 生成星星
    })
})

// 移除事件监听器以防内存泄漏
onUnmounted(() => {
    window.removeEventListener('mousemove', throttle(updateMousePosition, 16))
})

// 冒泡触发函数
function triggerBubble(message) {
    currentMessage.value = message
    showBubble.value = true

    // 重置动画
    if (bubbleTimeout) {
        clearTimeout(bubbleTimeout)
    }

    // 消息显示 0.5 秒后自动消失
    bubbleTimeout = setTimeout(() => {
        showBubble.value = false
        setTimeout(() => {
            currentMessage.value = ''
            store.commit('set_cursor_msg', '喵~')
        }, 300)
    }, 700)
}

// 创建随机星星
function createStars() {
    const starCount = Math.floor(Math.random() * 16) + 5 // 随机生成5-20颗星星
    stars.value = []

    for (let i = 0; i < starCount; i++) {
        const size = Math.random() * 10 + 10 // 随机大小10px - 20px
        const angle = Math.random() * 360 // 随机扩散角度
        const distance = Math.random() * 30 + 30 // 星星随机距离30px-60px
        const x = mouseX.value + Math.cos(angle) * distance
        const y = mouseY.value + Math.sin(angle) * distance
        const duration = 0.5 // 0.5秒内消失

        stars.value.push({
            style: {
                position: 'absolute',
                width: `${size}px`,
                height: `${size}px`,
                top: `${y}px`,
                left: `${x}px`,
                opacity: 1,
                backgroundImage: 'url(https://www.sunyuanling.com/assets/star.svg)',
                backgroundSize: 'cover',
                transition: `opacity ${duration}s ease, transform ${duration}s ease`,
                transform: `scale(0)`
            }
        })

        // 设置星星在0.5秒内消失
        setTimeout(() => {
            stars.value[i].style.opacity = 0
            stars.value[i].style.transform = 'scale(1.0)'
        }, 0)

        // 清除星星
        setTimeout(() => {
            stars.value = []
        }, duration * 1000)
    }
}

// 动态计算冒泡框的样式
const bubbleStyle = computed(() => {
    return {
        top: `${mouseY.value - 10}px`,
        left: `${mouseX.value + 20}px`,
    }
})
</script>


<style scoped>
.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.float_hand {
    width: 100vw;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    z-index: 9999;
    pointer-events: none;
}

.flost_box {
    position: absolute;
    color: rgb(243, 87, 191);
}

.msg_box {
    background-color: rgba(0, 0, 0, 0.2);
    color: rgb(245, 91, 245);
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 14px;
    pointer-events: none;
    transition: opacity 0.5s ease, transform 0.5s ease;
    /* 分开控制 */
    opacity: 0;
    position: absolute;
    left: 100px;
    min-width: 100px;
    display: flex;
    min-height: 30px;
    z-index: 99999;
}

.msg_box_show {
    transform: translateY(-10px);
    /* 略微上移 */
    opacity: 1;
}

.msg_box_hidden {
    transform: translateY(0);
    opacity: 0;
}

/*星星的显示和隐藏样式*/
.star_box {
    position: absolute;
    width: 50px;
    height: 50px;
    transition: opacity 0.5s ease, transform 0.5s ease, scale 0.5s ease;
    z-index: 99999;
    transform: scale(0.0);
}

.star_box_show {
    opacity: 1;
    transform: scale(1.0);
}

.star_box_hidden {
    opacity: 0;
    transform: scale(0.0);
}

.float_hand {
    width: 100vw;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    z-index: 9999;
    pointer-events: none;
}

.flost_box {
    position: absolute;
    color: rgb(243, 87, 191);
}

.star_container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 99999;
}

.star {
    position: absolute;
    background-color: yellow;
    border-radius: 50%;
    pointer-events: none;
    transition: opacity 0.5s ease, transform 0.5s ease;
}

.float_hand {
    width: 100vw;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    z-index: 9999;
    pointer-events: none;
}

.flost_box {
    position: absolute;
    color: rgb(243, 87, 191);
}

.star_container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 99999;
}

.star {
    position: absolute;
    background-color: yellow;
    border-radius: 50%;
    pointer-events: none;
    transition: opacity 0.5s ease, transform 0.5s ease;
}
</style>
