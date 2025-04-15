<template>
    <div class="collect_page">
        收藏
        <div class="menu_box">
            <div class="menu_item">
                <span @click="set_filter_data('is_open', 'all')">全部状态</span>
                <span @click="set_filter_data('is_open', 'public')">公开</span>
                <span @click="set_filter_data('is_open', 'private')">私密</span>
                <span @click="choose_status=true">进入选择</span>
                <span @click="choose_status=false">退出选择</span>
            </div>
            <div class="menu_item">
                <span @click="set_filter_data('work_type','all')">全部</span>
                <span @click="set_filter_data('work_type','ill')">插画</span>
                <span @click="set_filter_data('work_type','comic')">漫画</span>
                <span @click="set_filter_data('work_type','novel')">小说</span>
            </div>
            <div class="menu_item_sub">
                <span @click="choose_all()">全选</span>
                <span @click="cancel_choose_all()">取消全选</span>
                <span @click="update_collect_status('collect','false',choose_work_list)">取消收藏</span>
                <span @click="update_collect_status('open','false',choose_work_list)">设置为私密收藏</span>
                <span @click="update_collect_status('open','true',choose_work_list)">设置为公开收藏</span>
            </div>
        </div>        
        <div class="work_list">
            <div class="item" v-for="(value,key,index) in work_list" :key="index">
                <div class="item_1" v-for="(item,index_1) in value" :key="index_1">
                    <span class="title">{{item.work_name}}</span>
                    <span class="type">{{key}}&nbsp;{{key=='ill'?'插画':key=='comic'? '漫画':'小说'}}</span>
                    <img class="image" :src="file_name(key,item)" alt="图像" width="150px" height="200px">
                    <div class="user_info">
                        <div class="avatar">
                            <img :src="'https://www.sunyuanling.com/server/static/image/avatar_thumbnail/'+item.user_avatar" alt="头像">
                        </div>
                        <span class="username">{{item.username}}</span>
                    </div>
                    <div class="choose_box" v-if="choose_status">
                        <div class="choose_img" v-if="item.is_choose==0" @click="choose_work(key,index_1,item.work_type,1,item.work_id)">
                            <img src="https://www.sunyuanling.com/server/static/svg/未选择.svg" alt="未选择">
                        </div>
                        <div class="is_choose" v-if="item.is_choose==1" @click="choose_work(key,index_1,item.work_type,0,item.work_id)">
                            <img src="https://www.sunyuanling.com/server/static/svg/正确.svg" alt="正确">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <page :total="total" :pageSize="limit" @page-change="load_more($event)"></page>
    </div>
</template>

<script setup>
import {ref,onMounted,computed} from 'vue'
import {useRouter} from 'vue-router'
import { useStore } from '@assets/model/store';
import { BaseApi } from '@/base_api';
import page from '@assets/model/page.vue';

const store = useStore();
const router = useRouter();
const api=new BaseApi()

const filter_work_list = computed(() => {
    let result = work_list.value
    //筛选作品公开状态
    if (filter_open.value !== 'all') {
        result = result.filter(item => item.is_open === (filter_open.value === 1 ? true : false))
    }
    //筛选作品类型
    if (filter_type.value !== 'all') {
        result = result.filter(item => item.work_type === filter_type.value)
    }
    return result
})

const choose_status=ref(false)
const work_list=ref()
let limit=ref(10)
let offset=ref(0)
let total=ref(0)
let filter_data=ref({
    is_open:'public',
    work_type:'all'
})
//选择作品
let choose_work_list=ref([])
function choose_work(key, index, work_type, status, work_id) {
    const list = choose_work_list.value
    const exists_index = list.findIndex(i => i.work_id === work_id)

    if (status === 1) {
        // 选中作品
        if (exists_index === -1) {
            list.push({ key, work_type, work_id })
        }
        work_list.value[key][index].is_choose = 1
    } else if (status === 0) {
        // 取消选择 → 从列表中移除
        if (exists_index !== -1) {
            list.splice(exists_index, 1)
        }
        work_list.value[key][index].is_choose = 0
    }
}

//全选
function choose_all() {
    for (let key in work_list.value) {
        const works = work_list.value[key]
        for (let index = 0; index < works.length; index++) {
            const item = works[index]
            choose_work(key, index, key, 1, item.work_id)
        }
    }
}


//取消全选
function cancel_choose_all() {
    for (let key in work_list.value) {
        const works = work_list.value[key]
        for (let index = 0; index < works.length; index++) {
            const item = works[index]
            choose_work(key, index, key, 0, item.work_id)
        }
    }
}

//筛选作品
async function set_filter_data(type,item){
    if(type=='is_open'){
        filter_data.value.is_open=item
    }
    else if(type=='work_type'){
        filter_data.value.work_type=item
    }
    await get_work_list()
}
//获取收藏作品
const get_work_list=async ()=>{
    let res=await api.post('GetUserInfo/GetUserCollect_new',{
        limit:limit.value,
        offset:offset.value,
        filter_data:filter_data.value
    })
    if(res.status==200){
        console.log(res)
        work_list.value=res.result.data.work_list
        total.value=res.result.data.total
    }
    else{
        console.log(res)
    }
}
//加载更多
const load_more=async (target_page)=>{
    offset.value=(target_page-1)*limit.value
    get_work_list()
}

//更新收藏状态
const update_collect_status=async (type,status,work_list)=>{
    let res=await api.post('GetUserInfo/UpdateCollectStatus',{
        type,status,work_list
    })
    if(res.status==200){
        alert('操作成功')
        await get_work_list()
    }
    else{
        alert('操作失败')
        console.log(res)
    }
}

//格式化路径
const file_name=(work_type,item)=>{
    let url='https://www.sunyuanling.com/server/static/image/'
    if(work_type=='novel'){
        return url+'novel/thumbnail/'+item.work_cover
    }
    else if(work_type=='ill'){
        return url+'/thumbnail/'+item.content_file_list.split(/[,，]/)[0]
    }
    else if(work_type=='comic'){
        return url+'/comic/thumbnail/'+item.content_file_list.split(/[，,]/)[0]
    }
}

onMounted(()=>{
    get_work_list()
})

</script>

<style lang="scss" scoped>
.collect_page{
    display: flex;
    flex-direction: column;
    gap:10px;
    .menu_box {
        display: flex;
        flex-direction: column;
        gap: 12px;
      
        .menu_item,
        .menu_item_sub {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
        }
      
        span {
          padding: 6px 14px;
          border-radius: 20px;
          background-color: #f0f0f0;
          cursor: pointer;
          font-size: 14px;
          color: #333;
          border: 1px solid transparent;
          transition: all 0.25s;
        }
      
        span:hover {
          background-color: rgb(0, 150, 250);
          color: #fff;
          transform: scale(1.05);
        }
      
        span:active {
          transform: scale(0.95);
        }
      
        .active {
          background-color: rgb(0, 150, 250);
          color: #fff;
          border: 1px solid rgb(0, 100, 200);
        }
      }
      
    .work_list{
        display: flex;
        flex-wrap: wrap;
        gap:10px;
        .item{
            display: flex;
            flex-wrap: wrap;
            gap:10px;
            min-width: 150px;
            align-items: center;
            justify-content: space-between;
            .item_1{
                display: flex;
                flex-direction: column;
                gap:10px;
                position: relative;
                padding: 10px;
                .title{
                    font-size: 18px;
                    font-weight: bold;
                    color: #333;
                }
                .type{
                    font-size: 14px;
                    color: #666;
                }
                .image{
                    width: 150px;
                    height: 200px;
                    object-fit: cover;
                }
                .user_info{
                    display: flex;
                    align-items: center;
                    gap:10px;
                    .avatar{
                        width: 30px;
                        height: 30px;
                        border-radius: 50%;
                        overflow: hidden;
                        img{
                            width: 100%;
                            height: 100%;
                            object-fit: cover;
                        }
                    }
                    .username{
                        font-size: 14px;
                        color: #666
                    }
                }
                .choose_box{
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    top:0px;
                    left:0px;
                    background-color:rgba(0,0,0,0.3);
                    transition: all 0.2s;
                    border-radius: 5px;
                    img{
                        position: absolute;
                        bottom: 5px;
                        right: 5px;
                        width: 30px;
                        height: 30px;
                        cursor: pointer;
                    }
                }
            }
        }
    }
}
</style>