<template>
  <div class="space-y-6">
    <div class="neo-hero p-6">
      <p class="neo-label">Management</p>
      <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white">Update Resident</h1>
      <p class="mt-2 text-neo-muted">Update resident details by mobile phone</p>
    </div>

    <Card>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="neo-label mb-2 block">First Name *</label>
          <Input v-model="form.firstName" :class="{ 'ring-2 ring-red-500/50': errors.firstName }" />
          <p v-if="errors.firstName" class="mt-1 text-sm text-red-400">{{ errors.firstName }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">Last Name *</label>
          <Input v-model="form.lastName" :class="{ 'ring-2 ring-red-500/50': errors.lastName }" />
          <p v-if="errors.lastName" class="mt-1 text-sm text-red-400">{{ errors.lastName }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">Mobile Phone *</label>
          <Input v-model="form.mobilePhone" :class="{ 'ring-2 ring-red-500/50': errors.mobilePhone }" />
          <p v-if="errors.mobilePhone" class="mt-1 text-sm text-red-400">{{ errors.mobilePhone }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">Home Phone</label>
          <Input v-model="form.homePhone" :class="{ 'ring-2 ring-red-500/50': errors.homePhone }" />
          <p v-if="errors.homePhone" class="mt-1 text-sm text-red-400">{{ errors.homePhone }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">Email</label>
          <Input v-model="form.email" type="email" :class="{ 'ring-2 ring-red-500/50': errors.email }" />
          <p v-if="errors.email" class="mt-1 text-sm text-red-400">{{ errors.email }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">Type *</label>
          <select v-model="form.type" class="neo-select">
            <option value="individual">Individual</option>
            <option value="organization">Organization</option>
            <option value="institution">Institution</option>
          </select>
        </div>

        <div class="flex flex-col gap-3 pt-4 sm:flex-row">
          <Button type="submit" :disabled="loading">{{ loading ? 'Updating...' : 'Update Resident' }}</Button>
          <Button type="button" variant="secondary" @click="resetForm">Clear</Button>
        </div>

        <p v-if="error" class="text-sm text-red-400">{{ error }}</p>
      </form>
    </Card>

    <Toast v-if="toast.message" :message="toast.message" :type="toast.type" />

    <div v-if="showConfirmation" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm" @click.self="showConfirmation = false">
      <div class="neo-raised w-full max-w-md p-6">
        <h2 class="mb-4 text-xl font-semibold text-white">Confirm Update</h2>
        <p class="mb-6 text-neo-muted">Are you sure you want to update this resident?</p>
        <div class="flex flex-col gap-3 sm:flex-row">
          <Button @click="confirmUpdate">Confirm</Button>
          <Button variant="secondary" @click="showConfirmation = false">Cancel</Button>
        </div>
      </div>
    </div>

    <div v-if="showNotFound" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm" @click.self="showNotFound = false">
      <div class="neo-raised w-full max-w-md p-6">
        <h2 class="mb-4 text-xl font-semibold text-white">Resident Not Found</h2>
        <p class="mb-6 text-neo-muted">No resident found with this mobile phone. Would you like to add a new resident?</p>
        <div class="flex flex-col gap-3 sm:flex-row">
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
