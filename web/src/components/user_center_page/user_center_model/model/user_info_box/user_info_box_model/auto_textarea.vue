<script setup>
import { ref, watch, onMounted, defineEmits, defineProps } from 'vue';

const emit = defineEmits(['update:modelValue']);
const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  maxlength: {
    type: Number,
    default: 3000
  },
  rows: {
    type: Number,
    default: 4
  },
  placeholder: {
    type: String,
    default: '自动文本框'
  },
  initialWidth: {
    type: String,
    default: '100%'
  },
  initialHeight: {
    type: String,
    default: 'auto'
  },
  allowResizeWidth: {
    type: Boolean,
    default: false
  },
  allowResizeHeight: {
    type: Boolean,
    default: true
  },
  fontsize: {
    type: Number,
    default: 16
  },
  lineheight: {
    type: Number,
    default: 1.5
  }
});

const textarea = ref(null);
const internalValue = ref(props.modelValue);

const adjustHeight = () => {
  if (textarea.value) {
    textarea.value.style.height = 'auto';
    textarea.value.style.height = `${textarea.value.scrollHeight}px`;
  }
};

watch(
  () => props.modelValue,
  (newValue) => {
    internalValue.value = newValue;
    adjustHeight();
  }
);

watch(
  () => internalValue.value,
  (newValue) => {
    emit('update:modelValue', newValue);
    adjustHeight();
  }
);

onMounted(() => {
  adjustHeight();
});
</script>

<template>
  <textarea
    ref="textarea"
    :maxlength="maxlength"
    :rows="rows"
    :placeholder="placeholder"
    :style="{ width: initialWidth, height: initialHeight, resize: (allowResizeWidth && allowResizeHeight) ? 'both' : (allowResizeHeight ? 'vertical' : 'none'), fontSize: fontsize + 'px', lineHeight: lineheight }"
    v-model="internalValue"
    @input="adjustHeight"
  ></textarea>
</template>

<style scoped>
textarea {
  width: 100%;
  border: none;
  outline: none;
  box-sizing: border-box;
  padding: 8px;
  border-radius: 5px;
  min-height: 30px;
  background-color: rgba(133,133,133,0.2);
}
</style>
