<template>
    <div class="create_new_series">
        <div class="background">
            <div class="title">
                <div></div>
                <span style="font-weight:bold;">新建系列</span>
                <div class="close_btn" @click="close_page()">
                    <img class="icon" src="https://www.sunyuanling.com/assets/close.svg">
                </div>
            </div>
            <div class="content">
                <div class="work_title">
                    <label style="font-weight:bold;">系列标题</label>
                    <input type="text" v-model="work_info.title" maxlength="100">
                </div>
                <div class="work_name">
                    <label style="font-weight:bold;">作品名称</label>
                    <input type="text" v-model="work_info.work_name" maxlength="100">
                </div>
                <div class="work_introducation">
                    <label style="font-weight:bold;">作品介绍</label>
                    <auto_textarea style="border:1px solid rgba(77,77,77,0.8);" v-model="work_info.introducation"
                        :maxlength="300000" :rows="5" placeholder="请输入作品介绍..." :fontsize="14" :lineheight="1.6">
                    </auto_textarea>
                </div>
                <div class="tags_box">
                    <div class="add_tag_btn">
                        <label style="font-weight:bold;">作品标签</label>
                        <input type="text" v-model="temp_tag_list" placeholder="请输入标签..." @keyup.enter="add_tag">
                    </div>
                    <div class="tags_list">
                        <div class="tag_item" v-for="(item, index) in work_info.tags" :key="index">
                            <span>{{ item }}</span>
                            <div class="delete_btn" @click="delete_tag(index)">
                                <img class="icon" src="https://www.sunyuanling.com/assets/close.svg">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="age_classification">
                    <label style="font-weight:bold;">作品年龄分类</label>
                    <div class="age_classification_list">
                        <input type="radio" value="16" name="age_classification" v-model="work_info.age_classification">
                        <label>全年龄</label>
                        <input type="radio" value="18" name="age_classification" v-model="work_info.age_classification">
                        <span>R-18</span>
                        <input type="radio" value="18+" name="age_classification"
                            v-model="work_info.age_classification">
                        <span>R-18G</span>
                    </div>
                </div>
                <div class="work_status">
                    <switch_btn @change_status="get_work_status"></switch_btn>
                    <span>连载中</span>
                </div>
                <div class="choose_cover" style="gap:10px;display:flex;flex-direction:column;">
                    <span>封面</span>
                    <div class="cover_list">
                        <scroll_box :msg_type="'image'" :msg_list="set_template_cover_path()"
                            @chose_item="get_choose_cover_path" @choose_cover_file="get_choose_cover_file"
                            @clear_cover_file="clear_choose_cover_file"></scroll_box>
                    </div>
                </div>
                <preview_cover :title="work_info.title" :template_name="work_info.choose_cover_path"
                    :file="user_choose_cover_file" @temp_cover_path="user_choose_cover_path"
                    @clear_uploaded_file="clear_choose_cover_file">
                </preview_cover>
                <is_original @series_info="get_series_info"></is_original>
                <div class="btn_box">
                    <div class="sure_btn" @click="set_send_work_info()">
                        <span>确定</span>
                    </div>
                    <div class="cancel_btn" @click="close_page()">
                        <span>取消</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import auto_textarea from '../../../../models/auto_textarea.vue';
import switch_btn from '../../../../models/switch_btn.vue';
import scroll_box from '../../../../models/scroll_box.vue';
import preview_cover from './preview_cover.vue'
import is_original from './is_original.vue';
import { ref, watch, defineEmits } from 'vue';
import * as cookies from '@/assets/js/cookies'

let token = cookies.get_cookie('token');
let user_info = JSON.parse(cookies.get_cookie('userinfo'));
const emit = defineEmits(['close_create_new_series', 'new_series_info']);
const new_series_info = ref({});
const template_cover = ref(['template_1.jpg', 'template_2.jpg', 'template_3.jpg', 'template_4.jpg', 'template_5.jpg',
    'template_6.jpg', 'template_7.jpg'
]);

function set_template_cover_path() {
    const path = 'https://www.sunyuanling.com/image/novel/cover_material/';
    return template_cover.value.map(cover => path + cover);
}

function close_page() {
    emit('close_create_new_series', false);
}

function create_new_series() {
    emit('new_series_info', new_series_info.value);
}
let temp_tag_list = ref()
// 作品系列信息
const work_info = ref({
    work_name: '',
    title: '',
    introducation: '',
    tags: [],
    age_classification: '',
    work_status: '',
    choose_cover_path: '',
    token: token,
    user_info: user_info,
    cover_type: 'default_cover',
});
let user_choose_cover_file = ref(null);
//删除指定索引标签
function delete_tag(index) {
    work_info.value.tags.splice(index, 1);
}
//按回车键增加标签
function add_tag() {
    const new_tag = temp_tag_list.value.trim();
    if (new_tag === '') {
        alert('标签不能为空！');
        return;
    }
    if (work_info.value.tags.includes(new_tag)) {
        alert('标签已存在！');
        return;
    }
    work_info.value.tags.push(new_tag);
    temp_tag_list.value = '';
}
let user_choose_cover_path = (item) => {
    work_info.value.user_choose_cover_path = item
}

watch(work_info, (new_value) => {
    new_series_info.value = { ...new_value };
    create_new_series();
    console.log(new_value);
}, { deep: true });

const tags_list_input = ref(null);
watch(() => work_info.value.tags, (new_value) => {
    if (tags_list_input.value) {
        tags_list_input.value.value = new_value.split(',');
    }
});

function get_work_status(status) {
    work_info.value.work_status = status ? '连载中' : '已完结';
    console.log(work_info.value);
}

// 获取子组件传值
function get_choose_cover_file(file) {
    user_choose_cover_file.value = file;
}

// 通知本组件清空文件
function clear_choose_cover_file() {
    user_choose_cover_file.value = null;
}

function get_choose_cover_path(path) {
    if (path != 'custom_cover') {
        work_info.value.choose_cover_path = path;
        user_choose_cover_file.value = null; // 清空用户选择的文件
    } else {
        console.log('自定义封面')
        work_info.value.cover_type = 'custom_cover'
    }
}

// 监视作品标题和封面路径，如果变化先清空用户选择的封面文件
watch(() => work_info.value.title, () => {
    user_choose_cover_file.value = null;
});

watch(() => work_info.value.choose_cover_path, () => {
    user_choose_cover_file.value = null;
});
let series_info = ref()
function get_series_info(item) {
    series_info.value = item
    work_info.value.series_name = series_info.value.series_name
    work_info.value.is_original = series_info.value.is_original
}
//组装最后的消息并上传
async function set_send_work_info() {
    console.log('work_info', work_info.value)
    let file = new FormData()
    file.append('file', user_choose_cover_file.value)
    file.append('work_info', JSON.stringify(work_info.value))
    try {
        const res = await fetch('https://www.sunyuanling.com/api/file/UploadNewSeries/', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' +localStorage.getItem('token')
            },
            body: file
        })
        if (res.ok) {
            const data = await res.json()
            if (data.status == 'success') {
                alert(data.message)
            }
            else {
                alert(data.message)
            }
        }
        else {
            console.log('服务器错误')
            console.log(res.status)
        }
    }
    catch (e) {
        console.log(e)
    }
}
</script>


<style scoped>
input {
    width: 100%;
    padding: 5px;
    border: 1px solid rgba(77, 77, 77, 0.5);
    border-radius: 5px;
    outline: none;
    background-color: rgba(143, 143, 143, 0.1);

}

.create_new_series {
    width: 100vw;
    height: 100vh;
    position: fixed;
    top: 0px;
    left: 0px;
    display: flex;
    flex-direction: column;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 10;
    padding: 50px;
    box-sizing: border-box;
}

.background {
    width: auto;
    height: auto;
    display: flex;
    flex-direction: column;
    background-color: rgba(255, 255, 255, 1);
    min-height: 100px;
    min-width: 550px;
    margin: auto;
    padding: 5px 20px;
    border-radius: 15px;
    overflow: auto;
    max-width: 550px;
}

.background::-webkit-scrollbar {
    display: none;
}

.title {
    width: auto;
    height: 50px;
    display: flex;
    justify-content: space-between;
    font-size: 18px;
    align-items: center;
    border-bottom: 1px solid rgba(133, 133, 133, 1);
    margin-top: 5px;
    font-weight: bold;
}

.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.close_btn {
    display: flex;
    width: 30px;
    height: 30px;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

.close_btn:hover {
    background-color: rgba(0, 0, 0, 0.3);
    border-radius: 50%;
    transition: all 0.2 ease-in-out;
}

.content {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.work_status {
    width: auto;
    display: flex;
    height: auto;
    align-items: center;
    gap: 10px;
}

.work_title,
.work_name {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
}


.work_introducation {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.tags_box {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.add_tag_btn {
    display: flex;
    flex-direction: column;
}

.tags_list {
    width: 100%;
    display: flex;
    gap: 5px;
    align-items: center;
}

.tags_list input {
    width: 100%;
}

.tag_item {
    display: flex;
    position: relative;
    width: auto;
    height: auto;
    align-items: center;
    background-color: rgba(188, 188, 188, 1);
    padding: 5px 25px;
    border-radius: 5px;
}

.delete_btn {
    position: absolute;
    display: flex;
    width: 15px;
    height: 15px;
    right: 0;
    top: 0;
    cursor: pointer;
}

.delete_btn:hover {
    border-radius: 50%;
    background-color: rgba(188, 188, 188, 0.8);
    transition: 0.2s;
}

.delete_btn img {
    width: 10px;
    height: 10px;
    object-fit: cover;
}

.age_classification {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.age_classification input {
    width: 15px;
    height:15px;
}
.age_classification_list{
    width: auto;
    height: auto;
    display: flex;
    gap: 10px;
}


.btn_box {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 80%;
    height: auto;
    padding: 5px;
    margin: 5px auto;
    justify-content: center;
    align-items: center;
}

.sure_btn {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px 10px;
    border-radius: 15px;
    background-color: rgba(0, 150, 250, 1);
    color: white;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
}

.sure_btn:hover {
    opacity: 0.8;
    transition: all 0.3s ease-in-out;
}

.cancel_btn {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px 10px;
    border-radius: 15px;
    background-color: rgba(188, 188, 188, 1);
    color: white;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
}

.cancel_btn:hover {
    opacity: 0.8;
    transition: all 0.3s ease-in-out;
}
</style>