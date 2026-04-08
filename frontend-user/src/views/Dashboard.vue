<template>
  <div class="space-y-8">
    <!-- Welcome Banner -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-dark-800/80 via-dark-900/60 to-dark-800/80 border border-dark-700/50 p-8 md:p-10">
      <!-- Background decorations -->
      <div class="absolute top-0 right-0 w-80 h-80 bg-gradient-to-br from-cyan-500/15 to-blue-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
      <div class="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-blue-500/10 to-blue-600/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/3"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-[radial-gradient(ellipse_at_center,rgba(6,182,212,0.05)_0%,transparent_70%)]"></div>
      
      <div class="relative flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div class="flex-1">
          <!-- Greeting badge -->
          <div class="inline-flex items-center space-x-2 px-3 py-1.5 bg-cyan-500/10 border border-cyan-500/20 rounded-full text-cyan-400 text-sm font-medium mb-4">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
            </span>
            <span>{{ getGreeting() }}</span>
          </div>
          
          <!-- Main title -->
          <h1 class="text-3xl md:text-4xl font-bold mb-3">
            <span class="text-white">你好，</span>
            <span class="bg-gradient-to-r from-cyan-400 via-blue-400 to-blue-400 bg-clip-text text-transparent">{{ auth.user?.username }}</span>
            <span class="text-white">！</span>
          </h1>
          
          <!-- Subtitle with stats -->
          <p class="text-dark-400 text-lg mb-4">准备好继续你的游戏开发之旅了吗？</p>
          
          <!-- Quick stats -->
          <div class="flex flex-wrap gap-4 text-sm">
            <div class="flex items-center gap-2 text-dark-400">
              <div class="w-8 h-8 bg-cyan-500/10 rounded-lg flex items-center justify-center">
                <i class="fas fa-file-alt text-cyan-400 text-xs"></i>
              </div>
              <span><span class="text-white font-semibold">{{ allPages.length }}</span> 篇文档</span>
            </div>
            <div class="flex items-center gap-2 text-dark-400">
              <div class="w-8 h-8 bg-amber-500/10 rounded-lg flex items-center justify-center">
                <i class="fas fa-lightbulb text-amber-400 text-xs"></i>
              </div>
              <span><span class="text-white font-semibold">{{ allIdeas.length }}</span> 个想法</span>
            </div>
            <div class="flex items-center gap-2 text-dark-400">
              <div class="w-8 h-8 bg-emerald-500/10 rounded-lg flex items-center justify-center">
                <i class="fas fa-comments text-emerald-400 text-xs"></i>
              </div>
              <span><span class="text-white font-semibold">{{ rooms.length }}</span> 个聊天室</span>
            </div>
          </div>
        </div>
        
        <!-- Right side decoration / avatar -->
        <div class="hidden md:flex items-center justify-center">
          <div class="relative">
            <div class="w-24 h-24 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-2xl flex items-center justify-center text-4xl font-bold text-white shadow-lg shadow-cyan-500/30">
              {{ auth.user?.username?.[0]?.toUpperCase() }}
            </div>
            <div class="absolute -bottom-1 -right-1 w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center border-4 border-dark-900">
              <i class="fas fa-check text-white text-xs"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <router-link v-for="(action, i) in quickActions" :key="action.path" :to="action.path"
        class="group card p-5 hover-lift hover-glow cursor-pointer"
        :style="{ animationDelay: `${i * 0.05}s` }">
        <div :class="['w-12 h-12 rounded-xl flex items-center justify-center mb-3 transition-all duration-300 group-hover:scale-110', action.bgClass]">
          <i :class="[action.icon, action.iconClass, 'text-xl']"></i>
        </div>
        <p class="font-medium">{{ action.name }}</p>
        <p class="text-sm text-dark-500 mt-1">{{ action.desc }}</p>
      </router-link>
    </div>

    <!-- Quick Idea Input -->
    <div class="card p-6">
      <div class="flex items-center space-x-3 mb-4">
        <div class="w-10 h-10 bg-amber-500/20 rounded-xl flex items-center justify-center">
          <i class="fas fa-bolt text-amber-400"></i>
        </div>
        <div>
          <h2 class="font-semibold">快速记录想法</h2>
          <p class="text-sm text-dark-500">灵感稍纵即逝，立即记录</p>
        </div>
      </div>
      <form @submit.prevent="quickIdea" class="flex gap-3">
        <input v-model="quickContent" placeholder="输入你的灵感..." class="input-modern flex-1">
        <button type="submit" :disabled="!quickContent.trim()" 
          class="px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl font-medium transition-all duration-300 hover:shadow-lg hover:shadow-amber-500/30 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap">
          <i class="fas fa-paper-plane mr-2"></i>保存
        </button>
      </form>
    </div>

    <!-- Content Grid -->
    <div class="grid lg:grid-cols-2 gap-6">
      <!-- Recent Wiki Pages -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-5">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-cyan-500/20 rounded-xl flex items-center justify-center">
              <i class="fas fa-book text-cyan-400"></i>
            </div>
            <h2 class="font-semibold text-lg">最近文档</h2>
            <span v-if="allPages.length" class="text-xs text-dark-500 bg-dark-800 px-2 py-0.5 rounded-full">
              {{ allPages.length }}
            </span>
          </div>
          <router-link v-if="allPages.length > 4" to="/wiki" class="text-sm text-cyan-400 hover:text-cyan-300 transition-colors flex items-center space-x-1">
            <span>查看全部</span>
            <i class="fas fa-arrow-right text-xs"></i>
          </router-link>
        </div>
        
        <div v-if="allPages.length">
          <!-- Pages Grid -->
          <div class="grid grid-cols-2 gap-3">
            <router-link v-for="page in displayedPages" :key="page.id" :to="`/wiki/${page.slug}`"
              class="p-4 rounded-xl bg-dark-800/50 hover:bg-dark-700/50 border border-dark-700 hover:border-cyan-500/30 transition-all duration-300 hover:scale-[1.02] group h-[140px] flex flex-col">
              <h3 class="font-medium text-sm truncate group-hover:text-cyan-400 transition-colors">{{ page.title }}</h3>
              <p class="text-xs text-dark-500 mt-1.5 line-clamp-2 flex-1">{{ page.content?.slice(0, 60) || '暂无内容' }}</p>
              <div class="flex items-center justify-between mt-auto pt-2 border-t border-dark-700/50 text-[10px] text-dark-500">
                <span class="flex items-center gap-1">
                  <i class="fas fa-user"></i>
                  {{ page.author?.username }}
                </span>
                <span>{{ formatDate(page.updated_at) }}</span>
              </div>
            </router-link>
          </div>
        </div>
        <div v-else class="text-center py-10">
          <div class="w-16 h-16 bg-dark-800 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <i class="fas fa-book-open text-dark-600 text-2xl"></i>
          </div>
          <p class="text-dark-500 mb-4">还没有文档</p>
          <router-link to="/wiki/new" class="text-cyan-400 hover:text-cyan-300 text-sm font-medium">
            创建第一个 →
          </router-link>
        </div>
      </div>

      <!-- Recent Ideas -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-5">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-amber-500/20 rounded-xl flex items-center justify-center">
              <i class="fas fa-lightbulb text-amber-400"></i>
            </div>
            <h2 class="font-semibold text-lg">最近想法</h2>
            <span v-if="allIdeas.length > 4" class="text-xs text-dark-500 bg-dark-800 px-2 py-0.5 rounded-full">
              {{ allIdeas.length }}
            </span>
          </div>
          <router-link v-if="allIdeas.length > 4" to="/ideas" class="text-sm text-cyan-400 hover:text-cyan-300 transition-colors flex items-center space-x-1">
            <span>查看全部</span>
            <i class="fas fa-arrow-right text-xs"></i>
          </router-link>
        </div>
        
        <div v-if="allIdeas.length">
          <!-- Ideas Grid -->
          <div class="grid grid-cols-2 gap-3">
            <router-link v-for="idea in displayedIdeas" :key="idea.id" :to="`/ideas/${idea.id}`"
              class="p-4 rounded-xl bg-dark-800/50 hover:bg-dark-700/50 border border-dark-700 hover:border-amber-500/30 transition-all duration-300 hover:scale-[1.02] group h-[140px] flex flex-col">
              <h3 class="font-medium text-sm truncate group-hover:text-amber-400 transition-colors">{{ idea.title }}</h3>
              <p class="text-xs text-dark-500 mt-1.5 line-clamp-2 flex-1">{{ idea.content }}</p>
              <div class="flex items-center justify-between mt-auto pt-2 border-t border-dark-700/50 text-[10px] text-dark-500">
                <span class="flex items-center gap-1">
                  <i class="fas fa-user"></i>
                  {{ idea.author?.username }}
                </span>
                <span>{{ formatDate(idea.created_at) }}</span>
              </div>
            </router-link>
          </div>
        </div>
        <div v-else class="text-center py-10">
          <div class="w-16 h-16 bg-dark-800 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <i class="fas fa-lightbulb text-dark-600 text-2xl"></i>
          </div>
          <p class="text-dark-500 mb-4">还没有想法</p>
          <router-link to="/ideas/new" class="text-cyan-400 hover:text-cyan-300 text-sm font-medium">
            记录第一个 →
          </router-link>
        </div>
      </div>
    </div>

    <!-- Chat Rooms -->
    <div class="card p-6">
      <div class="flex items-center justify-between mb-5">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-emerald-500/20 rounded-xl flex items-center justify-center">
            <i class="fas fa-comments text-emerald-400"></i>
          </div>
          <h2 class="font-semibold text-lg">聊天室</h2>
        </div>
        <router-link to="/chat" class="text-sm text-cyan-400 hover:text-cyan-300 transition-colors flex items-center space-x-1">
          <span>查看全部</span>
          <i class="fas fa-arrow-right text-xs"></i>
        </router-link>
      </div>
      
      <div v-if="rooms.length" class="flex flex-wrap gap-3">
        <router-link v-for="room in rooms" :key="room.id" :to="`/chat/room/${room.id}`"
          class="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-dark-800/50 hover:bg-dark-700/50 border border-dark-700 hover:border-emerald-500/30 transition-all duration-200 group">
          <i class="fas fa-hashtag text-emerald-400 text-sm"></i>
          <span class="group-hover:text-emerald-400 transition-colors">{{ room.name }}</span>
        </router-link>
      </div>
      <div v-else class="text-center py-6">
        <p class="text-dark-500">还没有聊天室，<router-link to="/chat" class="text-cyan-400 hover:text-cyan-300">创建一个</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const auth = useAuthStore()
const showToast = inject('showToast')
const allPages = ref([])
const allIdeas = ref([])
const rooms = ref([])
const quickContent = ref('')
const ideasExpanded = ref(false)
const pagesExpanded = ref(false)

const displayedPages = computed(() => {
  if (pagesExpanded.value) return allPages.value
  return allPages.value.slice(0, 4)
})

const displayedIdeas = computed(() => {
  if (ideasExpanded.value) return allIdeas.value
  return allIdeas.value.slice(0, 4)
})

const quickActions = [
  { path: '/wiki/new', name: '新建文档', desc: '记录设计', icon: 'fas fa-plus', bgClass: 'bg-cyan-500/20', iconClass: 'text-cyan-400' },
  { path: '/ideas/new', name: '记录想法', desc: '捕捉灵感', icon: 'fas fa-lightbulb', bgClass: 'bg-amber-500/20', iconClass: 'text-amber-400' },
  { path: '/chat', name: '聊天室', desc: '团队交流', icon: 'fas fa-users', bgClass: 'bg-emerald-500/20', iconClass: 'text-emerald-400' },
  { path: '/ai', name: 'AI 助手', desc: '智能对话', icon: 'fas fa-robot', bgClass: 'bg-blue-500/20', iconClass: 'text-blue-400' }
]

const ideaClass = (color) => ({
  blue: 'idea-blue',
  green: 'idea-green',
  yellow: 'idea-yellow',
  red: 'idea-red',
  pink: 'idea-pink'
}[color] || 'bg-dark-800/50 border-dark-700')

const formatDate = (d) => {
  const date = new Date(d)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 6) return '夜深了，注意休息'
  if (hour < 9) return '早上好'
  if (hour < 12) return '上午好'
  if (hour < 14) return '中午好'
  if (hour < 18) return '下午好'
  if (hour < 22) return '晚上好'
  return '夜深了，注意休息'
}

onMounted(async () => {
  const [wikiRes, ideasRes, chatRes] = await Promise.all([
    api.get('/wiki'),
    api.get('/ideas'),
    api.get('/chat/rooms')
  ])
  allPages.value = wikiRes.data.pages.slice(0, 10)
  allIdeas.value = ideasRes.data.ideas.slice(0, 10)
  rooms.value = chatRes.data.public.slice(0, 6)
})

async function quickIdea() {
  if (!quickContent.value.trim()) return
  await api.post('/ideas/quick', { content: quickContent.value })
  quickContent.value = ''
  showToast('想法已保存')
  const { data } = await api.get('/ideas')
  allIdeas.value = data.ideas.slice(0, 10)
}
</script>
