<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">{{ isEdit ? '编辑想法' : '新建想法' }}</h1>
      <router-link :to="isEdit ? `/ideas/${$route.params.id}` : '/ideas'" class="btn-ghost">
        <i class="fas fa-times mr-2"></i>取消
      </router-link>
    </div>

    <form @submit.prevent="save" class="card p-8 space-y-6">
      <div>
        <label class="block text-sm font-medium text-dark-300 mb-2">标题</label>
        <input v-model="title" required placeholder="给你的想法起个名字" class="input-modern">
      </div>

      <div>
        <label class="block text-sm font-medium text-dark-300 mb-2">内容</label>
        <textarea v-model="content" rows="6" required placeholder="详细描述你的想法..."
          class="input-modern resize-none"></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-dark-300 mb-3">卡片颜色</label>
        <div class="flex flex-wrap gap-3">
          <button v-for="c in colors" :key="c.value" type="button" @click="color = c.value"
            :class="['w-12 h-12 rounded-xl transition-all duration-200 border-2', c.bg,
              color === c.value ? 'border-white scale-110 shadow-lg' : 'border-transparent hover:scale-105']">
          </button>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-dark-300 mb-2">标签</label>
        <input v-model="tags" placeholder="用逗号分隔，如：角色设计, 战斗系统" class="input-modern">
        <p class="text-xs text-dark-500 mt-2">标签可以帮助你更好地组织想法</p>
      </div>

      <div class="flex justify-end pt-4 border-t border-dark-800">
        <button type="submit" :disabled="saving" class="btn-primary flex items-center space-x-2">
          <i :class="saving ? 'fas fa-spinner fa-spin' : 'fas fa-save'"></i>
          <span>{{ saving ? '保存中...' : '保存想法' }}</span>
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
const isEdit = computed(() => !!route.params.id)

const title = ref('')
const content = ref('')
const color = ref('blue')
const tags = ref('')
const saving = ref(false)

const colors = [
  { value: 'blue', bg: 'bg-blue-500' },
  { value: 'green', bg: 'bg-emerald-500' },
  { value: 'yellow', bg: 'bg-amber-500' },
  { value: 'red', bg: 'bg-rose-500' },
  { value: 'pink', bg: 'bg-pink-500' }
]

onMounted(async () => {
  if (isEdit.value) {
    const { data } = await api.get(`/ideas/${route.params.id}`)
    title.value = data.title
    content.value = data.content
    color.value = data.color
    tags.value = data.tags
  }
})

async function save() {
  saving.value = true
  try {
    const payload = { title: title.value, content: content.value, color: color.value, tags: tags.value }
    if (isEdit.value) {
      await api.put(`/ideas/${route.params.id}`, payload)
      router.push(`/ideas/${route.params.id}`)
    } else {
      const { data } = await api.post('/ideas', payload)
      router.push(`/ideas/${data.id}`)
    }
  } finally {
    saving.value = false
  }
}
</script>
