<template>
    <div class="novel_chapter_contribute" v-if="novel_info">
        <div class="content">
            <div class="title">
                <span></span>
                <h1>投稿的章节</h1>
                <div class="close_page" @click="close_page()">
                    <img src="https://www.sunyuanling.com/assets/close.svg" alt="关闭页面" class="icon">
                </div>
            </div>
            <div class="chapter_search">
                <input type="text" placeholder="搜索章节名称" v-model="search_type">
                <button @click="search_chapter">搜索</button>
            </div>
            <div class="filter_buttons">
                <button :class="filter_status == 'all' ? 'all' : ''" @click="set_filter('all')">全部</button>
                <button :class="filter_status == 'approved' ? 'approved' : ''" @click="set_filter('approved')">审核通过</button>
                <button :class="filter_status == 'pending' ? 'pending' : ''" @click="set_filter('pending')">待审核</button>
                <button :class="filter_status == 'rejected' ? 'rejected' : ''" @click="set_filter('rejected')">审核未通过</button>
            </div>
            <div class="work_info">
                <div class="work_cover">
                    <img :src="'https://www.sunyuanling.com/image/novel/thumbnail/' + novel_info.work_cover" alt="作品封面">
                </div>
                <div class="info">
                    <div class="info_item">
                        <span>作品名称：</span>
                        <span>{{ novel_info.work_name }}</span>
                    </div>
                    <div class="info_item">
                        <span>作者：</span>
                        <span>{{ userinfo.username }}</span>
                    </div>
                    <div class="info_item">
                        <span>作品连载状态：</span>
                        <span>{{ novel_info.work_status }}</span>
                    </div>
                </div>
            </div>
            <div class="chapter" v-if="filtered_chapter_list.length > 0">
                <div class="chapter_info_list" v-for="(item, index) in filtered_chapter_list" :key="index">
                    <div class="chapter_info">
                        <div class="chapter_info_item">
                            <span>章节名称</span>
                            <span>{{ item.title }}</span>
                        </div>
                        <div class="chapter_info_item">
                            <span>投稿时间</span>
                            <span>{{ item.create_time }}</span>
                        </div>
                        <div class="chapter_info_item">
                            <span>审核状态</span>
                            <span>{{ (item.chapter_approved == 0 ? '未通过' : (item.chapter_approved == 1 ? '通过' :
                                '待审核')) }}</span>
                        </div>
                        <div class="chapter_info_item">
                            <span>审核意见</span>
                            <span>{{ item.approved_opinion == null ? '无' : item.approved_opinion }}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
                <p>没有符合条件的章节。</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted, computed } from 'vue';
import { get_chapter_list, get_novel_info } from '../../js/get_worklist';

const props = defineProps({
    work_id: { default: 0 },
});

const emits = defineEmits(['close_page']);
function close_page() {
    emits('close_page');
}

const userinfo = ref(JSON.parse(localStorage.getItem('userinfo')));
let chapter_list = ref([]);
let novel_info = ref();
let search_type = ref('');
let filter_status = ref('all');

// 获取章节列表
onMounted(async () => {
    chapter_list.value = await get_chapter_list(props.work_id);
    if (chapter_list.value.status == 'success') {
        chapter_list.value = chapter_list.value.data;
    } else {
        chapter_list.value = [];
        console.log(chapter_list.value.message);
    }
    novel_info.value = await get_novel_info(props.work_id);
    if (novel_info.value.status == 'success') {
        novel_info.value = novel_info.value.data[0];
    } else {
        novel_info.value = null;
        console.log(novel_info.value.message);
    }
});

// 搜索章节
function search_chapter() {
    // 搜索逻辑将在 computed 中处理
}

// 设置筛选条件
function set_filter(status) {
    filter_status.value = status;
}

// 计算筛选和搜索后的章节列表
const filtered_chapter_list = computed(() => {
    return chapter_list.value.filter(item => {
        // 根据筛选条件过滤
        if (filter_status.value == 'approved' && item.chapter_approved != 1) {
            return false;
        } else if (filter_status.value == 'pending' && item.chapter_approved != 2) {
            return false;
        } else if (filter_status.value == 'rejected' && item.chapter_approved != 0) {
            return false;
        }

        // 根据搜索条件过滤
        if (search_type.value) {
            return item.title.includes(search_type.value);
        }

        return true;
    });
});
</script>

<style scoped>
.novel_chapter_contribute {
    width: 100vw;
    height: 100vh;
    min-height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 200;
    display: flex;
    justify-content: center;
    align-items: center
}

.content {
    width: 80%;
    height: 80%;
    max-height: 80%;
    overflow-y: auto;
    box-sizing: border-box;
    padding: 10px;
    margin: 50px;
    background-color: white;
    display: flex;
    flex-direction: column;
    border-radius: 15px;
    gap: 10px;
}

.title {
    width: 100%;
    height: 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.close_page {
    width: 35px;
    height: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

.close_page:hover {
    border-radius: 50%;
    background-color: rgb(133, 133, 133);
    transition: all 0.2s ease-in-out;
    transform: scale(1.05);
    transform: translateY(-2px);
}

.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.chapter_search {
    width: 100%;
    height: 50px;
    display: flex;
    gap: 10px;
    align-items: center;
}

.chapter_search input {
    width: 80%;
    height: 100%;
    border-radius: 5px;
    border: 1px solid rgba(133, 133, 133, 1);
    padding: 2px;
}

.chapter_search button {
    width: 20%;
    height: 100%;
    border-radius: 15px;
    padding: 5px;
    border: none;
    cursor: pointer;
    background-color: rgba(0, 150, 250, 1);
    font-size: 18px;
    font-weight: bold;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
}

.chapter_search button:hover {
    opacity: 0.8;
    transform: scale(1.05);
    transition: all 0.2s ease-in-out;
    transform: translateY(-2px);
}

.work_info {
    width: 100%;
    height: auto;
    min-height: 200px;
    display: flex;
    gap: 10px;
    border-bottom: 1px solid rgba(133, 133, 133, 1);
    border-top: 1px solid rgba(133, 133, 133, 1);
}

.work_cover {
    width: auto;
    min-height: 140px;
    display: flex;
    padding: 5px;
}

.work_cover img {
    width: auto;
    height: auto;
    max-width: 200px;
    min-width: 140px;
    object-fit: cover;
    border-radius: 15px;
}

.info {
    width: auto;
    flex: 1;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    border-left: 1px solid rgba(133, 133, 133, 1);
    padding: 5px;
    gap: 10px;
}

.info_item {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
    min-height: 45px;
    background-color: rgba(233,233,233,1);
    padding:5px;
    border-radius: 5px;
}

.chapter {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.chapter_info_list {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border-bottom: 1px solid rgba(133, 133, 133, 1);
    background-color: rgba(211,211,211,1);
    overflow: hidden;
    padding:5px;
    border-radius: 5px;
}

.chapter_info {
    width: 100%;
    height: auto;
    display: flex;
    gap: 5px;
    flex-direction: column;
}

.chapter_info_item {
    width: calc(100% - 20px);
    height: auto;
    display: flex;
    gap: 5px;
    flex-direction: column;
    background-color: rgba(233,233,233,1);
    padding: 5px;
    border-radius: 5px;
}

.filter_buttons {
    width: 100%;
    height: auto;
    display: flex;
    gap: 10px;
}

.filter_buttons button {
    width: auto;
    height: auto;
    padding: 5px 10px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
}

.all,
.approved,
.pending,
.rejected {
    background-color: rgba(0, 150, 250, 1);
    color: white;
    font-weight: bold;
    transition: all 0.2s ease-in-out;
    transform: scale(1.05);
    transform: translateY(-1px);
}

.all:hover,
.approved:hover,
.pending:hover,
.rejected:hover {
    opacity: 0.8;
    transform: scale(1.05);
    transition: all 0.2s ease-in-out;
    transform: translateY(-2px);
}
</style>