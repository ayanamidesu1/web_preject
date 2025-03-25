<template>
    <div class="select_box" @click="onSelectBoxClick">
      <div class="select" @click="toggleSelect">
        <span class="select_title">{{ select_title }}</span>
        <img class="drop_down" :src="drop_down_icon_path" v-if="!show_select_list">
        <img class="drop_down" :src="drop_up_icon_path" v-else>
      </div>
      <transition name="select-list" @after-enter="afterEnter" @after-leave="afterLeave">
        <div class="select_list" v-if="show_select_list">
          <div class="select_item" v-for="(item, index) in select_list" :key="index" @click="selectItem(item, $event)">
            <span class="select_item_text">{{ item }}</span>
            <img v-if="selected_item === item" class="select_item_check" :src="select_item_check">
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  // Import necessary Vue composition API functions
  import { ref, onUnmounted, onMounted, defineEmits, defineProps, watch } from 'vue';
  
  // Define props with corrected spelling and appropriate default values
  const props = defineProps({
    select_title: {
      type: String,
      default: '新建系列'
    },
    select_list: {
      type: Array,
      default: () => ['新建系列']
    },
    drop_down_icon_path: {
      type: String,
      default: 'https://www.sunyuanling.com/assets/drop_down.svg'
    },
    drop_up_icon_path: {
      type: String,
      default: 'https://www.sunyuanling.com/assets/drop_up.svg'
    },
    select_item_check: {
      type: String,
      default: 'https://www.sunyuanling.com/assets/correct.svg'
    }
  });
  
  // Initialize reactive variables
  const drop_down_icon_path = ref(props.drop_down_icon_path);
  const drop_up_icon_path = ref(props.drop_up_icon_path);
  const select_title = ref(props.select_title);
  const select_list = ref(props.select_list);
  const select_item_check = ref(props.select_item_check);
  const show_select_list = ref(false);
  const selected_item = ref(null);
  const isInsideClick = ref(false);
  
  // Define emits
  const emit = defineEmits(['select-item']);
  
  // Function to emit the selected item
  function put_select_item(item) {
    emit('select-item', item);
  }
  
  // Watch for changes in selected_item to emit the selected item
  watch(selected_item, (newVal) => {
    if (newVal) {
      put_select_item(newVal);
    }
  });
  
  // Watch for changes in props and update corresponding reactive variables
  watch(
    () => props.select_title,
    (newVal) => {
      select_title.value = newVal;
    }
  );
  
  watch(
    () => props.select_list,
    (newVal) => {
      select_list.value = newVal;
    }
  );
  
  watch(
    () => props.drop_down_icon_path,
    (newVal) => {
      drop_down_icon_path.value = newVal;
    }
  );
  
  watch(
    () => props.drop_up_icon_path,
    (newVal) => {
      drop_up_icon_path.value = newVal;
    }
  );
  
  watch(
    () => props.select_item_check,
    (newVal) => {
      select_item_check.value = newVal;
    }
  );
  
  // Function to toggle the display of the select list
  function toggleSelect() {
    show_select_list.value = !show_select_list.value;
  }
  
  // Function to select an item from the list
  function selectItem(item, event) {
    event.stopPropagation();
    selected_item.value = item;
    select_title.value = item;
    show_select_list.value = false;
  }
  
  // Function to handle click events inside the select box
  function onSelectBoxClick() {
    isInsideClick.value = true;
  }
  
  // Function to handle click events outside the select box
  function handleClickOutside(event) {
    if (!isInsideClick.value) {
      show_select_list.value = false;
    }
    isInsideClick.value = false;
  }
  
  // Add event listener for clicks outside the select box
  document.addEventListener('click', handleClickOutside);
  
  // Remove event listener on component unmount
  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
  });
  
  // Fix transition classes issue after enter and leave
  function afterEnter(el) {
    el.style.maxHeight = 'none';
    el.style.opacity = '1';
  }
  
  function afterLeave(el) {
    el.style.maxHeight = '0';
    el.style.opacity = '0';
  }
  
  // Watch for props on mounted and update the reactive variables
  onMounted(() => {
    drop_down_icon_path.value = props.drop_down_icon_path;
    drop_up_icon_path.value = props.drop_up_icon_path;
    select_title.value = props.select_title;
    select_list.value = props.select_list;
    select_item_check.value = props.select_item_check;
  });
  </script>
  <script>
  export default {
    name:"rewrite_select"
  }
</script>
  
  <style scoped>
  .select_box {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    background-color: #dadada;
    border-radius: 5px;
    position: relative;
    padding: 1px;
  }
  .select {
    width: 100%;
    height: 100%;
    background-color: #d1d1d1;
    min-height: 30px;
    min-width: 10px;
    justify-content: center;
    align-items: center;
    display: flex;
    font-size: 14px;
    position: relative;
    cursor: pointer;
    border-radius:5px 5px 0px 0px;
  }
  .select:hover {
    background-color: rgba(133, 133, 133, 0.3);
    transition: all 0.2s ease-in-out;
  }
  .drop_down {
    position: absolute;
    right: 2px;
    top: 50%;
    transform: translateY(-50%);
    width: auto;
    height: 100%;
  }
  .select_title {
    color: #000;
  }
  .select_list {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease, opacity 0.3s ease;
    opacity: 0;
    border-top: 1px solid #555;
    background-color: #fff;
    position: absolute;
    left: 0px;
    top: 100%;
    border-radius: 0px 0px 5px 5px ;
  }
  .select_item {
    display: flex;
    position: relative;
    align-items: center;
    height: auto;
    width: auto;
    border-bottom: 1px solid #555;
    cursor: pointer;
    background-color: rgba(211,211,211,1);
    padding: 5px 10px;
    flex: 1;
  }
  .select_item:hover {
    background-color: rgba(133, 133, 133, 0.3);
    transition: all 0.2s ease-in-out;
  }
  .select_item_text {
    color: #000;
    text-align: center;
  }
  .select_item_check {
    position: absolute;
    right: 2px;
    top: 50%;
    transform: translateY(-50%);
    width: auto;
    height: 100%;
  }
  
  /* Transition classes */
  .select-list-enter-active,
  .select-list-leave-active {
    transition: max-height 0.3s ease-in-out, opacity 0.3s ease-in-out;
  }
  .select-list-enter-from,
  .select-list-leave-to {
    max-height: 0;
    opacity: 0;
  }
  .select-list-enter-to,
  .select-list-leave-from {
    max-height: 200px;
    opacity: 1;
  }
  </style>
  