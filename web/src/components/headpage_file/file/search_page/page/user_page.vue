<template>
    <div class="user_page">
        <div class="content">
            <div class="item_box">
                <div class="item" v-for="(item, index) in data" :key="index">
                    <div class="user_avatar">
                        <img :src="'https://www.sunyuanling.com/image/avatar_thumbnail/' + item.user_avatar">
                    </div>
                    <div class="user_info">
                        <div class="user_name">
                            <span>{{ item.username }}</span>
                        </div>
                        <div class="user_work" v-if="show_work_list.length > 0">
                            <div class="user_work_for" v-for="(work, workIndex) in show_work_list" :key="workIndex">
                                <div class="item_img" v-if="work.Illustration_id">
                                    <img :src="'https://www.sunyuanling.com/image/thumbnail/' + work.content_file_list.split(/[,，]/)[0]"
                                        @click="jump_to_page('ill', work.Illustration_id)">
                                </div>
                                <div class="item_img" v-else-if="work.id">
                                    <img :src="'https://www.sunyuanling.com/image/comic/thumbnail/' + work.content_file_list.split(/[,，]/)[0]"
                                        @click="jump_to_page('comic', work.id)">
                                </div>
                                <div class="item_img" v-else-if="work.work_id">
                                    <img :src="'https://www.sunyuanling.com/image/novel/thumbnail/' + work.work_cover"
                                        @click="jump_to_page('novel', work.work_id)">
                                </div>
                            </div>
                        </div>
                        <div class="brief_introduction">
                            <span>{{ item.user_self_introduction }}</span>
                        </div>
                        <div :class="{'follow_btn': !item.follow_status, 'unfollow_btn': item.follow_status}" @click="follow(item.username, item.userid)">
                            <span v-if="!item.follow_status">关注</span>
                            <span v-else>取消关注</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, defineProps,defineEmits } from 'vue';
import * as cookies from '../../../../../../../model/cookies.js'

const props = defineProps({
    user_data: {
        type: Object,
        default: () => ({})
    }
});

const data = ref(props.user_data);
const work_list = ref({});
const show_work_list = ref([]);
const userid = JSON.parse(cookies.get_cookie('userinfo')).userid;

const emit=defineEmits(['work_count']);
watch(() => props.user_data, async (newValue) => {
    data.value = newValue;
    await get_work_list();
    set_work_list();
    await set_follow_status();
    emit('work_count', {'type':'user','count':data.value.length})
});

onMounted(async () => {
    data.value = props.user_data;
    await get_work_list();
    set_work_list();
});

async function get_work_info(userid) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserWorkList/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({ userid })
        });

        if (!res.ok) {
            console.log('网络错误');
            return null;
        }

        const result = await res.json();
        if (result.status === 'success') {
            return result.data;
        } else {
            console.warn(result.message);
            return null;
        }
    } catch (error) {
        console.error('请求错误:', error);
        return null;
    }
}

async function get_work_list() {
    const temp_work_list = {};
    for (const user of data.value) {
        const userWorks = await get_work_info(user.userid);
        if (userWorks) {
            temp_work_list[user.userid] = userWorks;
        }
    }
    work_list.value = temp_work_list;
    console.log(work_list.value);
}

//获取用户关注列表
async function get_follow_list(id, target_id) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserFollowList/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                userid: userid,
                target_id: target_id,
            })
        })
        if (res.ok) {
            const data = await res.json()
            if (data.status == 'success') {
                return data.data
            }
            else {
                console.log('error')
                return []
            }
        }
    }
    catch (e) {
        console.log(e)
    }
}
//设置关注状态
async function set_follow_status() {
    let temp;
    try {

        for (let i = 0; i < data.value.length; i++) {
            temp = await get_follow_list(userid, data.value[i].userid);
            if (temp.length != 0) {
                data.value[i].follow_status = true
            }
            else {
                data.value[i].follow_status = false
            }
        }
    }
    catch (e) {
        console.log(e)
    }
}
function set_work_list() {
    show_work_list.value = [];
    const user_work_list = Object.values(work_list.value).flat();

    const ill_list = user_work_list.flatMap(user => user.ill || []);
    const comic_list = user_work_list.flatMap(user => user.comic || []);
    const novel_list = user_work_list.flatMap(user => user.novel || []);

    const addWorks = (list) => {
        for (const item of list) {
            if (show_work_list.value.length < 4) {
                show_work_list.value.push(item);
            } else {
                break;
            }
        }
    };

    addWorks(ill_list);
    addWorks(comic_list);
    addWorks(novel_list);

    console.log(show_work_list.value);
}
//页面带参跳转
function jump_to_page(type, id) {
    console.log(id);
    console.log(type);
    //window.location.href='https://localhost:3002/?id='+id+'&work_type='type'
}
//关注或者取消关注
async function follow(target_username,target_id)
{
    const res=await fetch('https://www.sunyuanling.com/api/GetUserInfo/UserAddFollow/',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'Authorization':'Bearer '+localStorage.getItem('token')
        },
        body:JSON.stringify({
            target_username:target_username,
            target_id:target_id,
            userid:userid,
            username:JSON.parse(cookies.get_cookie('userinfo')).username,
        })
    })
    if(res.ok)
    {
        const data=await res.json()
        if(data.status=='success')
        {
            alert(data.message);
            await set_follow_status();
        }
        else
        {
            alert('关注失败')
        }
    }
}
</script>

<style scoped>
.user_page {
    width: 80%;
    margin: 20px auto;
}

.content {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
    height: auto;
}

.item_box {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    width: 100%;
    height: auto;
}

.item {
    display: flex;
    gap: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 45%;
    height: auto;
}

.user_avatar {
    width: 50px;
}

.user_avatar img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
}

.user_info {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: calc(100% - 50px);
    flex: 1;
    height: auto;
}

.user_name {
    font-weight: bold;
}

.user_work {
    display: flex;
    gap: 10px;
    width: 100%;
}

.user_work_for {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: calc(100%/4);
    height: auto;
}

.item_img img {
    width: 100%;
    height: auto;
    object-fit: cover;
    cursor: pointer;
}

.brief_introduction {
    margin-top: 10px;
}

.follow_btn {
    display: flex;
    padding: 5px 10px;
    background-color: rgba(0, 150, 250, 1);
    width: 30%;
    height: auto;
    max-width: 80px;
    max-height: 30px;
    border-radius: 10px;
    justify-content: center;
    color: white;
    cursor: pointer;
    align-items: center;
    font-size: 16px;
    font-weight: bold;
}
.unfollow_btn {
    display: flex;
    padding: 5px 10px;
    background-color: rgba(133,133,133, 1);
    width: 30%;
    height: auto;
    max-width: 80px;
    max-height: 30px;
    border-radius: 10px;
    justify-content: center;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor:pointer;
}
</style>
