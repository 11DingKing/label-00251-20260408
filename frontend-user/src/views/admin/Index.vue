<template>
  <div>
    <!-- Header -->
    <div class="flex items-center space-x-4 mb-8">
      <div class="w-12 h-12 bg-amber-500/20 rounded-xl flex items-center justify-center">
        <i class="fas fa-cog text-amber-400 text-xl"></i>
      </div>
      <div>
        <h1 class="text-2xl font-bold">管理后台</h1>
        <p class="text-dark-400">系统管理与配置</p>
      </div>
    </div>
    
    <!-- Stats Grid -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div v-for="(stat, i) in statsCards" :key="stat.label" 
        class="card p-5 hover-lift"
        :style="{ animationDelay: `${i * 0.05}s` }">
        <div class="flex items-center justify-between mb-3">
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center', stat.bgClass]">
            <i :class="[stat.icon, stat.iconClass]"></i>
          </div>
          <span :class="['text-xs font-medium px-2 py-1 rounded-lg', stat.badgeClass]">
            {{ stat.change }}
          </span>
        </div>
        <div class="text-3xl font-bold mb-1">{{ stats[stat.key] }}</div>
        <div class="text-dark-500 text-sm">{{ stat.label }}</div>
      </div>
    </div>
    
    <!-- Quick Actions -->
    <h2 class="font-semibold text-lg mb-4">快捷操作</h2>
    <div class="grid md:grid-cols-2 gap-4">
      <router-link to="/admin/users" 
        class="card p-6 hover-lift hover-glow group cursor-pointer">
        <div class="flex items-center">
          <div class="w-14 h-14 bg-cyan-500/20 rounded-xl flex items-center justify-center mr-5 group-hover:scale-110 transition-transform">
            <i class="fas fa-users text-cyan-400 text-2xl"></i>
          </div>
          <div class="flex-1">
            <h3 class="font-semibold text-lg group-hover:text-cyan-400 transition-colors">用户管理</h3>
            <p class="text-dark-500">管理用户账户和权限</p>
          </div>
          <i class="fas fa-chevron-right text-dark-600 group-hover:text-cyan-400 group-hover:translate-x-1 transition-all"></i>
        </div>
      </router-link>
      
      <router-link to="/admin/ai" 
        class="card p-6 hover-lift hover-glow group cursor-pointer">
        <div class="flex items-center">
          <div class="w-14 h-14 bg-blue-500/20 rounded-xl flex items-center justify-center mr-5 group-hover:scale-110 transition-transform">
            <i class="fas fa-robot text-blue-400 text-2xl"></i>
          </div>
          <div class="flex-1">
            <h3 class="font-semibold text-lg group-hover:text-blue-400 transition-colors">AI 设置</h3>
            <p class="text-dark-500">配置 AI 服务 API</p>
          </div>
          <i class="fas fa-chevron-right text-dark-600 group-hover:text-blue-400 group-hover:translate-x-1 transition-all"></i>
        </div>
      </router-link>
    </div>

    <!-- System Info -->
    <div class="card p-6 mt-6">
      <h3 class="font-semibold mb-4 flex items-center">
        <i class="fas fa-info-circle text-dark-500 mr-2"></i>系统信息
      </h3>
      <div class="grid sm:grid-cols-3 gap-4 text-sm">
        <div class="p-3 bg-dark-800/50 rounded-xl">
          <span class="text-dark-500">版本</span>
          <p class="font-medium mt-1">v1.0.0</p>
        </div>
        <div class="p-3 bg-dark-800/50 rounded-xl">
          <span class="text-dark-500">环境</span>
          <p class="font-medium mt-1">Production</p>
        </div>
        <div class="p-3 bg-dark-800/50 rounded-xl">
          <span class="text-dark-500">状态</span>
          <p class="font-medium mt-1 text-emerald-400 flex items-center">
            <span class="w-2 h-2 bg-emerald-400 rounded-full mr-2"></span>运行中
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const stats = ref({ users: 0, wiki_pages: 0, ideas: 0, chat_rooms: 0 })

const statsCards = [
  { key: 'users', label: '用户', icon: 'fas fa-users', bgClass: 'bg-cyan-500/20', iconClass: 'text-cyan-400', badgeClass: 'bg-cyan-500/20 text-cyan-400', change: '活跃' },
  { key: 'wiki_pages', label: 'Wiki 页面', icon: 'fas fa-book', bgClass: 'bg-blue-500/20', iconClass: 'text-blue-400', badgeClass: 'bg-blue-500/20 text-blue-400', change: '文档' },
  { key: 'ideas', label: '想法卡片', icon: 'fas fa-lightbulb', bgClass: 'bg-amber-500/20', iconClass: 'text-amber-400', badgeClass: 'bg-amber-500/20 text-amber-400', change: '创意' },
  { key: 'chat_rooms', label: '聊天室', icon: 'fas fa-comments', bgClass: 'bg-emerald-500/20', iconClass: 'text-emerald-400', badgeClass: 'bg-emerald-500/20 text-emerald-400', change: '交流' }
]

onMounted(async () => {
  try {
    const { data } = await api.get('/admin/stats')
    stats.value = data
  } catch (e) {
    console.error('Failed to load stats:', e)
  }
})
</script>
