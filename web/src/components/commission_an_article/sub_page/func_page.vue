<template>
  <div class="func_page">
    <div class="func_list_box">
      <h4>约稿方案</h4>
        <div class="func_list"></div>
        <span>新建方案</span>
    </div>
    <div class="tips">
        <span>约稿提示：</span>

    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
</script>

<style scoped>
.func_page{
  width: 100%;
  display: grid;
  grid-template-rows: minmax(100px,30%) minmax(200px,70%);
  gap:10px;
}
.func_list_box{
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 2px 0 3px rgba(0, 0, 0, 0.2);
  background-color: rgb(255, 255, 255);
  padding: 10px;
}
.tips{
  display: flex;
  flex-direction: column;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 2px 0 3px rgba(0, 0, 0, 0.2);
  background-color: rgb(255, 255, 255);
}
</style>