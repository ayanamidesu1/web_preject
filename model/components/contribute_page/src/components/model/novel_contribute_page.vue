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
            <div class="item">
                <div class="work_cover">
                    <img src="https://www.sunyuanling.com/server/static/image/thumbnail/93414753_p0.jpg" alt="作品封面">
                </div>
                <div class="work_info">
                    <div class="work_info_item">
                        <span class="work_info_title">作品名称：</span>
                        <span class="work_info_content">测试</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">作者：</span>
                        <span class="work_info_content">admin</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">作品类型：</span>
                        <span class="work_info_content">插画</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">作品描述：</span>
                        <span class="work_info_content">简介</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">投稿时间：</span>
                        <span class="work_info_content">2024年8月22日18:08:59</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">审核状态：</span>
                        <span class="work_info_content">通过</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">审核人：</span>
                        <span class="work_info_content">admin</span>
                    </div>
                    <div class="work_info_item">
                        <span class="work_info_title">审核意见：</span>
                        <span class="work_info_content">意见</span>
                    </div>

                </div>
            </div>
            <div class="page">
                <span class="page_btn">上一页&nbsp;</span>
                <div class="page_num">
                    <span>{{ page }}&nbsp;/&nbsp;{{ all_page }}</span>
                </div>
                <span class="page_btn">&nbsp;下一页</span>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'

let search_type = ref('')
let work_list = ref([])
let offset = ref(0)
let limit = ref(10)
let page = ref(1)
let all_page = ref(1)
let title_choose_index = ref(0)

function choose_item(index) {
    title_choose_index.value = index
    console.log('前端筛选作品状态筛选')
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
    height: 200px;
    border-radius: 15px 0px 0px 15px;
    max-height: 200px;
    max-width: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.work_cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 15px;
}

.work_info {
    width: calc(100% - 220px);
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
    padding:5px;
    border-left: 1px solid rgba(133, 133, 133, 1);
}
.work_info_item{
    width:100%;
    height:auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
    min-height: 45px;
}
.work_info_title{
    width: 100%;
    height: auto;
    font-size: 16px;
    font-weight: bold;
}
.work_info_content{
    width:100%;
    height: auto;
    max-height: 100px;
    overflow-y:auto;
    font-size: 14px;
    color:rgb(0, 0, 0);
    min-height: 20px;
    background-color: rgb(197, 197, 197);
    border-radius: 5px;
}
.page{
    width:200px;
    height: 35px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin:10px auto;
    background-color: rgb(63, 183, 219);
    border-radius: 10px;
}
.page_btn{
    width:auto;
    height: auto;
    display: flex;
    padding:5px;
    justify-content: center;
    align-items: center;
}
.page_btn:hover{
    cursor: pointer;
    transform: scale(1.05);
    transition: all 0.2s ease-in-out;
    color: white;
}
</style>