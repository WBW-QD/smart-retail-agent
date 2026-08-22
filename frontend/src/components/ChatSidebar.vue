<template>
  <el-drawer v-model="visible" title="智能助手" direction="rtl" size="400px" :with-header="true">
    <div class="chat-container">
      <div ref="chatBody" class="chat-body">
        <div v-for="(msg, idx) in messages" :key="idx" :class="['msg', msg.role]">
          <div class="bubble">{{ msg.content }}</div>
        </div>
        <div v-if="loading" class="msg assistant">
          <div class="bubble typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
      <div class="chat-input">
        <el-input v-model="input" type="textarea" :rows="2" placeholder="输入问题，回车发送..." @keydown.enter.exact.prevent="send" />
        <el-button type="primary" :loading="loading" @click="send" style="margin-top:8px;width:100%">发送</el-button>
        <el-button text size="small" @click="clearChat" style="margin-top:4px">清空对话</el-button>
      </div>
    </div>
  </el-drawer>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { chat, getHistory, clearHistory as apiClear } from '../api'

const props = defineProps({ visible: Boolean })
const emit = defineEmits(['update:visible'])
const visible = ref(props.visible)
watch(() => props.visible, v => visible.value = v)
watch(visible, v => emit('update:visible', v))

const messages = ref([])
const input = ref('')
const loading = ref(false)
const chatBody = ref(null)

watch(() => props.visible, async (v) => {
  if (v && messages.value.length === 0) {
    try {
      const history = await getHistory()
      if (history.length > 0) messages.value = history
    } catch (e) {}
  }
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

const clearChat = async () => {
  await apiClear()
  messages.value = []
  ElMessage.success('对话已清空')
}
</script>

<style scoped>
.chat-container { display: flex; flex-direction: column; height: calc(100vh - 60px); }
.chat-body { flex: 1; overflow-y: auto; padding: 16px; background: #f9fafb; }
.msg { margin-bottom: 16px; display: flex; }
.msg.user { justify-content: flex-end; }
.bubble { max-width: 80%; padding: 10px 14px; border-radius: 12px; line-height: 1.5; font-size: 14px; white-space: pre-wrap; word-break: break-word; }
.msg.user .bubble { background: #409EFF; color: #fff; border-bottom-right-radius: 4px; }
.msg.assistant .bubble { background: #fff; color: #1f2937; border: 1px solid #e5e7eb; border-bottom-left-radius: 4px; }
.typing { display: flex; gap: 4px; align-items: center; }
.typing span { width: 6px; height: 6px; background: #9ca3af; border-radius: 50%; animation: bounce 1.4s infinite; }
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-6px); } }
.chat-input { padding: 12px; border-top: 1px solid #e5e7eb; background: #fff; }
</style>
