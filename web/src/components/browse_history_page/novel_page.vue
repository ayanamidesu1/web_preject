<template>
    <div class="novel_page">
        <h1>插画浏览历史</h1>
        <div class="item_list">
            <div class="item" v-for="(item, index) in novel_item" :key="index">
                <div class="work_cover">
                    <img :src="'https://www.sunyuanling.com/image/novel/thumbnail/' + item.work.work_cover"
                        alt="封面">
                    <div class="age_classification" v-if="item.work.age_classification >= 18">
                        <span>{{ item.work.age_classification }}</span>
                    </div>
                </div>
                <div class="work_info">
                    <div class="work_name">
                        <span @click="open_comic_content_page(item.work.work_id)">{{ item.work.work_name }}</span>
                    </div>
                    <span>作品ID：{{ item.work.work_id }}</span>
                    <div class="work_tags">
                        <span v-for="(tag_item, tag_index) in item.work.work_tags.split(/[,，]/)" :key="tag_index">
                            <span class="tag">#{{ tag_item }}</span>
                        </span>
                    </div>
                    <span>时间：{{item.time}}</span>
                </div>
            </div>
        </div>
    </div>
    <div class="check_point" ref="check_point" style="display: block;width:1px;height:1px;opacity: 0"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, defineProps,defineEmits } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

//打开内容页,并设置参数
function open_comic_content_page(work_id){
    store.commit('SET_WORK_ID',work_id)
    store.commit('SET_SINGLE_PAGE_STATUS',{'key':'content_index_page','value':true})
    //设置内容页为插画内容页
    store.commit('SET_CONTENT_PAGE',{'key':'novel_page','value':true})
}

// 定义传入的插画项目列表属性
const props = defineProps({
    novel_item: Array
})
//传出请求事件
const emit=defineEmits(['request'])

// 引用 DOM 元素
let check_point = ref(null)
let limit = 10
let offset = 0

// 创建 IntersectionObserver 实例
let observer = null

// 滚动检测回调函数
function handleIntersection(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            console.log('Reached the bottom, load more content here...')
            // 触发加载更多的逻辑，如更新数据
            offset += limit
            emit('request', {'limit':limit, 'offset':offset})
        }
    })
}

// 设置 IntersectionObserver
onMounted(() => {
    observer = new IntersectionObserver(handleIntersection, {
        root: null, // viewport
        rootMargin: '100px',
        threshold: 1.0
    })

    // 开始观察
    if (check_point.value) {
        observer.observe(check_point.value)
    }
})

// 在组件销毁时取消观察
onBeforeUnmount(() => {
    if (observer && check_point.value) {
        observer.unobserve(check_point.value)
    }
})

</script>

<style scoped>
.novel_page {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
}

.item_list {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.item {
    width: 100%;
    height: auto;
    display: flex;
    gap: 10px;
}

.work_cover {
    width: 200px;
    height: auto;
    max-height: 300px;
    position: relative;
    display: flex;
    min-width: 200px;
    border-radius: 15px;
    overflow: hidden;
}

.work_cover img {
    width: 100%;
    height: auto;
    object-fit: cover;
    max-height: 300px;
}

.page_count {
    width: auto;
    padding: 2px 3px;
    display: flex;
    position: absolute;
    right: 5px;
    top: 5px;
    z-index: 2;
    background-color: rgba(63, 63, 63, 0.8);
    border-radius: 5px;
    color: white;
}

.age_classification {
    width: auto;
    padding: 2px 3px;
    display: flex;
    position: absolute;
    left: 5px;
    top: 5px;
    z-index: 2;
    background-color: red;
    color: white;
    font-weight: bold;
    border-radius: 5px;
}

.work_info {
    width: calc(100% - 220px);
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.work_name {
    width: auto;
    display: flex;
}

.work_name:hover {
    cursor: pointer;
    text-decoration: underline;
}

.work_tags {
    width: 100%;
    display: flex;
    flex-direction: row;
    gap: 5px;
    color: rgb(0, 150, 250);
}

.icon {
    width: 15px;
    height: 15px;
    object-fit: cover;
}
</style>
