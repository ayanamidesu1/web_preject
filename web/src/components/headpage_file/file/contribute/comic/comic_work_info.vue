<template>
    <div class="ill_work_info">
        <div class="content">
            <div class="work_info">
                <input placeholder="标题" v-model="work_title">
                <textarea placeholder="描述/简介" v-model="work_introduce" style="resize: vertical;"></textarea>
            </div>
            <div class="work_tags">
                <input placeholder="作品标签" v-model="tag">
                <div class="add_tag_btn" @click="add_tags">
                    <img class="icon" src="https://www.sunyuanling.com/assets/add.svg">
                </div>
                <div class="tags_list" v-for="(item, index) in tags" :key="index">
                    <span>#{{ item }}</span>
                </div>
            </div>
            <div class="age_classification">
                <span>年龄分段：</span>
                <input type="radio" name="age" value="16" v-model="age_classification">全年龄
                <input type="radio" name="age" value="18" v-model="age_classification">R-18
                <input type="radio" name="age" value="18G" v-model="age_classification">R-18G
            </div>
            <div class="important_tips">
                <span>
                    以下作品禁止投稿。请在投稿之前进行确认。
                    <ol>
                        <li>他人制作的作品，发售中的商品图像，第三者持有权利的图像，游戏、视频作品的截图，包含屏幕截图图像的作品。
                        </li>
                        <li>挪用以上图像，从最初开始并非全部由您自己创作的作品。作品以外的照片图像。</li>
                        <li> 违反使用条款的作品投稿用户，将被停止公开投稿作品，停止账号使用。</li>
                    </ol>
                </span>
            </div>
            <div class="sure_btn">
                <div class="sure" @click="send_work_info">
                    <span>确定</span>
                    <img class="icon" src="https://www.sunyuanling.com/assets/select_correct.svg">
                </div>
                <div class="cancel" @click="clear_work_info">
                    <span>清空</span>
                    <img class="icon" src="https://www.sunyuanling.com/assets/close.svg">
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, defineEmits } from 'vue';

const tags = ref([]);
const work_title = ref('');
const work_introduce = ref('');
const age_classification = ref('');
const tag = ref('');
const emit = defineEmits(['work_info']);

// 添加标签
const add_tags = () => {
    if (tag.value) {
        tags.value.push(tag.value);
        tag.value = '';
        send_work_info();
    }
};

// 设置并发送作品信息
const send_work_info = () => {
    const work_info = {
        name: work_title.value,
        brief_introduction: work_introduce.value,
        age_classification: age_classification.value,
        work_tags: tags.value,
    };
    emit('work_info', work_info);
};

// 监听数据变化
watch([work_title, work_introduce, age_classification, tags], send_work_info, { deep: true });

// 清空作品信息
const clear_work_info = () => {
    work_title.value = '';
    work_introduce.value = '';
    age_classification.value = '';
    tags.value = [];
    send_work_info();
};
</script>

<style scoped>
.ill_work_info {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    box-sizing: border-box;
}

.content {
    width: 100%;
    max-width: 600px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.work_info,
.work_tags,
.age_classification,
.important_tips,
.sure_btn {
    width: 100%;
}

.work_info input,
.work_info textarea,
.work_tags input {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    box-sizing: border-box;
}

.work_tags {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.add_tag_btn {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.add_tag_btn img {
    width: 24px;
    height: 24px;
}

.tags_list {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.tags_list span {
    background-color: #e0e0e0;
    padding: 5px 10px;
    border-radius: 12px;
}

.age_classification {
    display: flex;
    align-items: center;
    gap: 10px;
}

.important_tips span {
    display: block;
    background-color: #ffeded;
    padding: 10px;
    border: 1px solid #ff8c8c;
    border-radius: 5px;
}

.sure_btn {
    display: flex;
    justify-content: space-between;
}

.sure,
.cancel {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.sure img,
.cancel img {
    width: 24px;
    height: 24px;
    margin-left: 5px;
}
</style>