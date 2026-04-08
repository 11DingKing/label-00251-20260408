<template>
  <div>
    <!-- Header with gradient background -->
    <div class="mb-10">
      <router-link to="/admin" class="group inline-flex items-center text-dark-400 hover:text-cyan-400 text-sm mb-4 transition-all duration-300">
        <i class="fas fa-arrow-left mr-2 group-hover:-translate-x-1 transition-transform"></i>返回管理后台
      </router-link>
      <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-600/20 via-blue-700/10 to-blue-600/20 p-8 border border-blue-500/20">
        <div class="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
        <div class="absolute bottom-0 left-0 w-48 h-48 bg-blue-500/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>
        <div class="relative flex items-center space-x-5">
          <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/30">
            <i class="fas fa-robot text-white text-2xl"></i>
          </div>
          <div>
            <h1 class="text-3xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">AI 服务设置</h1>
            <p class="text-dark-400 mt-1">配置 AI 服务提供商的 API，开启智能对话</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="grid gap-6">
      <div v-for="i in 3" :key="i" class="card p-8 animate-pulse">
        <div class="flex items-center mb-8">
          <div class="w-14 h-14 bg-dark-700 rounded-2xl mr-5"></div>
          <div class="flex-1">
            <div class="h-6 bg-dark-700 rounded-lg w-28 mb-3"></div>
            <div class="h-4 bg-dark-700 rounded w-40"></div>
          </div>
          <div class="w-12 h-6 bg-dark-700 rounded-full"></div>
        </div>
        <div class="grid md:grid-cols-2 gap-5">
          <div class="h-12 bg-dark-700 rounded-xl"></div>
          <div class="h-12 bg-dark-700 rounded-xl"></div>
        </div>
      </div>
    </div>

    <!-- Provider Cards -->
    <div v-else class="grid gap-6">
      <div v-for="(p, i) in providers" :key="p.id" 
        class="group relative overflow-hidden rounded-2xl bg-dark-800/80 backdrop-blur-sm border border-dark-700/50 p-8 transition-all duration-500 hover:border-blue-500/30 hover:shadow-xl hover:shadow-blue-500/5"
        :class="{ 'ring-2 ring-emerald-500/50 border-emerald-500/30': settings[p.id].is_enabled }"
        :style="{ animationDelay: `${i * 0.1}s` }">
        
        <!-- Background glow effect -->
        <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
          <div :class="['absolute top-0 right-0 w-32 h-32 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2', p.glowClass]"></div>
        </div>
        
        <!-- Active indicator -->
        <div v-if="settings[p.id].is_enabled" class="absolute top-4 right-4">
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full mr-2 animate-pulse"></span>
            运行中
          </span>
        </div>
        
        <div class="relative">
          <!-- Provider Header -->
          <div class="flex items-center justify-between mb-8">
            <div class="flex items-center">
              <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center mr-5 transition-transform duration-300 group-hover:scale-110', p.bgClass]">
                <i :class="[p.icon, p.iconClass, 'text-2xl']"></i>
              </div>
              <div>
                <h3 class="font-bold text-xl text-white">{{ p.name }}</h3>
                <p class="text-sm text-dark-400 mt-0.5">{{ p.desc }}</p>
              </div>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="settings[p.id].is_enabled" class="sr-only peer">
              <div class="w-14 h-7 bg-dark-600 rounded-full peer peer-checked:after:translate-x-7 after:content-[''] after:absolute after:top-[3px] after:left-[3px] after:bg-white after:rounded-full after:h-[22px] after:w-[22px] after:transition-all after:shadow-md peer-checked:bg-gradient-to-r peer-checked:from-emerald-500 peer-checked:to-teal-500"></div>
            </label>
          </div>
          
          <!-- Form Fields -->
          <div class="grid md:grid-cols-2 gap-5">
            <div class="space-y-2">
              <label class="flex items-center text-sm font-medium text-dark-300">
                <i class="fas fa-key mr-2 text-dark-500"></i>API Key
              </label>
              <div class="relative group/input">
                <input :type="showKey[p.id] ? 'text' : 'password'" v-model="settings[p.id].api_key" 
                  :placeholder="p.placeholder" 
                  class="w-full px-4 py-3.5 bg-dark-700/50 border border-dark-600 rounded-xl text-white placeholder-dark-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all pr-12">
                <button type="button" @click="showKey[p.id] = !showKey[p.id]"
                  class="absolute right-4 top-1/2 -translate-y-1/2 text-dark-500 hover:text-blue-400 transition-colors">
                  <i :class="showKey[p.id] ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
            </div>
            
            <div class="space-y-2">
              <label class="flex items-center text-sm font-medium text-dark-300">
                <i class="fas fa-microchip mr-2 text-dark-500"></i>模型选择
              </label>
              <select v-model="settings[p.id].model" 
                class="w-full px-4 py-3.5 bg-dark-700/50 border border-dark-600 rounded-xl text-white focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all appearance-none cursor-pointer"
                style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 24 24%27 fill=%27none%27 stroke=%27%236b7280%27 stroke-width=%272%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpolyline points=%276 9 12 15 18 9%27%3e%3c/polyline%3e%3c/svg%3e'); background-repeat: no-repeat; background-position: right 1rem center; background-size: 1em;">
                <option v-for="m in p.models" :key="m" :value="m" class="bg-dark-800">{{ m }}</option>
              </select>
            </div>
          </div>
          
          <!-- Action Button -->
          <div class="mt-8 flex justify-end">
            <button @click="save(p.id)" :disabled="saving[p.id]"
              class="relative px-8 py-3 bg-gradient-to-r from-blue-600 to-blue-600 rounded-xl font-semibold text-white transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/30 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-none overflow-hidden group/btn">
              <span class="absolute inset-0 bg-gradient-to-r from-blue-500 to-blue-500 opacity-0 group-hover/btn:opacity-100 transition-opacity"></span>
              <span class="relative flex items-center">
                <i :class="saving[p.id] ? 'fas fa-circle-notch fa-spin' : 'fas fa-save'" class="mr-2"></i>
                {{ saving[p.id] ? '保存中...' : '保存配置' }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Info Box -->
    <div class="mt-8 relative overflow-hidden rounded-2xl bg-gradient-to-br from-amber-500/10 to-orange-500/5 border border-amber-500/20 p-6">
      <div class="absolute top-0 right-0 w-32 h-32 bg-amber-500/10 rounded-full blur-3xl"></div>
      <div class="relative flex items-start space-x-4">
        <div class="w-12 h-12 bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg shadow-amber-500/20">
          <i class="fas fa-lightbulb text-white text-lg"></i>
        </div>
        <div>
          <h4 class="font-semibold text-amber-300 text-lg mb-2">使用提示</h4>
          <ul class="text-sm text-dark-300 space-y-2">
            <li class="flex items-start">
              <i class="fas fa-check text-amber-500/70 mr-2 mt-1 text-xs"></i>
              <span>同一时间只能启用一个 AI 服务提供商</span>
            </li>
            <li class="flex items-start">
              <i class="fas fa-check text-amber-500/70 mr-2 mt-1 text-xs"></i>
              <span>API Key 将被安全加密存储在服务器</span>
            </li>
            <li class="flex items-start">
              <i class="fas fa-check text-amber-500/70 mr-2 mt-1 text-xs"></i>
              <span>启用新服务会自动禁用其他服务</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted } from 'vue'
import api from '../../api'

const showToast = inject('showToast')

const providers = [
  { id: 'openai', name: 'OpenAI', desc: 'GPT-4o, GPT-4 Turbo, GPT-3.5', icon: 'fas fa-brain', bgClass: 'bg-gradient-to-br from-emerald-500/30 to-teal-500/20', iconClass: 'text-emerald-400', glowClass: 'bg-emerald-500/20', placeholder: 'sk-...', models: ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo'] },
  { id: 'anthropic', name: 'Anthropic', desc: 'Claude 4, Claude 3.5 Sonnet/Haiku', icon: 'fas fa-robot', bgClass: 'bg-gradient-to-br from-orange-500/30 to-amber-500/20', iconClass: 'text-orange-400', glowClass: 'bg-orange-500/20', placeholder: 'sk-ant-...', models: ['claude-sonnet-4-20250514', 'claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022', 'claude-3-opus-20240229'] },
  { id: 'google', name: 'Google AI', desc: 'Gemini 2.0 Flash, Gemini 1.5 Pro', icon: 'fab fa-google', bgClass: 'bg-gradient-to-br from-blue-500/30 to-cyan-500/20', iconClass: 'text-blue-400', glowClass: 'bg-blue-500/20', placeholder: 'AIza...', models: ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-1.5-flash'] }
]

const settings = reactive({
  openai: { api_key: '', model: 'gpt-4o-mini', is_enabled: false },
  anthropic: { api_key: '', model: 'claude-3-5-sonnet-20241022', is_enabled: false },
  google: { api_key: '', model: 'gemini-2.0-flash', is_enabled: false }
})

const showKey = reactive({ openai: false, anthropic: false, google: false })
const saving = ref({})
const loading = ref(true)

function syncSettings(data) {
  providers.forEach(p => {
    if (data[p.id]) Object.assign(settings[p.id], data[p.id])
  })
}

onMounted(async () => {
  try {
    const { data } = await api.get('/admin/ai-settings')
    syncSettings(data)
  } catch (e) {
    console.error('Failed to load AI settings:', e)
  } finally {
    loading.value = false
  }
})

async function save(provider) {
  saving.value[provider] = true
  try {
    await api.post('/admin/ai-settings', { provider, ...settings[provider] })
    const { data } = await api.get('/admin/ai-settings')
    syncSettings(data)
    showToast('设置已保存')
  } catch (e) {
    showToast('保存失败')
  } finally {
    saving.value[provider] = false
  }
}
</script>
