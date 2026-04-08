<template>
  <div class="h-[calc(100vh-8rem)] flex gap-4">
    <!-- Main Chat Area -->
    <div class="flex-1 flex flex-col card overflow-hidden">
      <!-- Header -->
      <div class="p-4 border-b border-dark-700/50 flex items-center justify-between">
        <div class="flex items-center">
          <router-link to="/chat" class="w-10 h-10 rounded-xl bg-dark-800/50 hover:bg-dark-700/50 flex items-center justify-center mr-4 transition-colors">
            <i class="fas fa-arrow-left text-dark-400"></i>
          </router-link>
          <div class="w-12 h-12 bg-emerald-500/20 rounded-xl flex items-center justify-center mr-4">
            <i class="fas fa-hashtag text-emerald-400 text-lg"></i>
          </div>
          <div>
            <h1 class="font-semibold text-lg">{{ room?.name }}</h1>
            <p class="text-sm text-dark-500">{{ room?.description || '暂无描述' }}</p>
          </div>
        </div>
        <button @click="showMembers = !showMembers" class="lg:hidden w-10 h-10 rounded-xl bg-dark-800/50 hover:bg-dark-700/50 flex items-center justify-center transition-colors">
          <i class="fas fa-users text-dark-400"></i>
        </button>
      </div>
      
      <!-- Messages -->
      <div ref="messagesEl" class="flex-1 overflow-y-auto p-4 space-y-4">
        <div v-for="msg in messages" :key="msg.id" 
          :class="['flex items-start gap-3', msg.author?.id === auth.user?.id ? 'flex-row-reverse' : '']">
          
          <!-- Avatar -->
          <div class="flex-shrink-0">
            <div :class="['w-9 h-9 rounded-xl flex items-center justify-center text-sm font-bold',
              msg.author?.id === auth.user?.id 
                ? 'bg-gradient-to-br from-cyan-500 to-blue-500' 
                : 'bg-gradient-to-br from-emerald-500 to-teal-500']">
              {{ msg.author?.username?.[0]?.toUpperCase() }}
            </div>
          </div>
          
          <!-- Message Bubble -->
          <div :class="['max-w-[70%]', msg.author?.id === auth.user?.id ? 'text-right' : '']">
            <div :class="['flex items-baseline gap-2 mb-1', msg.author?.id === auth.user?.id ? 'flex-row-reverse' : '']">
              <span class="font-medium text-sm truncate max-w-[120px]">{{ msg.author?.username }}</span>
              <span class="text-xs text-dark-500 flex-shrink-0">{{ formatTime(msg.created_at) }}</span>
            </div>
            <div :class="['inline-block rounded-2xl px-4 py-2.5 text-left max-w-full',
              msg.author?.id === auth.user?.id 
                ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-br-md' 
                : 'bg-dark-700/80 text-dark-100 rounded-bl-md']">
              <p class="break-all">{{ msg.content }}</p>
            </div>
          </div>
        </div>
        
        <div v-if="!messages.length" class="flex flex-col items-center justify-center h-full text-center">
          <div class="w-20 h-20 bg-dark-800 rounded-2xl flex items-center justify-center mb-4">
            <i class="fas fa-comments text-dark-600 text-3xl"></i>
          </div>
          <p class="text-dark-500">还没有消息</p>
          <p class="text-dark-600 text-sm mt-1">发送第一条消息开始聊天</p>
        </div>
      </div>
      
      <!-- Input -->
      <div class="p-4 border-t border-dark-700/50">
        <form @submit.prevent="sendMessage" class="flex gap-3">
          <input v-model="newMessage" placeholder="输入消息..." autocomplete="off" 
            class="input-modern flex-1">
          <button type="submit" :disabled="!newMessage.trim()"
            class="px-6 py-3 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-xl font-medium transition-all duration-300 hover:shadow-lg hover:shadow-emerald-500/30 disabled:opacity-50 disabled:cursor-not-allowed">
            <i class="fas fa-paper-plane"></i>
          </button>
        </form>
      </div>
    </div>
    
    <!-- Members Sidebar -->
    <div :class="['w-72 card p-4 hidden lg:block', showMembers ? '!block fixed right-4 top-20 bottom-4 z-40' : '']">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-semibold">成员 ({{ members.length }})</h2>
        <button @click="showMembers = false" class="lg:hidden w-8 h-8 rounded-lg bg-dark-800 hover:bg-dark-700 flex items-center justify-center">
          <i class="fas fa-times text-dark-400"></i>
        </button>
      </div>
      <div class="space-y-2">
        <div v-for="m in members" :key="m.id" 
          class="flex items-center space-x-3 p-2 rounded-xl">
          <div class="w-9 h-9 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-full flex items-center justify-center text-sm font-bold">
            {{ m.username[0].toUpperCase() }}
          </div>
          <span class="text-sm font-medium">{{ m.username }}</span>
        </div>
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
const room = ref(null)
const messages = ref([])
const members = ref([])
const newMessage = ref('')
const messagesEl = ref(null)
const showMembers = ref(false)
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
  const { data } = await api.get(`/chat/rooms/${route.params.id}`)
  room.value = data.room
  messages.value = data.messages
  members.value = data.members
  
  await api.post(`/chat/rooms/${route.params.id}/join`)
  
  socket = io()
  socket.emit('auth', { token: localStorage.getItem('token') })
  socket.emit('join', { room: `room_${route.params.id}` })
  
  socket.on('new_message', (msg) => {
    messages.value.push(msg)
    nextTick(() => { 
      if (messagesEl.value) {
        messagesEl.value.scrollTop = messagesEl.value.scrollHeight 
      }
    })
  })
  
  nextTick(() => { 
    if (messagesEl.value) {
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight 
    }
  })
})

onUnmounted(() => {
  if (socket) {
    socket.emit('leave', { room: `room_${route.params.id}` })
    socket.disconnect()
  }
})

function sendMessage() {
  if (!newMessage.value.trim()) return
  socket.emit('message', { 
    room_id: parseInt(route.params.id), 
    content: newMessage.value, 
    token: localStorage.getItem('token') 
  })
  newMessage.value = ''
}
</script>
