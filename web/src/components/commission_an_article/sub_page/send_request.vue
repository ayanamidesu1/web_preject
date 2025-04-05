<template>
  <div class="send_request">
    <span>发送的约稿申请</span>
    <div class="menu_item">
        <span :class="{is_active:filter_type=='all'}" @click="filter_type='all'">全部</span>
        <span :class="{is_active:filter_type=='cancel'}" @click="filter_type='cancel'">已取消</span>
        <div class="filter_condition">
          <span>筛选</span>
          <select>
            <option>所有状态</option>
            <option>待处理</option>
            <option>已处理</option>
            <option>创作中</option>
            <option>已完成</option>
          </select>
          <span>排序</span>
          <select>
            <option>最新</option>
            <option>按金额从高到低排序</option>
            <option>按截稿日期从早到晚排序</option>
          </select>
        </div>
      </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
let filter_type=ref('all')
</script>

<style scoped>
.send_request{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.menu_item{
    display: flex;
    gap:10px;
    align-items: center;
  }
  .menu_item span{
    padding: 5px 10px;
    cursor: pointer;
    transition: all 0.2s;
  }
  .filter_condition{
    display: flex;
    gap:10px;
    align-items: center;
  }
  .is_active{
    background-color: rgb(228, 223, 223);
    border-radius: 5px;
  }
</style>