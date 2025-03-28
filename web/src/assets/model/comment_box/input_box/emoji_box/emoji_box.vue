<template>
    <div class="emoji_box">
        <div class="content">
            <div class="emoji_title">
                <div class="title_item" v-for="(item, index) in Object.keys(emoji_list)" :key="index">
                    <img class="icon" :src="ip + emoji_list[item][0]" @click="set_emoji_title(item)">
                </div>
            </div>
            <div class="emoji_item">
                <div class="emoji_list">
                    <div class="item" v-for="(item, index) in emoji_list_item" :key="index">
                        <img class="icon" :src="ip + item" :alt="item" @click="send_emoji(item)">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref ,defineEmits} from 'vue';

const emits= defineEmits(['emoji'])

function send_emoji(emoji) {
    emits('emoji', emoji);
    console.log(emoji);
}

let ip = 'https://www.sunyuanling.com/server/static/emoji/';

let emoji_list = ref({
    'dog': [
        '狗头.svg',
        '吃瓜.svg',
        '大笑.svg',
        '害怕.svg',
        '滑稽.svg',
        '快哭了.svg',
        '破涕为笑.svg',
        '受虐滑稽.svg',
        '微笑.svg',
        '无语.svg',
        '捂脸.svg',
        '捂嘴笑.svg',
        '笑哭.svg',
        '阴险.svg',
        '张嘴闭眼笑.svg'
    ],
    'reversal_dog': [
        '张嘴闭眼笑.svg',
        '阴险.svg',
        '笑哭.svg',
        '捂嘴笑.svg',
        '捂脸.svg',
        '无语.svg',
        '微笑.svg',
        '受虐滑稽.svg',
        '破涕为笑.svg',
        '害怕.svg',
        '滑稽.svg',
        '快哭了.svg',
        '大笑.svg',
        '吃瓜.svg',
        '狗头.svg'
    ]
});

let emoji_title = ref('dog');
let emoji_list_item = ref(emoji_list.value[emoji_title.value]);

function set_emoji_title(title) {
    emoji_title.value = title;
    emoji_list_item.value = emoji_list.value[title]; // 修正这里
}

</script>

<style scoped>
.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.emoji_box {
    width: 400px;
    height: 300px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    border-radius: 5px;
    padding: 5px;
    border: 1px solid rgba(133, 133, 133, 0.8);
    background-color: rgba(255,255,255,1);
    z-index: 10;
    min-width: 200px;
    min-height: 200px;
    max-height: 400px;
    max-width: 400px;
}
.content{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap:5px;
}
.emoji_title{
    width: 100%;
    height: 40px;
    display: flex;
    gap:10px;
    border-bottom: 1px solid rgba(133, 133, 133, 0.8);
    align-items: center;
    justify-content: flex-start;
}
.title_item{
    width: 35px;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    transition: all 0.2s ease-in-out;
    cursor: pointer;
}
.title_item img{
    width: 30px;
    height: 30px;
}
.title_item:hover{
    background-color: rgba(133, 133, 133, 0.8);
}
.emoji_item{
    width: 100%;
    display: flex;
    height: auto;
}
.emoji_list{
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    gap:10px;
}
.item{
    display: flex;
    margin-top:10px;
    height: 30px;
    width: 30px;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    transition: all 0.2s ease-in-out;
    cursor: pointer;
}
.item:hover{
    background-color: rgba(133, 133, 133, 0.8);
}

</style>