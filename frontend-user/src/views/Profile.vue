<template>
  <div>
    <!-- Header -->
    <div class="flex items-center space-x-4 mb-8">
      <div class="w-12 h-12 bg-cyan-500/20 rounded-xl flex items-center justify-center">
        <i class="fas fa-user text-cyan-400 text-xl"></i>
      </div>
      <div>
        <h1 class="text-2xl font-bold">个人资料</h1>
        <p class="text-dark-400">管理你的账户信息</p>
      </div>
    </div>

    <!-- Profile Card -->
    <div class="card p-8">
      <!-- Avatar Section -->
      <div class="flex flex-col sm:flex-row items-center sm:items-start gap-6 mb-8 pb-8 border-b border-dark-700/50">
        <div class="relative group">
          <div class="w-24 h-24 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center text-4xl font-bold text-white shadow-lg shadow-cyan-500/20">
            {{ auth.user?.username?.[0]?.toUpperCase() }}
          </div>
          <div class="absolute inset-0 bg-black/50 rounded-2xl opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity cursor-pointer">
            <i class="fas fa-camera text-white text-xl"></i>
          </div>
        </div>
        <div class="text-center sm:text-left">
          <h2 class="text-2xl font-bold">{{ auth.user?.username }}</h2>
          <div class="flex items-center justify-center sm:justify-start gap-2 mt-2">
            <span :class="['px-3 py-1 rounded-lg text-sm font-medium',
              auth.user?.is_admin ? 'bg-amber-500/20 text-amber-400' : 'bg-dark-700 text-dark-400']">
              <i :class="auth.user?.is_admin ? 'fas fa-crown mr-1' : 'fas fa-user mr-1'"></i>
              {{ auth.user?.is_admin ? '管理员' : '成员' }}
            </span>
          </div>
          <p class="text-dark-500 text-sm mt-3">
            <i class="fas fa-calendar mr-2"></i>
            加入于 {{ formatDate(auth.user?.created_at) }}
          </p>
        </div>
      </div>

      <!-- Form -->
      <form @submit.prevent="save" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-2">
            <i class="fas fa-envelope mr-2 text-dark-500"></i>邮箱
          </label>
          <input v-model="email" type="email" class="input-modern" placeholder="your@email.com">
        </div>
        
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-2">
            <i class="fas fa-pen mr-2 text-dark-500"></i>个人简介
          </label>
          <textarea v-model="bio" rows="4" class="input-modern resize-none" 
            placeholder="介绍一下你自己..."></textarea>
          <p class="text-xs text-dark-500 mt-2">{{ bio.length }}/200 字符</p>
        </div>

        <div class="flex items-center justify-between pt-4">
          <p v-if="saved" class="text-emerald-400 text-sm flex items-center">
            <i class="fas fa-check-circle mr-2"></i>已保存
          </p>
          <div v-else></div>
          <button type="submit" :disabled="saving"
            class="btn-primary flex items-center space-x-2">
            <i :class="saving ? 'fas fa-spinner fa-spin' : 'fas fa-save'"></i>
            <span>{{ saving ? '保存中...' : '保存更改' }}</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Danger Zone -->
    <div class="card p-6 mt-6 border-rose-500/20">
      <h3 class="font-semibold text-rose-400 mb-4 flex items-center">
        <i class="fas fa-exclamation-triangle mr-2"></i>危险区域
      </h3>
      <div class="flex items-center justify-between">
        <div>
          <p class="font-medium">退出登录</p>
          <p class="text-sm text-dark-500">退出当前账户</p>
        </div>
        <button @click="logout" class="px-4 py-2 bg-rose-500/20 hover:bg-rose-500/30 text-rose-400 rounded-xl transition-colors">
          <i class="fas fa-sign-out-alt mr-2"></i>退出
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const router = useRouter()
const auth = useAuthStore()
const email = ref('')
const bio = ref('')
const saving = ref(false)
const saved = ref(false)

const formatDate = (d) => d ? new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' }) : '未知'

onMounted(() => {
  email.value = auth.user?.email || ''
  bio.value = auth.user?.bio || ''
})

async function save() {
  saving.value = true
  saved.value = false
  try {
    await api.put('/auth/profile', { email: email.value, bio: bio.value })
    await auth.fetchUser()
    saved.value = true
    setTimeout(() => { saved.value = false }, 3000)
  } finally {
    saving.value = false
  }
}

function logout() {
  auth.logout()
  router.push('/login')
}
</script>
