<template>
    <div class="user_background">
        <div class="content">
            <img :src="user_back_img" class="user_background_img">
            <div class="edit_btn_box">
                <div class="edit_btn btn" @click="edit_box_show = true">
                    <img src="https://www.sunyuanling.com/assets/edit.svg" class="icon">
                </div>
                <div class="delete_btn btn" @click="delete_user_back_img">
                    <img src="https://www.sunyuanling.com/assets/delete.svg" class="icon">
                </div>
            </div>
        </div>
        <edit_box :user_back_img="user_back_img" :token="token" v-if="edit_box_show" @close_page="edit_box_show = false"></edit_box>
    </div>
</template>

<script setup>
import { ref, defineProps } from 'vue'
import edit_box from './edit_box.vue';
import { delete_user_back } from '../../../js/update_userinfo';
const props = defineProps({
    user_back_img: {
        type: String,
        default: ''
    },
    token:{
        type:String,
        default: ''
    }
})
let edit_box_show = ref(false)
function delete_user_back_img() {
    // 弹窗确认
    let userConfirm = window.confirm('确定删除背景图片吗？');
    if (!userConfirm) {
        return;
    }
    delete_user_back(props.token);
}

</script>

<style scoped>
.user_background {
    width: 100%;
    height: 60vh;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.content {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
}

.user_background_img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.edit_btn_box {
    display: flex;
    width: auto;
    height: auto;
    position: absolute;
    right: 10px;
    bottom: 10px;
    justify-content: space-between;
    gap: 10px;
}

.btn {
    width: 35px;
    height: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.btn:hover {
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s;
    transform: translateY(-2px);
}
</style>