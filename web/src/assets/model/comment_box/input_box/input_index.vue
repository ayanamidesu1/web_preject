<template>
    <div class="input_index">
        <div class="content" ref="content">
            <div class="title_box" v-if="false">
                <textarea placeholder="请输入标题" v-model="title"></textarea>
            </div>
            <div ref="input_box" class="input_box" contenteditable="true" @mouseup="handleSelection"></div>
            <!-- <div class="input_img_box" ref="input_img_box" v-if="img_file_list.length > 0 || status_index == 1">
                <div class="img_list">
                    <div class="img_item" v-for="(item, index) in img_file_list" :key="index">
                        <img :src="item.url" alt="图像">
                        <div class="delete_img" @click="pop_img_file(index)">
                            <img class="icon" src="http://localhost:8000/static/svg/退出.svg" alt="删除">
                        </div>
                    </div>
                </div>
                <div class="add_img" @click="add_img_input_click()">
                    <img src="http://localhost:8000/static/svg/新增.svg" class="icon">
                    <input type="file" ref="add_img_input" accept="image/*" @change="push_img_file($event)"
                        style="display: none;pointer-events:none;">
                </div>
            </div> -->
            <div class="interaction_box">
                <div class="item_list">
                    <div class="item">
                        <div class="img" :class="{ choose_status: status_index == 0 }">
                            <img class="icon" :src="ip + 'emoji/张嘴闭眼笑.svg'" @click="set_status_index(0)">
                        </div>
                        <emoji_box v-if="status_index == 0" class="item_sub_box" @emoji="add_content_emoji($event)">
                        </emoji_box>
                    </div>
                    <!-- <div class="item">
                        <div class="img" :class="{ choose_status: status_index == 1 || img_file_list.length > 0 }">
                            <img class="icon" :src="ip + 'svg/图像.svg'" @click="set_status_index(1)">
                        </div>
                    </div> -->
                    <div class="item" @click="bold($event)">
                        <span style="font-weight: bold;">B</span>
                    </div>
                    <div class="item" @click="italic()">
                        <span><i>I</i></span>
                    </div>
                    <div class="item" @click="underline()">
                        <span><u>U</u></span>
                    </div>
                    <div class="item" @click="font_size_down()">
                        <span style="font-weight: bold;">F-</span>
                    </div>
                    <div class="item" @click="font_size_up()">
                        <span style="font-weight: bold;">F+</span>
                    </div>
                    <div class="item" @click="clear_all_span_style()">
                        <span style="font-weight: bold;">C</span>
                    </div>
                    <!-- <div class="item">
                        <span><img src="http://localhost:8000/static/svg/表格.svg"></span>
                    </div> -->
                </div>
                <div class="send_btn" @click="get_input_box_html()">
                    <span>发布</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue';
import emoji_box from './emoji_box/emoji_box.vue';
import {
    placeCaretAtEnd, getSelectedText, removeSelectedText, set_span_style, clear_all_span_style_in_ref,generateUniqueId
} from './js/input'

const emit = defineEmits(['html_content','title','content'])

let ip = 'https://www.sunyuanling.com/server/static/';
let input_box = ref(null);
let status_index = ref(-1);
let input_img_box = ref(null);
let title = ref('');
let content = ref(null);

//图像文件列表
let img_file_list = ref([]);
let back_img_file_list = []

// 切换状态索引
function set_status_index(index) {
    status_index.value = (status_index.value === index) ? -1 : index;
}

//模拟点击
function add_img_input_click() {
    input_img_box.value.querySelector('input').click();
}

// 向栈中压入解析为Base64的图像文件
function push_img_file(event) {
    const file = event.target.files[0];
    back_img_file_list.push(file)
    if (file) {
        format_img_file(file); // 将图像插入富文本框
        const reader = new FileReader();
        reader.onload = (e) => {
            img_file_list.value.push({ url: e.target.result });
        };
        reader.readAsDataURL(file); // 将文件转换为Data URL
    }
}
//从栈中弹出指定索引图像文件
function pop_img_file(index) {
    img_file_list.value.splice(index, 1);
}

// 新增动态HTML内容中的标签
function add_content_emoji(emoji, el) {
    console.log(emoji, el)
    if (input_box.value) {
        // 创建 img 元素并设置属性
        const img = document.createElement('img');
        img.src = `${ip}emoji/${emoji}`;
        img.className = 'emoji'; // 应用 class
        img.style.width = '16px';
        img.style.height = '16px';
        img.style.objectFit = 'cover';
        img.style.display = 'inline-block';
        img.alt = emoji;

        // 插入 img 元素
        input_box.value.appendChild(img);

        // 光标移动到文本框末尾
        placeCaretAtEnd(input_box.value);
    }
}

// 处理粘贴事件
function handlePasteEvent(event) {
    event.preventDefault();
    const clipboardData = event.clipboardData || window.Clipboard;

    if (!clipboardData) return;

    // 遍历剪贴板内容
    const items = clipboardData.items;
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.type.indexOf('image') !== -1) {
            const file = item.getAsFile();
            if (file) {
                format_img_file(file); // 将图像插入富文本框
                back_img_file_list.push(file); // 同步保存图像文件
                img_file_list.value.push({ url: URL.createObjectURL(file) }); // 将图像文件添加到列表
            }
        }
    }
}

//格式化图像文件，并且插入到input_box中
function format_img_file(file) {
    //生成一个唯一的UUID
    const uuid= generateUniqueId();
    const reader = new FileReader();
    reader.onload = (e) => {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.style.width = '100px';
        img.style.height = '100px';
        img.style.objectFit = 'cover';
        img.style.display = 'inline-block';
        img.id= uuid;
        input_box.value.appendChild(img);
    };
    reader.readAsDataURL(file);
}

// 字体加粗
function bold(e) {
    set_span_style({ 'font-weight': 'bold', 'background-color': 'white' })
}
// 字体倾斜
function italic(e) {
    set_span_style({ 'font-style': 'italic', 'background-color': 'white' })
}
// 字体下划线
function underline(e) {
    set_span_style({ 'text-decoration': 'underline', 'background-color': 'white' })
}
//增大字体
function font_size_up(e) {
    set_span_style({ 'font-size': '20px', 'background-color': 'white' })
}
//减小字体
function font_size_down(e) {
    set_span_style({ 'font-size': '12px', 'background-color': 'white' })
}
//清除所有样式
function clear_all_span_style(e) {
    clear_all_span_style_in_ref(input_box.value)
}

function handleSelection() {
    if (input_box.value) {
        //获取选中的文字
        let temp = window.getSelection().toString();
        if (temp) {
            const selectedText = getSelectedText(input_box.value);
            if (selectedText) {
                console.log("选中的文字:", selectedText);
            }
        }
    }
}
//取消文字选中
function cancel_selection(event) {
    const contentElement = content.value;

    // 判断点击的目标元素是否是 content 的子元素
    if (contentElement && !contentElement.contains(event.target)) {
        // 如果点击位置不在 content 内部，移除选中的文本
        removeSelectedText(contentElement);
    }
}

onMounted(async () => {
    //监听粘贴动作或拖动动作
    // 监听粘贴事件
    input_box.value.addEventListener('paste', (event) => {
        handlePasteEvent(event);
    });
    input_box.value.addEventListener('drop', (event) => {
        event.preventDefault();
        const files = event.dataTransfer.files;
        for (const file of files) {
            if (file.type.startsWith('image/')) {
                format_img_file(file); // 插入拖放的图像
                back_img_file_list.push(file); // 同步保存图像文件
            }
        }
    });
    // 监听点击事件，并传递事件对象
    document.addEventListener('click', (event) => {
        cancel_selection(event);
    });
})

let html_content_1 = ref()
//提取原始HTML内容
function get_input_box_html() {
    html_content_1.value = input_box.value.innerHTML
    let temp={
        //title:title.value,
        content:html_content_1.value,
        //file_list:img_file_list.value,
    }
    emit('content',temp)
    //重置input_box
    input_box.value.innerHTML = ''
}

</script>

<style scoped>
.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.emoji {
    width: 20px;
    height: 20px;
    object-fit: cover;
}

.input_box {
    font-size: 16px;
    width: calc(100% - 10px);
    height: auto;
    align-items: center;
    /*字间距*/
    letter-spacing: 1.5px;
    display: flex;
    gap: 2px;
    /*行间距*/
    line-height: 1.3;
    padding: 5px;
    border: 1px solid rgba(133, 133, 133, 1);
    border-radius: 5px;
    flex-wrap: wrap;
    text-wrap: wrap;
    max-width: calc(100% - 10px);
    min-height: 20px;
}

.input_img_box {
    display: flex;
    width: 100%;
    gap: 10px;
    flex-wrap: wrap;
    max-width: calc(100% - 10px);
    align-items: center;
}

.img_list {
    width: auto;
    height: auto;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.img_item {
    width: 100px;
    height: 100px;
    display: flex;
    background-color: rgba(133, 133, 133, 0.5);
    position: relative;
    border-radius: 10px;
}

.img_item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
}

.delete_img {
    position: absolute;
    display: flex;
    width: 20px;
    height: 20px;
    align-items: center;
    justify-content: center;
    background-color: rgba(133, 133, 133, 0.5);
    top: -2px;
    right: -2px;
    border-radius: 50%;
    cursor: pointer;
}

.delete_img:hover {
    opacity: 0.8;
    background-color: rgba(0, 150, 250, 0.5);
    transition: all 0.3s ease-in-out;
}

.delete_img img {
    width: 15px;
    height: 15px;
    object-fit: cover;
}

.add_img {
    width: 60px;
    height: 60px;
    display: flex;
    background-color: rgb(207, 207, 207);
    border-radius: 10px;
    cursor: pointer;
}

.add_img:hover {
    opacity: 0.8;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
    transform: scale(1.05);
}

.add_img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.choose_status {
    background-color: rgba(0, 150, 250, 0.5);
    transition: all 0.3s;
    transform: scale(1.05);
}

.input_index {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    background-color: rgba(255, 255, 255, 1);
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
    max-width: calc(100% - 20px);
    transition: all 0.3s;
}

.content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.title_box {
    width: 100%;
    display: flex;
    max-width: calc(100% - 10px);
    margin-bottom: 10px;
}

.title_box textarea {
    width: 100%;
    height: auto;
    border: 1px solid rgba(233, 233, 233, 1);
    border-radius: 10px;
    padding: 5px;
    resize: vertical;
    min-height: 28px;
    font-size: 18px;
    font-weight: bold;
}

.interaction_box {
    width: 100%;
    height: 60px;
    display: flex;
    gap: 10px;
    position: relative;
    justify-content: space-between;
}

.item_list {
    display: flex;
    gap: 10px;
}

.item {
    width: 60px;
    height: 60px;
    display: flex;
    position: relative;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}
.item img{
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.item:hover {
    background-color: rgba(133, 133, 133, 1);
    transition: all 0.3s;
    border-radius: 50%;
}

.img {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 50%;
}

.img img {
    width: 27.5px;
    height: 27.5px;
    object-fit: cover;
    margin: auto;
}

.item_sub_box {
    position: absolute;
    top: 80px;
    left: 0px;
}

.send_btn {
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 10px;
    color: white;
    background-color: rgba(0, 150, 250, 1);
    display: flex;
    justify-content: center;
    align-items: center;
    max-height: 26px;
    max-width: 46px;
    font-size: 18px;
    font-weight: 500;
    transition: all 0.3s ease-in-out;
}

.send_btn:hover {
    opacity: 0.8;
    transform: scale(1.02);
    transform: translateY(-2px);
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
}
</style>