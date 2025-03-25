<template>
    <div class="add_select_page" v-if="work_list">
        <div class="content">
            <div class="title">
                <span></span>
                <span><b>新增精选作品</b></span>
                <div class="close_btn" @click="close_btn">
                    <img class="icon" src="https://www.sunyuanling.com/assets/close.svg">
                </div>
            </div>
            <div class="choose_item">
                <div class="item" @click="item_index = 0" :class="item_index == 0 ? 'choose_status' : ''">
                    <span>插画</span>
                </div>
                <div class="item" @click="item_index = 1" :class="item_index == 1 ? 'choose_status' : ''">
                    <span>小说</span>
                </div>
                <div class="item" @click="item_index = 2" :class="item_index == 2 ? 'choose_status' : ''">
                    <span>漫画</span>
                </div>
            </div>
            <div class="item_page_ill" v-if="item_index == 0">
                <span>选择插画作品</span>
                <div class="ill_item_list">
                    <div class="ill_item" v-for="(item, index) in work_list.ill" :key="index">
                        <div class="item_page_img" @click="handleItemClick(item, 'ill')">
                            <img
                                :src="'https://www.sunyuanling.com/image/thumbnail/' + item.content_file_list.split(/[,，]/)[0]">
                            <div class="correct_box"
                                :class="includesLoose(select_work.ill, item.Illustration_id) ? 'correct_box_choose' : ''"
                                v-if="includesLoose(select_work.ill, item.Illustration_id)">
                                <img src="https://www.sunyuanling.com/assets/correct.svg" alt="" class="icon">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="item_page_novel" v-if="item_index == 1">
                <span>选择小说作品</span>
                <div class="novel_item_list">
                    <div class="novel_item" v-for="(item, index) in work_list.novel" :key="index">
                        <div class="item_page_img" @click="handleItemClick(item, 'novel')">
                            <img :src="'https://www.sunyuanling.com/image/novel/thumbnail/' + item.work_cover">
                            <div class="correct_box"
                                :class="includesLoose(select_work.novel, item.work_id) ? 'correct_box_choose' : ''"
                                v-if="includesLoose(select_work.novel, item.work_id)">
                                <img src="https://www.sunyuanling.com/assets/correct.svg" alt="" class="icon">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="item_page_comic" v-if="item_index == 2">
                <span>选择漫画作品</span>
                <div class="comic_item_list">
                    <div class="comic_item" v-for="(item, index) in work_list.comic" :key="index">
                        <div class="item_page_img" @click="handleItemClick(item, 'comic')">
                            <img
                                :src="'https://www.sunyuanling.com/image/comic/thumbnail/' + item.content_file_list.split(/[,，]/)[0]">
                            <div class="correct_box"
                                :class="includesLoose(select_work.comic, item.id) ? 'correct_box_choose' : ''"
                                v-if="includesLoose(select_work.comic, item.id)">
                                <img src="https://www.sunyuanling.com/assets/correct.svg" alt="" class="icon">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tips">
                <span>一共可以选择5个作品 当前还可选择{{remainingSelection}}</span>
            </div>
            <div class="btn_box">
                <div class="submit btn_choose" @click="submit_select_work()">
                    <span>确定</span>
                </div>
                <div class="cancel btn_choose" @click="close_btn">
                    <span>取消</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, onMounted, computed, defineEmits } from 'vue';
import { get_user_all_worklist } from '../../../../js/get_workinfo.js'
import { update_user_select_work } from '../../../../js/update_userinfo.js'

const props = defineProps({
    user_info: {
        type: Object,
        default: () => ({})
    },
    token: {
        type: String,
        default: ''
    }
})
const emit = defineEmits(['close_page'])

function close_btn() {
    emit('close_page', false)
}

const work_list = ref()
const item_index = ref(0)
const select_work = ref({
    ill: [],
    novel: [],
    comic: []
})
const temp_work_list = ref(JSON.parse(props.user_info.select_work))

const remainingSelection = computed(() => 5 - (
    select_work.value.ill.length +
    select_work.value.novel.length +
    select_work.value.comic.length
))

function set_select_work() {
    if (temp_work_list.value.ill != null) {
        select_work.value.ill = temp_work_list.value.ill
    }
    if (temp_work_list.value.novel != null) {
        select_work.value.novel = temp_work_list.value.novel
    }
    if (temp_work_list.value.comic != null) {
        select_work.value.comic = temp_work_list.value.comic
    }
}

function includesLoose(array, value) {
    if (!Array.isArray(array) || array.length === 0 || value === undefined || value === null) {
        return false
    }
    return array.some(item => item == value)
}

function handleItemClick(item, type) {
    let id
    if (type === 'ill') {
        id = item.Illustration_id
    } else if (type === 'novel') {
        id = item.work_id
    } else if (type === 'comic') {
        id = item.id
    }

    const currentList = select_work.value[type]

    if (includesLoose(currentList, id)) {
        select_work.value[type] = currentList.filter(x => x !== id)
    } else {
        const totalLength = select_work.value.ill.length + select_work.value.novel.length + select_work.value.comic.length
        if (totalLength < 5) {
            if (currentList.length < 5) {
                select_work.value[type].push(id)
            } else {
                alert('选择的作品数量已达单个类型上限（5个）')
            }
        } else {
            alert('选择的作品数量已达总上限（5个）')
        }
    }
}

async function submit_select_work() {
    const message = await update_user_select_work(props.token, select_work.value)
    if (message) {
        alert('提交成功')
        close_btn()
    } else {
        alert('提交失败')
    }
}

onMounted(async () => {
    work_list.value = await get_user_all_worklist(props.token)
    set_select_work()
})
</script>

<style scoped>
.add_select_page {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    max-height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-y: auto;
}

.content {
    width: auto;
    height: auto;
    display: flex;
    flex-direction: column;
    min-width: 450px;
    min-height: 100px;
    background-color: white;
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
    overflow-y: auto;
    max-width: 650px;
    box-sizing: border-box;
    margin: 80px auto;
    max-height: 90vh;
}

.content::-webkit-scrollbar {
    width: 0px;
}

.title {
    width: 100%;
    height: auto;
    padding: 5px 0px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.close_btn {
    width: 35px;
    height: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.close_btn:hover {
    cursor: pointer;
    transform: scale(1.1);
    transition: all 0.2s ease-in-out;
    background-color: rgba(133, 133, 133, 0.5);
    border-radius: 50%;
}

.choose_item {
    width: 100%;
    height: auto;
    display: flex;
    align-items: center;
}

.item {
    width: auto;
    height: auto;
    flex: 1;
    flex-grow: 1;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: 5px 10px;
    cursor: pointer;
}

.choose_status {
    border-bottom: 3px solid rgba(0, 150, 250, 1);
    color: rgba(0, 150, 250, 1);
    transform: translateY(-2px);
    transform: scale(1.1);
    transition: all 0.2s;
    font-weight: bold;
    background-color: rgba(133, 133, 133, 0.3);
    border-radius: 5px 5px 0px 0px;
}

.item_page {
    width: auto;
    height: auto;
    display: flex;
    flex-direction: column;
    padding: 10px;
}

.item_page_ill,
.item_page_comic,
.item_page_novel {
    width: 100%;
    height: auto;
    flex-wrap: wrap;
    display: flex;
    flex-direction: row;
}

.item_page_img {
    width: 100px;
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    border-radius: 10px;
    cursor: pointer;
}

.item_page_img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
}

.ill_item_list,
.novel_item_list,
.comic_item_list {
    width: 100%;
    height: auto;
    display: flex;
    margin-top: 10px;
    gap: 10px;
}

.correct_box {
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    position: absolute;
    right: 1px;
    top: 1px;
}

.correct_box img {
    width: 18px;
    height: 18px;
    object-fit: cover;
}

.correct_box_choose {
    background-color: rgba(0, 150, 250, 0.8);
    border-radius: 50%;
}

.btn_box {
    width: auto;
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px 15px;
    gap: 15px;
    align-self: flex-end;
    margin-top: 20px;
}

.submit {
    background-color: rgba(0, 150, 250, 1);
    color: #fff;
    border-radius: 15px;
    padding: 5px 15px;
    width: auto;
    height: auto;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 16px;
    font-weight: bold;
}

.cancel {
    background-color: rgb(97, 97, 97);
    color: #fff;
    border-radius: 15px;
    padding: 5px 15px;
    width: auto;
    height: auto;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 16px;
    font-weight: bold;
    margin-left: 10px;
}

.btn_choose:hover {
    opacity: 0.8;
    transition: all 0.2s;
    transform: scale(1.1);
    transform: translateY(-2px);
}
</style>