<template>
  <div class="flex flex-col lg:flex-row gap-6">
    <!-- Main Content -->
    <div class="flex-1 min-w-0">
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

        <!-- Diff Mode Indicator -->
        <div v-if="selectedRevision" class="mb-4 p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg flex items-center justify-between">
          <div class="flex items-center gap-2 text-amber-400">
            <i class="fas fa-history"></i>
            <span>正在查看与版本 #{{ selectedRevision.id }} 的对比（{{ formatDate(selectedRevision.created_at) }}）</span>
          </div>
          <button @click="clearDiff" class="btn-ghost text-sm text-amber-400 hover:bg-amber-500/10">
            <i class="fas fa-times mr-1"></i>关闭对比
          </button>
        </div>

        <!-- Content -->
        <div class="card p-8 md:p-10">
          <div v-if="diffHtml" class="markdown-body" v-html="diffHtml"></div>
          <div v-else class="markdown-body" v-html="page.html"></div>
        </div>
      </div>

      <!-- Loading -->
      <div v-else class="flex items-center justify-center py-20">
        <div class="w-12 h-12 border-4 border-dark-700 border-t-cyan-500 rounded-full animate-spin"></div>
      </div>
    </div>

    <!-- History Sidebar -->
    <div class="w-full lg:w-80 flex-shrink-0">
      <div class="card p-4 sticky top-4">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-lg flex items-center gap-2">
            <i class="fas fa-history text-cyan-400"></i>
            历史版本
          </h3>
          <button @click="loadRevisions" class="text-dark-400 hover:text-cyan-400 transition-colors" :disabled="loadingRevisions">
            <i class="fas fa-sync-alt" :class="{ 'fa-spin': loadingRevisions }"></i>
          </button>
        </div>

        <div v-if="loadingRevisions" class="flex items-center justify-center py-8">
          <div class="w-6 h-6 border-2 border-dark-700 border-t-cyan-500 rounded-full animate-spin"></div>
        </div>

        <div v-else-if="revisions.length === 0" class="text-center py-8 text-dark-400">
          <i class="fas fa-folder-open text-2xl mb-2"></i>
          <p>暂无历史版本</p>
        </div>

        <div v-else class="space-y-2 max-h-96 overflow-y-auto">
          <div
            v-for="(revision, index) in revisions"
            :key="revision.id"
            class="p-3 rounded-lg border transition-all cursor-pointer"
            :class="[
              selectedRevision?.id === revision.id 
                ? 'border-cyan-500 bg-cyan-500/10' 
                : 'border-dark-700 hover:border-dark-600 hover:bg-dark-800/50'
            ]"
            @click="selectRevision(revision)"
          >
            <div class="flex items-center justify-between mb-1">
              <span class="text-sm font-medium">
                {{ index === 0 ? '当前版本' : `版本 #${revision.id}` }}
              </span>
              <span v-if="index === 0" class="text-xs px-2 py-0.5 bg-cyan-500/20 text-cyan-400 rounded">
                最新
              </span>
            </div>
            <div class="flex items-center gap-2 text-xs text-dark-400">
              <div class="w-4 h-4 bg-gradient-to-br from-cyan-400 to-blue-500 rounded flex items-center justify-center text-white text-xs">
                {{ revision.editor?.username?.[0]?.toUpperCase() }}
              </div>
              <span>{{ revision.editor?.username }}</span>
              <span>•</span>
              <span>{{ formatDate(revision.created_at) }}</span>
            </div>
            
            <!-- Rollback Button -->
            <div v-if="index !== 0" class="mt-2 pt-2 border-t border-dark-700">
              <button
                @click.stop="rollbackToRevision(revision)"
                class="w-full text-xs text-amber-400 hover:text-amber-300 hover:bg-amber-500/10 px-2 py-1 rounded transition-colors flex items-center justify-center gap-1"
                :disabled="rollingBack === revision.id"
              >
                <i class="fas fa-undo" :class="{ 'fa-spin': rollingBack === revision.id }"></i>
                <span>{{ rollingBack === revision.id ? '回滚中...' : '回滚到此版本' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api'
import { diff_match_patch } from 'diff-match-patch'

const route = useRoute()
const router = useRouter()
const showToast = inject('showToast')
const page = ref(null)
const revisions = ref([])
const selectedRevision = ref(null)
const loadingRevisions = ref(false)
const rollingBack = ref(null)
const diffHtml = ref('')

const dmp = new diff_match_patch()

const formatDate = (d) => new Date(d).toLocaleString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })

onMounted(async () => {
  await loadPage()
  await loadRevisions()
})

async function loadPage() {
  const { data } = await api.get(`/wiki/${route.params.slug}`)
  page.value = data
}

async function loadRevisions() {
  loadingRevisions.value = true
  try {
    const { data } = await api.get(`/wiki/${route.params.slug}/revisions`)
    revisions.value = data
  } catch (error) {
    console.error('Failed to load revisions:', error)
    showToast('加载历史版本失败', 'error')
  } finally {
    loadingRevisions.value = false
  }
}

function selectRevision(revision) {
  if (selectedRevision.value?.id === revision.id) {
    clearDiff()
    return
  }
  
  selectedRevision.value = revision
  generateDiff(revision)
}

function clearDiff() {
  selectedRevision.value = null
  diffHtml.value = ''
}

function generateDiff(revision) {
  if (!page.value) return
  
  const oldText = revision.content
  const newText = page.value.content
  
  const diffs = dmp.diff_main(oldText, newText)
  dmp.diff_cleanupSemantic(diffs)
  
  diffHtml.value = diffsToHtml(diffs)
}

function diffsToHtml(diffs) {
  let html = ''
  for (const [type, text] of diffs) {
    const escapedText = escapeHtml(text)
    if (type === -1) {
      html += `<span class="bg-rose-500/30 text-rose-300 line-through decoration-rose-400">${escapedText}</span>`
    } else if (type === 1) {
      html += `<span class="bg-emerald-500/30 text-emerald-300">${escapedText}</span>`
    } else {
      html += escapedText
    }
  }
  return html.replace(/\n/g, '<br>')
}

function escapeHtml(text) {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

async function rollbackToRevision(revision) {
  if (!confirm(`确定要回滚到版本 #${revision.id} 吗？当前版本将被保存为历史记录。`)) {
    return
  }
  
  rollingBack.value = revision.id
  try {
    await api.post(`/wiki/${route.params.slug}/revisions/${revision.id}/rollback`)
    showToast('已成功回滚到历史版本')
    await loadPage()
    await loadRevisions()
    clearDiff()
  } catch (error) {
    console.error('Failed to rollback:', error)
    showToast('回滚失败', 'error')
  } finally {
    rollingBack.value = null
  }
}

async function deletePage() {
  if (!confirm('确定删除此文档？此操作不可撤销。')) return
  await api.delete(`/wiki/${route.params.slug}`)
  showToast('文档已删除')
  router.push('/wiki')
}
</script>

<style scoped>
.markdown-body {
  line-height: 1.8;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
  line-height: 1.4;
}

.markdown-body :deep(h1) { font-size: 2em; }
.markdown-body :deep(h2) { font-size: 1.5em; }
.markdown-body :deep(h3) { font-size: 1.25em; }

.markdown-body :deep(p) {
  margin-bottom: 1em;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  margin-bottom: 1em;
  padding-left: 2em;
}

.markdown-body :deep(li) {
  margin-bottom: 0.25em;
}

.markdown-body :deep(code) {
  background: rgba(0, 0, 0, 0.3);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'Fira Code', monospace;
}

.markdown-body :deep(pre) {
  background: rgba(0, 0, 0, 0.3);
  padding: 1em;
  border-radius: 8px;
  overflow-x: auto;
  margin-bottom: 1em;
}

.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
}

.markdown-body :deep(blockquote) {
  border-left: 4px solid rgba(255, 255, 255, 0.1);
  padding-left: 1em;
  margin: 1em 0;
  color: rgba(255, 255, 255, 0.7);
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1em;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.5em 1em;
  text-align: left;
}

.markdown-body :deep(th) {
  background: rgba(0, 0, 0, 0.2);
}

.markdown-body :deep(a) {
  color: #22d3ee;
  text-decoration: none;
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

.markdown-body :deep(hr) {
  border: none;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin: 2em 0;
}

.markdown-body :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}
</style>
