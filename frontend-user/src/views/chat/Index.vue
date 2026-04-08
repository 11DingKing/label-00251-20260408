<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold"><i class="fas fa-comments text-green-400 mr-2"></i>聊天</h1>
      <div class="flex items-center space-x-4">
        <button @click="showUsers = true" class="px-4 py-2 bg-dark-800 hover:bg-dark-700 rounded-lg transition"><i class="fas fa-user mr-2"></i>私聊</button>
        <button @click="showCreate = true" class="px-4 py-2 bg-accent hover:bg-accent-dark text-dark-950 font-medium rounded-lg transition"><i class="fas fa-plus mr-2"></i>创建聊天室</button>
      </div>
    </div>

    <div class="grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-lg font-semibold mb-4">公开聊天室</h2>
        <div v-if="publicRooms.length" class="space-y-3">
          <router-link v-for="room in publicRooms" :key="room.id" :to="`/chat/room/${room.id}`" class="block bg-dark-900 hover:bg-dark-800 rounded-xl p-4 border border-dark-700 transition">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center mr-3"><i class="fas fa-hashtag text-green-400"></i></div>
              <div>
                <h3 class="font-medium">{{ room.name }}</h3>
                <p class="text-sm text-dark-400">{{ room.description || '暂无描述' }}</p>
              </div>
            </div>
          </router-link>
        </div>
        <div v-else class="bg-dark-900 rounded-xl p-8 border border-dark-700 text-center">
          <i class="fas fa-comments text-dark-600 text-4xl mb-4"></i>
          <p class="text-dark-400">还没有公开聊天室</p>
        </div>
      </div>
      <div>
        <h2 class="text-lg font-semibold mb-4">我加入的聊天室</h2>
        <div v-if="myRooms.length" class="space-y-3">
          <router-link v-for="room in myRooms" :key="room.id" :to="`/chat/room/${room.id}`" class="block bg-dark-900 hover:bg-dark-800 rounded-xl p-4 border border-dark-700 transition">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-accent/20 rounded-lg flex items-center justify-center mr-3"><i :class="['fas', room.is_private ? 'fa-lock' : 'fa-hashtag', 'text-accent']"></i></div>
              <div>
                <h3 class="font-medium">{{ room.name }}</h3>
                <p class="text-sm text-dark-400">{{ room.is_private ? '私密' : '公开' }}</p>
              </div>
            </div>
          </router-link>
        </div>
        <div v-else class="bg-dark-900 rounded-xl p-8 border border-dark-700 text-center">
          <i class="fas fa-door-open text-dark-600 text-4xl mb-4"></i>
          <p class="text-dark-400">还没有加入任何聊天室</p>
        </div>
      </div>
    </div>

    <!-- Create Room Modal -->
    <div v-if="showCreate" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showCreate = false">
      <div class="bg-dark-900 rounded-xl p-6 border border-dark-700 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">创建聊天室</h2>
        <form @submit.prevent="createRoom" class="space-y-4">
          <input v-model="newRoom.name" placeholder="聊天室名称" required class="w-full bg-dark-800 border border-dark-600 rounded-lg px-4 py-3 focus:outline-none focus:border-accent">
          <textarea v-model="newRoom.description" placeholder="描述" rows="3" class="w-full bg-dark-800 border border-dark-600 rounded-lg px-4 py-3 focus:outline-none focus:border-accent resize-none"></textarea>
          <label class="flex items-center"><input type="checkbox" v-model="newRoom.is_private" class="mr-2">设为私密聊天室</label>
          <div class="flex justify-end space-x-4">
            <button type="button" @click="showCreate = false" class="px-4 py-2 text-dark-400">取消</button>
            <button type="submit" class="px-6 py-2 bg-accent hover:bg-accent-dark text-dark-950 font-medium rounded-lg transition">创建</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Users Modal -->
    <div v-if="showUsers" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showUsers = false">
      <div class="bg-dark-900 rounded-xl p-6 border border-dark-700 w-full max-w-md max-h-[80vh] overflow-auto">
        <h2 class="text-xl font-bold mb-4">选择私聊对象</h2>
        <div class="space-y-3">
          <router-link v-for="user in users" :key="user.id" :to="`/chat/private/${user.id}`" class="flex items-center p-3 bg-dark-800 hover:bg-dark-700 rounded-lg transition">
            <div class="w-10 h-10 bg-accent rounded-full flex items-center justify-center text-dark-950 font-medium mr-3">{{ user.username[0].toUpperCase() }}</div>
            <span>{{ user.username }}</span>
          </router-link>
        </div>
        <button @click="showUsers = false" class="mt-4 w-full py-2 bg-dark-800 hover:bg-dark-700 rounded-lg transition">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()
const publicRooms = ref([])
const myRooms = ref([])
const users = ref([])
const showCreate = ref(false)
const showUsers = ref(false)
const newRoom = reactive({ name: '', description: '', is_private: false })

onMounted(async () => {
  const [roomsRes, usersRes] = await Promise.all([api.get('/chat/rooms'), api.get('/chat/users')])
  publicRooms.value = roomsRes.data.public
  myRooms.value = roomsRes.data.my_rooms
  users.value = usersRes.data
})

async function createRoom() {
  const { data } = await api.post('/chat/rooms', newRoom)
  showCreate.value = false
  router.push(`/chat/room/${data.id}`)
}
</script>
