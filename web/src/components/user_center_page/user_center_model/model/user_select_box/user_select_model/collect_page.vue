<template>
  <div class="collect_page">
    <div class="content">
      <div class="is_open">
        <div class="switch_work_type">
          <span @click="work_show_type = 'all'"
            :class="work_show_type == 'all' ? 'switch_work_type_choose' : ''">所有作品</span>
          <span @click="work_show_type = 'ill'"
            :class="work_show_type == 'ill' ? 'switch_work_type_choose' : ''">插画</span>
          <span @click="work_show_type = 'comic'"
            :class="work_show_type == 'comic' ? 'switch_work_type_choose' : ''">漫画</span>
          <span @click="work_show_type = 'novel'"
            :class="work_show_type == 'novel' ? 'switch_work_type_choose' : ''">小说</span>
        </div>
        <div class="switch_open_status">
          <span @click="open_work_show_status = 1"
            :class="open_work_show_status == 1 ? 'switch_work_type_choose' : ''">公开</span>
          <span @click="open_work_show_status = 0"
            :class="open_work_show_status == 0 ? 'switch_work_type_choose' : ''">不公开</span>
        </div>
      </div>
      <div class="title">
        <span>作品</span>
        <span style="cursor: pointer;" @click="collect_control_box_show = !collect_control_box_show">管理收藏</span>
      </div>
      <div class="collect_control_box" v-if="collect_control_box_show">
        <div class="control_item" @click="choose_all_collect_work()">
          <span>全选</span>
        </div>
        <div class="control_item" @click="delete_select_collect_work()">
          <span>取消收藏</span>
        </div>
        <div class="control_item" v-if="open_work_show_status == 1" @click="set_select_collect_work_open_status(0)">
          <span>设置为不公开</span>
        </div>
        <div class="control_item" v-if="open_work_show_status == 0" @click="set_select_collect_work_open_status(1)">
          <span>设置为公开</span>
        </div>
        <div class="control_item" @click="collect_control_box_show = false"
          style="align-self: flex-end;position: absolute;right: 10px;">
          <span>结束</span>
        </div>
      </div>
      <div class="collect_list" v-if="filteredCollectWorklist.length">
        <div class="collect_item" v-for="(item, index) in filteredCollectWorklist" :key="index">
          <div class="item_box" v-if="item.work_status === 'normal'">
            <div class="work_type">
              <span>{{ get_work_type(item.type) }}</span>
            </div>
            <div class="work_item">
              <div class="image_container" @click="choose_item({'work_id':item.id,'work_type':item.type,'item':item})">
                <img :src="get_image_src(item)" alt="作品封面">
                <div class="age_tag" v-if="item.work_info.age_classification && item.work_info.age_classification > 18">
                  <span class="age_num">{{ item.work_info.age_classification }}</span>
                </div>
                <div class="work_count" v-if="get_file_count(item) > 1">
                  <span class="work_num">{{ get_file_count(item) }}</span>
                </div>
                <div class="choose_work_box" v-if="collect_control_box_show"
                  @click="toggle_choose_collect_work_list($event,item)">
                  <div class="choose_box"
                    :style="{ backgroundColor: choose_collect_work_list.includes(item) ? 'rgba(0,150,250,1)' : '' }">
                    <img class="icon" src="https://www.sunyuanling.com/assets/correct.svg">
                  </div>
                </div>
              </div>
              <div class="work_name">
                <span>{{ item.type === 'ill' ? item.work_info.name : item.work_info.work_name }}</span>
              </div>
              <div class="author_info">
                <div class="author_avatar">
                  <img :src="'https://www.sunyuanling.com/image/avatar_thumbnail/' + item.authorinfo.user_avatar"
                    alt="作者头像">
                </div>
                <div class="author_name">
                  <span>{{ item.authorinfo.username }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="if_all_none" v-if="filteredCollectWorklist.length <= 1 || !filteredCollectWorklist">
        <span>这里空空如也什么也没有</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, onMounted, computed, watch } from 'vue'
import { get_user_collect_worklist } from '../../../js/get_workinfo'
import { update_user_collect_work } from '../../../js/update_userinfo'
import {useStore} from 'vuex'
const store = useStore()

//选择作品
function choose_item(item)
{
  console.log(item)
  if (item.work_type == 'ill') {
        store.commit('SET_CONTENT_PAGE', {
            key: 'ill_page',
            value: true
        })
        store.commit('SET_SINGLE_PAGE_STATUS', { key: 'content_index_page', value: true })
        store.commit('SET_WORK_ID', item.item.workid)
        store.commit('SET_WORK_TYPE', item.work_type)
    }
    else if(item.work_type=='comic')
    {
        store.commit('SET_CONTENT_PAGE', {
            key: 'comic_page',
            value: true
        })
        store.commit('SET_SINGLE_PAGE_STATUS', { key: 'content_index_page', value: true })
        store.commit('SET_WORK_ID', item.item.workid)
        store.commit('SET_WORK_TYPE', item.work_type)
    }
    else if(item.work_type=='novel')
    {
        store.commit('SET_CONTENT_PAGE', {
            key: 'novel_page',
            value: true
        })
        store.commit('SET_SINGLE_PAGE_STATUS', { key: 'content_index_page', value: true })
        store.commit('SET_WORK_ID', item.item.workid)
        store.commit('SET_WORK_TYPE', item.work_type)
    }
}

const props = defineProps({
  user_info: {
    type: Object,
    default: () => ({})
  },
  token: {
    type: String,
    default: ''
  }
})

const collect_worklist = ref([])
const open_work_show_status = ref(1)
const work_show_type = ref('all')
const collect_control_box_show = ref(false)
const choose_collect_work_list = ref([])

function toggle_choose_collect_work_list(event,item) {
  const index = choose_collect_work_list.value.indexOf(item)
  if (index > -1) {
    choose_collect_work_list.value.splice(index, 1)
  } else {
    choose_collect_work_list.value.push(item)
  }
  console.log(choose_collect_work_list.value)
  //阻止点击事件传播
  event.stopPropagation()
}

//删除收藏作品
async function delete_select_collect_work() {
  let message_status = []
  for (let i = 0; i < choose_collect_work_list.value.length; i++) {
    message_status.push(await update_user_collect_work(props.token, choose_collect_work_list.value[i].id, choose_collect_work_list.value[i].type,
      'delete', null
    ))
  }
  if (message_status.includes(false)) {
    alert('删除失败')
  } else {
    alert('删除成功')
    collect_worklist.value = await get_user_collect_worklist(props.token)
  }
  //清除选择的列表
  choose_collect_work_list.value = []
}
//设置收藏作品公开状态
async function set_select_collect_work_open_status(open_status) {
  let message_status = []
  for (let i = 0; i < choose_collect_work_list.value.length; i++) {
    message_status.push(await update_user_collect_work(props.token, choose_collect_work_list.value[i].id, choose_collect_work_list.value[i].type,
      'set_open', open_status
    ))
  }
  if (message_status.includes(false)) {
    alert('设置失败')
  } else {
    alert('设置成功')
    collect_worklist.value = await get_user_collect_worklist(props.token)
  }
  //清空选择列表
  choose_collect_work_list.value = []
}

function choose_all_collect_work() {
  choose_collect_work_list.value = [...filteredCollectWorklist.value]
}

watch(collect_control_box_show, () => {
  if (collect_control_box_show.value == false) {
    choose_collect_work_list.value = []
  }
})

onMounted(async () => {
  collect_worklist.value = await get_user_collect_worklist(props.token)
  console.log(collect_worklist.value)
})

const filteredCollectWorklist = computed(() => {
  return collect_worklist.value.filter(item => {
    const matchesOpenStatus = item.is_open == open_work_show_status.value
    const matchesWorkType = work_show_type.value === 'all' || item.type === work_show_type.value
    return matchesOpenStatus && matchesWorkType
  })
})

function get_work_type(type) {
  switch (type) {
    case 'novel':
      return '小说'
    case 'ill':
      return '插画'
    case 'comic':
      return '漫画'
    default:
      return '其他'
  }
}

function get_image_src(item) {
  const { type, work_info } = item
  const baseUrl = 'https://www.sunyuanling.com/image/'
  if (type === 'novel') {
    return `${baseUrl}novel/thumbnail/${work_info.work_cover}`
  } else if (type === 'ill') {
    return `${baseUrl}thumbnail/${work_info.content_file_list.split(/[,，]/)[0]}`
  } else if (type === 'comic') {
    return `${baseUrl}comic/thumbnail/${work_info.content_file_list.split(/[，,]/)[0]}`
  }
  return ''
}

function get_file_count(item) {
  const { content_file_list } = item.work_info
  if (content_file_list) {
    const files = content_file_list.split(/[,，]/)
    return files.length
  }
  return 0
}
</script>



<style scoped>
.collect_page {
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.is_open {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.switch_work_type,
.switch_open_status {
  display: flex;
  gap: 10px;
}

.switch_work_type span,
.switch_open_status span {
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
  font-weight: 500;
}

.switch_work_type span:hover,
.switch_open_status span:hover {
  opacity: 0.8;
  background-color: rgba(0, 150, 250, 1);
  transform: scale(1.1);
  transform: translateY(-2px);
  color: white;
  transition: all 0.2s ease-in-out;
}

.switch_work_type_choose {
  background-color: rgba(0, 150, 250, 1);
  color: white;
}

.switch_open_status {
  margin-top: 10px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  display: flex;
  width: 100%;
  justify-content: space-between;
}

.collect_control_box {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
  width: 100%;
  margin-top: 10px;
  height: auto;
  position: relative;
  padding: 5px 10px;
}

.control_item {
  display: flex;
  width: auto;
  height: auto;
  justify-content: center;
  align-items: center;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  background-color: rgba(61, 61, 61, 0.5);
  color: white;
}

.control_item:hover {
  background-color: rgba(61, 61, 61, 0.8);
  transition: all 0.2s ease-in-out;
  transform: scale(1.1);
  transform: translateY(-2px);
}

.collect_list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  width: 100%;
  height: auto;
  overflow-y: auto;
}

.collect_item {
  box-sizing: border-box;
  display: flex;
}

.item_box {
  position: relative;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  width: 100%;
  height: 100%;
  margin: auto;
  gap: 5px;
  max-width: 220px;
  max-height: 350px;
  min-width: 200px;
  min-height: 350px;
}

.work_type {
  padding: 4px 8px;
  border-radius: 4px;
  width: 100%;
  height: auto;
}

.image_container {
  position: relative;
  width: 200px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.image_container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 15px;
}

.choose_work_box {
  width: 100%;
  height: 100%;
  display: flex;
  position: absolute;
  left: 0px;
  top: 0px;
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.2);
  overflow: hidden;
  transition: all 0.3s;
  border-radius: 15px;
  z-index:2;

}

.choose_work_box:hover {
  background-color: rgba(0, 0, 0, 0.35);
}

.choose_work_box::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 100%;
  width: 314%;
  height: 314%;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.5s;
  /* 扩散效果渐变 */
}

.choose_work_box:hover::after {
  transform: translate(-50%, -50%) scale(1);
}


.choose_box {
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.8);
  position: absolute;
  right: 10px;
  bottom: 10px;
  z-index: 2;
}

.choose_box img {
  width: 25px;
  height: 25px;
  object-fit: cover;
}

.icon {
  width: 25px;
  height: 25px;
  object-fit: cover;
}

.age_tag {
  position: absolute;
  top: 10px;
  left: 10px;
  background: red;
  color: white;
  padding: 4px 8px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 4px;
}

.work_count {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.work_item {
  display: flex;
  flex-direction: column;
  padding: 10px;
}

.work_name {
  margin-top: 10px;
}

.author_info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.author_avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.item_box_deleted {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  width: 200px;
  background: #f8d7da;
  color: #721c24;
  padding: 20px;
  border-radius: 10px;
  margin: auto;
}

.item_box_deleted_text {
  text-align: center;
}

.if_all_none {
  text-align: center;
  font-size: 18px;
  color: #888;
}
</style>
