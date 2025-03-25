<template>
    <div v-if="visible" class="message-box" :style="boxStyle">
      {{ message }}
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted, defineProps } from 'vue';
  
  const props = defineProps({
    message: {
      type: String,
      default: ''
    },
    mouse_position: {
      type: Object,
      default: () => ({ x: 0, y: 0 })
    }
  });
  
  const visible = ref(false);
  const boxStyle = ref({});
  
  // Track the timeout ID to clear existing animations
  let animationTimeout = null;
  
  const startAnimation = () => {
    // Clear any previous animations
    if (animationTimeout) {
      clearTimeout(animationTimeout);
    }
  
    // Show the message box and set initial styles
    visible.value = true;
    boxStyle.value = {
      position: 'fixed',
      left: `${props.mouse_position.x}px`,
      top: `${props.mouse_position.y}px`,
      zIndex: 100,
      opacity: 1,
      transition: 'top 1.5s linear, opacity 1.5s linear'
    };
  
    // Start the animation to move and fade out the message box
    setTimeout(() => {
      boxStyle.value = {
        ...boxStyle.value,
        top: `${props.mouse_position.y - 30}px`,
        opacity: 0
      };
    }, 0);
  
    // Hide the message box after the animation duration
    animationTimeout = setTimeout(() => {
      visible.value = false;
    }, 1500);
  };
  
  onMounted(() => {
    // Watch for message changes to start animation
    watch(() => props.message, (newValue) => {
      if (newValue) {
        startAnimation();
      }
    });
  });
  </script>
  
  <style scoped>
  .message-box {
    color: rgba(0, 150, 250, 1);
    padding: 10px;
    border-radius: 5px;
    white-space: nowrap;
  }
  </style>
  