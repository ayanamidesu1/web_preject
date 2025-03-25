<template>
  <div>
    <h2>{{ draw_title }}</h2>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { defineComponent, ref, defineProps } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

const props = defineProps({
  work_title: {
    type: String,
    default: '全部作品的数据统计'
  },
  history_data: {
    type: Array,
    default: () => [114, 51, 41]
  },
  week_data: {
    type: Array,
    default: () => [191, 98, 20]
  }
})

console.log(props)
const draw_title = ref(props.work_title)

// 注册 Chart.js 组件和 datalabels 插件
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ChartDataLabels);

// 计算增加的数据，确保不出现负数
const calculateIncreasedData = () => {
  return props.week_data.map((value, index) => {
    const increase = value - props.history_data[index];
    return increase > 0 ? increase : 0;
  });
};

// 图表数据和选项
const chartData = ref({
  labels: ['浏览', '点赞', '收藏'],
  datasets: [
    {
      label: '一周之前的历史作品数据',
      backgroundColor: '#42A5F5',
      data: props.history_data
    },
    {
      label: '一周的作品数据',
      backgroundColor: '#FF6384',
      data: props.week_data
    },
    {
      label: '增加的数据',
      backgroundColor: '#FFCE56',
      data: calculateIncreasedData()
    }
  ]
});

const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    tooltip: {
      callbacks: {
        label: function (tooltipItem) {
          return tooltipItem.dataset.label + ': ' + tooltipItem.raw;
        }
      }
    },
    datalabels: {
      formatter: (value) => {
        return Math.round(value); // 强制格式化为整数
      },
      color: '#000', // 数据标签的颜色
      anchor: 'end', // 标签的位置
      align: 'top', // 标签对齐方式
      offset: 4, // 标签与柱状图的距离
    }
  }
});
</script>

<style scoped>
/* Add styles here */
</style>
