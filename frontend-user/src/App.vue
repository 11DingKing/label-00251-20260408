<template>
  <div class="min-h-screen">
    <!-- 背景装饰 -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
    </div>

    <!-- 导航栏 -->
    <nav v-if="auth.isLoggedIn" class="glass sticky top-0 z-50 border-b border-white/5">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <router-link to="/dashboard" class="flex items-center space-x-3 group">
            <div class="w-10 h-10 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:shadow-cyan-500/40 transition-all duration-300">
              <i class="fas fa-gamepad text-white text-lg"></i>
            </div>
            <span class="font-bold text-xl hidden sm:block bg-gradient-to-r from-white to-dark-300 bg-clip-text text-transparent">
              GameDev Hub
            </span>
          </router-link>

          <!-- Desktop Nav -->
          <div class="hidden md:flex items-center space-x-1">
            <router-link v-for="item in navItems" :key="item.path" :to="item.path"
              :class="['nav-item px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200',
                $route.path.startsWith(item.path) ? 'bg-dark-800 text-white' : 'text-dark-400 hover:text-white hover:bg-dark-800/50']">
              <i :class="[item.icon, 'text-sm']"></i>
              <span>{{ item.name }}</span>
            </router-link>
          </div>

          <!-- Right Side -->
          <div class="flex items-center space-x-3">
            <!-- Admin -->
            <router-link v-if="auth.isAdmin" to="/admin" 
              class="w-9 h-9 rounded-lg bg-dark-800/50 flex items-center justify-center text-dark-400 hover:text-white hover:bg-dark-700 transition-all">
              <i class="fas fa-cog"></i>
            </router-link>

            <!-- User Menu -->
            <div class="relative" ref="userMenuRef">
              <button @click="showUserMenu = !showUserMenu"
                class="flex items-center space-x-2 px-2 py-1.5 rounded-xl hover:bg-dark-800/50 transition-all group">
                <div class="w-8 h-8 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center text-white font-medium text-sm shadow-lg shadow-cyan-500/20">
                  {{ auth.user?.username?.[0]?.toUpperCase() }}
                </div>
                <span class="hidden sm:block text-sm font-medium">{{ auth.user?.username }}</span>
                <i class="fas fa-chevron-down text-xs text-dark-400 group-hover:text-white transition-colors"></i>
              </button>

              <Transition name="dropdown">
                <div v-if="showUserMenu" class="absolute right-0 mt-2 w-56 glass rounded-xl shadow-2xl border border-white/10 overflow-hidden animate-scale-in">
                  <div class="p-3 border-b border-white/5">
                    <p class="font-medium">{{ auth.user?.username }}</p>
                    <p class="text-sm text-dark-400">{{ auth.user?.email }}</p>
                  </div>
                  <div class="p-2">
                    <router-link to="/profile" @click="showUserMenu = false"
                      class="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-dark-700/50 transition-colors">
                      <i class="fas fa-user text-dark-400"></i>
                      <span>个人资料</span>
                    </router-link>
                    <button @click="logout" class="w-full flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-rose-500/10 text-rose-400 transition-colors">
                      <i class="fas fa-sign-out-alt"></i>
                      <span>退出登录</span>
                    </button>
                  </div>
                </div>
              </Transition>
            </div>

            <!-- Mobile Menu Button -->
            <button @click="showMobileMenu = !showMobileMenu" class="md:hidden w-9 h-9 rounded-lg bg-dark-800/50 flex items-center justify-center">
              <i :class="showMobileMenu ? 'fas fa-times' : 'fas fa-bars'"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Menu -->
      <Transition name="mobile-menu">
        <div v-if="showMobileMenu" class="md:hidden glass border-t border-white/5 animate-fade-in">
          <div class="px-4 py-3 space-y-1">
            <router-link v-for="item in navItems" :key="item.path" :to="item.path" @click="showMobileMenu = false"
              :class="['flex items-center space-x-3 px-4 py-3 rounded-xl transition-all',
                $route.path.startsWith(item.path) ? 'bg-dark-800 text-white' : 'text-dark-400 hover:bg-dark-800/50']">
              <i :class="[item.icon]"></i>
              <span>{{ item.name }}</span>
            </router-link>
          </div>
        </div>
      </Transition>
    </nav>

    <!-- Toast 通知 -->
    <Transition name="toast">
      <div v-if="toast.show" class="fixed top-20 right-4 z-50 animate-slide-in">
        <div :class="['glass px-5 py-3 rounded-xl shadow-2xl flex items-center space-x-3',
          toast.type === 'error' ? 'border-rose-500/50' : 'border-cyan-500/50']">
          <i :class="[toast.type === 'error' ? 'fas fa-exclamation-circle text-rose-400' : 'fas fa-check-circle text-cyan-400']"></i>
          <span>{{ toast.message }}</span>
        </div>
      </div>
    </Transition>

    <!-- Main Content -->
    <main :class="auth.isLoggedIn ? 'relative' : 'relative'">
      <div :class="auth.isLoggedIn ? 'max-w-7xl mx-auto px-4 sm:px-6 py-6' : ''">
        <router-view v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, provide, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const showUserMenu = ref(false)
const showMobileMenu = ref(false)
const userMenuRef = ref(null)

const navItems = [
  { path: '/wiki', name: 'Wiki', icon: 'fas fa-book' },
  { path: '/ideas', name: '想法', icon: 'fas fa-lightbulb' },
  { path: '/chat', name: '聊天', icon: 'fas fa-comments' },
  { path: '/ai', name: 'AI助手', icon: 'fas fa-robot' }
]

// Toast 系统
const toast = ref({ show: false, message: '', type: 'success' })
function showToast(message, type = 'success') {
  toast.value = { show: true, message, type }
  setTimeout(() => { toast.value.show = false }, 3000)
}
provide('showToast', showToast)

function logout() {
  auth.logout()
  showUserMenu.value = false
  router.push('/login')
}

// 点击外部关闭菜单
function handleClickOutside(e) {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    showUserMenu.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
.dropdown-enter-active, .dropdown-leave-active {
  transition: all 0.2s ease;
}
.dropdown-enter-from, .dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from { opacity: 0; transform: translateX(100px); }
.toast-leave-to { opacity: 0; transform: translateX(100px); }

.mobile-menu-enter-active, .mobile-menu-leave-active {
  transition: all 0.3s ease;
}
.mobile-menu-enter-from, .mobile-menu-leave-to {
  opacity: 0;
  max-height: 0;
}
</style>
