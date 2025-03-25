<template>
    <div class="work_tags">
        <div class="left_btn" @click="scrollTabs(-400)">
            <svg t="1715776937217" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                p-id="4252" width="200" height="200">
                <path
                    d="M510.86222222 1020.58666667c281.71377778 0 510.86222222-229.14844445 510.86222223-510.86222222S792.576-1.13777778 510.86222222-1.13777778 0 228.01066667 0 509.72444445s229.14844445 510.86222222 510.86222222 510.86222222z m0-950.72711112c242.57422222 0 439.86488889 197.29066667 439.86488889 439.8648889S753.43644445 949.58933333 510.86222222 949.58933333c-242.57422222 0-439.86488889-197.29066667-439.86488889-439.86488888S268.288 69.85955555 510.86222222 69.85955555zM307.65511111 532.48c-13.88088889-13.88088889-13.88088889-36.29511111 0-50.176l260.89244444-260.89244445c13.88088889-13.88088889 36.29511111-13.88088889 50.176 0 13.88088889 13.88088889 13.88088889 36.29511111 0 50.176L382.976 507.33511111l235.86133333 235.86133334c13.88088889 13.88088889 13.88088889 36.29511111 0 50.176-6.94044445 6.94044445-16.04266667 10.35377778-25.03111111 10.35377777-9.10222222 0-18.20444445-3.41333333-25.03111111-10.35377777L307.65511111 532.48z"
                    fill="#333303" p-id="4253"></path>
            </svg>
        </div>
        <div class="tags" ><span class="tag" v-for="index in 20" :key="index">{{ tag }}{{index}}</span></div>
        <div class="right_btn" @click="scrollTabs(400)">
            <svg t="1715776983773" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                p-id="6057" width="200" height="200">
                <path
                    d="M896 512a384 384 0 1 0-384 384 384 384 0 0 0 384-384z m64 0A448 448 0 1 1 512 64a448 448 0 0 1 448 448z"
                    p-id="6058"></path>
                <path
                    d="M425.28 310.72a32 32 0 0 1 45.44-45.44l224 224a32 32 0 0 1 0 45.44l-224 224a32 32 0 0 1-45.44-45.44L626.88 512z"
                    p-id="6059"></path>
            </svg>
        </div>
    </div>
</template>

<script>
import { ref, reactive, toRefs, watch, onMounted, onUnmounted } from 'vue';
export default {
    name: 'work_tags',
}
</script>

<script setup>
let tag = ref('标签');
let colorArr=ref(['rgb(126, 183, 200)','rgb(126, 186, 200)','rgb(157, 200, 126)','rgb(200, 126, 170)','rgb(200, 126, 146)',
    'rgb(126, 129, 200)','rgb(167, 126, 200)','rgb(200, 170, 126)','rgb(126, 200, 167)','rgb(126, 200, 129)',
]);//颜色集
//标签栏横向滚动效果

function scrollTabs(scrollAmount){
    const tags=document.querySelector('.tags'); 
    const animationDuration = 0.3 * 1000; // 0.5秒转为毫秒
    const fps = 60; // 帧率
    const frameDuration = animationDuration / fps; // 每帧持续时间
    const framesCount = Math.ceil(animationDuration / frameDuration); // 总帧数
    let count = 0;

    function animateScroll() {
        if (count < framesCount) {
            tags.scrollLeft += scrollAmount / framesCount;
            count++;
            requestAnimationFrame(animateScroll);
        }
    }

    animateScroll();
}

//随机生成颜色
function randomColor(){
    let tag=document.querySelectorAll('.tag');
    tag.forEach(function(item){
        let randomNum=Math.floor(Math.random()*colorArr.value.length);
        item.style.backgroundColor=colorArr.value[randomNum];
    });
}
onMounted(() => {
    randomColor();
});

</script>

<style scoped>
.work_tags {
    display: flex;
    width: 80%;
    height: 60px;
    margin: 0 auto;
    justify-content: center;
    align-items: center;
    position: relative;
    align-items: center;
}

.tags{
    display: flex;
    width:100%;
    height: 100%;
    align-items: center;
    overflow-x:auto;
    scrollbar-width: none;
    white-space: nowrap;
    transition: transform 0.3s ease;
}
.tag{
    display: flex;
    justify-content: center;
    align-items: center;
    margin:0 10px;
    background-color: rgba(253, 116, 246,1);
    padding-left: 15px;
    padding-right: 15px;
    padding-top: 5px;
    padding-bottom: 5px;
    color: white;
    border-radius: 20px;
    min-height: 40px;
    opacity: 0.8;
}
.tag:hover{
    opacity: 1;
    cursor: pointer;
    transition: all 0.3s ease;
}
.left_btn {
    position: absolute;
    display: flex;
    left: 0;
    width: 40px;
    height: 40px;
    background-color: rgba(230,230,230,0.6);
    border-radius: 50%;
    justify-content: center;
    align-items: center;
    opacity: 0;
    z-index: 2;
}
.left_btn:hover {
    background-color: rgba(200,200,200,0.6);
    cursor: pointer;
    transition: all 0.3s ease;
    opacity: 1;
}
.left_btn svg{
    object-fit: cover;
    width: 80%;
    height: 80%;
}
.right_btn {
    position: absolute;
    display: flex;
    right: 0;
    width: 40px;
    height: 40px;
    background-color: rgba(230,230,230,0.6);
    border-radius: 50%;
    justify-content: center;
    align-items: center;
    opacity: 0;
    z-index:2;
}
.right_btn:hover {
    background-color: rgba(200,200,200,0.6);
    cursor: pointer;
    transition: all 0.3s ease;
    opacity: 1;
}
.right_btn svg{
    object-fit: cover;
    width: 80%;
    height: 80%;
}
</style>