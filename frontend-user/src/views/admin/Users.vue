<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
      <div>
        <router-link to="/admin" class="inline-flex items-center text-dark-400 hover:text-cyan-400 text-sm mb-2 transition-colors">
          <i class="fas fa-arrow-left mr-2"></i>返回管理后台
        </router-link>
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-cyan-500/20 rounded-xl flex items-center justify-center">
            <i class="fas fa-users text-cyan-400 text-xl"></i>
          </div>
          <div>
            <h1 class="text-2xl font-bold">用户管理</h1>
            <p class="text-dark-400">共 {{ users.length }} 位用户</p>
          </div>
        </div>
      </div>
      <button @click="openModal()" class="btn-primary flex items-center space-x-2">
        <i class="fas fa-plus"></i>
        <span>添加用户</span>
      </button>
    </div>
    
    <!-- Users Table -->
    <div class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="bg-dark-800/50 border-b border-dark-700/50">
              <th class="px-6 py-4 text-left text-sm font-medium text-dark-400">用户</th>
              <th class="px-6 py-4 text-left text-sm font-medium text-dark-400 hidden sm:table-cell">邮箱</th>
              <th class="px-6 py-4 text-left text-sm font-medium text-dark-400">角色</th>
              <th class="px-6 py-4 text-right text-sm font-medium text-dark-400">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-dark-700/50">
            <tr v-for="user in users" :key="user.id" class="hover:bg-dark-800/30 transition-colors">
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-full flex items-center justify-center text-sm font-bold mr-3">
                    {{ user.username[0].toUpperCase() }}
                  </div>
                  <div>
                    <span class="font-medium">{{ user.username }}</span>
                    <p class="text-xs text-dark-500 sm:hidden">{{ user.email }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-dark-400 hidden sm:table-cell">{{ user.email }}</td>
              <td class="px-6 py-4">
                <span :class="['inline-flex items-center px-3 py-1 rounded-lg text-xs font-medium',
                  user.is_admin ? 'bg-amber-500/20 text-amber-400' : 'bg-dark-700 text-dark-400']">
                  <i :class="[user.is_admin ? 'fas fa-crown' : 'fas fa-user', 'mr-1.5 text-[10px]']"></i>
                  {{ user.is_admin ? '管理员' : '成员' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <template v-if="user.id !== auth.user?.id">
                  <div class="flex items-center justify-end gap-2">
                    <button @click="openModal(user)" class="px-3 py-1.5 bg-dark-700 hover:bg-dark-600 rounded-lg text-sm transition-colors">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="toggleAdmin(user)" 
                      class="px-3 py-1.5 bg-dark-700 hover:bg-dark-600 rounded-lg text-sm transition-colors"
                      :title="user.is_admin ? '撤销管理员' : '设为管理员'">
                      <i :class="user.is_admin ? 'fas fa-user' : 'fas fa-crown'"></i>
                    </button>
                    <button @click="deleteUser(user)" 
                      class="px-3 py-1.5 bg-rose-500/20 hover:bg-rose-500/30 text-rose-400 rounded-lg text-sm transition-colors">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </template>
                <span v-else class="text-dark-500 text-sm flex items-center justify-end">
                  <i class="fas fa-user-check mr-1.5"></i>当前用户
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Empty State -->
      <div v-if="!users.length" class="text-center py-16">
        <div class="w-16 h-16 bg-dark-800 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <i class="fas fa-users text-dark-600 text-2xl"></i>
        </div>
        <p class="text-dark-500">暂无用户</p>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="showModal = false">
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>
          <div class="relative w-full max-w-md card p-6 space-y-5">
            <div class="flex items-center justify-between">
              <h3 class="text-xl font-bold">{{ editingUser ? '编辑用户' : '添加用户' }}</h3>
              <button @click="showModal = false" class="text-dark-400 hover:text-white">
                <i class="fas fa-times"></i>
              </button>
            </div>

            <form @submit.prevent="saveUser" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-dark-300 mb-1.5">用户名</label>
                <input v-model="form.username" type="text" required :disabled="!!editingUser"
                  class="w-full px-4 py-3 bg-dark-800 border border-dark-600 rounded-xl focus:outline-none focus:border-cyan-500 disabled:opacity-50"
                  placeholder="输入用户名">
              </div>

              <div>
                <label class="block text-sm font-medium text-dark-300 mb-1.5">邮箱</label>
                <input v-model="form.email" type="email" required
                  class="w-full px-4 py-3 bg-dark-800 border border-dark-600 rounded-xl focus:outline-none focus:border-cyan-500"
                  placeholder="输入邮箱">
              </div>

              <div>
                <label class="block text-sm font-medium text-dark-300 mb-1.5">
                  {{ editingUser ? '新密码（留空不修改）' : '密码' }}
                </label>
                <input v-model="form.password" type="password" :required="!editingUser"
                  class="w-full px-4 py-3 bg-dark-800 border border-dark-600 rounded-xl focus:outline-none focus:border-cyan-500"
                  placeholder="输入密码">
              </div>

              <div class="flex items-center space-x-3">
                <input v-model="form.is_admin" type="checkbox" id="is_admin" class="w-4 h-4 rounded">
                <label for="is_admin" class="text-sm text-dark-300">设为管理员</label>
              </div>

              <div v-if="error" class="p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400 text-sm">
                {{ error }}
              </div>

              <div class="flex justify-end space-x-3 pt-2">
                <button type="button" @click="showModal = false" class="px-5 py-2.5 bg-dark-700 hover:bg-dark-600 rounded-xl transition-colors">
                  取消
                </button>
                <button type="submit" :disabled="saving" class="btn-primary">
                  <i v-if="saving" class="fas fa-spinner fa-spin mr-2"></i>
                  {{ saving ? '保存中...' : '保存' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import api from '../../api'

const auth = useAuthStore()
const showToast = inject('showToast')
const users = ref([])
const showModal = ref(false)
const editingUser = ref(null)
const saving = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  email: '',
  password: '',
  is_admin: false
})

async function load() {
  const { data } = await api.get('/admin/users')
  users.value = data
}

onMounted(load)

function openModal(user = null) {
  editingUser.value = user
  error.value = ''
  if (user) {
    form.username = user.username
    form.email = user.email
    form.password = ''
    form.is_admin = user.is_admin
  } else {
    form.username = ''
    form.email = ''
    form.password = ''
    form.is_admin = false
  }
  showModal.value = true
}

async function saveUser() {
  saving.value = true
  error.value = ''
  try {
    if (editingUser.value) {
      await api.put(`/admin/users/${editingUser.value.id}`, form)
      showToast('用户已更新')
    } else {
      await api.post('/admin/users', form)
      showToast('用户已创建')
    }
    showModal.value = false
    load()
  } catch (e) {
    error.value = e.response?.data?.error || '操作失败'
  } finally {
    saving.value = false
  }
}

async function toggleAdmin(user) {
  await api.post(`/admin/users/${user.id}/toggle-admin`)
  showToast(user.is_admin ? '已撤销管理员权限' : '已设为管理员')
  load()
}

async function deleteUser(user) {
  if (!confirm(`确定删除用户 ${user.username}？此操作不可撤销。`)) return
  await api.delete(`/admin/users/${user.id}`)
  showToast('用户已删除')
  load()
}
</script>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .card, .modal-leave-to .card { transform: scale(0.95); }
</style>
