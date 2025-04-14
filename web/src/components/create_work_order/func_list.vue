<template>
    <div class="list">
        <div class="list_box">
            <div class="item" v-for="(item,index) in list" :key="index" @click="choose_item(index)">
                <img :src="getCoverUrl(item.cover)" alt="封面" class="cover" />
                <div class="content">
                    <h3 class="title">{{ item.title }}</h3>
                    <p class="intro">{{ item.introduce }}</p>
                    <div class="price">￥{{ Number(item.amount_of_money).toFixed(2) }}</div>
                </div>
            </div>
        </div>
        <div class="check_point" style="display: inline-block;width:100%;height:1px;opacity:0;" ref="check_point"></div>
    </div>
</template>


<script setup>
import { ref, defineProps, computed, defineEmits, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router';
import { useStore } from '@assets/model/store';
import { BaseApi } from '@/base_api';

const store = useStore();
const router = useRouter();
const api = new BaseApi();

const props = defineProps({
    user_id: {
        type: String,
    }
})
const emit = defineEmits(['choose_item'])

let limit = ref(10)
let offset = ref(0)
let total = ref(0)
let list = ref([])
let check_point = ref(null)

//选择方案
function choose_item(index){
    emit('choose_item',list.value[index])
}

const getCoverUrl = (fileName) => {
    // 根据你项目封面图路径调整此处
    return `https://www.sunyuanling.com/server/static/image/${fileName}`
}


//获取方案列表
const get_list=async()=>{
    let res=await api.post('api/GetUserFuncList',{
        target_user_id:props.user_id,
        limit:limit.value,
        offset:offset.value
    })
    if(res.status==200)
    {
        console.log(res)
        list.value=res.result.data
        total.value=res.result.total
    }
    else{
        console.log(res)
    }
}

//加载更多
const load_more=()=>{
    offset.value+=limit.value
    if(offset.value<total.value){
        get_list()
    }
    else{
        console.log('没有更多了')
    }
}
//滚动加载
let obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            load_more();
        }
    });
}, {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
});

onMounted(()=>{
    get_list()
    obs.observe(check_point.value)
    if(list.value.length>0){
        emit('choose_item',list.value[0])
    }
})
onUnmounted(()=>{
    obs.disconnect()
})

</script>

<style lang="scss" scoped>
.list_box {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 16px;
}

.item {
    display: flex;
    align-items: flex-start;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    padding: 12px;
    cursor: pointer;
    transition: transform 0.2s ease;

    &:hover {
        transform: translateY(-2px);
    }

    .cover {
        width: 120px;
        height: 80px;
        object-fit: cover;
        border-radius: 8px;
        margin-right: 12px;
    }

    .content {
        flex: 1;

        .title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 6px;
        }

        .intro {
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
            line-height: 1.4;
        }

        .price {
            font-size: 14px;
            color: #f40;
            font-weight: bold;
        }
    }
}

</style>