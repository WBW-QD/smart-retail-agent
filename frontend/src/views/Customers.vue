<template>
  <div>
    <el-card shadow="hover" style="margin-bottom:16px">
      <el-table :data="customers" stripe @row-click="selectCustomer" highlight-current-row>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="total_spent" label="总消费" width="120">
          <template #default="{ row }">¥{{ row.total_spent }}</template>
        </el-table-column>
        <el-table-column prop="order_count" label="订单数" width="90" />
        <el-table-column prop="preferred_category" label="偏好品类" width="120" />
        <el-table-column prop="tags" label="标签">
          <template #default="{ row }">
            <el-tag v-for="t in row.tags.split(',')" :key="t" size="small" style="margin-right:4px">{{ t }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-row :gutter="16" v-if="selected">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header><span style="font-weight:600">顾客详情 - {{ selected.name }}</span></template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="电话">{{ profile.phone }}</el-descriptions-item>
            <el-descriptions-item label="总消费">¥{{ profile.total_spent }}</el-descriptions-item>
            <el-descriptions-item label="订单数">{{ profile.order_count }}</el-descriptions-item>
            <el-descriptions-item label="客单价">¥{{ profile.avg_order }}</el-descriptions-item>
            <el-descriptions-item label="偏好品类">{{ profile.preferred_category }}</el-descriptions-item>
            <el-descriptions-item label="最近购买">{{ profile.last_purchase }}</el-descriptions-item>
          </el-descriptions>
          <div style="margin-top:16px">
            <div style="margin-bottom:8px;font-weight:600">历史订单</div>
            <el-table :data="profile.order_history" size="small" stripe>
              <el-table-column prop="date" label="日期" />
              <el-table-column prop="product_id" label="商品ID" width="80" />
              <el-table-column prop="quantity" label="数量" width="80" />
              <el-table-column prop="amount" label="金额">
                <template #default="{ row }">¥{{ row.amount }}</template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header><span style="font-weight:600">AI 营销文案生成</span></template>
          <div style="margin-bottom:12px">
            <el-radio-group v-model="activityType">
              <el-radio-button label="会员促销">会员促销</el-radio-button>
              <el-radio-button label="新品推荐">新品推荐</el-radio-button>
              <el-radio-button label="生日祝福">生日祝福</el-radio-button>
              <el-radio-button label="召回唤醒">召回唤醒</el-radio-button>
            </el-radio-group>
          </div>
          <el-button type="primary" :loading="marketingLoading" @click="generateMarketing" style="margin-bottom:12px">生成文案</el-button>
          <div v-if="marketingText" class="marketing-box">
            <div class="marketing-text">{{ marketingText }}</div>
            <el-button type="success" size="small" @click="copyText">一键复制</el-button>
          </div>
          <el-empty v-else description="选择顾客后生成营销文案" :image-size="80" />
        </el-card>
      </el-col>
    </el-row>
    <el-empty v-else description="点击上方表格选择顾客" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getCustomers, getCustomerProfile, getMarketing } from '../api'

const customers = ref([])
const selected = ref(null)
const profile = ref({ order_history: [] })
const activityType = ref('会员促销')
const marketingText = ref('')
const marketingLoading = ref(false)

onMounted(async () => {
  customers.value = await getCustomers()
})

const selectCustomer = async (row) => {
  selected.value = row
  profile.value = await getCustomerProfile(row.id)
  marketingText.value = ''
}

const generateMarketing = async () => {
  if (!selected.value) return
  marketingLoading.value = true
  try {
    const res = await getMarketing(selected.value.id, activityType.value)
    marketingText.value = res.marketing_text
  } catch (e) {
    marketingText.value = '生成失败'
  } finally {
    marketingLoading.value = false
  }
}

const copyText = () => {
  navigator.clipboard.writeText(marketingText.value)
  ElMessage.success('已复制到剪贴板')
}
</script>

<style scoped>
.marketing-box { background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 16px; }
.marketing-text { white-space: pre-wrap; line-height: 1.6; margin-bottom: 12px; color: #0c4a6e; }
</style>
