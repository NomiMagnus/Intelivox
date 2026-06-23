<template>
  <div class="space-y-6">
    <div class="neo-hero p-6">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p class="neo-label">{{ $t('userManagement.label') }}</p>
          <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white">{{ $t('userManagement.title') }}</h1>
          <p class="mt-2 text-neo-muted">{{ $t('userManagement.subtitle') }}</p>
        </div>
        <div class="flex w-full max-w-md flex-col gap-3 sm:flex-row sm:items-center">
          <Input v-model="searchTerm" :placeholder="$t('userManagement.searchPlaceholder')" @keyup.enter="load" />
          <Button @click="load">{{ $t('userManagement.search') }}</Button>
        </div>
      </div>
    </div>

    <!-- Create user (admin only) -->
    <Card v-if="auth.isAdmin">
      <h2 class="text-xl font-semibold text-white">{{ $t('userManagement.createTitle') }}</h2>
      <p class="mt-1 text-sm text-neo-muted">{{ $t('userManagement.createHint') }}</p>
      <form @submit.prevent="handleCreate" class="mt-4 grid gap-4 sm:grid-cols-2">
        <div>
          <label class="neo-label mb-2 block">{{ $t('userManagement.idNumber') }}</label>
          <Input v-model="newUser.id_number" :class="{ 'ring-2 ring-red-500/50': errors.id_number }" />
          <p v-if="errors.id_number" class="mt-1 text-sm text-red-400">{{ errors.id_number }}</p>
        </div>
        <div>
          <label class="neo-label mb-2 block">{{ $t('userManagement.username') }}</label>
          <Input v-model="newUser.username" :class="{ 'ring-2 ring-red-500/50': errors.username }" />
          <p v-if="errors.username" class="mt-1 text-sm text-red-400">{{ errors.username }}</p>
        </div>
        <div>
          <label class="neo-label mb-2 block">{{ $t('userManagement.firstName') }}</label>
          <Input v-model="newUser.first_name" />
        </div>
        <div>
          <label class="neo-label mb-2 block">{{ $t('userManagement.lastName') }}</label>
          <Input v-model="newUser.last_name" />
        </div>
        <div>
          <label class="neo-label mb-2 block">{{ $t('userManagement.email') }}</label>
          <Input v-model="newUser.email" type="email" :class="{ 'ring-2 ring-red-500/50': errors.email }" />
          <p v-if="errors.email" class="mt-1 text-sm text-red-400">{{ errors.email }}</p>
        </div>
        <div>
          <label class="neo-label mb-2 block">{{ $t('userManagement.phone') }}</label>
          <Input v-model="newUser.phone" />
        </div>
        <div>
          <label class="neo-label mb-2 block">{{ $t('userManagement.department') }}</label>
          <Input v-model="newUser.department" />
        </div>
        <div>
          <label class="neo-label mb-2 block">{{ $t('userManagement.role') }}</label>
          <select v-model="newUser.role" class="neo-select">
            <option v-for="role in roles" :key="role.code" :value="role.code">{{ role.name || role.code }}</option>
          </select>
        </div>
        <div class="sm:col-span-2">
          <Button type="submit" :disabled="creating">{{ creating ? $t('userManagement.creating') : $t('userManagement.create') }}</Button>
          <p class="mt-2 text-sm text-neo-muted">{{ $t('userManagement.genericPasswordNote') }}</p>
        </div>
      </form>
    </Card>

    <!-- Users list -->
    <Card>
      <div class="flex flex-wrap items-center justify-between gap-3">
        <h2 class="text-xl font-semibold text-white">{{ $t('userManagement.listTitle') }}</h2>
        <Button variant="secondary" @click="load">{{ $t('userManagement.reload') }}</Button>
      </div>

      <div v-if="loading" class="neo-inset mt-4 p-6 text-neo-muted">{{ $t('userManagement.loading') }}</div>
      <div v-else-if="users.length === 0" class="neo-inset mt-4 p-6 text-neo-muted">{{ $t('userManagement.empty') }}</div>

      <div v-else class="mt-4 grid gap-4 md:grid-cols-2">
        <div v-for="u in users" :key="u.id" class="neo-raised p-4">
          <div class="flex items-start justify-between gap-3">
            <div>
              <h3 class="text-lg font-semibold text-white">
                {{ [u.first_name, u.last_name].filter(Boolean).join(' ') || u.username }}
              </h3>
              <p class="text-sm text-neo-muted">@{{ u.username }} · {{ u.id_number }}</p>
            </div>
            <span
              class="neo-inset rounded-full px-3 py-1 text-xs"
              :class="u.status === 'active' ? 'text-green-300' : 'text-red-300'"
            >{{ $t('userManagement.status_' + u.status) }}</span>
          </div>
          <div class="mt-3 space-y-1 text-sm text-neo-muted">
            <p class="flex items-center gap-3"><i class="pi pi-envelope" /> {{ u.email }}</p>
            <p v-if="u.phone" class="flex items-center gap-3"><i class="pi pi-phone" /> {{ u.phone }}</p>
            <p v-if="u.department" class="flex items-center gap-3"><i class="pi pi-building" /> {{ u.department }}</p>
            <p class="flex items-center gap-3">
              <i class="pi pi-id-card" />
              <span class="flex flex-wrap gap-1">
                <span v-for="r in u.roles" :key="r.id" class="neo-inset rounded-full px-2 py-0.5 text-xs">
                  {{ r.name || r.code }}
                </span>
                <span v-if="u.roles.length === 0">—</span>
              </span>
            </p>
          </div>
          <div v-if="auth.isAdmin" class="mt-4 flex flex-wrap gap-2">
            <Button variant="secondary" @click="openEdit(u)">{{ $t('userManagement.edit') }}</Button>
            <Button v-if="u.status === 'active'" variant="secondary" @click="confirmDeactivate(u)">
              {{ $t('userManagement.deactivate') }}
            </Button>
          </div>
        </div>
      </div>
    </Card>

    <!-- Edit modal -->
    <div v-if="editing" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm" @click.self="editing = null">
      <div class="neo-raised w-full max-w-lg p-6">
        <h2 class="mb-4 text-xl font-semibold text-white">{{ $t('userManagement.editTitle') }}</h2>
        <div class="grid gap-4 sm:grid-cols-2">
          <div>
            <label class="neo-label mb-2 block">{{ $t('userManagement.idNumber') }}</label>
            <Input v-model="editForm.id_number" />
          </div>
          <div>
            <label class="neo-label mb-2 block">{{ $t('userManagement.username') }}</label>
            <Input v-model="editForm.username" />
          </div>
          <div>
            <label class="neo-label mb-2 block">{{ $t('userManagement.firstName') }}</label>
            <Input v-model="editForm.first_name" />
          </div>
          <div>
            <label class="neo-label mb-2 block">{{ $t('userManagement.lastName') }}</label>
            <Input v-model="editForm.last_name" />
          </div>
          <div>
            <label class="neo-label mb-2 block">{{ $t('userManagement.email') }}</label>
            <Input v-model="editForm.email" type="email" />
          </div>
          <div>
            <label class="neo-label mb-2 block">{{ $t('userManagement.phone') }}</label>
            <Input v-model="editForm.phone" />
          </div>
          <div>
            <label class="neo-label mb-2 block">{{ $t('userManagement.department') }}</label>
            <Input v-model="editForm.department" />
          </div>
        </div>
        <div class="mt-6 flex flex-col gap-3 sm:flex-row">
          <Button :disabled="savingEdit" @click="saveEdit">{{ savingEdit ? $t('userManagement.saving') : $t('common.confirm') }}</Button>
          <Button variant="secondary" @click="editing = null">{{ $t('common.cancel') }}</Button>
        </div>
      </div>
    </div>

    <Toast v-if="toast.message" :message="toast.message" :type="toast.type" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../stores/auth'
import type { Role, User } from '../types'
import * as userService from '../services/user.service'
import Input from '../components/ui/Input.vue'
import Button from '../components/ui/Button.vue'
import Card from '../components/ui/Card.vue'
import Toast from '../components/ui/Toast.vue'

const { t } = useI18n()
const auth = useAuthStore()

const users = ref<User[]>([])
const roles = ref<Role[]>([])
const searchTerm = ref('')
const loading = ref(false)

const newUser = reactive({
  id_number: '',
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  department: '',
  role: 'user',
})
const errors = reactive<Record<string, string>>({})
const creating = ref(false)

const editing = ref<User | null>(null)
const editForm = reactive<Record<string, string>>({})
const savingEdit = ref(false)

const toast = reactive({ message: '', type: 'info' as 'success' | 'error' | 'info' })

function notify(message: string, type: 'success' | 'error' | 'info' = 'info') {
  toast.message = ''
  // force re-trigger of the Toast watcher even for repeated messages
  requestAnimationFrame(() => {
    toast.message = message
    toast.type = type
  })
}

async function load() {
  loading.value = true
  try {
    users.value = await userService.fetchUsers(searchTerm.value.trim() || undefined)
  } catch (e: any) {
    notify(e.response?.data?.detail || t('userManagement.loadError'), 'error')
  } finally {
    loading.value = false
  }
}

async function loadRoles() {
  try {
    roles.value = await userService.fetchRoles()
  } catch {
    roles.value = []
  }
}

function validateCreate() {
  Object.keys(errors).forEach((key) => delete errors[key])
  let valid = true
  if (!newUser.id_number.trim()) {
    errors.id_number = t('userManagement.idRequired')
    valid = false
  }
  if (!newUser.username.trim()) {
    errors.username = t('userManagement.usernameRequired')
    valid = false
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newUser.email)) {
    errors.email = t('userManagement.emailFormat')
    valid = false
  }
  return valid
}

async function handleCreate() {
  if (!validateCreate()) return
  creating.value = true
  try {
    await userService.createUser({
      id_number: newUser.id_number.trim(),
      username: newUser.username.trim(),
      email: newUser.email.trim(),
      first_name: newUser.first_name || undefined,
      last_name: newUser.last_name || undefined,
      phone: newUser.phone || undefined,
      department: newUser.department || undefined,
      role_codes: [newUser.role],
    })
    notify(t('userManagement.createSuccess'), 'success')
    Object.assign(newUser, {
      id_number: '', username: '', first_name: '', last_name: '', email: '', phone: '', department: '', role: 'user',
    })
    await load()
  } catch (e: any) {
    notify(e.response?.data?.detail || t('userManagement.createError'), 'error')
  } finally {
    creating.value = false
  }
}

function openEdit(u: User) {
  editing.value = u
  Object.assign(editForm, {
    id_number: u.id_number ?? '',
    username: u.username ?? '',
    first_name: u.first_name ?? '',
    last_name: u.last_name ?? '',
    email: u.email ?? '',
    phone: u.phone ?? '',
    department: u.department ?? '',
  })
}

async function saveEdit() {
  if (!editing.value) return
  savingEdit.value = true
  try {
    await userService.updateUser(editing.value.id, { ...editForm } as Partial<User>)
    notify(t('userManagement.updateSuccess'), 'success')
    editing.value = null
    await load()
  } catch (e: any) {
    notify(e.response?.data?.detail || t('userManagement.updateError'), 'error')
  } finally {
    savingEdit.value = false
  }
}

async function confirmDeactivate(u: User) {
  if (!window.confirm(t('userManagement.deactivateConfirm'))) return
  try {
    await userService.deleteUser(u.id)
    notify(t('userManagement.deactivateSuccess'), 'success')
    await load()
  } catch (e: any) {
    notify(e.response?.data?.detail || t('userManagement.deactivateError'), 'error')
  }
}

onMounted(() => {
  load()
  loadRoles()
})
</script>
