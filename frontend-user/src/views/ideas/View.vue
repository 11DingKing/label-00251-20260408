<template>
  <div v-if="idea">
    <!-- Idea Card -->
    <div :class="['card p-8 border mb-6', ideaClass(idea.color)]">
      <div class="flex items-start justify-between mb-6">
        <router-link to="/ideas" class="text-dark-400 hover:text-cyan-400 transition-colors text-sm">
          <i class="fas fa-arrow-left mr-2"></i>返回
        </router-link>
        <div class="flex items-center space-x-2">
          <router-link :to="`/ideas/${idea.id}/edit`" class="btn-ghost">
            <i class="fas fa-edit"></i>
          </router-link>
          <button @click="deleteIdea" class="btn-ghost text-rose-400 hover:bg-rose-500/10">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>

      <h1 class="text-2xl md:text-3xl font-bold mb-4">{{ idea.title }}</h1>
      <p class="text-dark-200 whitespace-pre-wrap text-lg leading-relaxed">{{ idea.content }}</p>

      <div class="flex items-center justify-between mt-8 pt-6 border-t border-white/10">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center text-white font-medium">
            {{ idea.author?.username?.[0]?.toUpperCase() }}
          </div>
          <div>
            <p class="font-medium">{{ idea.author?.username }}</p>
            <p class="text-sm text-dark-500">{{ formatDate(idea.created_at) }}</p>
          </div>
        </div>
      </div>

      <!-- Tags -->
      <div v-if="idea.tags" class="flex flex-wrap gap-2 mt-6">
        <router-link v-for="t in idea.tags.split(',')" :key="t" :to="`/ideas?tag=${t.trim()}`"
          class="px-3 py-1.5 bg-dark-700/50 hover:bg-dark-600/50 rounded-lg text-sm transition-colors">
          <i class="fas fa-tag text-dark-500 mr-1 text-xs"></i>{{ t.trim() }}
        </router-link>
      </div>
    </div>

    <!-- Comments -->
    <div class="card p-6">
      <h2 class="font-semibold text-lg mb-6 flex items-center space-x-2">
        <i class="fas fa-comments text-dark-500"></i>
        <span>评论 ({{ idea.comments?.length || 0 }})</span>
      </h2>

      <div v-if="idea.comments?.length" class="space-y-4 mb-6">
        <div v-for="c in idea.comments" :key="c.id" class="flex space-x-3 animate-fade-in">
          <div class="w-9 h-9 bg-dark-700 rounded-lg flex items-center justify-center text-sm flex-shrink-0">
            {{ c.author?.username?.[0]?.toUpperCase() }}
          </div>
          <div class="flex-1 bg-dark-800/50 rounded-xl p-4">
            <div class="flex items-center space-x-2 mb-2">
              <span class="font-medium text-sm">{{ c.author?.username }}</span>
              <span class="text-xs text-dark-500">{{ formatDate(c.created_at) }}</span>
            </div>
            <p class="text-dark-300">{{ c.content }}</p>
          </div>
        </div>
      </div>

      <form @submit.prevent="addComment" class="flex gap-3">
        <input v-model="comment" placeholder="添加评论..." required class="input-modern flex-1">
        <button type="submit" :disabled="!comment.trim()" class="btn-primary px-6">
          <i class="fas fa-paper-plane"></i>
        </button>
      </form>
    </div>
  </div>

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
const idea = ref(null)
const comment = ref('')

const ideaClass = (color) => ({
  blue: 'idea-blue',
  green: 'idea-green',
  yellow: 'idea-yellow',
  red: 'idea-red',
  pink: 'idea-pink'
}[color] || 'bg-dark-800/50 border-dark-700')

const formatDate = (d) => new Date(d).toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })

async function load() {
  const { data } = await api.get(`/ideas/${route.params.id}`)
  idea.value = data
}

onMounted(load)

async function deleteIdea() {
  if (!confirm('确定删除这个想法？')) return
  await api.delete(`/ideas/${route.params.id}`)
  showToast('想法已删除')
  router.push('/ideas')
}

async function addComment() {
  if (!comment.value.trim()) return
  await api.post(`/ideas/${route.params.id}/comments`, { content: comment.value })
  comment.value = ''
  showToast('评论已添加')
  load()
}
</script>
