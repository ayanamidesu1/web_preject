<template>
    <div class="novel_contribute_page">
        <h2>投稿的插画</h2>
        <div class="content">
            <div class="title">
                <span :class="title_choose_index == 0 ? 'is_choose' : ''" @click="choose_item(0)">全部作品</span>
                <span :class="title_choose_index == 1 ? 'is_choose' : ''" @click="choose_item(1)">审核通过作品</span>
                <span :class="title_choose_index == 2 ? 'is_choose' : ''" @click="choose_item(2)">审核未通过作品</span>
                <span :class="title_choose_index == 3 ? 'is_choose' : ''" @click="choose_item(3)">审核中</span>
            </div>
            <div class="search">
                <input type='text' v-model="search_type" placeholder="搜索投稿的作品">
                <span>搜索</span>
            </div>
            <div class="item" v-for="(item, index) in work_list" :key="index">
                <div class="work_cover">
                    <img :src="'https://www.sunyuanling.com/image/novel/thumbnail/' + item.work_cover" alt="作品封面">
                    <div class="show_work_chapter" @click="show_chapter_page(item.work_id)">
                        <span>查看作品的章节</span>
                    </div>
                </div>
                <div class="work_info">
                    <div class="work_info_item">
                        <span class="work_info_title">作品名称：</span>
                        <span class="work_info_content">{{ item.work_name }}</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">作者：</span>
                        <span class="work_info_content">{{ userinfo.username }}</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">作品类型：</span>
                        <span class="work_info_content">小说</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">作品描述：</span>
                        <span class="work_info_content">{{ item.brief_introduction }}</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">投稿时间：</span>
                        <span class="work_info_content">{{ item.work_create_time }}</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">审核状态：</span>
                        <span class="work_info_content">{{ item.work_approved == 0 ? '未通过' : (item.work_approved == 1 ?
                            '通过' : '审核中') }}</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">审核人：</span>
                        <span class="work_info_content">admin</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">审核意见：</span>
                        <span class="work_info_content">{{ item.approved_opinion == null ? '无意见' : item.approved_opinion
                            }}</span>
                    </div>
                </div>
            </div>
            <div class="page">
                <span class="page_btn" @click="page_change(-1)">上一页&nbsp;</span>
                <div class="page_num">
                    <span>{{ page }}&nbsp;/&nbsp;{{ all_page }}</span>
                </div>
                <span class="page_btn" @click="page_change(1)">&nbsp;下一页</span>
            </div>
        </div>
    </div>
    <chatper_page :work_id="novel_work_id" v-if="chatper_page_show" @close_page="close_chapter_page"></chatper_page>
</template>

<script setup>
import { ref, onMounted,watch } from 'vue'
import { get_worklist } from '../../js/get_worklist.js'
import chatper_page from './novel_chapter_contribute.vue'
import {search_novel_work} from '../../js/search_work.js'

let chatper_page_show = ref(false)
let novel_work_id = ref()

function show_chapter_page(work_id) {
    chatper_page_show.value = true
    novel_work_id.value = work_id
}

function close_chapter_page() {
    chatper_page_show.value = false
}

let search_type = ref('')
let work_list = ref([])
let offset = ref(0)
let limit = ref(3)
let page = ref(1)
let all_page = ref(1)
let all_count = ref(0)
let title_choose_index = ref(0)
let userinfo = ref(JSON.parse(localStorage.getItem('userinfo')))

// 筛选作品状态
function choose_item(index) {
    title_choose_index.value = index
    console.log('前端筛选作品状态')
}

// 获取作品列表
async function fetch_worklist() {
    const response = await get_worklist(offset.value, limit.value);
    if (response.status === 'success') {
        all_count.value = response.total_count.novel;  // 更新总作品数
        all_page.value = Math.ceil(all_count.value / limit.value);  // 更新总页数
        work_list.value = response.data.novel;
    } else {
        alert('获取作品列表失败');
    }
}

// 页面加载时获取作品列表
onMounted(fetch_worklist);

// 翻页功能实现
async function page_change(direction) {
    if (direction === -1 && page.value === 1) {
        // 如果当前是第一页，则不能继续往前翻
        return;
    } else if (direction === 1 && page.value >= all_page.value) {
        // 如果已经是最后一页，不能继续往后翻
        alert('已经是最后一页');
        return;
    }

    // 计算新的offset和page
    offset.value += direction * limit.value;
    if (offset.value < 0) {
        offset.value = 0;
    }

    // 更新当前页
    page.value = Math.floor(offset.value / limit.value) + 1;

    // 获取新的作品列表
    await fetch_worklist();
}

watch([search_type, title_choose_index], async () => {
    // 如果搜索框为空，并且选择的是全部作品
    if (search_type.value === '' && title_choose_index.value === 0) {
        // 重新获取作品列表
        await fetch_worklist();
    } else {
        // 否则根据搜索条件获取作品
        await search_work(search_type.value, title_choose_index.value);
    }
});


//搜索功能实现
async function search_work(search_key, work_status) {
    let status = ''
    if (work_status == 0) {
        status = 'all'
    } else if (work_status == 1) {
        status = 'pass'
    } else if (work_status == 2) {
        status = 'fail'
    } else if (work_status == 3) {
        status = 'unaudited'
    }
    else {
        status = 'all'
    }
    const data = await search_novel_work(search_key, status)
    console.log(data)
    if (data.status == 'success') {
        work_list.value = data.data
    }
    else {
        console.log(data.message)
        alert('没有相关作品')
        await fetch_worklist()
        title_choose_index.value = 0
        search_type.value = null
    }
}
</script>

<style scoped>
.novel_contribute_page {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.title {
    width: auto;
    height: auto;
    display: flex;
    flex-direction: row;
    gap: 10px;
}

.title span {
    width: auto;
    height: auto;
    padding: 5px 10px;
    font-size: 16px;
    font-weight: bold;
    border-radius: 5px;
}

.title span:hover {
    cursor: pointer;
    transform: scale(1.05);
    transition: all 0.2s ease-in-out;
}

.is_choose {
    background-color: rgba(0, 150, 250, 1);
    color: white;
    transition: all 0.2s ease-in-out;
    transform: scale(1.05);
    transform: translateY(-2px);
}

.search {
    width: 400px;
    height: 30px;
    display: flex;
    flex-direction: row;
    gap: 10px;
    align-items: center;
}

.search input {
    width: 300px;
    background-color: rgba(233, 233, 233, 1);
    height: 100%;
    border-radius: 10px;
    border: 1px solid rgba(0, 0, 0, 0);
}

.search span {
    width: 80px;
    height: 26px;
    font-size: 16px;
    font-weight: bold;
    border-radius: 5px;
    padding: 5px 10px;
    cursor: pointer;
    background-color: rgba(0, 150, 250, 1);
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
}

.search span:hover {
    opacity: 0.8;
    transform: scale(1.05);
    transition: all 0.2s ease-in-out;
}

.item {
    width: 100%;
    height: auto;
    gap: 10px;
    min-height: 200px;
    display: flex;
    flex-direction: row;
    border-radius: 15px;
    background-color: rgba(233, 233, 233, 1);
}

.work_cover {
    width: 200px;
    height: auto;
    border-radius: 15px 0px 0px 15px;
    max-height: 280px;
    max-width: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin:auto;
    margin-left: 5px;
}

.work_cover img {
    width: auto;
    height: auto;
    max-width: 200px;
    object-fit: cover;
    border-radius: 15px;
}

.work_info {
    width: calc(100% - 220px);
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
    padding: 5px;
    border-left: 1px solid rgba(133, 133, 133, 1);
}

.work_info_item {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
    min-height: 45px;
}

.work_info_title {
    width: 100%;
    height: auto;
    font-size: 16px;
    font-weight: bold;
}

.work_info_content {
    width: 100%;
    height: auto;
    max-height: 100px;
    overflow-y: auto;
    font-size: 14px;
    color: rgb(0, 0, 0);
    min-height: 20px;
    background-color: rgb(197, 197, 197);
    border-radius: 5px;
}

.page {
    width: 200px;
    height: 35px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin: 10px auto;
    background-color: rgb(63, 183, 219);
    border-radius: 10px;
}

.page_btn {
    width: auto;
    height: auto;
    display: flex;
    padding: 5px;
    justify-content: center;
    align-items: center;
}

.page_btn:hover {
    cursor: pointer;
    transform: scale(1.05);
    transition: all 0.2s ease-in-out;
    color: white;
}
.show_work_chapter{
    width:90%;
    height: auto;
    display: flex;
    margin-top: 20px;
    margin-left:auto;
    margin-right: auto;
    text-align: center;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 150, 250, 1);
    border-radius: 15px;
    padding: 5px 5px;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}
.show_work_chapter:hover{
    transform: scale(1.05);
    transition: all 0.2s ease-in-out;
}
</style>