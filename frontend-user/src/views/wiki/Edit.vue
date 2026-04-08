<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">{{ isEdit ? '编辑文档' : '新建文档' }}</h1>
      <router-link :to="isEdit ? `/wiki/${$route.params.slug}` : '/wiki'" class="btn-ghost">
        <i class="fas fa-times mr-2"></i>取消
      </router-link>
    </div>

    <form @submit.prevent="save" class="space-y-6">
      <div class="grid md:grid-cols-4 gap-4 items-end">
        <div class="md:col-span-3">
          <label class="block text-sm font-medium text-dark-300 mb-2">标题</label>
          <input v-model="title" required placeholder="文档标题" class="input-modern">
        </div>
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-2">分类</label>
          <input v-model="category" placeholder="未分类" class="input-modern">
        </div>
      </div>

      <div>
        <div class="flex items-center justify-between mb-2">
          <label class="text-sm font-medium text-dark-300">内容 (支持 Markdown)</label>
          <div class="flex items-center space-x-2">
            <button type="button" @click="insertMarkdown('**', '**')" class="btn-ghost text-xs px-2 py-1">
              <i class="fas fa-bold"></i>
            </button>
            <button type="button" @click="insertMarkdown('*', '*')" class="btn-ghost text-xs px-2 py-1">
              <i class="fas fa-italic"></i>
            </button>
            <button type="button" @click="insertMarkdown('`', '`')" class="btn-ghost text-xs px-2 py-1">
              <i class="fas fa-code"></i>
            </button>
            <button type="button" @click="insertMarkdown('- ', '')" class="btn-ghost text-xs px-2 py-1">
              <i class="fas fa-list"></i>
            </button>
            <div class="w-px h-4 bg-dark-700"></div>
            <button type="button" @click="showPreview = !showPreview" 
              :class="['btn-ghost text-xs px-3 py-1', showPreview ? 'text-cyan-400' : '']">
              <i class="fas fa-eye mr-1"></i>预览
            </button>
          </div>
        </div>
        
        <div class="grid md:grid-cols-2 gap-4">
          <div class="relative h-[520px]">
            <textarea ref="editorRef" v-model="content" placeholder="开始写作..."
              class="input-modern font-mono text-sm resize-none w-full h-full" @input="updatePreview"></textarea>
          </div>
          <div v-show="showPreview" class="card p-6 overflow-auto markdown-body h-[520px] text-left">
            <div v-if="previewHtml" v-html="previewHtml"></div>
            <p v-else class="text-dark-500 italic">预览将显示在这里...</p>
          </div>
          <div v-show="!showPreview" class="hidden md:block"></div>
        </div>
      </div>

      <div class="flex items-center justify-end space-x-4 pt-4 border-t border-dark-800">
        <button type="submit" :disabled="saving" class="btn-primary flex items-center space-x-2">
          <i :class="saving ? 'fas fa-spinner fa-spin' : 'fas fa-save'"></i>
          <span>{{ saving ? '保存中...' : '保存文档' }}</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.slug)

const title = ref('')
const content = ref('')
const category = ref('未分类')
const showPreview = ref(true)
const previewHtml = ref('')
const saving = ref(false)
const editorRef = ref(null)

let previewTimeout = null

async function updatePreview() {
  clearTimeout(previewTimeout)
  previewTimeout = setTimeout(async () => {
    if (!content.value.trim()) { 
      previewHtml.value = ''
      return 
    }
    try {
      const { data } = await api.post('/wiki/preview', { content: content.value })
      previewHtml.value = data.html
    } catch (e) {
      console.error('Preview error:', e)
    }
  }, 300)
}

onMounted(async () => {
  if (isEdit.value) {
    const { data } = await api.get(`/wiki/${route.params.slug}`)
    title.value = data.title
    content.value = data.content
    category.value = data.category
    previewHtml.value = data.html
  }
})

function insertMarkdown(before, after) {
  const el = editorRef.value
  const start = el.selectionStart
  const end = el.selectionEnd
  const text = content.value
  const selected = text.substring(start, end)
  content.value = text.substring(0, start) + before + selected + after + text.substring(end)
  setTimeout(() => {
    el.focus()
    el.setSelectionRange(start + before.length, end + before.length)
  }, 0)
}

async function save() {
  saving.value = true
  try {
    if (isEdit.value) {
      await api.put(`/wiki/${route.params.slug}`, { title: title.value, content: content.value, category: category.value })
      router.push(`/wiki/${route.params.slug}`)
    } else {
      const { data } = await api.post('/wiki', { title: title.value, content: content.value, category: category.value })
      router.push(`/wiki/${data.slug}`)
    }
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
</style>
