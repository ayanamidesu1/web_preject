<template>
    <div class="comic_recommend">
        <div class="content">
            <div class="item" v-for="(item, index) in work_info" :key="index">
                <div class="work_cover" @click="choose_item(item.id)">
                    <img class="cover_img"
                        :src="'https://www.sunyuanling.com/image/comic/thumbnail/' + item.content_file_list.split(/[,，]/)[0]">
                    <div class="page_count" v-if="item.content_file_list.split(/[,，]/).length > 1">
                        <img class="icon" src="https://www.sunyuanling.com/assets/page_count.svg">
                       {{ item.content_file_list.split(/[,，]/).length }}
                    </div>
                    <div class="age_tag" v-if="item.age_classification!=16">
                        R-{{ item.age_classification }}
                    </div>
                </div>
                <div class="work_info">
                    <span>{{ item.name }}</span>
                </div>
                <div class="author_info" @click="choose_user(item.author_info.userid)">
                    <div class="author_avatar">
                        <img class="author_avatar"
                            :src="'https://www.sunyuanling.com/image/avatar_thumbnail/' + item.author_info.user_avatar">
                    </div>
                    <div class="author_name">
                        {{ item.author_info.username }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
// eslint-disable-next-line no-unused-vars
import { ref, defineProps, defineEmits, computed } from 'vue'
import { useStore } from 'vuex';
const store = useStore();
const props = defineProps({
    work_info: {
        type: Array,
        default: () => {
            return []
        }
    },
})
const emit = defineEmits(['choose_item', 'choose_user'])
function choose_item(item) {
    console.log(item)
    emit('choose_item', item)
    store.commit('SET_CONTENT_PAGE', { key: 'comic_page', value: true })
    store.commit('SET_SINGLE_PAGE_STATUS', { key: 'content_index_page', value: true })
    store.commit('SET_WORK_ID', item)
}
function choose_user(item) {
    console.log(item)
    emit('choose_user', item)
    store.commit('SET_OTHER_USERID', item)
    store.commit('SET_SINGLE_PAGE_STATUS', { 'key': 'other_user_center_page', 'value': true })
}
// eslint-disable-next-line no-unused-vars
let work_cover = computed(() => props.work_info)
</script>

<style scoped>
.comic_recommend {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
}

.content {
    width: 100%;
    height: auto;
    flex-wrap: wrap;
    display: flex;
    gap: 10px;
}

.item {
    width: 200px;
    height: auto;
    margin: 10px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    justify-content: flex-start;
}

.work_cover {
    position: relative;
    width: 200px;
    height: auto;
    cursor: pointer;
}

.cover_img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
    min-height: 200px;
    max-height: 200px;
    max-width: 200px;
    min-width: 200px;
}

.page_count {
    position: absolute;
    top: 5px;
    right: 5px;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 5px;
}

.age_tag {
    position: absolute;
    top: 5px;
    left: 5px;
    background-color: red;
    color: white;
    font-size: 16px;
    font-weight: bold;
    padding: 2px 5px;
    border-radius: 5px;
}

.work_info {
    margin-top: 10px;
}

.author_info {
    display: flex;
    width: 100%;
    align-items: center;
    margin-top: 10px;
    cursor: pointer;
}

.author_avatar {
    width: 40px;
    height: 40px;
    overflow: hidden;
    border-radius: 50%;
    margin-right: 10px;
}

.author_avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.author_name {
    font-size: 14px;
}
.icon{
    width: 15px;
    height: 15px;
    object-fit: cover;
}
</style>
