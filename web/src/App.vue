<template>
  <router-view></router-view>
  <!-- <root></root> -->
</template>

<script>
import Root from './components/root.vue'; // 注意组件名通常首字母大写  

export default {
  components: {
    Root // 注册组件  
  }
}
</script>

<style scoped></style>