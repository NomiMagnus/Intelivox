<template>
  <div class="space-y-6">
    <div class="rounded-3xl border border-white/10 bg-slate-950/90 p-6 shadow-xl shadow-black/20">
      <h1 class="text-3xl font-semibold text-white">Update Resident</h1>
      <p class="mt-2 text-slate-400">Update resident details by mobile phone</p>
    </div>

    <Card>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">First Name *</label>
          <Input v-model="form.firstName" :class="{ 'border-red-500': errors.firstName }" />
          <p v-if="errors.firstName" class="text-sm text-red-400 mt-1">{{ errors.firstName }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Last Name *</label>
          <Input v-model="form.lastName" :class="{ 'border-red-500': errors.lastName }" />
          <p v-if="errors.lastName" class="text-sm text-red-400 mt-1">{{ errors.lastName }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Mobile Phone *</label>
          <Input v-model="form.mobilePhone" :class="{ 'border-red-500': errors.mobilePhone }" />
          <p v-if="errors.mobilePhone" class="text-sm text-red-400 mt-1">{{ errors.mobilePhone }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Home Phone</label>
          <Input v-model="form.homePhone" :class="{ 'border-red-500': errors.homePhone }" />
          <p v-if="errors.homePhone" class="text-sm text-red-400 mt-1">{{ errors.homePhone }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Email</label>
          <Input v-model="form.email" type="email" :class="{ 'border-red-500': errors.email }" />
          <p v-if="errors.email" class="text-sm text-red-400 mt-1">{{ errors.email }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Type *</label>
          <select v-model="form.type" class="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-2 text-white">
            <option value="individual">Individual</option>
            <option value="organization">Organization</option>
            <option value="institution">Institution</option>
          </select>
        </div>

        <div class="flex gap-3 pt-4">
          <Button type="submit" :disabled="loading">{{ loading ? 'Updating...' : 'Update Resident' }}</Button>
          <Button type="button" variant="secondary" @click="resetForm">Clear</Button>
        </div>

        <p v-if="error" class="text-sm text-red-400">{{ error }}</p>
      </form>
    </Card>

    <Toast v-if="toast.message" :message="toast.message" :type="toast.type" />

    <div v-if="showConfirmation" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showConfirmation = false">
      <div class="rounded-3xl border border-white/10 bg-slate-950 p-6 shadow-xl max-w-md w-full mx-4">
        <h2 class="text-xl font-semibold text-white mb-4">Confirm Update</h2>
        <p class="text-slate-300 mb-6">Are you sure you want to update this resident?</p>
        <div class="flex gap-3">
          <Button @click="confirmUpdate">Confirm</Button>
          <Button variant="secondary" @click="showConfirmation = false">Cancel</Button>
        </div>
      </div>
    </div>

    <div v-if="showNotFound" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showNotFound = false">
      <div class="rounded-3xl border border-white/10 bg-slate-950 p-6 shadow-xl max-w-md w-full mx-4">
        <h2 class="text-xl font-semibold text-white mb-4">Resident Not Found</h2>
        <p class="text-slate-300 mb-6">No resident found with this mobile phone. Would you like to add a new resident?</p>
        <div class="flex gap-3">
          <Button @click="confirmCreate">Add New Resident</Button>
          <Button variant="secondary" @click="showNotFound = false">Cancel</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { updateResidentByPhone, createResident, searchResidents } from '../services/resident.service'
import Input from '../components/ui/Input.vue'
import Button from '../components/ui/Button.vue'
import Card from '../components/ui/Card.vue'
import Toast from '../components/ui/Toast.vue'

const form = reactive({
  firstName: '',
  lastName: '',
  mobilePhone: '',
  homePhone: '',
  email: '',
  type: 'individual',
  status: 'active'
})

const errors = reactive<Record<string, string>>({})
const showConfirmation = ref(false)
const showNotFound = ref(false)
const loading = ref(false)
const error = ref('')
const toast = reactive({ message: '', type: 'info' as 'success' | 'error' | 'info' })

function validateForm() {
  Object.keys(errors).forEach(key => delete errors[key])
  let valid = true

  if (!form.firstName.trim()) {
    errors.firstName = 'First name is required'
    valid = false
  } else if (form.firstName.length > 128) {
    errors.firstName = 'First name must be less than 128 characters'
    valid = false
  }

  if (!form.lastName.trim()) {
    errors.lastName = 'Last name is required'
    valid = false
  } else if (form.lastName.length > 128) {
    errors.lastName = 'Last name must be less than 128 characters'
    valid = false
  }

  if (!form.mobilePhone.trim()) {
    errors.mobilePhone = 'Mobile phone is required'
    valid = false
  } else if (!/^[+0-9()\-\s]{7,32}$/.test(form.mobilePhone)) {
    errors.mobilePhone = 'Invalid phone format (7-32 characters, +0-9()-space)'
    valid = false
  }

  if (form.homePhone && !/^[+0-9()\-\s]{7,32}$/.test(form.homePhone)) {
    errors.homePhone = 'Invalid phone format (7-32 characters, +0-9()-space)'
    valid = false
  }

  if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Invalid email format'
    valid = false
  }

  return valid
}

function handleSubmit() {
  if (validateForm()) {
    showConfirmation.value = true
  }
}

async function confirmUpdate() {
  showConfirmation.value = false
  loading.value = true
  error.value = ''

  try {
    const residents = await searchResidents(form.mobilePhone)
    if (residents.length === 0) {
      loading.value = false
      showNotFound.value = true
      return
    }

    await updateResidentByPhone(form.mobilePhone, {
      first_name: form.firstName,
      last_name: form.lastName,
      mobile_phone: form.mobilePhone,
      home_phone: form.homePhone || null,
      email: form.email || null,
      type: form.type,
      status: form.status
    })
    toast.message = 'Resident updated successfully!'
    toast.type = 'success'
    resetForm()
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to update resident'
    toast.message = error.value
    toast.type = 'error'
  } finally {
    loading.value = false
  }
}

async function confirmCreate() {
  showNotFound.value = false
  loading.value = true
  error.value = ''

  try {
    await createResident({
      first_name: form.firstName,
      last_name: form.lastName,
      mobile_phone: form.mobilePhone,
      home_phone: form.homePhone || null,
      email: form.email || null,
      type: form.type,
      status: form.status
    })
    toast.message = 'Resident created successfully!'
    toast.type = 'success'
    resetForm()
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to create resident'
    toast.message = error.value
    toast.type = 'error'
  } finally {
    loading.value = false
  }
}

function resetForm() {
  form.firstName = ''
  form.lastName = ''
  form.mobilePhone = ''
  form.homePhone = ''
  form.email = ''
  form.type = 'individual'
  form.status = 'active'
  Object.keys(errors).forEach(key => delete errors[key])
  error.value = ''
}
</script>
