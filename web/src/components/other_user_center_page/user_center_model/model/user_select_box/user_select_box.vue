<template>
  <div class="user_select_box" v-if="user_info">
    <div class="content">
        <div class="select_page">
            <div class="page_item" @click="select_index_page=0" :class="select_index_page==0?'choose_item':''">
                主页
            </div>
            <div class="page_item" @click="select_index_page=1" :class="select_index_page==1?'choose_item':''">
                插画
            </div>
            <div class="page_item" @click="select_index_page=2" :class="select_index_page==2?'choose_item':''">
                小说
            </div>
            <div class="page_item" @click="select_index_page=3" :class="select_index_page==3?'choose_item':''">
                收藏
            </div>
        </div>
        <user_index_select :user_info="user_info" :token="token" :userid="userid" v-if="select_index_page==0"></user_index_select>
        <ill_select :user_info="user_info" :token="token" :userid="userid" v-if="select_index_page==1"></ill_select>
        <novel_select :user_info="user_info" :token="token" :userid="userid" v-if="select_index_page==2"></novel_select>
        <collect_page :user_info="user_info" :token="token" :userid="userid" v-if="select_index_page==3"></collect_page>
    </div>
  </div>
</template>

<script setup>
import {ref,defineProps} from 'vue'
import user_index_select from './user_select_model/user_index_select.vue'
import ill_select from './user_select_model/ill_select.vue';
import novel_select from './user_select_model/novel_select.vue';
import collect_page from './user_select_model/collect_page.vue';
let props=defineProps({
    user_info:{
        type:Object,
        default:()=>{
            return {}
        }
    },
    token:{
        type:String,
        default:''
    },
    userid:{
        type:String,
        default:''
    }
})
let select_list=ref(JSON.parse( props.user_info.select_work))

let select_index_page=ref(0)
</script>

<style scoped>
.user_select_box{
    width: 90%;
    height: auto;
    display: flex;
    flex-direction: column;
    margin:10px auto;
}
.content{
    display: flex;
    width: 100%;
    height: 100%;
    flex-direction: column;
    gap: 10px;
}
.select_page{
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: row;
    margin-top: 10px;
}
.page_item{
    width: auto;
    height: auto;
    display: flex;
    padding: 5px 15px;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    font-size: 18px;
}
.choose_item{
    border-bottom: 3px solid rgba(0,150,250,1);
    color: rgba(0,150,250,1);
    transform: translateY(-2px);
    transition: all 0.2s;
    font-weight: bold;
}
</style>