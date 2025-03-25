<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="index" @scroll="handleScroll">
      <component :is="work_typeComponent" :work_info="work_list" />
      <div v-if="loading">加载中...</div>
    </div>
  </template>
  
  <script setup>
  import { defineProps, ref, onMounted, onUnmounted, computed } from 'vue'
  import { get_recommend } from './js/get_recommend'
  import ill_recommend from './ill_recommend.vue'
  import comic_recommend from './comic_recommend.vue'
  import novel_recommend from './novel_recommend.vue'
  
  const props = defineProps({
    token: String,
    work_type: String
  })
  
  let work_list = ref([])
  let work_offset = ref(0)
  let work_limit = ref(20)
  let loading = ref(false)
  
  const work_typeComponent = computed(() => {
    switch (props.work_type) {
      case 'ill': return ill_recommend
      case 'comic': return comic_recommend
      case 'novel': return novel_recommend
      default: return null
    }
  })
  
  const loadMore = async () => {
    if (loading.value) return
    loading.value = true
  
    const new_works = await get_recommend(props.token, props.work_type, work_offset.value, work_limit.value)
    work_list.value = [...work_list.value, ...new_works]
    work_offset.value += work_limit.value
    loading.value = false
  }
  
  const handleScroll = () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop
    const clientHeight = window.innerHeight || document.documentElement.clientHeight
    const scrollHeight = document.documentElement.scrollHeight
  
    if (scrollTop + clientHeight >= scrollHeight - 200) {
      loadMore()
    }
  }
  
  onMounted(() => {
    window.addEventListener('scroll', handleScroll)
    loadMore()
  })
  
  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })
  </script>
  
  <style scoped>
  .index {
    width: 100%;
    height: auto;
    overflow-y: auto;
    overflow-x: hidden;
  }
  </style>
  