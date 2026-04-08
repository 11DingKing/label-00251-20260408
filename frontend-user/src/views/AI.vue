<template>
  <div class="h-[calc(100vh-8rem)] flex flex-col">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center">
          <i class="fas fa-robot text-blue-400 text-xl"></i>
        </div>
        <div>
          <h1 class="text-2xl font-bold">AI 助手</h1>
          <p class="text-dark-400">智能游戏开发顾问</p>
        </div>
      </div>
      <div v-if="!aiEnabled" class="px-4 py-2 bg-amber-500/20 text-amber-400 rounded-xl text-sm flex items-center space-x-2">
        <i class="fas fa-exclamation-triangle"></i>
        <span>未配置</span>
      </div>
    </div>
    
    <!-- Chat Container -->
    <div v-if="aiEnabled" class="flex-1 card flex flex-col overflow-hidden">
      <!-- Messages -->
      <div ref="chatEl" class="flex-1 overflow-y-auto p-4 space-y-4">
        <!-- Welcome Message -->
        <div class="flex items-start space-x-3">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-500 rounded-xl flex items-center justify-center flex-shrink-0">
            <i class="fas fa-robot text-white"></i>
          </div>
          <div class="bg-dark-800/50 rounded-2xl rounded-tl-md px-4 py-3 max-w-[80%]">
            <p class="text-dark-200">你好！我是游戏开发助手，可以帮你：</p>
            <ul class="mt-2 space-y-1 text-dark-400 text-sm">
              <li>💡 头脑风暴游戏创意</li>
              <li>🎮 讨论游戏机制设计</li>
              <li>🔧 提供技术实现建议</li>
              <li>📊 分析设计方案优缺点</li>
            </ul>
          </div>
        </div>
        
        <!-- Chat History -->
        <div v-for="(msg, i) in chatHistory" :key="i" 
          :class="['flex items-start space-x-3', msg.role === 'user' ? 'flex-row-reverse space-x-reverse' : '']">
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0',
            msg.role === 'user' ? 'bg-gradient-to-br from-cyan-500 to-blue-500 rounded-full' : 'bg-gradient-to-br from-blue-500 to-blue-500']">
            <i v-if="msg.role === 'assistant'" class="fas fa-robot text-white"></i>
            <span v-else class="font-bold text-white">{{ auth.user?.username?.[0]?.toUpperCase() }}</span>
          </div>
          <div :class="['rounded-2xl px-4 py-3 max-w-[80%]',
            msg.role === 'user' ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-tr-md' : 'bg-dark-800/50 text-dark-200 rounded-tl-md']">
            <p class="whitespace-pre-wrap break-words">{{ msg.content }}</p>
          </div>
        </div>
        
        <!-- Loading -->
        <div v-if="loading" class="flex items-start space-x-3">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-500 rounded-xl flex items-center justify-center">
            <i class="fas fa-robot text-white"></i>
          </div>
          <div class="bg-dark-800/50 rounded-2xl rounded-tl-md px-4 py-3">
            <div class="flex items-center space-x-2">
              <div class="flex space-x-1">
                <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
                <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
                <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
              </div>
              <span class="text-dark-400 text-sm">思考中...</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Quick Prompts -->
      <div class="px-4 py-3 border-t border-dark-700/50 flex gap-2 overflow-x-auto">
        <button v-for="prompt in quickPrompts" :key="prompt.text" @click="quickPrompt(prompt.text)"
          class="flex items-center space-x-2 px-4 py-2 bg-dark-800/50 hover:bg-dark-700/50 rounded-xl text-sm whitespace-nowrap transition-all duration-200 hover:scale-105 border border-dark-700 hover:border-dark-600">
          <i :class="[prompt.icon, 'text-blue-400']"></i>
          <span>{{ prompt.label }}</span>
        </button>
      </div>
      
      <!-- Input -->
      <div class="p-4 border-t border-dark-700/50">
        <form @submit.prevent="sendMessage" class="flex gap-3">
          <input v-model="message" placeholder="输入你的问题..." autocomplete="off" 
            class="input-modern flex-1" :disabled="loading">
          <button type="submit" :disabled="loading || !message.trim()"
            class="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-500 rounded-xl font-medium transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed">
            <i :class="loading ? 'fas fa-spinner fa-spin' : 'fas fa-paper-plane'"></i>
          </button>
        </form>
      </div>
    </div>
    
    <!-- Not Configured State -->
    <div v-else class="flex-1 card flex items-center justify-center">
      <div class="text-center max-w-md">
        <div class="w-24 h-24 bg-dark-800 rounded-3xl flex items-center justify-center mx-auto mb-6">
          <i class="fas fa-robot text-dark-600 text-4xl"></i>
        </div>
        <h2 class="text-2xl font-bold mb-3">AI 助手未配置</h2>
        <p class="text-dark-400 mb-6">管理员需要配置 AI 服务 API 才能使用此功能</p>
        <router-link v-if="auth.isAdmin" to="/admin/ai" 
          class="btn-primary inline-flex items-center space-x-2">
          <i class="fas fa-cog"></i>
          <span>前往配置</span>
        </router-link>
        <p v-else class="text-dark-500 text-sm">请联系管理员开启此功能</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const auth = useAuthStore()
const aiEnabled = ref(false)
const message = ref('')
const chatHistory = ref([])
const loading = ref(false)
const chatEl = ref(null)

const quickPrompts = [
  { icon: 'fas fa-brain', label: '头脑风暴', text: '帮我想一些有趣的游戏机制' },
  { icon: 'fas fa-expand', label: '扩展想法', text: '帮我扩展这个想法' },
  { icon: 'fas fa-search', label: '设计分析', text: '帮我分析这个设计的优缺点' },
  { icon: 'fas fa-code', label: '技术建议', text: '这个功能应该如何实现？' }
]

onMounted(async () => {
  try {
    const { data } = await api.get('/ai/status')
    aiEnabled.value = data.enabled
  } catch (e) {
    aiEnabled.value = false
  }
})

function quickPrompt(text) {
  message.value = text
}

async function sendMessage() {
  if (!message.value.trim() || loading.value) return
  
  const userMsg = message.value
  chatHistory.value.push({ role: 'user', content: userMsg })
  message.value = ''
  loading.value = true
  
  nextTick(() => { 
    if (chatEl.value) chatEl.value.scrollTop = chatEl.value.scrollHeight 
  })
  
  try {
    const { data } = await api.post('/ai/chat', { 
      message: userMsg, 
      history: chatHistory.value.slice(0, -1) 
    })
    chatHistory.value.push({ role: 'assistant', content: data.response })
  } catch (e) {
    chatHistory.value.push({ 
      role: 'assistant', 
      content: '抱歉，出现了错误：' + (e.response?.data?.error || '请稍后重试') 
    })
  } finally {
    loading.value = false
    nextTick(() => { 
      if (chatEl.value) chatEl.value.scrollTop = chatEl.value.scrollHeight 
    })
  }
}
</script>
