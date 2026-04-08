<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-12">
    <!-- 背景 -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative w-full max-w-md animate-fade-in-up">
      <!-- Logo -->
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center space-x-3 group">
          <div class="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/30 group-hover:shadow-cyan-500/50 transition-all">
            <i class="fas fa-gamepad text-white text-xl"></i>
          </div>
          <span class="font-bold text-2xl">GameDev Hub</span>
        </router-link>
        <h1 class="text-2xl font-bold mt-6 mb-2">欢迎回来</h1>
        <p class="text-dark-400">登录你的账户继续</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleLogin" class="card p-8 space-y-6">
        <!-- Error -->
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
            <input v-model="username" type="text" required placeholder="输入用户名"
              class="w-full bg-dark-800 border-2 border-dark-600 rounded-xl px-4 py-3.5 pl-11 text-white placeholder-dark-500 focus:outline-none focus:border-cyan-500 focus:bg-dark-800/80 transition-all">
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-dark-300">密码</label>
          <div class="relative group">
            <i class="fas fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-dark-400 group-focus-within:text-cyan-400 transition-colors"></i>
            <input v-model="password" :type="showPassword ? 'text' : 'password'" required placeholder="输入密码"
              class="w-full bg-dark-800 border-2 border-dark-600 rounded-xl px-4 py-3.5 pl-11 pr-11 text-white placeholder-dark-500 focus:outline-none focus:border-cyan-500 focus:bg-dark-800/80 transition-all">
            <button type="button" @click="showPassword = !showPassword" 
              class="absolute right-4 top-1/2 -translate-y-1/2 text-dark-400 hover:text-cyan-400 transition-colors">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
        </div>

        <button type="submit" :disabled="loading"
          class="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl font-semibold text-lg transition-all duration-300 hover:shadow-lg hover:shadow-cyan-500/30 disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden group">
          <span v-if="!loading">登录</span>
          <span v-else class="flex items-center justify-center space-x-2">
            <i class="fas fa-spinner fa-spin"></i>
            <span>登录中...</span>
          </span>
          <div class="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-400 opacity-0 group-hover:opacity-100 transition-opacity -z-10"></div>
        </button>
      </form>

      <p class="text-center mt-6 text-dark-400">
        还没有账户？
        <router-link to="/register" class="text-cyan-400 hover:text-cyan-300 font-medium transition-colors">
          立即注册
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await auth.login(username.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.error || '登录失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.shake-enter-active { animation: shake 0.5s ease; }
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-5px); }
  40%, 80% { transform: translateX(5px); }
}
</style>
