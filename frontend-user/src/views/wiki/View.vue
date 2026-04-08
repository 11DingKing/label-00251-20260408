<template>
  <div v-if="page">
    <!-- Breadcrumb & Actions -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
      <div class="flex items-center space-x-2 text-sm min-w-0">
        <router-link to="/wiki" class="text-dark-400 hover:text-cyan-400 transition-colors flex-shrink-0">
          <i class="fas fa-book mr-1"></i>Wiki
        </router-link>
        <i class="fas fa-chevron-right text-dark-600 text-xs flex-shrink-0"></i>
        <span class="text-dark-400 truncate">{{ page.category }}</span>
      </div>
      <div class="flex items-center space-x-2 flex-shrink-0">
        <router-link :to="`/wiki/${page.slug}/edit`" class="btn-ghost flex items-center space-x-2">
          <i class="fas fa-edit"></i>
          <span>编辑</span>
        </router-link>
        <button @click="deletePage" class="btn-ghost text-rose-400 hover:bg-rose-500/10 flex items-center space-x-2">
          <i class="fas fa-trash"></i>
          <span class="hidden sm:inline">删除</span>
        </button>
      </div>
    </div>

    <!-- Title -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-bold mb-3">{{ page.title }}</h1>
      <div class="flex flex-wrap items-center gap-4 text-sm text-dark-400">
        <span class="flex items-center gap-2">
          <div class="w-6 h-6 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-md flex items-center justify-center text-white text-xs">
            {{ page.author?.username?.[0]?.toUpperCase() }}
          </div>
          <span>{{ page.author?.username }}</span>
        </span>
        <span class="flex items-center gap-1.5">
          <i class="fas fa-clock text-xs"></i>
          <span>更新于 {{ formatDate(page.updated_at) }}</span>
        </span>
        <span class="px-3 py-1 rounded-lg bg-dark-800/50 text-xs leading-none">{{ page.category }}</span>
      </div>
    </div>

    <!-- Content -->
    <div class="card p-8 md:p-10">
      <div class="markdown-body" v-html="page.html"></div>
    </div>
  </div>

  <!-- Loading -->
  <div v-else class="flex items-center justify-center py-20">
    <div class="w-12 h-12 border-4 border-dark-700 border-t-cyan-500 rounded-full animate-spin"></div>
  </div>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api'

const route = useRoute()
const router = useRouter()
const showToast = inject('showToast')
const page = ref(null)

const formatDate = (d) => new Date(d).toLocaleString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })

onMounted(async () => {
  const { data } = await api.get(`/wiki/${route.params.slug}`)
  page.value = data
})

async function deletePage() {
  if (!confirm('确定删除此文档？此操作不可撤销。')) return
  await api.delete(`/wiki/${route.params.slug}`)
  showToast('文档已删除')
  router.push('/wiki')
}
</script>
