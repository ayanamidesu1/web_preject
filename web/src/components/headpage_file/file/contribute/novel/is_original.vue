<template>
    <div class="is_original">
        <span><b>描写内容</b></span>
        <div class="is_original_box">
            <switch_btn @change_status="get_is_original"></switch_btn>
            <span>是否为原创</span>
        </div>
        <div class="tips">
            <span style="color:rgba(77,77,77,0.8);font-size:14px;">若该作品的所有内容（如：故事、人物、设定等）都是您的原创，请选择此项。</span>
        </div>
        <re_select :select_title="select_title" :select_list="select_list" @select-item="get_select_item" style="z-index:5;"></re_select>
    </div>
</template>

<script setup>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted,defineEmits } from 'vue';
import switch_btn from '../../../../models/switch_btn.vue'
import re_select from '../../../../models/select.vue'
let select_title=ref('选择作品类型')
let select_list=ref(['恋爱','异世界穿越','现代奇幻','悬疑','恐怖','科幻','日常','历史','百合','同人向','其他文体','随笔','剧本',
'轻小说','游戏','种田','其他'
])
let select_item=ref()
let is_original=ref(false)
function get_select_item(item){
    select_item.value=item
}
function get_is_original(item)
{
    is_original.value=item
}
let emit=defineEmits(['series_info'])
// eslint-disable-next-line no-unused-vars
watch([select_item,is_original],()=>{
    emit('series_info',{'series_name':select_item.value,'is_original':is_original.value,})
})
</script>

<style scoped>
.is_original{
    width:100%;
    height: auto;
    display: flex;
    flex-direction: column;
    position: relative;
    gap:10px;
    padding: 5px;
}
.is_original_box{
    display: flex;
    width: 100%;
    height: auto;
    gap:10px;
    align-items: center;
}
</style>