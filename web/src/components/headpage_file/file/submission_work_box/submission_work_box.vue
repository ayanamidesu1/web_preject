<template>
    <div class="submission_work_box_page">
        <div class="submission_work_box_item" @click="set_page_type('ill')">
            <div class="submission_work_box_icon">
                <img class="icon" src="https://www.sunyuanling.com/assets/photo.svg">
            </div>
            <div class="submission_work_box_text">插画</div>
        </div>
        <div class="submission_work_box_item" @click="set_page_type('ill')">
            <div class="submission_work_box_icon">
                <img class="icon" src="https://www.sunyuanling.com/assets/play.svg">
            </div>
            <div class="submission_work_box_text">动图</div>
        </div>
        <div class="submission_work_box_item" @click="set_page_type('comic')">
            <div class="submission_work_box_icon">
                <img class="icon" src="https://www.sunyuanling.com/assets/comic.svg">
            </div>
            <div class="submission_work_box_text">漫画</div>
        </div>
        <div class="submission_work_box_item" @click="set_page_type('novel')">
            <div class="submission_work_box_icon">
                <img class="icon" src="https://www.sunyuanling.com/assets/novel.svg">
            </div>
            <div class="submission_work_box_text">小说</div>
        </div>
    </div>
    
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted } from 'vue';
import{useStore } from 'vuex'
export default {
    name: 'submission_work_box',
}
</script>

<script setup>
const store=useStore()

function set_page_type(type){
 store.commit('SET_UPLOAD_WORK_TYPE',type)
 //store.commit('SET_UPLOAD_WORK',true)
 store.commit('SET_SINGLE_PAGE_STATUS',{key:'upload_work',value:true})
}
</script>

<style scoped>
.submission_work_box_page {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    position: relative;
}

.submission_work_box_item {
    display: flex;
    margin-top: 10px;
    width: 98%;
    height: 40px;
    padding: 5px;
    margin-left: auto;
    margin-right: auto;
    align-items: center;
}

.submission_work_box_item:hover {
    background-color: rgba(184, 184, 184, 0.7);
    cursor: pointer;
    transition: 0.2s;
    border-radius: 5px;
}

.submission_work_box_icon {
    width: 30px;
    height: 30px;
    overflow: hidden;
    margin-left: 5px;
    margin-right: 10px;
}

.submission_work_box_icon svg {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.icon{
    width: 30px;
    height: 30px;
    object-fit: cover;
}
</style>
