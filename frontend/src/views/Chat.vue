<template>
  <div class="chat-page">
    <el-card shadow="hover" class="chat-card">
      <template #header>
        <div class="chat-header">
          <span style="font-weight:600">智能对话 - 零售营运助手</span>
          <el-button type="danger" size="small" text @click="clearAll">清空对话</el-button>
        </div>
      </template>
      <div ref="chatBody" class="chat-body">
        <div v-for="(msg, idx) in messages" :key="idx" :class="['msg', msg.role]">
          <div class="avatar">{{ msg.role === 'user' ? '我' : 'AI' }}</div>
          <div class="bubble">{{ msg.content }}</div>
        </div>
        <div v-if="loading" class="msg assistant">
          <div class="avatar">AI</div>
          <div class="bubble typing"><span></span><span></span><span></span></div>
        </div>
      </div>
      <div class="chat-input-area">
        <el-input v-model="input" type="textarea" :rows="3" placeholder="向零售营运助手提问，例如：如何提升复购率？库存周转率怎么优化？" @keydown.enter.exact.prevent="send" />
        <div class="input-actions">
          <span class="hint">回车发送，Shift+回车换行</span>
          <el-button type="primary" :loading="loading" @click="send">发送</el-button>
        </div>
      </div>
    </el-card>

    <el-card shadow="hover" class="quick-card">
      <template #header><span style="font-weight:600">快捷提问</span></template>
      <div class="quick-list">
        <el-button v-for="q in quickQuestions" :key="q" @click="quickAsk(q)" class="quick-btn">{{ q }}</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { chat, getHistory, clearHistory } from '../api'

const messages = ref([])
const input = ref('')
const loading = ref(false)
const chatBody = ref(null)

const quickQuestions = [
  '如何提升顾客复购率？',
  '库存周转率低怎么优化？',
  '生鲜品类损耗大怎么办？',
  '会员体系应该怎么设计？',
  '淡季如何提升销售额？'
]

onMounted(async () => {
  try {
    const history = await getHistory()
    messages.value = history
    scrollBottom()
  } catch (e) {}
})

const scrollBottom = () => nextTick(() => {
  if (chatBody.value) chatBody.value.scrollTop = chatBody.value.scrollHeight
})

const send = async () => {
  if (!input.value.trim() || loading.value) return
  const text = input.value.trim()
  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true
  scrollBottom()
  try {
    const res = await chat(text)
    messages.value.push({ role: 'assistant', content: res.reply })
  } catch (e) {
    ElMessage.error('发送失败，请检查后端服务')
  } finally {
    loading.value = false
    scrollBottom()
  }
}

const quickAsk = (q) => {
  input.value = q
  send()
}

const clearAll = async () => {
  await clearHistory()
  messages.value = []
  ElMessage.success('对话已清空')
}
</script>

<style scoped>
.chat-page { display: flex; gap: 16px; height: calc(100vh - 120px); }
.chat-card { flex: 1; display: flex; flex-direction: column; }
.chat-card :deep(.el-card__body) { flex: 1; display: flex; flex-direction: column; padding: 0; overflow: hidden; }
.chat-header { display: flex; justify-content: space-between; align-items: center; }
.chat-body { flex: 1; overflow-y: auto; padding: 20px; background: #f9fafb; }
.msg { display: flex; gap: 10px; margin-bottom: 20px; }
.msg.user { flex-direction: row-reverse; }
.avatar { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: bold; flex-shrink: 0; }
.msg.user .avatar { background: #409EFF; color: #fff; }
.msg.assistant .avatar { background: #10b981; color: #fff; }
.bubble { max-width: 70%; padding: 12px 16px; border-radius: 12px; line-height: 1.6; font-size: 14px; white-space: pre-wrap; word-break: break-word; }
.msg.user .bubble { background: #409EFF; color: #fff; border-bottom-right-radius: 4px; }
.msg.assistant .bubble { background: #fff; color: #1f2937; border: 1px solid #e5e7eb; border-bottom-left-radius: 4px; }
.typing { display: flex; gap: 4px; align-items: center; }
.typing span { width: 6px; height: 6px; background: #9ca3af; border-radius: 50%; animation: bounce 1.4s infinite; }
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-6px); } }
.chat-input-area { padding: 16px; border-top: 1px solid #e5e7eb; background: #fff; }
.input-actions { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; }
.hint { color: #9ca3af; font-size: 12px; }
.quick-card { width: 260px; }
.quick-list { display: flex; flex-direction: column; gap: 8px; }
.quick-btn { width: 100%; justify-content: flex-start; }
</style>
