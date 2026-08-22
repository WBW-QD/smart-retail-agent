<template>
  <div>
    <el-card shadow="hover" style="margin-bottom:16px">
      <div class="selector">
        <span style="margin-right:12px;font-weight:600">选择顾客：</span>
        <el-select v-model="selectedCustomer" placeholder="请选择顾客" style="width:240px" @change="onCustomerChange">
          <el-option v-for="c in customers" :key="c.id" :label="`${c.name} (消费¥${c.total_spent})`" :value="c.id" />
        </el-select>
        <el-button type="primary" :loading="loading" @click="generateRec" style="margin-left:12px">生成推荐</el-button>
      </div>
    </el-card>

    <el-row :gutter="16">
      <el-col :span="10">
        <el-card shadow="hover" v-if="profile">
          <template #header><span style="font-weight:600">顾客画像</span></template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="姓名">{{ profile.name }}</el-descriptions-item>
            <el-descriptions-item label="总消费">¥{{ profile.total_spent }}</el-descriptions-item>
            <el-descriptions-item label="订单数">{{ profile.order_count }}</el-descriptions-item>
            <el-descriptions-item label="客单价">¥{{ profile.avg_order }}</el-descriptions-item>
            <el-descriptions-item label="偏好品类">{{ profile.preferred_category }}</el-descriptions-item>
            <el-descriptions-item label="最近购买">{{ profile.last_purchase }}</el-descriptions-item>
            <el-descriptions-item label="标签">
              <el-tag v-for="t in profile.tags" :key="t" style="margin-right:4px">{{ t }}</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :span="14">
        <el-card shadow="hover">
          <template #header><span style="font-weight:600">AI 推荐结果</span></template>
          <div v-if="loading" class="loading-tip">
            <el-icon class="is-loading" :size="32"><Loading /></el-icon>
            <span>Agent 正在分析顾客偏好并生成推荐...</span>
          </div>
          <div v-else-if="recommendation" class="rec-result">{{ recommendation }}</div>
          <el-empty v-else description="选择顾客后点击生成推荐" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import { getCustomers, getCustomerProfile, getRecommendation } from '../api'

const customers = ref([])
const selectedCustomer = ref(null)
const profile = ref(null)
const recommendation = ref('')
const loading = ref(false)

onMounted(async () => {
  customers.value = await getCustomers()
})

const onCustomerChange = async (id) => {
  profile.value = await getCustomerProfile(id)
  recommendation.value = ''
}

const generateRec = async () => {
  if (!selectedCustomer.value) return
  loading.value = true
  try {
    const res = await getRecommendation(selectedCustomer.value)
    recommendation.value = res.recommendation
  } catch (e) {
    recommendation.value = '推荐生成失败，请检查后端服务'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.selector { display: flex; align-items: center; }
.loading-tip { display: flex; flex-direction: column; align-items: center; gap: 12px; color: #9ca3af; padding: 40px 0; }
.rec-result { white-space: pre-wrap; line-height: 1.8; font-size: 14px; color: #1f2937; }
</style>
