<template>
  <div class="user_box">
    <div class="user_info">
        <div class="user_avatar">
            <img :src="'https://www.sunyuanling.com/server/static/image/avatar_thumbnail/'+(user.user_avatar||'default.jpg')" alt="头像">
        </div>
        <div class="user_name">
            <span>{{ user.username }}</span>
        </div>
    </div>
    <input_index @content="get_comment_connect"/>
  </div>
</template>


<script setup>
import { ref,computed } from 'vue'
import {useStore} from '@assets/model/store/index'
import input_index from './input_box/input_index.vue';
import {useCommentStore} from './store'

const store = useStore()
const use_comment_store=useCommentStore()

let user=computed(()=>store.$state.user)

let comment_connect=ref()
function get_comment_connect(e){
    console.log(e)
    comment_connect.value=e
    use_comment_store.set_main_reply(comment_connect.value)
    use_comment_store.debug()
}

</script>

<style scoped>
.user_box{
    display: flex;
    gap:20px;
    height:fit-content;
    max-height: 400px;
    width: 100%;
    align-items: center;
    border-bottom: 1px solid #ccc;
    flex-direction: column;
}
.user_info{
    display: flex;
    gap:20px;
    width: fit-content;
    height: fit-content;
    max-height: 100px;
    align-self: flex-start;
}
.user_avatar{
    width:80px;
    height: 80px;
}
.user_avatar img{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}
.user_name{
    display: flex;
    align-items: center;
    font-size: 20px;
    font-weight: 600;
}
</style>