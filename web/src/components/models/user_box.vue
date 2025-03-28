<template>
  <div class="user_box" v-if="user">
    <div class="avatar">
        <img 
        :src="'https://www.sunyuanling.com/server/static/image/user_thumbnail/'+(user.user_avatar||'default_avatar.jpg')" 
        alt="头像" width="50px" height="50px">
    </div>
    <div class="user_name">
        <span>
            {{user.username}}
        </span>
    </div>
  </div>
</template>


<script setup>
import { ref,defineProps,onMounted } from 'vue'
import { useStore } from '@assets/model/store/index';
import { useRouter } from 'vue-router';
import { BaseApi } from '@/base_api';

const store = useStore();
const router = useRouter();
const user = ref({});
const api=new BaseApi()

const props=defineProps({
    user_id:{
        type:Number,
        default:0
    }
})

async function get_user_info(){
    let res=await api.get_user_info_by_id(props.user_id)
    user.value=res.result.data
}
onMounted(async ()=>{
    await get_user_info()
    console.log(props.user_id);
})

</script>

<style scoped>
.user_box{
    display: flex;
    gap:10px;
    align-items: center;
    max-width: 200px;
}
.avatar img{
    border-radius: 50%;
}
</style>