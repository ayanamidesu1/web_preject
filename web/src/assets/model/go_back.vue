<template>
    <div class="go_back">
      <div class="btn_box" @click="go_back" ref="btn_box">
        <img class="icon" src="https://www.sunyuanling.com/assets/left.svg">
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, nextTick } from 'vue';
  import { useStore } from 'vuex';
  
  const store = useStore();
  const btn_box = ref(null);
  
  function go_back() {
    store.dispatch('goBack').then(() => {
      nextTick(() => {
        if (btn_box.value) {
          btn_box.value.click();
        } else {
          // eslint-disable-next-line no-unused-vars
          let a=null;
        }
      });
    });
  }
  </script>
  
  <style scoped>
  .go_back {
    display: flex;
    width: 40px;
    height: 40px;
    padding: 5px;
    position: fixed;
    top: 80px;
    left: 10px;
    background-color: rgba(133, 133, 133, 1);
    border-radius: 50%;
    opacity: 0.6;
    z-index: 15;
  }
  .go_back:hover {
    opacity: 1;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
  }
  .btn_box {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
  .btn_box:hover {
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    transition: all 0.3s;
  }
  .icon {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  </style>
  