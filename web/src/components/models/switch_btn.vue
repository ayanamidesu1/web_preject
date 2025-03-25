<template>
  <div class="toggle-container" @click="toggle">
    <div class="toggle-switch" :class="{ on: isOn }">
      <div class="toggle-circle"></div>
    </div>
  </div>
</template>

<script setup>
import { ref,defineEmits } from 'vue';

const isOn = ref(false);
let emit=defineEmits(['change_status'])
function change_status()
{
    emit('change_status',isOn.value)
}
const toggle = () => {
  isOn.value = !isOn.value;
  change_status();
};
</script>

<style scoped>
.toggle-container {
  width: 60px;
  height: 27.5px;
  border-radius: 12.5px;
  background-color: #ccc;
  position: relative;
  cursor: pointer;
  transition: background-color 0.3s;
}

.toggle-switch {
  width: 100%;
  height: 100%;
  border-radius: 12.5px;
  position: relative;
  transition: background-color 0.3s;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.toggle-switch::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 27.5px;
  background-color: rgba(0, 150, 250, 1);
  transition: width 0.3s;
  border-radius: 0px 50% 50% 0px;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
}

.toggle-switch.on::before {
  width: 120%;
}

.toggle-circle {
  width: 22.5px;
  height: 22.5px;
  border-radius: 50%;
  background-color: #fff;
  position: absolute;
  left: 2px;
  transition: left 0.3s;
  z-index: 1;
}

.toggle-switch.on .toggle-circle {
  left: 35px;
}
.toggle-switch.on{
  box-shadow: 0px 0px 5px 2px rgba(0,150,250,0.8);
}
</style>
