<template>
    <div class="edit_box">
        <div class="content">
            <div class="title">
                <span></span>
                <span>封面设置</span>
                <div class="close_btn" @click="close_page()">
                    <img src="https://www.sunyuanling.com/assets/close.svg" class="icon">
                </div>
            </div>
            <div class="img_box">
                <img :src="user_back_img" class="user_background_img">
                <div class="upload_img" @click="change_img()">
                    <img src="https://www.sunyuanling.com/assets/image.svg">
                    <input type="file" accept="image/*" ref="upload_img" style="display: none;" @change="get_img_item">
                </div>
            </div>
            <div class="tips_box">
                <div class="tips">
                    <span>适用格式：</span>
                    <span>.jpg .png .jpeg .webp</span>
                </div>
                <div class="tips">
                    <span>最大容量：</span>
                    <span>8M以内</span>
                </div>
                <div class="tips">
                    <span>建议尺寸：</span>
                    <span>1920*1080</span>
                </div>
                <div class="tips">
                    <span>最大尺寸：</span>
                    <span>4096*4096</span>
                </div>
            </div>
            <div class="tips_box" style="flex-direction: row;">
                <div class="tips">
                    <img src="https://www.sunyuanling.com/assets/info.svg" class="icon">
                    <span>根据您上传的图片及设备显示不同，图片四周有可能会显示不全。</span>
                </div>
            </div>
            <span style="width: 90%;margin:0px auto;font-size:14px;color:rgb(133,133,133);">
                请不要上传R-18或使用规则中禁止投稿的作品。如果您上传了相关图片，设置可能会被清除。
            </span>
            <div class="btn_box">
                <div class="sure_btn btn" @click="sure_btn()">
                    <span>同意上传</span>
                </div>
                <div class="cancel btn" @click="close_page()">
                    <span>取消</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import { update_user_back } from '../js/update_userinfo';

const props = defineProps({
    token: {
        type: String,
        default: ''
    },
    user_back_img: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['close_page'])
const user_back_img = ref(props.user_back_img)
const upload_img = ref(null)
let img_file=ref()

function close_page() {
    emit('close_page', false)
}

function change_img() {
    upload_img.value.click()
}

function get_img_item(e) {
    const file = e.target.files[0]
    if (file) {
        const reader = new FileReader()
        reader.onload = (event) => {
            user_back_img.value = event.target.result
        }
        reader.readAsDataURL(file)
    }
    img_file.value=file
}
async function sure_btn(){
    let user_data={
        token: props.token,
    }
    let status=await update_user_back(img_file.value, props.token, user_data)
    if(status){
        close_page()
    }
    else{
        alert('上传失败')
    }
}
</script>

<style scoped>
.edit_box {
    position: fixed;
    width: 100vw;
    height: 100vh;
    left: 0;
    top: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index:11;
}

.content {
    box-sizing: border-box;
    display: flex;
    width: 100%;
    min-width: 200px;
    max-width: 400px;
    height: auto;
    flex-direction: column;
    border-radius: 15px;
    box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
    gap: 10px;
    margin: 20px auto;
    background-color: rgba(255, 255, 255, 1);
}

.title {
    width: 100%;
    height: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 18px;
    font-weight: bold;
}

.img_box {
    width: 100%;
    height: auto;
    max-height: 200px;
    display: flex;
    position: relative;
    overflow: hidden;
}
.upload_img{
    width: 100%;
    height: 100%;
    display: flex;
    position: absolute;
    top: 0;
    left: 0;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, 0.5);
    opacity: 0;
}
.upload_img img{
    width: 40%;
    height: auto;
    object-fit: cover;
}
.upload_img:hover{
    opacity: 1;
    cursor: pointer;
    transition: all 0.2s;

}
.user_background_img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.close_btn {
    width: 35px;
    height: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 5px;
    margin-top: 5px;
}

.close_btn:hover {
    cursor: pointer;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    transition: all 0.2s;
    transform: scale(1.1);
}

.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.tips_box {
    width: 90%;
    display: flex;
    height: auto;
    gap: 10px;
    flex-direction: column;
    margin-top: 20px;
    margin-left: auto;
    margin-right: auto;
    background-color: rgb(188, 188, 188);
    padding: 5px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.tips {
    width: 100%;
    display: flex;
    justify-content: space-between;
    gap: 5px;
}
.btn_box{
    width: 60%;
    height: auto;
    gap: 20px;
    display: flex;
    flex-direction: column;
    margin:10px auto;
    justify-content: center;
    align-items: center;
}
.btn{
    cursor: pointer;
    font-size: 20px;
    font-weight: bold;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.btn:hover{
    opacity: 0.8;
    transition: all 0.2s;
    transform: translateY(-2px);
}
.sure_btn{
    background-color: rgb(0,150,250);
    color: white;
    padding: 10px 25px;
    border-radius: 15px;
}
.cancel{
    background-color: rgb(207, 207, 207);
    color: rgb(0, 0, 0);
    padding: 10px 25px;
    border-radius: 15px;
}
</style>