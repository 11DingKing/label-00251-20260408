<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 bg-amber-500/20 rounded-xl flex items-center justify-center">
          <i class="fas fa-lightbulb text-amber-400 text-xl"></i>
        </div>
        <div>
          <h1 class="text-2xl font-bold">想法卡片</h1>
          <p class="text-dark-400">捕捉每一个灵感</p>
        </div>
      </div>
      <router-link to="/ideas/new" class="btn-primary flex items-center justify-center space-x-2">
        <i class="fas fa-plus"></i>
        <span>新建想法</span>
      </router-link>
    </div>

    <!-- Tags Filter -->
    <div v-if="tags.length" class="flex flex-wrap gap-2 mb-6">
      <button @click="currentTag = ''" 
        :class="['px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200',
          !currentTag ? 'bg-amber-500 text-white shadow-lg shadow-amber-500/30' : 'bg-dark-800/50 text-dark-400 hover:bg-dark-700/50 hover:text-white']">
        全部
      </button>
      <button v-for="tag in tags" :key="tag" @click="currentTag = tag"
        :class="['px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200',
          currentTag === tag ? 'bg-amber-500 text-white shadow-lg shadow-amber-500/30' : 'bg-dark-800/50 text-dark-400 hover:bg-dark-700/50 hover:text-white']">
        {{ tag }}
      </button>
    </div>

    <!-- Ideas Grid -->
    <div v-if="ideas.length" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <router-link v-for="(idea, i) in ideas" :key="idea.id" :to="`/ideas/${idea.id}`"
        :class="['card p-5 border transition-all duration-300 hover:scale-[1.02] hover-glow relative group', ideaClass(idea.color)]"
        :style="{ animationDelay: `${i * 0.03}s` }">
        <!-- Pin Badge -->
        <div v-if="idea.is_pinned" class="absolute top-3 right-3">
          <div class="w-8 h-8 bg-amber-500/20 rounded-lg flex items-center justify-center">
            <i class="fas fa-thumbtack text-amber-400 text-sm"></i>
          </div>
        </div>

        <h3 class="font-semibold text-lg mb-2 pr-10">{{ idea.title }}</h3>
        <p class="text-dark-400 text-sm line-clamp-3 mb-4">{{ idea.content }}</p>
        
        <div class="flex items-center justify-between text-xs text-dark-500">
          <div class="flex items-center space-x-2">
            <div class="w-5 h-5 bg-dark-700 rounded flex items-center justify-center text-[10px]">
              {{ idea.author?.username?.[0]?.toUpperCase() }}
            </div>
            <span>{{ idea.author?.username }}</span>
          </div>
          <span>{{ formatDate(idea.created_at) }}</span>
        </div>

        <!-- Tags -->
        <div v-if="idea.tags" class="flex flex-wrap gap-1 mt-3">
          <span v-for="t in idea.tags.split(',').slice(0, 3)" :key="t" 
            class="px-2 py-0.5 bg-dark-700/50 rounded text-xs text-dark-400">
            {{ t.trim() }}
          </span>
        </div>
      </router-link>
    </div>

    <!-- Empty State -->
    <div v-else class="card p-16 text-center">
      <div class="w-20 h-20 bg-dark-800 rounded-2xl flex items-center justify-center mx-auto mb-6">
        <i class="fas fa-lightbulb text-dark-600 text-3xl"></i>
      </div>
      <h3 class="text-xl font-semibold mb-2">还没有想法</h3>
      <p class="text-dark-400 mb-6">记录你的第一个灵感</p>
      <router-link to="/ideas/new" class="btn-primary inline-flex items-center space-x-2">
        <i class="fas fa-plus"></i>
        <span>新建想法</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '../../api'

const ideas = ref([])
const tags = ref([])
const currentTag = ref('')

const ideaClass = (color) => ({
  blue: 'idea-blue',
  green: 'idea-green',
  yellow: 'idea-yellow',
  red: 'idea-red',
  pink: 'idea-pink'
}[color] || 'bg-dark-800/50 border-dark-700')

const formatDate = (d) => new Date(d).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })

async function load() {
  const params = currentTag.value ? { tag: currentTag.value } : {}
  const { data } = await api.get('/ideas', { params })
  ideas.value = data.ideas
  tags.value = data.tags
}

watch(currentTag, load)
onMounted(load)
</script>
