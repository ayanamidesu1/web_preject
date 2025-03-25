<template>
    <div class="more_info_box">
        <div class="content">
            <div class="title">
                <span></span>
                <span>个人信息</span>
                <div class="close_btn btn" @click="close_page()">
                    <img class="icon" src="https://www.sunyuanling.com/assets/close.svg" alt="关闭">
                </div>
            </div>
            <div class="user_avatar">
                <img :src="'https://www.sunyuanling.com/image/avatar_thumbnail/' + user_info.user_avatar" alt="用户头像">
            </div>
            <div class="address">
                <img class="icon" src="https://www.sunyuanling.com/assets/location.svg" alt="地址图标">
                <span>{{ user_info.user_address }}</span>
            </div>
            <div class="sex">
                <span>性别: {{ user_info.sex }}</span>
            </div>
            <div class="age">
                <span>年龄: {{ age }}</span>
            </div>
            <div class="birthday">
                <span>生日: {{ formattedBirthday }}</span>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted } from 'vue';

const props = defineProps({
    user_info: {
        type: Object,
        default: () => {
            return {};
        }
    }
})

const emit = defineEmits(['close_page'])
const age = ref('')
const formattedBirthday = ref('')

function close_page() {
    emit('close_page', false)
}

function calculateAge(birthday) {
    const today = new Date();
    const birthDate = new Date(birthday);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDifference = today.getMonth() - birthDate.getMonth();
    if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
}

function formatBirthday(birthday) {
    const dateFormats = [
        { regex: /^\d{4}年\d{1,2}月\d{1,2}日$/, format: 'YYYY年MM月DD日' },
        { regex: /^\d{4}\/\d{1,2}\/\d{1,2}$/, format: 'YYYY/MM/DD' },
        { regex: /^\d{4}-\d{1,2}-\d{1,2}$/, format: 'YYYY-MM-DD' },
        { regex: /^\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{2}:\d{2}$/, format: 'YYYY-MM-DDTHH:mm:ss' }
    ];

    for (const { regex, format } of dateFormats) {
        if (regex.test(birthday)) {
            return birthday;
        }
    }
    return '未知格式';
}

onMounted(() => {
    if (props.user_info.birthday) {
        formattedBirthday.value = formatBirthday(props.user_info.birthday);
        age.value = calculateAge(props.user_info.birthday);
    }
})
</script>

<style scoped>
.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.more_info_box {
    width: 100vw;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    display: flex;
    background-color: rgba(0, 0, 0, 0.5);
    align-items: center;
    justify-content: center;
    z-index: 15;
}

.content {
    width: 80%;
    max-width: 500px;
    padding: 20px;
    border-radius: 15px;
    background-color: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.title {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.user_avatar img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
}

.address, .sex, .age, .birthday {
    display: flex;
    align-items: center;
    gap: 10px;
}

.close_btn {
    cursor: pointer;
    display: flex;
    width: 35px;
    height: 35px;
    justify-content: center;
    align-items: center;
}
.btn:hover{
    opacity: 0.8;
    border-radius: 50%;
    transition: all 0.2s;
    transform: translateY(-2px);
    background-color: rgba(133,133,133,1);
}
</style>
