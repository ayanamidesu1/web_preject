<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="recommend">
    <recommend :token="token" :work_type="work_type"></recommend>
  </div>
</template>

<script setup>
import recommend from '@/assets/model/recommend_page/modle/index.vue'
import { defineProps } from 'vue';

const props=defineProps({
    token:{
        type:String,
        default:''
    },
    work_type:{
        type:String,
        default:''
    }
})
</script>

<style scoped>
  
</style>