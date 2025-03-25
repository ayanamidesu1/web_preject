<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="sidebar">
        <div class="title"><span>首页</span></div>
        <div class="sidebar_content">
            <div class="sidebar_content_item" style="" @click="switch_index_page(0)">
                <div class="sidebar_content_item_icon">
                    <img src="https://www.sunyuanling.com/assets/photo.svg" class="icon">
                </div>
                <div class="sidebar_content_item_text"><span>插画</span></div>
            </div>
            <div class="sidebar_content_item" @click="switch_index_page(0)">
                <div class="sidebar_content_item_icon">
                    <img src="https://www.sunyuanling.com/assets/play.svg" class="icon">
                </div>
                <div class="sidebar_content_item_text">动图</div>
            </div>
            <div class="sidebar_content_item" @click="switch_index_page(1)">
                <div class="sidebar_content_item_icon">
                    <img src="https://www.sunyuanling.com/assets/comic.svg" class="icon">
                </div>
                <div class="sidebar_content_item_text"><span>漫画</span></div>
            </div>
            <div class="sidebar_content_item" @click="switch_index_page(2)">
                <div class="sidebar_content_item_icon">
                    <img class="icon" src="https://www.sunyuanling.com/assets/novel.svg">
                </div>
                <div class="sidebar_content_item_text"><span>小说</span></div>
            </div>
            <br>
            <div class="sidebar_content_item">
                <div class="sidebar_content_item_icon">
                    <img class="icon" src="https://www.sunyuanling.com/assets/people.svg">
                </div>
                <div class="sidebar_content_item_text"><span>已关注用户的新作</span></div>
            </div>
            <div class="sidebar_content_item">
                <div class="sidebar_content_item_icon">
                    <img class="icon" src="https://www.sunyuanling.com/assets/find.svg">
                </div>
                <div class="sidebar_content_item_text"><span>发现</span></div>
            </div>
            <br>
            <div class="sidebar_content_item">
                <div class="sidebar_content_item_icon">
                    <img class="icon" src="https://www.sunyuanling.com/assets/rank_list.svg">
                </div>
                <div class="sidebar_content_item_text"><span>排行榜</span></div>
            </div>
            <div class="sidebar_content_item">
                <div class="sidebar_content_item_icon">
                    <img class="icon" src="https://www.sunyuanling.com/assets/smail.svg">
                </div>
                <div class="sidebar_content_item_text"><span>大家的新作</span></div>
            </div>
            <div class="sidebar_content_item">
                <div class="sidebar_content_item_icon">
                    <img class="icon" src="https://www.sunyuanling.com/assets/flag.svg">
                </div>
                <div class="sidebar_content_item_text"><span>比赛</span></div>
            </div>
            <div class="sidebar_content_item">
                <div class="sidebar_content_item_icon">
                    <img class="icon" src="https://www.sunyuanling.com/assets/red_love.svg">
                </div>
                <div class="sidebar_content_item_text"><span>约稿</span></div>
            </div>
            <br>
            <div class="sidebar_content_item">
                <div class="sidebar_content_item_icon">
                    <img class="icon" src="https://www.sunyuanling.com/assets/scroll.svg">
                </div>
                <div class="sidebar_content_item_text"><span>用户企划</span></div>
            </div>
            <div class="sidebar_content_item">
                <div class="sidebar_content_item_icon">
                    <img class="icon" src="https://www.sunyuanling.com/assets/pencil.svg">
                </div>
                <div class="sidebar_content_item_text"><span>绘图方法</span></div>
            </div>
            <div class="sidebar_content_item">
                <div class="sidebar_content_item_icon">
                    <img class="icon" src="https://www.sunyuanling.com/assets/idea.svg">
                </div>
                <div class="sidebar_content_item_text"><span>创作点子</span></div>
            </div>
            <div class="show_more" v-show="show_more" @click="show_more_btn">
                <div class="show_more_icon mr ml">
                    <img class="icon" src="https://www.sunyuanling.com/assets/drop_down.svg">
                </div>
                <div class="show_more_text ml">
                    <span>查看更多</span>
                </div>
            </div>
            <div class="show_more_content" v-show="show_more_content">

                <div class="show_more_content_item">
                    <div class="show_more_content_icon mr ml">
                        <img src="https://www.sunyuanling.com/assets/paper_airplane.svg" class="icon">
                    </div>
                    <div class="show_more_content_item_text mr ml"><span>动态</span></div>
                </div>
                <div class="show_more_content_item">
                    <div class="show_more_content_icon mr ml">
                        <img class="icon" src="https://www.sunyuanling.com/assets/blue_people.svg">
                    </div>
                    <div class="show_more_content_item_text mr ml ">群组</div>
                </div>
                <div class="show_more_content_item">
                    <div class="show_more_content_icon mr ml">
                        <img class="icon" src="https://www.sunyuanling.com/assets/gift_pack.svg">
                    </div>
                    <div class="show_more_content_item_text mr ml ">活动</div>
                </div>
                <div class="show_more_content_item" @click="show_more_hidden_btn">
                    <div class="show_more_content_icon mr ml">
                        <img class="icon" src="https://www.sunyuanling.com/assets/drop_up.svg">
                    </div>
                    <div class="show_more_content_item_text mr ml ">收起</div>
                </div>
            </div>
            <div class="other">
                <span>{{notice_content}}</span>
            </div>
        </div>
        <div class="notice">
            <span>{{notice_content}}</span>
        </div>
    </div>
</template>
<script>
import { onMounted, ref } from 'vue'
import * as cookies from '../../../../../../model/cookies.js'
import {useStore} from 'vuex'
export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: 'sidebar'
}
</script>
<script setup>
let show_more_content = ref(false);
let show_more = ref(true);
let token = cookies.get_cookie('token')
let notice_content = ref()
const store = useStore()

function switch_index_page(index)
{
    switch(index)
    {
        case 0:
            store.commit('SET_PAGESTATUS',0)
            store.commit('SET_INDEXPAGE',0)
            store.commit('SET_SINGLE_PAGE_STATUS',{key:'index_page',value:true})
            break;
        case 1:
            store.commit('SET_PAGESTATUS',1)
            store.commit('SET_INDEXPAGE',1)
            store.commit('SET_SINGLE_PAGE_STATUS',{key:'index_page',value:true})
            break;
        case 2:
            store.commit('SET_PAGESTATUS',2)
            store.commit('SET_INDEXPAGE',2)
            store.commit('SET_SINGLE_PAGE_STATUS',{key:'index_page',value:true})
            break;
    }
}
function show_more_btn() {
    if (show_more.value == true) {
        show_more.value = false;
        show_more_content.value = true;
    }
}
function show_more_hidden_btn() {
    if (show_more.value == false) {
        show_more.value = true;
        show_more_content.value = false;
    }
}
//获取公告信息
async function get_notice() {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/notice_control/NoticeOperations/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body: JSON.stringify({
                operate_type: 'search',
                token: token,
            })
        })
        if (res.ok) {
            const data = await res.json()
            if (data.status == 'success') {
                notice_content.value = data.data[0].content;
            }
            else {
                console.log(data.message)
            }
        }
        else {
            const data=await res.json()
            console.log(res.status)
            console.log(data.message)
        }
    }
    catch (error) {
        console.log(error)
    }
}
onMounted(async () => {
    await get_notice();
})
</script>

<style scoped>
/*通用样式*/
.mt {
    margin-top: 5px;
}

.ml {
    margin-left: 5px;
}

.mr {
    margin-right: 5px;
}

.mb {
    margin-bottom: 5px;
}

.show_more_content {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: auto;
}

.show_more_content_item {
    display: flex;
    width: 100%;
    height: 35px;
    align-items: center;
}

.show_more_content_item:hover {
    background-color: rgb(148, 148, 148);
    cursor: pointer;
    border-radius: 5px;
}

.show_more_content_icon {
    width: 30px;
    height: 30px;
    overflow: hidden;
}

.show_more_content_icon svg {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.show_more {
    display: flex;
    width: 100%;
    height: 30px;
    margin-top: 5px;
    align-items: center;
}

.show_more:hover {
    background-color: rgb(148, 148, 148);
    border-radius: 5px;
    cursor: pointer;
}

.show_more_icon {
    display: flex;
    width: 40px;
    height: 40px;
    overflow: hidden;
    align-items: center;
}

.show_more_icon svg {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.title {
    font-size: 18px;
    color: rgb(148, 148, 148);
    margin-top: 10px;
    align-content: center;
    font-weight: bold;
    margin-bottom: 5px;
    border-bottom: 1px solid rgb(255, 255, 255);
}

.sidebar {
    display: flex;
    position: fixed;
    flex-direction: column;
    width: 210px;
    height: 100%;
    padding: 5px;
    background-color: rgb(241, 241, 241);
}

.sidebar_content {
    display: block;
    flex-direction: column;
    width: auto;
    height: 70%;
    overflow-y: auto;
    overflow-x: hidden;
    justify-content: center;
    padding: 5px;
    position: relative;
}

.sidebar_content_item {
    display: flex;
    width: 100%;
    height: 40px;
    margin-top: 5px;
    justify-content: flex-start;
    align-items: center;
    margin-top: 5px;
    margin-bottom: 5px;
    padding: 5px;
}

.sidebar_content_item:hover {
    background-color: rgba(148, 148, 148, 0.5);
    border-radius: 5px;
    cursor: pointer;
    transition: 0.2s;
}

.sidebar_content_item_icon {
    display: flex;
    width: 40px;
    height: 40px;
    overflow: hidden;
    margin-left: 5px;
    margin-right: 5px;
    align-items: center;
}

.sidebar_content_item_icon svg {
    width: 100%;
    height: 100%;
    fill: rgb(148, 148, 148);
    object-fit: cover;
}

.notice {
    display: flex;
    width: 100%;
    height: auto;
    flex-grow: 1;
    margin-top: 5px;
}

.icon {
    width: 30px;
    height: 30px;
    object-fit: cover;
}
</style>