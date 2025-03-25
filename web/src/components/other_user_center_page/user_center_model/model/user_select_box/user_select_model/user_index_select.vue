<template>
    <div class="user_index_select" v-if="msg_list && msg_list.length > 0">
        <div class="title">
            <span><b>精选</b></span>
        </div>
        <div class="content">
            <scroll_box :msg_list="msg_list" @open_select_box="add_select_page_show = true"
                @chose_item="get_choose_item">
            </scroll_box>
        </div>
    </div>
    <div class="if_all_none" v-else>
        <span>这里空空如也什么也没有</span>
      </div>
</template>

<script setup>
import { ref, defineProps, onMounted } from 'vue';
import scroll_box from './model/scroll_box.vue';
import { get_workinfo } from '../../../js/get_workinfo';
import { useStore } from 'vuex'
const store = useStore()
const props = defineProps({
    user_info: {
        type: Object,
        default: () => ({})
    },
    token: {
        type: String,
        default: ''
    },
    userid:{
        type: String,
        default: ''
    },
});

// 构建滚动盒子所需的数据结构
let msg_list = ref(JSON.parse(props.user_info.select_work));
let add_select_page_show = ref(false);
function get_msg_list() {
    let result = [];
    for (let work_type in msg_list.value) {
        // 遍历 work_type 对应的 ID 列表
        for (let id of msg_list.value[work_type]) {
            result.push({ work_type: work_type, work_id: id });
        }
    }
    console.log(result);
    return result;
}

//获取用户点击的内容
function get_choose_item(item) {
    console.log(item);
    if (item.work_type == 'ill') {
        store.commit('SET_CONTENT_PAGE', {
            key: 'ill_page',
            value: true
        })
        store.commit('SET_SINGLE_PAGE_STATUS', { key: 'content_index_page', value: true })
        store.commit('SET_WORK_ID', item.work_id)
        store.commit('SET_WORK_TYPE', item.work_type)
    }
    else if(item.work_type=='comic')
    {
        store.commit('SET_CONTENT_PAGE', {
            key: 'comic_page',
            value: true
        })
        store.commit('SET_SINGLE_PAGE_STATUS', { key: 'content_index_page', value: true })
        store.commit('SET_WORK_ID', item.work_id)
        store.commit('SET_WORK_TYPE', item.work_type)
    }
    else if(item.work_type=='novel')
    {
        store.commit('SET_CONTENT_PAGE', {
            key: 'novel_page',
            value: true
        })
        store.commit('SET_SINGLE_PAGE_STATUS', { key: 'content_index_page', value: true })
        store.commit('SET_WORK_ID', item.work_id)
        store.commit('SET_WORK_TYPE', item.work_type)
    }
}

onMounted(async () => {
    get_msg_list();
    msg_list.value = await get_workinfo(props.token, props.userid,get_msg_list());
    console.log(msg_list.value);
});
</script>



<style scoped>
.if_all_none {
    text-align: center;
    font-size: 18px;
    color: #888;
  } 
</style>