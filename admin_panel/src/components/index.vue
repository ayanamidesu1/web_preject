<template>
  <div class="index">
    <header_page></header_page>
    <div class="content">
        <router-view></router-view>
    </div>
  </div>
</template>


<script setup>
import { ref,onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '@/model/store/store';
import header_page from '@/components/model/header_page.vue'
import { BaseApi } from '@/base_api';
const router = useRouter()
const store = useStore()
const api = new BaseApi()
//获取自身信息
async function get_self_info(){
    try{
        let res=await api.get_self_info()
        if(res.status==200){
            store.$state.user=res.result.data
        }
        else{
            console.log(res)
            router.push('/login')
        }
    }
    catch(e){
        console.log(e)
    }
}
//登录状态验证
async function check_login_status(){
    try{
        let res=await api.verify_login()
        if(res.status==200){
            return
        }
        else{
            console.log(res)
            router.push('/login')
        }
    }
    catch(e){
        console.log(e)
    }
}
onMounted(()=>{
    check_login_status()
    get_self_info()
})

</script>

<style scoped>
.index{
    display: grid;
    width:90%;
    margin: 10px auto;
    grid-template-rows: 100px 1fr;
}
</style>