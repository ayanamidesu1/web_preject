<template>
    <div class="content" @click="closeAllMenus" v-if="work_content">
        <div class="novel_content">
            <div class="title">{{ work_title }}</div>
            <div class="content" v-html="work_content"></div>
            <div class="right_side">
                <div class="previous_chapter align_center" @click="switch_chapter(-1)">
                    <img class="icon" src="https://www.sunyuanling.com/assets/left.svg">
                    <span>上一章</span>
                </div>
                <div class="next_chapter align_center" @click="switch_chapter(1)">
                    <img class="icon" src="https://www.sunyuanling.com/assets/right.svg">
                    下一章
                </div>
                <div class="open_setting align_center" @click.stop="toggleSettings('setting')">
                    <img class="icon" src="https://www.sunyuanling.com/assets/setting.svg">
                    <span>打开设置</span>
                </div>
                <div class="directory align_center" @click.stop="toggleSettings('directory')">
                    <img class="icon" src="https://www.sunyuanling.com/assets/more.svg">
                    <span>目录</span>
                </div>
                <div class="set_light_mode align_center" @click="toggleLightMode">
                    <img class="icon"
                        :src="'https://www.sunyuanling.com/assets/' + (light_mode ? 'moon.svg' : 'sun.svg')">
                    <div class="light_mode">{{ light_mode ? '夜间模式' : '日间模式' }}</div>
                </div>
                <directory_page :work_info="work_info" v-if="directory_show" @get_chapter="get_content"
                    @close_page="toggleSettings('close_all')"></directory_page>
                <transition name="fade">
                    <div class="font_setting" v-if="showSettings" ref="settingsMenu">
                        <div class="title">设置</div>
                        <div class="item">
                            字体
                            <select v-model="fontFamily" @change="updateStyles">
                                <option value="微软雅黑">微软雅黑</option>
                                <option value="黑体">黑体</option>
                                <option value="宋体">宋体</option>
                                <option value="楷体">楷体</option>
                            </select>
                        </div>
                        <div class="item">
                            字号
                            <select v-model="fontSize" @change="updateStyles">
                                <option value="14px">14px</option>
                                <option value="16px">16px</option>
                                <option value="18px">18px</option>
                                <option value="20px">20px</option>
                                <option value="22px">22px</option>
                                <option value="24px">24px</option>
                                <option value="26px">26px</option>
                            </select>
                        </div>
                        <div class="item">
                            背景
                            <input type="color" v-model="backgroundColor" @input="updateStyles">
                        </div>
                        <div class="item">
                            阅读页面宽度
                            <input type="range" v-model="pageWidth" min="500" max="1200" step="100"
                                @input="updateStyles">
                        </div>
                        <div class="item">
                            字体颜色
                            <input type="color" v-model="fontColor" @input="updateStyles">
                        </div>
                    </div>
                </transition>
            </div>
        </div>
    </div>
    <div class="loading" v-else-if="!work_content">
        <div class="loading_content">加载中...</div>
        <img src="https://www.sunyuanling.com/image/loading.gif">
    </div>
</template>

<script setup>
import { ref, watch, defineProps, onMounted, onUnmounted } from 'vue';
import directory_page from './model/directory_page.vue'
import { get_novel_content } from '../js/get_workinfo';

const props = defineProps({
    content: {
        type: String,
        default: ''
    },
    title: {
        type: String,
        default: ''
    },
    work_info: {
        type: Array,
        default: () => []
    },
    chapter_index: {
        type: Number,
        default: 0
    }
});

const showSettings = ref(false);
const fontFamily = ref('Arial');
const fontSize = ref('16px');
const backgroundColor = ref('#ffffff');
const fontColor = ref('#000000');
const pageWidth = ref(800);
const light_mode = ref(false);
const directory_show = ref(false);
const work_content = ref(props.content);
const work_title = ref(props.title);
const chapter_index = ref(props.chapter_index);
const settingsMenu = ref(null);

async function get_content(item) {
    work_content.value = await get_novel_content('sunyuanling', item.belong_to_series_id, item.title);
    work_title.value = item.title;
    chapter_index.value = item.index;
}

async function switch_chapter(index) {
    let c_index = chapter_index.value;
    c_index += index;
    if (c_index < 0 || c_index >= props.work_info.length) {
        return;
    }
    chapter_index.value = c_index;
    work_content.value = await get_novel_content('sunyuanling', props.work_info[c_index].belong_to_series_id,
        props.work_info[c_index].title);
    work_title.value = props.work_info[c_index].title;
}

watch(props, () => {
    work_content.value = props.content;
    work_title.value = props.title;
    chapter_index.value = props.chapter_index;
});

function toggleSettings(page) {
    switch (page) {
        case 'setting':
            showSettings.value = !showSettings.value;
            directory_show.value = false;
            break;
        case 'directory':
            directory_show.value = !directory_show.value;
            showSettings.value = false;
            break;
        case 'close_all':
            if (directory_show.value || showSettings.value) {
                directory_show.value = false;
                showSettings.value = false;
            }
            break;
    }
}

const closeAllMenus = (event) => {
    if (settingsMenu.value && !settingsMenu.value.contains(event.target)) {
        toggleSettings('close_all');
    }
};

const toggleLightMode = () => {
    light_mode.value = !light_mode.value;
    updateStyles();
};

const updateStyles = () => {
    const body = document.body;
    const root = document.documentElement;
    root.style.setProperty('--fontFamily', fontFamily.value);
    root.style.setProperty('--fontSize', fontSize.value);
    root.style.setProperty('--backgroundColor', light_mode.value ? '#333' : backgroundColor.value);
    root.style.setProperty('--fontColor', light_mode.value ? '#f5f5f5' : fontColor.value);
    root.style.setProperty('--pageWidth', `${pageWidth.value}px`);

    body.style.backgroundColor = light_mode.value ? '#333' : backgroundColor.value;
    body.style.color = light_mode.value ? '#f5f5f5' : fontColor.value;
};

watch([fontFamily, fontSize, backgroundColor, fontColor, pageWidth, light_mode], updateStyles, { immediate: true });

onMounted(() => {
    document.addEventListener('click', closeAllMenus);
    document.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
    document.removeEventListener('click', closeAllMenus);
    document.removeEventListener('keydown', handleKeyDown);
    // Reset body styles when component is destroyed
    document.body.style.backgroundColor = '';
    document.body.style.color = '';
});

const handleKeyDown = (event) => {
    if (event.key === 'ArrowLeft') {
        switch_chapter(-1);
    } else if (event.key === 'ArrowRight') {
        switch_chapter(1);
    }
};
</script>

<style scoped>
.content {
    width: 100%;
    background-color: var(--backgroundColor, #ffffff);
    color: var(--fontColor, #000000);
    display: flex;
    flex-direction: column;
    transition: background-color 0.3s, color 0.3s;
}

.novel_content {
    position: relative;
    max-width: var(--pageWidth, 800px);
    margin: 0 auto;
    padding: 20px;
    background-color: var(--backgroundColor, #ffffff);
    color: var(--fontColor, #000000);
    transition: background-color 0.3s, color 0.3s;
}

.title {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 10px;
}

.content {
    font-family: var(--fontFamily, Arial);
    font-size: var(--fontSize, 16px);
    text-indent: 2em;
    line-height: 2em;
    letter-spacing: 0.1em;
}

.font_setting {
    position: absolute;
    top: 50px;
    right: 100px;
    width: 300px;
    padding: 10px;
    border: 1px solid #ddd;
    background: #f9f9f9;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
}

.font_setting .title {
    font-weight: bold;
    margin-bottom: 10px;
}

.font_setting .item {
    margin-bottom: 10px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}

.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.right_side {
    position: fixed;
    right: 30px;
    top: 100px;
    display: flex;
    flex-direction: column;
    width: auto;
    height: auto;
    padding: 5px;
    background-color: rgb(192, 188, 188);
    border-radius: 15px;
    z-index: 2;
    align-items: flex-start;
    justify-content: center;
}

.directory {
    display: flex;
    position: relative;
}

.align_center {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    text-indent: 0em;
    cursor: pointer;
    border-radius: 5px;
    width: 90%;
    padding: 5px 5px;
    flex-direction: column;
    gap: 5px;
}

.align_center:hover {
    background-color: rgb(209, 209, 209);
    transition: all 0.3s ease-in-out;
    transform: translateY(-2px);
}
</style>