<template>
    <div class="user_control" @scroll="handle_scroll">
        <h1>用户管理</h1>
        <div class="content" v-if="user_data">
            <div class="search_user">
                <input type="text" placeholder="搜索用户" v-model="search_type" />
            </div>
            <div class="item" v-for="(item, index) in filteredUserData" :key="index">
                <h5>用户名</h5>
                <div class="item_name" contenteditable="true">{{ item.username }}</div>
                <h5>用户ID</h5>
                <div class="item_userid">{{ item.userid }}</div>
                <h5>用户性别</h5>
                <div class="item_sex" contenteditable="true">{{ item.sex }}</div>
                <h5>用户密码</h5>
                <div class="item_password" contenteditable="true">{{ item.password }}</div>
                <h5>用户邮箱</h5>
                <div class="item_email" contenteditable="true">{{ item.email }}</div>
                <h5>用户电话</h5>
                <div class="item_phone" contenteditable="true">{{ item.phone }}</div>
                <h5>用户vip状态</h5>
                <div class="item_vip" contenteditable="true">{{ item.vip === 1 ? 'VIP用户' : '普通用户' }}</div>
                <h5>用户账号状态</h5>
                <div class="item_account_status">
                    <select v-model="item.account_status">
                        <option value="0">封禁</option>
                        <option value="1">正常</option>
                        <option value="2">禁言</option>
                    </select>
                </div>
                <h5>用户权限</h5>
                <div class="item_account_permission">
                    <select v-model="item.account_permissions">
                        <option value="0">普通用户</option>
                        <option value="1">管理员</option>
                        <option value="2">超级管理员</option>
                    </select>
                </div>
                <div class="item_show" @click="choose_user(item)">查看详细信息（修改）</div>
                <div class="item_delete" @click="deleteUser(index)">删除</div>
            </div>
            <div v-if="loadingMore" class="loading">加载中...</div>
        </div>
    </div>
    <user_infomation v-if="user_infomation_show" :user_info="user_data_info" @close_page="close_user_info_page"></user_infomation>
</template>

<script setup>
import { get_user_list } from './js/get_user_list';
import { ref, onMounted, computed, watch, onUnmounted } from 'vue';
import user_infomation from './user_infomation.vue';


const user_infomation_show = ref(false);
const user_list = ref([]);
const user_data = ref([]);
const search_type = ref('');
const user_data_info = ref({});
const offset = ref(0);
const limit = ref(3);
const total = ref(0);
const loadingMore = ref(false);

onMounted(async () => {
    await loadMoreUsers();
    window.addEventListener('scroll', handle_scroll);
});

const filteredUserData = computed(() => {
    const query = search_type.value.toLowerCase();
    return user_data.value.filter(user => 
        user.username.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query)
    );
});

async function loadMoreUsers() {
    // 检查是否已经加载完所有用户
    
    
    loadingMore.value = true;
    try {
        const response = await get_user_list(offset.value, limit.value);
        total.value = response.data.total; // 更新总用户数
        const newUsers = response.data.user_list;
        
        if (newUsers.length > 0) {
            user_data.value = [...user_data.value, ...newUsers];
            offset.value += limit.value;
        }
    } catch (error) {
        console.error('加载用户列表出错:', error);
    } finally {
        loadingMore.value = false;
    }
    if (loadingMore.value || offset.value >= total.value) return;
}



function deleteUser(index) {
    user_data.value.splice(index, 1);
}

function choose_user(item) {
    user_data_info.value = item;
    user_infomation_show.value = true;
}

function close_user_info_page() {
    user_infomation_show.value = false;
}

function handle_scroll() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const windowHeight = window.innerHeight || document.documentElement.clientHeight;
    const documentHeight = document.documentElement.scrollHeight;

    if (scrollTop + windowHeight >= documentHeight - 10) {
        loadMoreUsers();
    }
}

onUnmounted(() => {
    window.removeEventListener('scroll', handle_scroll);
});
</script>



<style scoped>
.user_control {
    padding: 20px;
    display: flex;
    flex-direction: column;
    width: 100%;
}

h1 {
    font-size: 24px;
    margin-bottom: 20px;
}

.search_user {
    margin-bottom: 20px;
}

.search_user input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
    font-size: 16px;
}

.content {
    margin-top: 10px;
}

.item {
    border: 1px solid #ddd;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.item div {
    margin-bottom: 10px;
}

.item_name,
.item_sex,
.item_password,
.item_email,
.item_phone,
.item_vip {
    border: 1px solid #ccc;
    padding: 8px;
    border-radius: 5px;
    background-color: #fff;
}

.item_userid {
    font-weight: bold;
    font-size: 16px;
}

.item_account_status select,
.item_account_permission select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #fff;
}

.item_show, .item_sure, .item_delete {
    cursor: pointer;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
}

.item_show {
    background-color: #007bff;
    color: #fff;
    margin-bottom: 5px;
}

.item_show:hover {
    background-color: #0056b3;
}

.item_sure {
    background-color: #28a745;
    color: #fff;
    margin-bottom: 5px;
}

.item_sure:hover {
    background-color: #218838;
}

.item_delete {
    background-color: #dc3545;
    color: #fff;
}

.item_delete:hover {
    background-color: #c82333;
}
</style>
