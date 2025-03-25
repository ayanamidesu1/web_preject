<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import { ref,defineProps } from 'vue'
import index from './model/index.vue';
import go_back from '../../go_back.vue'

const props=defineProps({
  token:{
    default:'sunyuanling'
  },
})

</script>

<template>
<div class="root">
  <h1>作品数据分析</h1>
  <index :token="props.token"></index>
  <go_back></go_back>
</div>
</template>

<style scoped>

</style>
