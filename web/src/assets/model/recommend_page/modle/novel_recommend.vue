<template>
    <div class="novel_recommend">
        <div class="content">
            <div class="item" v-for="(item,index) in work_info" :key="index" >
                <div class="work_cover" @click="choose_item(item.work_id)">
                    <img class="cover_img" :src="'https://www.sunyuanling.com/image/novel/thumbnail/'+item.work_cover">
                </div>
                <div class="work_info">
                    <div class="work_name">
                        <span>{{item.work_name}}</span>
                    </div>
                    <div class="brief_introduction">
                        <span>{{item.brief_introduction}}</span>
                    </div>
                    <div class="work_status">
                        <span>{{item.category}}</span>
                        <span>{{item.is_vip_work==1?'vip作品':'免费作品'}}</span>
                        <span>{{item.work_status}}</span>
                    </div>
                    <div class="author_info" @click="choose_user(item.author_info.userid)">
                        <div class="author_avatar">
                            <img class="avatar_img" :src="'https://www.sunyuanling.com/image/avatar_thumbnail/'+item.author_info.user_avatar">
                        </div>
                        <div class="author_name">
                            <span>{{item.author_info.username}}</span>
                        </div>
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
const emit = defineEmits(['choose_item','choose_user'])
function choose_item(item) {
    console.log(item)
    emit('choose_item', item)
    store.commit('SET_CONTENT_PAGE', { key: 'novel_page', value: true })
    store.commit('SET_SINGLE_PAGE_STATUS', { key: 'content_index_page', value: true })
    store.commit('SET_WORK_ID', item)
}
function choose_user(item){
    console.log(item)
    emit('choose_user', item)
    store.commit('SET_OTHER_USERID', item)
    store.commit('SET_SINGLE_PAGE_STATUS', { 'key': 'other_user_center_page', 'value': true })
}
// eslint-disable-next-line no-unused-vars
let work_cover = computed(() => props.work_info)
</script>

<style scoped>
.novel_recommend {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: auto;
}

.content {
    display: flex;
    width: 100%;
    height: auto;
    flex-wrap: wrap;
    gap: 20px;
}

.item {
    display: flex;
    margin-bottom: 20px;
    gap: 10px;
    max-width: 35vw;
    min-width: 35vw;
}

.work_cover {
    flex: 0 0 160px; /* 固定封面宽度 */
    width: 160px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.cover_img {
    width: 100%;
    height:100%;
    object-fit: cover;
    border-radius: 8px;

}

.work_info {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    gap: 5px;
}

.work_name,
.author_info {
    margin-bottom: 10px;
}

.brief_introduction
{
    width: 100%;
    height: auto;
    max-height: 60px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    color: #999;
    font-size: 14px;
    line-height: 1.5;
}

.work_status{
    width: 100%;
    height: auto;
    display: flex;
    gap: 10px;
}

.work_name span,
.brief_introduction span,
.work_status span,
.author_name span {
    display: block;
}

.author_info {
    display: flex;
    align-items: center;
    cursor: pointer;
    width: 100%;
    height: auto;
}

.author_avatar {
    flex: 0 0 40px; 
    margin-right: 10px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.avatar_img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}
</style>