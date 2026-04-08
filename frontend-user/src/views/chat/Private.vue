<template>
  <div class="h-[calc(100vh-8rem)] flex flex-col">
    <!-- Header -->
    <div class="relative overflow-hidden rounded-t-2xl bg-gradient-to-r from-dark-800/90 via-dark-800/80 to-dark-800/90 backdrop-blur-xl border border-dark-700/50 border-b-0">
      <!-- Background decoration -->
      <div class="absolute inset-0 bg-gradient-to-r from-cyan-500/5 via-transparent to-blue-500/5"></div>
      <div class="absolute top-0 right-0 w-32 h-32 bg-cyan-500/10 rounded-full blur-3xl"></div>
      
      <div class="relative p-5 flex items-center">
        <router-link to="/chat" class="w-10 h-10 rounded-xl bg-dark-700/50 hover:bg-dark-600/50 flex items-center justify-center mr-4 transition-all duration-300 hover:scale-105 group">
          <i class="fas fa-arrow-left text-dark-400 group-hover:text-cyan-400 transition-colors"></i>
        </router-link>
        
        <div class="relative mr-4">
          <div class="w-14 h-14 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center text-xl font-bold shadow-lg shadow-cyan-500/20">
            {{ otherUser?.username?.[0]?.toUpperCase() }}
          </div>
          <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-400 rounded-full border-2 border-dark-800"></div>
        </div>
        
        <div>
          <h1 class="font-bold text-xl">{{ otherUser?.username }}</h1>
          <p class="text-sm text-dark-400 flex items-center mt-0.5">
            <i class="fas fa-lock text-cyan-400 mr-2 text-xs"></i>
            私密对话
          </p>
        </div>
      </div>
    </div>
    
    <!-- Messages -->
    <div ref="messagesEl" class="flex-1 bg-dark-800/40 backdrop-blur-sm border-x border-dark-700/50 overflow-y-auto p-6 space-y-6">
      <!-- Date Divider -->
      <div class="flex items-center justify-center">
        <div class="px-4 py-1.5 bg-dark-700/50 rounded-full text-xs text-dark-400">
          今天
        </div>
      </div>
      
      <div v-for="msg in messages" :key="msg.id" 
        :class="['flex items-start gap-3', msg.author?.id === auth.user?.id ? 'flex-row-reverse' : '']">
        
        <!-- Avatar -->
        <div class="flex-shrink-0">
          <div :class="['w-9 h-9 rounded-xl flex items-center justify-center text-sm font-bold',
            msg.author?.id === auth.user?.id 
              ? 'bg-gradient-to-br from-cyan-500 to-blue-500' 
              : 'bg-gradient-to-br from-blue-500 to-blue-600']">
            {{ msg.author?.username?.[0]?.toUpperCase() }}
          </div>
        </div>
        
        <!-- Message Bubble -->
        <div :class="['max-w-[70%]', msg.author?.id === auth.user?.id ? 'text-right' : '']">
          <div :class="['inline-block rounded-2xl px-4 py-2.5 text-left max-w-full',
            msg.author?.id === auth.user?.id 
              ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-br-md' 
              : 'bg-dark-700/80 text-dark-100 rounded-bl-md']">
            <p class="break-all">{{ msg.content }}</p>
          </div>
          <span :class="['text-xs text-dark-500 mt-1 block', msg.author?.id === auth.user?.id ? 'text-right' : '']">
            {{ formatTime(msg.created_at) }}
          </span>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-if="!messages.length" class="flex flex-col items-center justify-center h-full text-center py-20">
        <div class="w-24 h-24 bg-gradient-to-br from-dark-700 to-dark-800 rounded-3xl flex items-center justify-center mb-6 shadow-xl">
          <i class="fas fa-comments text-dark-500 text-4xl"></i>
        </div>
        <h3 class="text-xl font-semibold mb-2">开始对话</h3>
        <p class="text-dark-400 max-w-xs">与 {{ otherUser?.username }} 的私密对话，消息仅双方可见</p>
      </div>
    </div>
    
    <!-- Input -->
    <div class="relative overflow-hidden rounded-b-2xl bg-dark-800/90 backdrop-blur-xl border border-dark-700/50 border-t-0">
      <div class="absolute inset-0 bg-gradient-to-r from-cyan-500/5 via-transparent to-blue-500/5"></div>
      
      <div class="relative p-4">
        <form @submit.prevent="sendMessage" class="flex gap-3">
          <div class="flex-1 relative">
            <input v-model="newMessage" placeholder="输入消息..." autocomplete="off" 
              class="w-full px-5 py-4 bg-dark-700/50 border-2 border-dark-600/50 rounded-2xl text-white placeholder-dark-400 focus:outline-none focus:border-cyan-500/50 focus:bg-dark-700/80 transition-all duration-300">
          </div>
          <button type="submit" :disabled="!newMessage.trim()"
            class="px-6 py-4 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl font-medium transition-all duration-300 hover:shadow-lg hover:shadow-cyan-500/30 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 disabled:hover:shadow-none">
            <i class="fas fa-paper-plane text-lg"></i>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { io } from 'socket.io-client'
import { useAuthStore } from '../../stores/auth'
import api from '../../api'

const route = useRoute()
const auth = useAuthStore()
const otherUser = ref(null)
const messages = ref([])
const newMessage = ref('')
const messagesEl = ref(null)
let socket

const formatTime = (d) => {
  const now = new Date()
  const date = new Date(d)
  const diff = Math.floor((now - date) / 1000)
  
  if (diff < 60) return '刚刚'
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`
  if (diff < 604800) return `${Math.floor(diff / 86400)}天前`
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

onMounted(async () => {
  const { data } = await api.get(`/chat/private/${route.params.id}`)
  otherUser.value = data.user
  messages.value = data.messages
  
  socket = io()
  socket.emit('auth', { token: localStorage.getItem('token') })
  
  socket.on('new_private_message', (msg) => {
    if ((msg.author?.id === parseInt(route.params.id)) || 
        (msg.author?.id === auth.user?.id && msg.recipient_id === parseInt(route.params.id))) {
      messages.value.push(msg)
      nextTick(() => { 
        if (messagesEl.value) {
          messagesEl.value.scrollTop = messagesEl.value.scrollHeight 
        }
      })
    }
  })
  
  nextTick(() => { 
    if (messagesEl.value) {
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight 
    }
  })
})

onUnmounted(() => { 
  if (socket) socket.disconnect() 
})

function sendMessage() {
  if (!newMessage.value.trim()) return
  socket.emit('private_message', { 
    recipient_id: parseInt(route.params.id), 
    content: newMessage.value, 
    token: localStorage.getItem('token') 
  })
  newMessage.value = ''
}
</script>
