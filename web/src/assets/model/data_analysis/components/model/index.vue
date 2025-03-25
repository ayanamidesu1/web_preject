<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="index">
        <div class="content">
            <div class="title">
                <div class="all_work_data">
                    <span @click="data_analysis">全部的作品数据</span>
                    <span @click="ill_work">全部插画作品</span>
                    <span @click="comic_work">全部漫画作品</span>
                    <span @click="novel_work">全部小说作品</span>
                </div>
               
                <div class="close_data_analysis" v-if="page == 'draw_page'">
                    <span @click="page = 'choose_work_page'">关闭数据分析</span>
                </div>
                <div class="appiont_work">
                    <span @click="choose_type = 'appiont'; searchWorks()">搜索作品</span>
                </div>
            </div>
            <input v-model="ago_date">
            <span>自定义时间段单位：（天）</span>
            <div class="draw_page" v-if="page == 'draw_page'">
                <drawing_index_page :work_title="work_title" 
                :history_data="his_data" :week_data="tar_data" :key="rand_id"/>
            </div>
            <div class="content_item" v-if="page == 'choose_work_page'">
                <div class="choose_appiont_work">
                    <div class="search_box">
                        <input v-model="search_type" type="text" placeholder="请输入作品名">
                        <span @click="searchWorks">搜索</span>
                    </div>
                    <span @click="choose_type = 'all'; searchWorks()">全部</span>
                    <span @click="choose_type = 'novel'; searchWorks()">小说</span>
                    <span @click="choose_type = 'comic'; searchWorks()">漫画</span>
                    <span @click="choose_type = 'ill'; searchWorks()">插画</span>
                </div>
            </div>
        </div>
        <work_list :work_list="filtered_work_list" @choose_item="get_appoint_work_data_api"></work_list>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, defineProps } from 'vue'
import { get_all_work_data ,get_appoint_work_data} from './js/get_user_workdata'
import { get_all_user_work } from './js/get_user_all_work'
import work_list from './work_list.vue'
import drawing_index_page from './drawing_index_page.vue'

const props = defineProps({
    token: {
        default: ''
    }
})

const choose_type = ref('all')
const all_work_data = ref()
const all_work_list = ref()
const search_type = ref('')
const selected_status = ref('') // 用于小说连载状态筛选
const page = ref('choose_work_page')
const his_data = ref([])
const tar_data = ref([])
const work_title=ref('')
const rand_id=ref()
const ago_date=ref(7)

const all_work_interaction_data_tar = ref({
    watch: 0,
    like: 0,
    collect: 0
})
const all_work_interaction_data_his = ref({
    watch: 0,
    like: 0,
    collect: 0
})
const ill_data_tar = ref({
    watch: 0,
    like: 0,
    collect: 0
})

const ill_data_his = ref({
    watch: 0,
    like: 0,
    collect: 0
})

const comic_data_tar = ref({
    watch: 0,
    like: 0,
    collect: 0
})

const comic_data_his = ref({
    watch: 0,
    like: 0,
    collect: 0
})

const novel_data_tar = ref({
    watch: 0,
    like: 0,
    collect: 0
})

const novel_data_his = ref({
    watch: 0,
    like: 0,
    collect: 0
})


function data_analysis(item) {
    all_work()
    page.value = 'draw_page'
}

async function get_appoint_work_data_api(item){
    console.log(item)
    let work_id=item.work_id
    let work_type=item.work_type
    let token=props.token
    let data=await get_appoint_work_data(token,ago_date.value,work_id,work_type)
    console.log(data)
    all_work_interaction_data_tar.value=data.target_work_data
    all_work_interaction_data_his.value=data.history_work_data
    all_work()
}

function all_work() {
    his_data.value[0] = all_work_interaction_data_his.value.watch+1
    his_data.value[1] = all_work_interaction_data_his.value.like+1
    his_data.value[2] = all_work_interaction_data_his.value.collect+1
    tar_data.value[0] = all_work_interaction_data_tar.value.watch+1
    tar_data.value[1] = all_work_interaction_data_tar.value.like+1
    tar_data.value[2] = all_work_interaction_data_tar.value.collect+1
    page.value = 'draw_page'
    work_title.value='所有作品'
    rand_id.value=Math.random()
}

function ill_work() {
    his_data.value[0] = ill_data_his.value.watch+1
    his_data.value[1] = ill_data_his.value.like+1
    his_data.value[2] = ill_data_his.value.collect+1
    tar_data.value[0] = ill_data_tar.value.watch+1
    tar_data.value[1] = ill_data_tar.value.like+1
    tar_data.value[2] = ill_data_tar.value.collect+1
    page.value = 'draw_page'
    work_title.value='插画作品'
    rand_id.value=Math.random()
}
function comic_work() {
    his_data.value[0] = comic_data_his.value.watch+1
    his_data.value[1] = comic_data_his.value.like+1
    his_data.value[2] = comic_data_his.value.collect+1
    tar_data.value[0] = comic_data_tar.value.watch+1
    tar_data.value[1] = comic_data_tar.value.like+1
    tar_data.value[2] = comic_data_tar.value.collect+1
    page.value = 'draw_page'
    work_title.value='漫画作品'
    rand_id.value=Math.random()
}
function novel_work() {
    his_data.value[0] = novel_data_his.value.watch+1
    his_data.value[1] = novel_data_his.value.like+1
    his_data.value[2] = novel_data_his.value.collect+1
    tar_data.value[0] = novel_data_tar.value.watch+1
    tar_data.value[1] = novel_data_tar.value.like+1
    tar_data.value[2] = novel_data_tar.value.collect+1
    page.value = 'draw_page'
    work_title.value='小说作品'
    rand_id.value=Math.random()
}


onMounted(async () => {
    all_work_data.value = await get_all_work_data(props.token, ago_date.value)
    all_work_list.value = await get_all_user_work(props.token)
    console.log(all_work_data.value)
    console.log(all_work_list.value)
    Object.keys(all_work_data.value.history_data).forEach((key) => {
        const data = all_work_data.value.history_data[key];
        all_work_interaction_data_his.value.watch += data.watch || 0;
        all_work_interaction_data_his.value.like += data.like || 0;
        all_work_interaction_data_his.value.collect += data.collect || 0;
    });
    Object.keys(all_work_data.value.target_data).forEach((key) => {
        const data = all_work_data.value.target_data[key];
        all_work_interaction_data_tar.value.watch += data.watch || 0;
        all_work_interaction_data_tar.value.like += data.like || 0;
        all_work_interaction_data_tar.value.collect += data.collect || 0;
    });
    console.log(all_work_interaction_data_tar.value)
    console.log(all_work_interaction_data_his.value)
    ill_data_his.value = all_work_data.value.history_data.ill
    ill_data_tar.value = all_work_data.value.target_data.ill
    comic_data_his.value = all_work_data.value.history_data.comic
    comic_data_tar.value = all_work_data.value.target_data.comic
    novel_data_his.value = all_work_data.value.history_data.novel
    novel_data_tar.value = all_work_data.value.target_data.novel
})

const searchWorks = () => {
    // 只需更新 search_type，filtered_work_list 会自动更新
    let temp = search_type.value
    search_type.value = temp
}

const filterWorks = (workList, query) => {
    if (!query) return filterByType(choose_type.value, workList)

    const filtered = {
        ill: workList.ill.filter(item => item.name.toLowerCase().includes(query.toLowerCase()) || item.work_tags.toLowerCase().includes(query.toLowerCase())),
        comic: workList.comic.filter(item => item.work_name.toLowerCase().includes(query.toLowerCase()) || item.work_tags.toLowerCase().includes(query.toLowerCase())),
        novel: workList.novel.filter(item => item.work_name.toLowerCase().includes(query.toLowerCase()) || item.work_tags.toLowerCase().includes(query.toLowerCase()))
    }
    return filterByType(choose_type.value, filtered)
}

const filterByType = (type, workList) => {
    if (type === 'all') return workList
    return {
        ill: type === 'ill' ? workList.ill : [],
        comic: type === 'comic' ? workList.comic : [],
        novel: type === 'novel' ? workList.novel : []
    }
}

const filtered_work_list = computed(() => {
    let filtered = filterWorks(all_work_list.value, search_type.value)

    // 处理小说的连载状态筛选
    if (selected_status.value) {
        filtered.novel = filtered.novel.filter(novel => novel.work_status === selected_status.value)
    }

    return filtered
})
</script>


<style scoped>
/* 其他样式不变 */

.content {
    padding: 16px;
    background-color: #f9f9f9;
}

.title {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
}

.all_work_data,
.appiont_work {
    cursor: pointer;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 16px;
    transition: all 0.3s, color 0.3s;
}


.appiont_work {
    background-color: #fff;
    color: #007bff;
    border: 1px solid #007bff;
}

.appiont_work:hover {
    background-color: #0056b3;
    color: #fff;
}

.choose_appiont_work {
    margin-top: 16px;
}

.search_box {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
}

.search_box input {
    flex: 1;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

.search_box span {
    cursor: pointer;
    background-color: #007bff;
    color: #fff;
    padding: 12px 24px;
    border-radius: 4px;
    font-size: 16px;
    transition: background-color 0.3s;
}

.search_box span:hover {
    background-color: #0056b3;
}

.choose_appiont_work span {
    cursor: pointer;
    display: inline-block;
    padding: 8px 12px;
    margin: 0 4px;
    border-radius: 4px;
    font-size: 14px;
    transition: background-color 0.3s, color 0.3s;
}

.choose_appiont_work span:hover {
    background-color: #007bff;
    color: #fff;
}

.all_work_data {
    width: auto;
    display: flex;
    height: auto;
    gap: 10px;
}

.all_work_data span {
    width: auto;
    height: auto;
    padding: 5px 10px;
    background-color: rgba(0, 150, 250, 1);
    border-radius: 8px;
    color: white;
    cursor: pointer;
}

.all_work_data span:hover {
    opacity: 0.8;
    transition: all 0.2s ease-in-out;
    transform: scale(1.05);
}
</style>
