<template>
    <div class="preview_cover">
        <span>封面预览</span>
        <div class="cover_box">
            <img :src="cover_img_src" alt="封面预览" ref="cover_img">
        </div>
    </div>
</template>

<script setup>
import { ref, watch, defineEmits, defineProps, onMounted } from 'vue';
import * as cookies from '@/assets/js/cookies'

const cover_img_src = ref('');
const token = cookies.get_cookie('token');
const props = defineProps({
    title: {
        type: String,
        default: '示例标题'
    },
    template_name: {
        type: String,
        default: 'template_1'
    },
    file: {
        type: File,
        default: null
    }
});

const emit = defineEmits(['temp_cover_path']);

const get_preview_cover = async () => {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/file/GetPreviewCover/', {
            method: 'post',
            headers: { 'Content-Type': 'application/json' ,'Authorization': 'Bearer ' +localStorage.getItem('token')},
            body: JSON.stringify({
                token: token,
                template_name: props.template_name,
                title: props.title
            })
        });
        if (res.ok) {
            const data = await res.json();
            if (data.status === 'success') {
                return data.cover_path;
            } else {
                console.log(data.message);
            }
        } else {
            console.log('网络错误' + res.status);
        }
    } catch (e) {
        console.log(e);
    }
};

const update_cover_img = async () => {
    if (props.file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            cover_img_src.value = e.target.result;
        };
        reader.readAsDataURL(props.file);
    } else if (props.title || props.template_name) {
        cover_img_src.value = 'https://www.sunyuanling.com/image/novel/temp_cover/' + await get_preview_cover();
        console.log('服务器绘制封面');
    } else {
        cover_img_src.value = ''; // 清空封面预览
    }
    emit('temp_cover_path', cover_img_src.value);
};

onMounted(async () => {
    await update_cover_img();
});

watch(() => ({ ...props }), async (newVal, oldVal) => {
    if (newVal.file !== oldVal.file || newVal.title !== oldVal.title || newVal.template_name !== oldVal.template_name) {
        cover_img_src.value = ''; // 先清空值
        await update_cover_img();
    }
}, { deep: true });
</script>

<style scoped>
.preview_cover {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.cover_box {
    width: 100%;
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 10px auto;
    background-color: rgba(233, 233, 233, 1);
    border-radius: 10px;
    padding: 10px 0px;
}

.cover_box img {
    width: 30%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
}
</style>
