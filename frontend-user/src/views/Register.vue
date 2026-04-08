<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-12">
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative w-full max-w-md animate-fade-in-up">
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center space-x-3 group">
          <div class="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/30 group-hover:shadow-cyan-500/50 transition-all">
            <i class="fas fa-gamepad text-white text-xl"></i>
          </div>
          <span class="font-bold text-2xl">GameDev Hub</span>
        </router-link>
        <h1 class="text-2xl font-bold mt-6 mb-2">创建账户</h1>
        <p class="text-dark-400">加入游戏开发团队</p>
      </div>

      <form @submit.prevent="handleRegister" class="card p-8 space-y-5">
        <Transition name="shake">
          <div v-if="error" class="flex items-center space-x-3 p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400">
            <i class="fas fa-exclamation-circle"></i>
            <span>{{ error }}</span>
          </div>
        </Transition>

        <div class="space-y-2">
          <label class="text-sm font-medium text-dark-300">用户名</label>
          <div class="relative group">
            <i class="fas fa-user absolute left-4 top-1/2 -translate-y-1/2 text-dark-400 group-focus-within:text-cyan-400 transition-colors"></i>
            <input v-model="username" type="text" required placeholder="选择一个用户名" 
              class="w-full bg-dark-800 border-2 border-dark-600 rounded-xl px-4 py-3.5 pl-11 text-white placeholder-dark-500 focus:outline-none focus:border-cyan-500 focus:bg-dark-800/80 transition-all">
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-dark-300">邮箱</label>
          <div class="relative group">
            <i class="fas fa-envelope absolute left-4 top-1/2 -translate-y-1/2 text-dark-400 group-focus-within:text-cyan-400 transition-colors"></i>
            <input v-model="email" type="email" required placeholder="your@email.com" 
              class="w-full bg-dark-800 border-2 border-dark-600 rounded-xl px-4 py-3.5 pl-11 text-white placeholder-dark-500 focus:outline-none focus:border-cyan-500 focus:bg-dark-800/80 transition-all">
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-dark-300">密码</label>
          <div class="relative group">
            <i class="fas fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-dark-400 group-focus-within:text-cyan-400 transition-colors"></i>
            <input v-model="password" :type="showPassword ? 'text' : 'password'" required minlength="6" placeholder="至少6个字符" 
              class="w-full bg-dark-800 border-2 border-dark-600 rounded-xl px-4 py-3.5 pl-11 pr-11 text-white placeholder-dark-500 focus:outline-none focus:border-cyan-500 focus:bg-dark-800/80 transition-all">
            <button type="button" @click="showPassword = !showPassword" 
              class="absolute right-4 top-1/2 -translate-y-1/2 text-dark-400 hover:text-cyan-400 transition-colors">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <!-- 密码强度指示器 -->
          <div class="flex space-x-1 mt-2">
            <div v-for="i in 4" :key="i" :class="['h-1 flex-1 rounded-full transition-all duration-300', passwordStrength >= i ? strengthColors[passwordStrength - 1] : 'bg-dark-700']"></div>
          </div>
          <p v-if="password" class="text-xs" :class="strengthTexts[passwordStrength - 1]?.color || 'text-dark-500'">
            {{ strengthTexts[passwordStrength - 1]?.text || '请输入密码' }}
          </p>
        </div>

        <button type="submit" :disabled="loading"
          class="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl font-semibold text-lg transition-all duration-300 hover:shadow-lg hover:shadow-cyan-500/30 disabled:opacity-50 relative overflow-hidden group">
          <span v-if="!loading">创建账户</span>
          <span v-else class="flex items-center justify-center space-x-2">
            <i class="fas fa-spinner fa-spin"></i>
            <span>注册中...</span>
          </span>
        </button>

        <p class="text-center text-xs text-dark-500">
          注册即表示同意我们的服务条款和隐私政策
        </p>
      </form>

      <p class="text-center mt-6 text-dark-400">
        已有账户？
        <router-link to="/login" class="text-cyan-400 hover:text-cyan-300 font-medium">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)

const strengthColors = ['bg-rose-500', 'bg-amber-500', 'bg-emerald-500', 'bg-cyan-500']
const strengthTexts = [
  { text: '密码太弱', color: 'text-rose-400' },
  { text: '密码一般', color: 'text-amber-400' },
  { text: '密码较强', color: 'text-emerald-400' },
  { text: '密码很强', color: 'text-cyan-400' }
]

const passwordStrength = computed(() => {
  const p = password.value
  if (!p) return 0
  let score = 0
  if (p.length >= 6) score++
  if (p.length >= 10) score++
  if (/[A-Z]/.test(p) && /[a-z]/.test(p)) score++
  if (/[0-9]/.test(p) || /[^A-Za-z0-9]/.test(p)) score++
  return score
})

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    await auth.register(username.value, email.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.error || '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>
