<template>
  <div class="auth-page h-screen flex items-center justify-center px-4 overflow-hidden">
    <!-- 背景 -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl transition-all duration-1000" 
        :class="isLogin ? 'translate-x-0' : 'translate-x-20'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl transition-all duration-1000"
        :class="isLogin ? 'translate-x-0' : '-translate-x-20'"></div>
    </div>

    <div class="relative w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-6 animate-fade-in">
        <router-link to="/" class="inline-flex items-center space-x-3 group">
          <div class="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/30 group-hover:shadow-cyan-500/50 transition-all">
            <i class="fas fa-gamepad text-white text-xl"></i>
          </div>
          <span class="font-bold text-2xl">GameDev Hub</span>
        </router-link>
      </div>

      <!-- Tab Switcher -->
      <div class="flex bg-dark-800/60 backdrop-blur-sm rounded-2xl p-1.5 mb-5 border border-dark-700/50">
        <button @click="switchTo('login')" 
          class="flex-1 py-3 px-6 rounded-xl font-medium transition-all duration-300 relative"
          :class="isLogin ? 'text-white' : 'text-dark-400 hover:text-dark-300'">
          <span class="relative z-10">登录</span>
          <Transition name="tab">
            <div v-if="isLogin" class="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-xl border border-cyan-500/30"></div>
          </Transition>
        </button>
        <button @click="switchTo('register')" 
          class="flex-1 py-3 px-6 rounded-xl font-medium transition-all duration-300 relative"
          :class="!isLogin ? 'text-white' : 'text-dark-400 hover:text-dark-300'">
          <span class="relative z-10">注册</span>
          <Transition name="tab">
            <div v-if="!isLogin" class="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-blue-600/20 rounded-xl border border-blue-500/30"></div>
          </Transition>
        </button>
      </div>

      <!-- Form Container with fixed height -->
      <div class="relative h-[480px]">
        <Transition :name="slideDirection" mode="out-in">
          <!-- Login Form -->
          <form v-if="isLogin" key="login" @submit.prevent="handleLogin" class="card p-7 space-y-5 absolute inset-x-0 top-0">
            <div class="text-center mb-1">
              <h1 class="text-2xl font-bold">欢迎回来</h1>
              <p class="text-dark-400 text-sm mt-1">登录你的账户继续</p>
            </div>

            <Transition name="shake">
              <div v-if="error" class="flex items-center space-x-3 p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400 text-sm">
                <i class="fas fa-exclamation-circle"></i>
                <span>{{ error }}</span>
              </div>
            </Transition>

            <div class="space-y-1.5">
              <label class="text-sm font-medium text-dark-300">用户名</label>
              <div class="relative group">
                <i class="fas fa-user absolute left-4 top-1/2 -translate-y-1/2 text-dark-400 group-focus-within:text-cyan-400 transition-colors"></i>
                <input v-model="loginForm.username" type="text" required placeholder="输入用户名"
                  class="w-full bg-dark-800 border-2 border-dark-600 rounded-xl px-4 py-3 pl-11 text-white placeholder-dark-500 focus:outline-none focus:border-cyan-500 transition-all">
              </div>
            </div>

            <div class="space-y-1.5">
              <label class="text-sm font-medium text-dark-300">密码</label>
              <div class="relative group">
                <i class="fas fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-dark-400 group-focus-within:text-cyan-400 transition-colors"></i>
                <input v-model="loginForm.password" :type="showLoginPwd ? 'text' : 'password'" required placeholder="输入密码"
                  class="w-full bg-dark-800 border-2 border-dark-600 rounded-xl px-4 py-3 pl-11 pr-11 text-white placeholder-dark-500 focus:outline-none focus:border-cyan-500 transition-all">
                <button type="button" @click="showLoginPwd = !showLoginPwd" 
                  class="absolute right-4 top-1/2 -translate-y-1/2 text-dark-400 hover:text-cyan-400 transition-colors">
                  <i :class="showLoginPwd ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
            </div>

            <button type="submit" :disabled="loading"
              class="w-full py-3.5 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl font-semibold text-lg transition-all duration-300 hover:shadow-lg hover:shadow-cyan-500/30 disabled:opacity-50 disabled:cursor-not-allowed">
              <span v-if="!loading">登录</span>
              <span v-else class="flex items-center justify-center space-x-2">
                <i class="fas fa-spinner fa-spin"></i>
                <span>登录中...</span>
              </span>
            </button>
          </form>

          <!-- Register Form -->
          <form v-else key="register" @submit.prevent="handleRegister" class="card p-7 space-y-4 absolute inset-x-0 top-0">
            <div class="text-center mb-1">
              <h1 class="text-2xl font-bold">创建账户</h1>
              <p class="text-dark-400 text-sm mt-1">加入游戏开发团队</p>
            </div>

            <Transition name="shake">
              <div v-if="error" class="flex items-center space-x-3 p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400 text-sm">
                <i class="fas fa-exclamation-circle"></i>
                <span>{{ error }}</span>
              </div>
            </Transition>

            <div class="space-y-1.5">
              <label class="text-sm font-medium text-dark-300">用户名</label>
              <div class="relative group">
                <i class="fas fa-user absolute left-4 top-1/2 -translate-y-1/2 text-dark-400 group-focus-within:text-blue-400 transition-colors"></i>
                <input v-model="registerForm.username" type="text" required placeholder="选择一个用户名"
                  class="w-full bg-dark-800 border-2 border-dark-600 rounded-xl px-4 py-3 pl-11 text-white placeholder-dark-500 focus:outline-none focus:border-blue-500 transition-all">
              </div>
            </div>

            <div class="space-y-1.5">
              <label class="text-sm font-medium text-dark-300">邮箱</label>
              <div class="relative group">
                <i class="fas fa-envelope absolute left-4 top-1/2 -translate-y-1/2 text-dark-400 group-focus-within:text-blue-400 transition-colors"></i>
                <input v-model="registerForm.email" type="email" required placeholder="your@email.com"
                  class="w-full bg-dark-800 border-2 border-dark-600 rounded-xl px-4 py-3 pl-11 text-white placeholder-dark-500 focus:outline-none focus:border-blue-500 transition-all">
              </div>
            </div>

            <div class="space-y-1.5">
              <label class="text-sm font-medium text-dark-300">密码</label>
              <div class="relative group">
                <i class="fas fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-dark-400 group-focus-within:text-blue-400 transition-colors"></i>
                <input v-model="registerForm.password" :type="showRegPwd ? 'text' : 'password'" required minlength="6" placeholder="至少6个字符"
                  class="w-full bg-dark-800 border-2 border-dark-600 rounded-xl px-4 py-3 pl-11 pr-11 text-white placeholder-dark-500 focus:outline-none focus:border-blue-500 transition-all">
                <button type="button" @click="showRegPwd = !showRegPwd" 
                  class="absolute right-4 top-1/2 -translate-y-1/2 text-dark-400 hover:text-blue-400 transition-colors">
                  <i :class="showRegPwd ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
              <!-- 密码强度 -->
              <div class="flex space-x-1 mt-1.5">
                <div v-for="i in 4" :key="i" 
                  :class="['h-1 flex-1 rounded-full transition-all duration-300', passwordStrength >= i ? strengthColors[passwordStrength - 1] : 'bg-dark-700']"></div>
              </div>
            </div>

            <button type="submit" :disabled="loading"
              class="w-full py-3.5 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl font-semibold text-lg transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed">
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
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const isLogin = ref(route.path === '/login')
const slideDirection = ref('slide-left')
const error = ref('')
const loading = ref(false)
const showLoginPwd = ref(false)
const showRegPwd = ref(false)

const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({ username: '', email: '', password: '' })

const strengthColors = ['bg-rose-500', 'bg-amber-500', 'bg-emerald-500', 'bg-cyan-500']

const passwordStrength = computed(() => {
  const p = registerForm.password
  if (!p) return 0
  let score = 0
  if (p.length >= 6) score++
  if (p.length >= 10) score++
  if (/[A-Z]/.test(p) && /[a-z]/.test(p)) score++
  if (/[0-9]/.test(p) || /[^A-Za-z0-9]/.test(p)) score++
  return score
})

watch(() => route.path, (path) => {
  isLogin.value = path === '/login'
})

function switchTo(mode) {
  error.value = ''
  slideDirection.value = mode === 'login' ? 'slide-right' : 'slide-left'
  isLogin.value = mode === 'login'
  router.replace(mode === 'login' ? '/login' : '/register')
}

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await auth.login(loginForm.username, loginForm.password)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.error || '登录失败，请重试'
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    await auth.register(registerForm.username, registerForm.email, registerForm.password)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.error || '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  position: fixed;
  inset: 0;
}

.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease;
}
.slide-left-enter-from { opacity: 0; transform: translateX(30px); }
.slide-left-leave-to { opacity: 0; transform: translateX(-30px); }
.slide-right-enter-from { opacity: 0; transform: translateX(-30px); }
.slide-right-leave-to { opacity: 0; transform: translateX(30px); }

.tab-enter-active,
.tab-leave-active {
  transition: all 0.3s ease;
}
.tab-enter-from,
.tab-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.shake-enter-active { animation: shake 0.5s ease; }
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-5px); }
  40%, 80% { transform: translateX(5px); }
}
</style>
