<template>
  <div class="ill_page">
    <div class="upload_work_box">
      <input type="file" id="upload_work_file" accept="image/*" style="display: none;" ref="upload_work_file" multiple
        @change="handleFileUpload">
      <div class="upload_btn_box" v-if="temp_file_list.length <= 0">
        <div class="upload_btn" @click="upload_work_file_click()">
          <div class="upload_svg">
            <img class="icon" src="https://www.sunyuanling.com/assets/photo.svg">
            <img src="https://www.sunyuanling.com/assets/add.svg" class="add_icon">
          </div>
          上传作品
        </div>
      </div>
      <div class="work_statement" v-if="temp_file_list.length <= 0">
        <span>格式：JPEG/JPG/GIF/PNG/TIFF</span>
        <span>大小：32MB以下</span>
        <span>数量：200张以下，合计不超过300MB</span>
      </div>
      <div class="upload_work_list" v-if="temp_file_list.length > 0">
        <div class="tips_info">
          文件数量：{{ temp_file_list.length }}
          文件总大小：{{ (file_size / (1024 * 1024)).toFixed(2) }}MB
        </div>
        <div class="item">
          <div class="work_item" v-for="(item, index) in temp_file_list" :key="item.filename">
            <img :src="item.url" alt="文件预览">
            <div class="delete_btn" @click="delete_work(index)">
              <img class="icon" src="https://www.sunyuanling.com/assets/close.svg">
            </div>
            <div class="filename">{{ item.filename }}</div>
          </div>
          <div class="add_work_btn" @click="add_work">
            <img  src="https://www.sunyuanling.com/assets/add.svg">
          </div>
        </div>
      </div>
    </div>
    <ill_page_info @work_info="get_sub_work_info" />
    <div class="submit_btn" @click="submit_work">
      <span>投稿</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import ill_page_info from './ill_work_info.vue';
import * as cookies from '@/assets/js/cookies'

let temp_file_list = ref([]);
let file_size = ref(0);
let file_count = ref(0);
let work_info = ref({});
let userinfo = ref(JSON.parse(cookies.get_cookie('userinfo')))
console.log(userinfo.value)

//接收子组件信息
function get_sub_work_info(info) {
  work_info.value = info;
  work_info.value.username = userinfo.value.username
  work_info.value.userid = userinfo.value.userid
  work_info.value.work_type='ill'
  work_info.value.token = cookies.get_cookie('token')
  console.log(work_info.value)
}

function upload_work_file_click() {
  // 模拟点击上传文件
  document.getElementById('upload_work_file').click();
}

watch(() => temp_file_list.value, (newValue) => {
  let totalSize = 0;
  for (let i = 0; i < newValue.length; i++) {
    totalSize += newValue[i].file.size;
  }
  file_size.value = totalSize;
  file_count.value = newValue.length;
});

function handleFileUpload(event) {
  const files = event.target.files;
  let totalSize = 0;

  for (let i = 0; i < files.length; i++) {
    totalSize += files[i].size;
  }

  if (files.length > 200 - temp_file_list.value.length) {
    alert('不能超过200个文件！');
    return;
  }

  if (totalSize > (300 * 1024 * 1024 - temp_file_list.value.reduce((acc, file) => acc + file.file.size, 0))) {
    alert('文件总大小不能超过300MB！');
    return;
  }

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const reader = new FileReader();

    reader.onload = (e) => {
      temp_file_list.value.push({ file, url: e.target.result, filename: file.name });
    };

    reader.readAsDataURL(file);
  }
}

function delete_work(index) {
  requestAnimationFrame(() => {
    temp_file_list.value.splice(index, 1);
  });
}

function add_work() {
  upload_work_file_click();
}

async function submit_work() {  
  try {  
    const formData = new FormData();  
    temp_file_list.value.forEach((item, index) => {  
      formData.append('files', item.file, item.file.name); // 最好包含文件名  
    });  
    formData.append('work_info', JSON.stringify(work_info.value)); // 将 work_info 转换为 JSON 字符串  
  
    const res = await fetch('https://www.sunyuanling.com/api/file/UploadFile/', {  
      method: 'POST',  
      headers: {  
        'Authorization': 'Bearer ' + localStorage.getItem('token'),  
      },
      body: formData, // 直接使用 FormData  
    });  
  
    if (res.ok) {  
      const data = await res.json();  
      console.log(data.message);  
      alert('上传成功');
    } else {  
      console.log('服务器错误');  
      console.log(res.status);  
    }  
  } catch (e) {  
    console.log(e);  
  }  
  console.log('提交作品信息', work_info.value, temp_file_list.value);  
}
</script>

<style scoped>
.icon {
  width: 25px;
  height: 25px;
  object-fit: cover;
  position: relative;
}

.upload_svg {
  position: relative;
  display: flex;
  width: 35px;
  height: 35px;
  padding: 2px;
}

.add_icon {
  top: -1px;
  right: -2px;
  width: 15px;
  height: 15px;
  position: absolute;
}

.ill_page {
  width: 100%;
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
}

.upload_work_box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 25vh;
  background-color: #d1d1d1;
  color: white;
  padding: 10px;
  box-sizing: border-box;
}

.upload_btn_box {
  display: flex;
  padding: 5px 15px;
  background-color: #0096fa;
  border-radius: 15px;
  cursor: pointer;
}

.upload_btn_box:hover {
  opacity: 0.8;
  transition: 0.2s;
}

.upload_btn {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
}

.work_statement {
  display: flex;
  flex-direction: column;
  padding: 5px 10px;
}

.upload_work_list {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.item {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 10px;
  width: 100%;
}

.work_item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 160px;
  height: 160px;
  position: relative;
  margin: 15px 10px;
}

.work_item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.add_work_btn {
  width: 160px;
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 1;
}

.add_work_btn:hover {
  opacity: 0.8;
  transition: 0.2s;
}
.add_work_btn img{
  width:90%;
  height: 90%;
  object-fit: cover;
}

.delete_btn {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: -2px;
  right: -2px;
  border-radius: 50%;
  cursor: pointer;
}

.delete_btn img {
  width: 25px;
  height: 25px;
  object-fit: cover;
}

.delete_btn:hover {
  background-color: rgba(188, 188, 188, 1);
  transition: all 0.3s ease-in-out;
}

.filename {
  position: absolute;
  bottom: -20px;
  left: 0;
  width: 100%;
  text-align: center;
}

.submit_btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px 15px;
  border-radius: 15px;
  background-color: #0096fa;
  color: white;
  font-size: 18px;
  font-weight: bold;
  margin: 10px auto;
  cursor: pointer;
}

.submit_btn:hover {
  opacity: 0.8;
  transition: all 0.3s ease-in-out;
}
</style>
