<template>
  <div>
    <el-row :gutter="16" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-label">总销售额</div>
          <div class="stat-value">¥{{ stats.total_sales?.toFixed(2) || '0.00' }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-label">订单总数</div>
          <div class="stat-value">{{ stats.total_orders || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-label">客单价</div>
          <div class="stat-value">¥{{ stats.avg_order?.toFixed(2) || '0.00' }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-label">热销品类数</div>
          <div class="stat-value">{{ stats.top_categories?.length || 0 }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top:16px">
      <el-col :span="14">
        <el-card shadow="hover">
          <template #header><span style="font-weight:600">销售趋势</span></template>
          <div ref="trendChart" style="height:300px"></div>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover">
          <template #header><span style="font-weight:600">热销品类 TOP5</span></template>
          <div ref="categoryChart" style="height:300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="hover" style="margin-top:16px">
      <template #header><span style="font-weight:600">智能数据分析</span></template>
      <div class="query-box">
        <el-input v-model="question" placeholder="例如：上周哪个品类卖得最好？" @keyup.enter="askQuery" />
        <el-button type="primary" :loading="queryLoading" @click="askQuery" style="margin-left:8px">提问</el-button>
      </div>
      <div v-if="queryAnswer" class="query-answer">
        <el-alert type="info" :closable="false" show-icon>
          <template #title>{{ queryAnswer }}</template>
        </el-alert>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getDashboardSales, queryDashboard } from '../api'

const stats = ref({})
const trendChart = ref(null)
const categoryChart = ref(null)
const question = ref('')
const queryAnswer = ref('')
const queryLoading = ref(false)
let trendInst = null, categoryInst = null

const loadData = async () => {
  const data = await getDashboardSales()
  stats.value = data
  await nextTick()
  renderTrend(data.date_trend || [])
  renderCategory(data.top_categories || [])
}

const renderTrend = (data) => {
  if (!trendChart.value) return
  trendInst = echarts.init(trendChart.value)
  trendInst.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 20, top: 20, bottom: 30 },
    xAxis: { type: 'category', data: data.map(d => d.date), axisLabel: { fontSize: 11 } },
    yAxis: { type: 'value', name: '销售额(元)' },
    series: [{ data: data.map(d => d.value), type: 'line', smooth: true, areaStyle: { color: 'rgba(64,158,255,0.2)' }, lineStyle: { color: '#409EFF' }, itemStyle: { color: '#409EFF' } }]
  })
}

const renderCategory = (data) => {
  if (!categoryChart.value) return
  categoryInst = echarts.init(categoryChart.value)
  categoryInst.setOption({
    tooltip: { trigger: 'item' },
    series: [{ type: 'pie', radius: ['40%', '70%'], data: data, label: { formatter: '{b}: ¥{c}' } }]
  })
}

const askQuery = async () => {
  if (!question.value.trim()) return
  queryLoading.value = true
  try {
    const res = await queryDashboard(question.value)
    queryAnswer.value = res.answer
  } catch (e) {
    queryAnswer.value = '查询失败，请检查后端服务'
  } finally {
    queryLoading.value = false
  }
}

onMounted(() => {
  loadData()
  window.addEventListener('resize', () => {
    trendInst?.resize()
    categoryInst?.resize()
  })
})
</script>

<style scoped>
.stat-cards .stat-card { text-align: center; }
.stat-label { color: #6b7280; font-size: 14px; margin-bottom: 8px; }
.stat-value { font-size: 28px; font-weight: 700; color: #1f2937; }
.query-box { display: flex; margin-bottom: 16px; }
.query-answer { margin-top: 8px; white-space: pre-wrap; line-height: 1.6; }
</style>
