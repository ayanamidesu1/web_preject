<template>
  <div class="root_page">
    <div class="header_box">
        <header_box></header_box>
    </div>
    <div class="content_box">
        <router-view></router-view>
    </div>
  </div>
</template>


<script setup>
import { ref,onMounted,computed } from 'vue'
import header_box from './headpage_file/header_box.vue';
import { useStore } from '@assets/model/store/index';
import { BaseApi } from '@/base_api';
const store = useStore()
const api=new BaseApi()

onMounted(async ()=>{
  //登录验证
  let result=await api.verify_login()
  if(result.status==200){
    let user=await api.get_self_info()
    console.log('用户信息\n',user)
    store.$state.user=user.result.data
  }
  else{
    console.log('错误\n',result)
  }
  //获取用户信息
})

</script>

<style scoped>
.switch_page {
  display: flex;
  width: 80%;
  margin: 0 auto;
  margin-top: 20px;
}

.switch_page > span {
  margin-left: 10px;
  padding: 5px;
  margin: 0;
  font-size: 18px;
  cursor: pointer;
  font-weight: bold;
}

.switch_page > span.active {
  background-color: rgba(233, 233, 233, 1);
  border-bottom: 3px solid rgba(0, 150, 250, 1);
}
</style>