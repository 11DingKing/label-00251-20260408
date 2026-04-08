<template>
  <div class="min-h-screen relative overflow-hidden">
    <!-- 背景动画 -->
    <div class="absolute inset-0">
      <div class="absolute top-20 left-10 w-72 h-72 bg-cyan-500/20 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute top-40 right-20 w-96 h-96 bg-blue-500/15 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s"></div>
      <div class="absolute bottom-20 left-1/3 w-80 h-80 bg-blue-500/15 rounded-full blur-3xl animate-pulse" style="animation-delay: 2s"></div>
    </div>

    <!-- 网格背景 -->
    <div class="absolute inset-0 bg-[linear-gradient(rgba(6,182,212,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(6,182,212,0.03)_1px,transparent_1px)] bg-[size:60px_60px]"></div>

    <!-- 导航 -->
    <nav class="relative z-10 px-6 py-4">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/30">
            <i class="fas fa-gamepad text-white text-lg"></i>
          </div>
          <span class="font-bold text-xl">GameDev Hub</span>
        </div>
        <div class="flex items-center space-x-4">
          <router-link to="/login" class="btn-ghost">登录</router-link>
          <router-link to="/register" class="btn-primary">开始使用</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="relative z-10 flex flex-col items-center justify-center px-6 pt-20 pb-32">
      <div class="text-center max-w-4xl animate-fade-in-up">
        <!-- Badge -->
        <div class="group inline-flex items-center space-x-3 px-5 py-2.5 bg-dark-800/60 backdrop-blur-md border border-dark-700/50 rounded-full mb-10 hover:border-cyan-500/30 transition-all duration-500 cursor-default">
          <span class="relative flex h-2.5 w-2.5">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          <span class="text-sm text-dark-300 group-hover:text-dark-200 transition-colors">为游戏开发者打造的协作平台</span>
          <i class="fas fa-sparkles text-cyan-400 text-xs opacity-0 group-hover:opacity-100 transition-opacity"></i>
        </div>

        <!-- Title with enhanced animation -->
        <h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold mb-8 leading-tight">
          <span class="inline-block bg-gradient-to-r from-white via-white to-dark-300 bg-clip-text text-transparent hover:scale-105 transition-transform duration-300 cursor-default">让创意</span>
          <br>
          <span class="inline-block mt-2 bg-gradient-to-r from-cyan-400 via-blue-400 to-blue-400 bg-clip-text text-transparent bg-[length:200%_auto] animate-gradient-x">
            自由流动
          </span>
        </h1>

        <!-- Subtitle with feature highlights -->
        <p class="text-xl text-dark-400 mb-12 max-w-2xl mx-auto leading-relaxed">
          <span class="inline-flex items-center">
            <span class="text-cyan-400 font-medium">Wiki 文档</span>
            <span class="mx-2 text-dark-600">•</span>
            <span class="text-emerald-400 font-medium">实时聊天</span>
            <span class="mx-2 text-dark-600">•</span>
            <span class="text-amber-400 font-medium">想法卡片</span>
            <span class="mx-2 text-dark-600">•</span>
            <span class="text-blue-400 font-medium">AI 助手</span>
          </span>
          <br>
          <span class="text-dark-500 text-lg mt-2 inline-block">一站式游戏开发协作体验</span>
        </p>

        <!-- CTA Buttons with enhanced effects -->
        <div class="flex flex-col sm:flex-row gap-5 justify-center mb-20">
          <router-link to="/register" class="group relative px-10 py-4 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl font-semibold text-lg overflow-hidden transition-all duration-500 hover:shadow-2xl hover:shadow-cyan-500/40 hover:scale-105 hover:-translate-y-1">
            <span class="relative z-10 flex items-center justify-center">
              <span>免费开始</span>
              <i class="fas fa-arrow-right ml-3 group-hover:translate-x-1 transition-transform"></i>
            </span>
            <div class="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <!-- Shine effect -->
            <div class="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
          </router-link>
          <router-link to="/login" class="group px-10 py-4 bg-dark-800/60 backdrop-blur-md border border-dark-700/50 rounded-2xl font-semibold text-lg hover:bg-dark-800/80 hover:border-dark-600 transition-all duration-500 hover:scale-105 hover:-translate-y-1">
            <span class="flex items-center justify-center">
              <i class="fas fa-user mr-3 text-dark-500 group-hover:text-cyan-400 transition-colors"></i>
              <span>已有账户</span>
            </span>
          </router-link>
        </div>

        <!-- Features Grid -->
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 max-w-5xl mx-auto">
          <div v-for="(feature, i) in features" :key="i" 
            class="group relative overflow-hidden rounded-2xl bg-dark-800/60 backdrop-blur-sm border border-dark-700/50 p-6 cursor-default transition-all duration-500 hover:border-transparent hover:-translate-y-2 hover:shadow-2xl"
            :class="feature.hoverBorder"
            :style="{ animationDelay: `${i * 0.1}s` }">
            <!-- Glow effect on hover -->
            <div :class="['absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500', feature.glowBg]"></div>
            <div :class="['absolute -top-20 -right-20 w-40 h-40 rounded-full blur-3xl opacity-0 group-hover:opacity-30 transition-all duration-500 group-hover:scale-150', feature.glowColor]"></div>
            
            <div class="relative flex flex-col items-center text-center">
              <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center mb-5 transition-all duration-500 group-hover:scale-110 group-hover:rotate-3 group-hover:shadow-lg', feature.bgClass, feature.shadowClass]">
                <i :class="[feature.icon, feature.iconClass, 'text-2xl transition-transform duration-500 group-hover:scale-110']"></i>
              </div>
              <h3 class="font-bold text-lg mb-2 text-white group-hover:text-white transition-colors">{{ feature.title }}</h3>
              <p class="text-dark-400 text-sm leading-relaxed group-hover:text-dark-300 transition-colors">{{ feature.desc }}</p>
              
              <!-- Arrow indicator -->
              <div class="mt-4 flex items-center text-sm font-medium opacity-0 group-hover:opacity-100 transition-all duration-300" :class="feature.iconClass">
                <span>了解更多</span>
                <i class="fas fa-arrow-right ml-2 text-xs"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Section -->
    <div class="relative z-10 py-24 border-t border-white/5">
      <div class="max-w-5xl mx-auto px-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div v-for="(stat, i) in stats" :key="stat.label" 
            class="group relative text-center p-6 rounded-2xl transition-all duration-500 hover:bg-dark-800/50 cursor-default"
            :style="{ animationDelay: `${i * 0.15}s` }">
            <!-- Animated background -->
            <div class="absolute inset-0 rounded-2xl bg-gradient-to-br opacity-0 group-hover:opacity-10 transition-opacity duration-500" :class="stat.gradient"></div>
            
            <div class="relative">
              <div class="text-5xl font-bold mb-3 transition-all duration-500 group-hover:scale-110 group-hover:-translate-y-1" :class="stat.textClass">
                {{ stat.value }}
              </div>
              <div class="text-dark-400 font-medium group-hover:text-dark-300 transition-colors">{{ stat.label }}</div>
            </div>
            
            <!-- Bottom line animation -->
            <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-0.5 rounded-full group-hover:w-16 transition-all duration-500" :class="stat.lineClass"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="relative z-10 py-8 border-t border-white/5">
      <div class="max-w-7xl mx-auto px-6 text-center text-dark-500 text-sm">
        <p>© 2024 GameDev Hub. 为游戏开发者打造</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
const features = [
  { 
    icon: 'fas fa-book', 
    title: 'Wiki 文档', 
    desc: '支持 Markdown，实时预览，团队知识库', 
    bgClass: 'bg-gradient-to-br from-cyan-500/30 to-blue-500/20', 
    iconClass: 'text-cyan-400',
    shadowClass: 'group-hover:shadow-cyan-500/30',
    hoverBorder: 'hover:border-cyan-500/30',
    glowBg: 'bg-gradient-to-br from-cyan-500/5 to-transparent',
    glowColor: 'bg-cyan-500'
  },
  { 
    icon: 'fas fa-comments', 
    title: '实时聊天', 
    desc: '群聊私聊，即时沟通，高效协作', 
    bgClass: 'bg-gradient-to-br from-emerald-500/30 to-teal-500/20', 
    iconClass: 'text-emerald-400',
    shadowClass: 'group-hover:shadow-emerald-500/30',
    hoverBorder: 'hover:border-emerald-500/30',
    glowBg: 'bg-gradient-to-br from-emerald-500/5 to-transparent',
    glowColor: 'bg-emerald-500'
  },
  { 
    icon: 'fas fa-lightbulb', 
    title: '想法卡片', 
    desc: '灵感记录，标签分类，创意管理', 
    bgClass: 'bg-gradient-to-br from-amber-500/30 to-orange-500/20', 
    iconClass: 'text-amber-400',
    shadowClass: 'group-hover:shadow-amber-500/30',
    hoverBorder: 'hover:border-amber-500/30',
    glowBg: 'bg-gradient-to-br from-amber-500/5 to-transparent',
    glowColor: 'bg-amber-500'
  },
  { 
    icon: 'fas fa-robot', 
    title: 'AI 助手', 
    desc: '智能对话，创意激发，效率倍增', 
    bgClass: 'bg-gradient-to-br from-blue-500/30 to-blue-600/20', 
    iconClass: 'text-blue-400',
    shadowClass: 'group-hover:shadow-blue-500/30',
    hoverBorder: 'hover:border-blue-500/30',
    glowBg: 'bg-gradient-to-br from-blue-500/5 to-transparent',
    glowColor: 'bg-blue-500'
  }
]

const stats = [
  { value: '∞', label: '无限创意', textClass: 'bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent', gradient: 'from-cyan-500 to-blue-500', lineClass: 'bg-gradient-to-r from-cyan-500 to-blue-500' },
  { value: '24/7', label: '随时协作', textClass: 'bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent', gradient: 'from-emerald-500 to-teal-500', lineClass: 'bg-gradient-to-r from-emerald-500 to-teal-500' },
  { value: '100%', label: '免费使用', textClass: 'bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent', gradient: 'from-amber-500 to-orange-500', lineClass: 'bg-gradient-to-r from-amber-500 to-orange-500' },
  { value: '🚀', label: '极速体验', textClass: '', gradient: 'from-blue-500 to-blue-600', lineClass: 'bg-gradient-to-r from-blue-500 to-blue-600' }
]
</script>
