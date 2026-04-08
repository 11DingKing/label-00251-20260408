<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 bg-cyan-500/20 rounded-xl flex items-center justify-center">
          <i class="fas fa-book text-cyan-400 text-xl"></i>
        </div>
        <div>
          <h1 class="text-2xl font-bold">Wiki 文档</h1>
          <p class="text-dark-400">团队知识库</p>
        </div>
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <div class="relative">
          <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-dark-400"></i>
          <input v-model="search" @input="doSearch" placeholder="搜索文档..." 
            class="w-full sm:w-72 pl-11 pr-4 py-3 bg-dark-800/50 border-2 border-dark-700 rounded-xl text-white placeholder-dark-400 focus:outline-none focus:border-cyan-500/50 focus:bg-dark-800 transition-all duration-300">
        </div>
        <router-link to="/wiki/new" class="btn-primary flex items-center justify-center space-x-2">
          <i class="fas fa-plus"></i>
          <span>新建文档</span>
        </router-link>
      </div>
    </div>

    <!-- Categories -->
    <div v-if="categories.length" class="flex gap-2 mb-6 overflow-x-auto pb-2 scrollbar-hide">
      <button @click="filterCategory = ''" 
        :class="['px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 whitespace-nowrap flex-shrink-0 active:scale-95', 
          !filterCategory ? 'bg-cyan-500 text-white' : 'bg-dark-800/50 text-dark-400']">
        全部
      </button>
      <button v-for="cat in categories" :key="cat" @click="filterCategory = cat"
        :class="['px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 whitespace-nowrap flex-shrink-0 active:scale-95',
          filterCategory === cat ? 'bg-cyan-500 text-white' : 'bg-dark-800/50 text-dark-400']">
        {{ cat }}
      </button>
    </div>

    <!-- Pages Grid -->
    <div v-if="filteredPages.length" class="grid gap-4">
      <router-link v-for="page in filteredPages" :key="page.id" :to="`/wiki/${page.slug}`"
        class="card p-4 sm:p-6 transition-colors active:bg-dark-800/80">
        <div class="flex items-start justify-between gap-3">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-2">
              <h2 class="text-base sm:text-lg font-semibold truncate">{{ page.title }}</h2>
              <span class="px-2 py-0.5 rounded-lg bg-dark-700/50 text-xs text-dark-400 truncate max-w-[100px] flex-shrink-0">{{ page.category }}</span>
            </div>
            <p class="text-dark-400 text-sm line-clamp-2">{{ page.content?.slice(0, 200) }}</p>
            <div class="flex items-center gap-3 mt-3 text-xs text-dark-500">
              <span class="flex items-center gap-1">
                <i class="fas fa-user"></i>
                <span>{{ page.author?.username }}</span>
              </span>
              <span class="flex items-center gap-1">
                <i class="fas fa-clock"></i>
                <span>{{ formatDate(page.updated_at) }}</span>
              </span>
            </div>
          </div>
          <i class="fas fa-chevron-right text-dark-600 mt-1 flex-shrink-0"></i>
        </div>
      </router-link>
    </div>

    <!-- Empty State -->
    <div v-else class="card p-16 text-center">
      <div class="w-20 h-20 bg-dark-800 rounded-2xl flex items-center justify-center mx-auto mb-6">
        <i class="fas fa-book-open text-dark-600 text-3xl"></i>
      </div>
      <h3 class="text-xl font-semibold mb-2">{{ search ? '没有找到相关文档' : '还没有文档' }}</h3>
      <p class="text-dark-400 mb-6">{{ search ? '尝试其他关键词' : '创建第一个文档开始记录' }}</p>
      <router-link v-if="!search" to="/wiki/new" class="btn-primary inline-flex items-center space-x-2">
        <i class="fas fa-plus"></i>
        <span>创建文档</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const pages = ref([])
const categories = ref([])
const search = ref('')
const filterCategory = ref('')
const searchResults = ref(null)

const filteredPages = computed(() => {
  if (searchResults.value) return searchResults.value
  if (!filterCategory.value) return pages.value
  return pages.value.filter(p => p.category === filterCategory.value)
})

const formatDate = (d) => new Date(d).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })

onMounted(async () => {
  const { data } = await api.get('/wiki')
  pages.value = data.pages
  categories.value = data.categories
})

let searchTimeout
async function doSearch() {
  clearTimeout(searchTimeout)
  if (!search.value.trim()) { searchResults.value = null; return }
  searchTimeout = setTimeout(async () => {
    const { data } = await api.get('/wiki/search', { params: { q: search.value } })
    searchResults.value = data
  }, 300)
}
</script>
