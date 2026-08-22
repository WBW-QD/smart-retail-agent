<template>
  <div>
    <el-card shadow="hover" style="margin-bottom:16px">
      <div class="summary">
        <el-tag type="danger" size="large">低库存预警：{{ lowStockCount }} 件</el-tag>
        <el-tag type="success" size="large">商品总数：{{ inventory.length }} 件</el-tag>
      </div>
    </el-card>

    <el-card shadow="hover">
      <el-table :data="inventory" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="商品名称" min-width="180" />
        <el-table-column prop="category" label="品类" width="120" />
        <el-table-column prop="price" label="价格" width="100">
          <template #default="{ row }">¥{{ row.price }}</template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="100">
          <template #default="{ row }">
            <span :style="{ color: row.low_stock ? '#ef4444' : '#1f2937', fontWeight: row.low_stock ? 'bold' : 'normal' }">{{ row.stock }}</span>
            <el-tag v-if="row.low_stock" type="danger" size="small" style="margin-left:6px">预警</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sales_30d" label="近30天销量" width="120" />
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" :loading="restockId === row.id" @click="getRestock(row)">补货建议</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" title="AI 补货建议" width="500px">
      <div v-if="restockResult">
        <el-alert :title="restockResult.product" type="info" :closable="false" show-icon style="margin-bottom:16px" />
        <div class="suggestion-box">{{ restockResult.suggestion }}</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getInventory, getRestockSuggestion } from '../api'

const inventory = ref([])
const restockId = ref(null)
const dialogVisible = ref(false)
const restockResult = ref(null)

const lowStockCount = computed(() => inventory.value.filter(i => i.low_stock).length)

onMounted(async () => {
  inventory.value = await getInventory()
})

const getRestock = async (row) => {
  restockId.value = row.id
  try {
    const res = await getRestockSuggestion(row.id)
    restockResult.value = res
    dialogVisible.value = true
  } catch (e) {
    restockResult.value = { product: row.name, suggestion: '获取建议失败' }
    dialogVisible.value = true
  } finally {
    restockId.value = null
  }
}
</script>

<style scoped>
.summary { display: flex; gap: 16px; }
.suggestion-box { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 16px; white-space: pre-wrap; line-height: 1.7; color: #14532d; }
</style>
