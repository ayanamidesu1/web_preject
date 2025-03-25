<template>
    <div class="ill_index" ref="ill_index">
        <go_back></go_back>
        <div class="content" v-if="work_info">
            <div class="item_box">
                <div class="item" v-for="(item, index) in work_info.content_file_list.split(/[,，]/)" :key="index">
                    <div class="img_box" v-if="index < max_img_len">
                        <img :src="'https://www.sunyuanling.com/image/content_thumbnail/' + item" class="item_img"
                            @click="show_work_info(item)">
                    </div>
                </div>
                <div class="show_more_btn"
                    v-if="max_img_len == 1 && work_info.content_file_list.split(/[,，]/).length > 1" ref="show_more_btn">
                    <div class="show_more_background"></div>
                    <span @click="show_all_img()">查看全部</span>
                </div>
            </div>
            <div class="fixed_interaction" ref="fixed_interaction">
                <interaction :like_status="like_status" :collect_status="collect_status" @like_status="get_like_status"
                    @collect_status="get_collect_status"></interaction>
            </div>
            <div class="float_interaction" ref="float_interaction">
                <interaction :like_status="like_status" :collect_status="collect_status" @like_status="get_like_status"
                    @collect_status="get_collect_status"></interaction>
            </div>
            <work_info_box :work_data="work_data" :work_create_time="work_info.create_time" :work_id="work_id"></work_info_box>
            <div class="author_info_box_bottom" v-if="work_info">
                <author_info_bottom :author_id="work_info.belong_to_user_id" @chose_item="get_choose_item" :key="work_id"></author_info_bottom>
            </div>
            <div class="comment_section">
                <comment_section :work_type="'ill'" :token="token" :work_id="String(work_id)" 
                :user_avatar_path="user_avatar_path"
                :key="work_id">

                </comment_section>
            </div>
            <h3>推荐插画作品</h3>
            <div class="recommend_page">
                <recommend :work_type="'ill'" :token="store_token"></recommend>
            </div>
        </div>
        <div class="author_info_box" v-if="work_info">
            <author_info :author_id="work_info.belong_to_user_id" @chose_item="get_choose_item" :key="work_info.belong_to_user_id"></author_info>
        </div>
       
        
    </div>
    <img_content_page :item_path="item_path" v-if="img_content_page_show" @close_img_content_page="close_content_page">
    </img_content_page>
    
    
</template>

<script setup>
import { ref, watch, onMounted, defineProps,onUnmounted,nextTick,computed } from 'vue';
import { useStore } from 'vuex';
import go_back from '../go_back.vue';
import img_content_page from '../img_content_page/img_content_page.vue';
import author_info from './author_box/author_info.vue';
import author_info_bottom from './author_box/model/author_info.vue'
import interaction from './author_box/model/interaction_bar.vue'
import work_info_box from './author_box/model/work_info_bar.vue'
import comment_section from './comment_section.vue'
import * as cookies from '@/assets/js/cookies'
import * as user_interaction from '@/assets/js/interaction'
import recommend from '@/assets/model/recommend_page/modle/index.vue'


const store = useStore();
const work_id = ref('');
const work_info = ref();
const img_content_page_show = ref(false);
const item_path = ref('');
let max_img_len = ref(1)
let show_more_btn = ref(null)
let fixed_interaction = ref(null)
let float_interaction = ref(null)
let store_token = computed(()=>store.getters.token)
let token=store_token.value
let like_status = ref(false)
let collect_status = ref(false)
let work_data = ref({
    'like': '100',
    'collect': '100',
    'watch': '100'
})
let user_avatar_path=ref(JSON.parse(cookies.get_cookie('userinfo')).user_avatar)

console.log(user_avatar_path.value)
//接收子组件状态
async function get_like_status(item) {
    like_status.value = item
    like_status.value = await user_interaction.like_work(work_id.value, 'add', token, 'ill', work_info.value.name) == 1 ? true : false
}
async function get_collect_status(item) {
    collect_status.value = item
    collect_status.value = await user_interaction.collect_work(
        work_id.value, 'add', token, 'ill', work_info.value.name) == 1 ? true : false;
}

let lastScrollTop = 0; // 上一个滚动位置

function float_interaction_bar(status) {
    try {
        if (!fixed_interaction.value || !float_interaction.value || !status) {
            return;
        }
        let window_height = window.innerHeight;
        let fixed_interaction_bottom = fixed_interaction.value.getBoundingClientRect().bottom;
        
        if (fixed_interaction_bottom <= window_height) {
            // 当固定互动栏距离窗体底部的距离小于或等于窗体高度时，隐藏浮动互动栏
            float_interaction.value.style.transform = 'translateY(100%)';
        } else {
            // 否则显示浮动互动栏
            float_interaction.value.style.transform = 'translateY(0)';
        }
        
        // 确保在初始状态设置完成后添加滚动事件监听器
        window.addEventListener('scroll', handleScroll);
    } catch (e) {
        console.log(e);
    }
}

function handleScroll() {
    if (float_interaction.value) {
        const currentScrollTop = window.scrollY;
        if (currentScrollTop > lastScrollTop) {
            // 向下滚动，隐藏浮动互动栏
            float_interaction.value.style.transform = 'translateY(100%)';
        } else {
            // 向上滚动，显示浮动互动栏
            float_interaction.value.style.transform = 'translateY(0)';
            float_interaction_bar(true)
        }
        lastScrollTop = currentScrollTop;
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // 或 'auto'
    });
}

onMounted(() => {
    float_interaction_bar(true); // 初始调用
    window.addEventListener('scroll', handleScroll);
    //加载时自动滚动到最上方
    scrollToTop();
});


watch(() => store.getters.work_id,async (newValue) => {
    work_id.value = newValue;
    scrollToTop();
    await get_work_info();
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
    float_interaction_bar(false); // 清理状态
});

//查看更多按钮实现
function show_all_img() {
    max_img_len.value = work_info.value.content_file_list.split(/[,，]/).length + 1;
}

const props = defineProps({
    work_id: {
        type: String,
        default: '1'
    }
});



onMounted(async () => {
    work_id.value = store.getters.work_id;
    await get_work_info();
    await user_interaction.watch_work(parseInt(work_id.value,), token, 'ill', work_info.value.name);
    //请求点赞状态
    like_status.value = await user_interaction.like_work(
        work_id.value, 'search', token, 'ill', work_info.value.name) == 1 ? true : false;
    collect_status.value = await user_interaction.collect_work(
        work_id.value, 'search', token, 'ill', work_info.value.name) == 1 ? true : false;
    work_data.value.watch = await user_interaction.watch_work(work_id.value, token, 'ill', work_info.value.name)
    work_data.value.like = await user_interaction.like_work(work_id.value, 'count', token, 'ill', work_info.value.name)
    work_data.value.collect = await user_interaction.collect_work(work_id.value, 'count', token, 'ill', work_info.value.name)
});
watch(work_id, async () => {
    await get_work_info();
    await user_interaction.watch_work(parseInt(work_id.value,), token, 'ill', work_info.value.name);
    //请求点赞状态
    like_status.value = await user_interaction.like_work(
        work_id.value, 'search', token, 'ill', work_info.value.name) == 1 ? true : false;
    collect_status.value = await user_interaction.collect_work(
        work_id.value, 'search', token, 'ill', work_info.value.name) == 1 ? true : false;
    work_data.value.watch = await user_interaction.watch_work(work_id.value, token, 'ill', work_info.value.name)
    work_data.value.like = await user_interaction.like_work(work_id.value, 'count', token, 'ill', work_info.value.name)
    work_data.value.collect = await user_interaction.collect_work(work_id.value, 'count', token, 'ill', work_info.value.name)
})
// 使用ID请求作品信息
async function get_work_info() {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/get_work_info/GetIllInfo/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body: JSON.stringify({
                work_id: work_id.value
            })
        });
        if (res.ok) {
            const data = await res.json();
            if (data.status === 'success') {
                work_info.value = data.data[0];
                console.log(work_info.value)
            } else {
                console.log(data.message);
            }
        }
    } catch (e) {
        console.log(e);
    }
}

// 查看作品详情
function show_work_info(item) {
    img_content_page_show.value = true;
    item_path.value = `https://www.sunyuanling.com/image/${item}`;
    store.commit('SET_ITEM_PATH', item)
}

watch(img_content_page_show, (newValue) => {
    if (newValue) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = '';
    }
});

function close_content_page() {
    img_content_page_show.value = false;
}
//获取子组件传递的作品ID并设置在本页面
async function get_choose_item(item) {
    work_id.value = item.work_id;
    await user_interaction.watch_work(work_id.value, token, 'ill', work_info.value.name);
}

</script>

<style scoped>
.ill_index {
    display: flex;
    width: 85%;
    height: auto;
    margin: 10px auto;
    background-color: rgba(0, 0, 0, 0.05);
    border-radius: 10px;
}

.content {
    display: flex;
    flex-direction: column;
    width: 70%;
    height: 100%;
    position: relative;
    gap: 10px;
}

.item_box {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    position: relative;
    margin-top: 10px;
}

.item {
    display: flex;
    width: 95%;
    height: auto;
    justify-content: center;
    margin: 0px auto;
    border-radius: 10px;
    overflow: hidden;
    cursor: zoom-in;
    flex-direction: column;
}

.item_img {
    width: 100%;
    height: auto;
    object-fit: cover;
}

.author_info_box {
    display: flex;
    width: 30%;
    height: auto;
    padding-right: 10px;
    max-width: 30%;
    min-width: 30%;
}
.author_info_box_bottom{
    display: flex;
    width: 100%;
    height: auto;
}

.show_more_btn {
    display: flex;
    width: 100%;
    height: auto;
    align-items: center;
    justify-content: center;
    position: absolute;
    bottom: 0px;
    min-height: 80px;
    background-color: transparent;
}

.show_more_background {
    position: absolute;
    inset: 0px;
    background-color: rgba(255, 255, 255, 1);
    mask-image: linear-gradient(transparent, rgb(0, 0, 0) 100%, rgb(0, 0, 0) 0px);
}

.show_more_btn span {
    width: auto;
    height: auto;
    background-color: rgb(58, 58, 58);
    padding: 10px 20px;
    color: rgba(255, 255, 255, 1);
    border-radius: 15px;
    font-size: 20px;
    font-weight: bold;
    z-index: 2;
    cursor: pointer;
}

.float_interaction {
    position: fixed;
    bottom: 0px;
    width: 60%;
    background: linear-gradient(to top, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0));
    height: 80px;
    display: flex;
    align-items: center;
    transition: all 0.3s ease-in-out;
}
.comment_section{
    width: 100%;
    margin-top: 10px;
}
.recommend_page{
    width: 85vw;
    display: flex;
    margin:5px auto;
}
</style>