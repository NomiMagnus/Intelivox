<template>
  <div class="space-y-6">
    <div class="neo-hero p-6">
      <p class="neo-label">{{ $t('update.label') }}</p>
      <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white">{{ $t('update.title') }}</h1>
      <p class="mt-2 text-neo-muted">{{ $t('update.subtitle') }}</p>
    </div>

    <Card>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="neo-label mb-2 block">{{ $t('update.firstName') }}</label>
          <Input v-model="form.firstName" :class="{ 'ring-2 ring-red-500/50': errors.firstName }" />
          <p v-if="errors.firstName" class="mt-1 text-sm text-red-400">{{ errors.firstName }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">{{ $t('update.lastName') }}</label>
          <Input v-model="form.lastName" :class="{ 'ring-2 ring-red-500/50': errors.lastName }" />
          <p v-if="errors.lastName" class="mt-1 text-sm text-red-400">{{ errors.lastName }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">{{ $t('update.mobilePhone') }}</label>
          <Input v-model="form.mobilePhone" :class="{ 'ring-2 ring-red-500/50': errors.mobilePhone }" />
          <p v-if="errors.mobilePhone" class="mt-1 text-sm text-red-400">{{ errors.mobilePhone }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">{{ $t('update.homePhone') }}</label>
          <Input v-model="form.homePhone" :class="{ 'ring-2 ring-red-500/50': errors.homePhone }" />
          <p v-if="errors.homePhone" class="mt-1 text-sm text-red-400">{{ errors.homePhone }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">{{ $t('update.email') }}</label>
          <Input v-model="form.email" type="email" :class="{ 'ring-2 ring-red-500/50': errors.email }" />
          <p v-if="errors.email" class="mt-1 text-sm text-red-400">{{ errors.email }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">{{ $t('update.type') }}</label>
          <select v-model="form.type" class="neo-select">
            <option value="individual">{{ $t('update.typeIndividual') }}</option>
            <option value="organization">{{ $t('update.typeOrganization') }}</option>
            <option value="institution">{{ $t('update.typeInstitution') }}</option>
          </select>
        </div>

        <div class="flex flex-col gap-3 pt-4 sm:flex-row">
          <Button type="submit" :disabled="loading">{{ loading ? $t('update.updating') : $t('update.submit') }}</Button>
          <Button type="button" variant="secondary" @click="resetForm">{{ $t('update.clear') }}</Button>
        </div>

        <p v-if="error" class="text-sm text-red-400">{{ error }}</p>
      </form>
    </Card>

    <Toast v-if="toast.message" :message="toast.message" :type="toast.type" />

    <div v-if="showConfirmation" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm" @click.self="showConfirmation = false">
      <div class="neo-raised w-full max-w-md p-6">
        <h2 class="mb-4 text-xl font-semibold text-white">{{ $t('update.confirmTitle') }}</h2>
        <p class="mb-6 text-neo-muted">{{ $t('update.confirmBody') }}</p>
        <div class="flex flex-col gap-3 sm:flex-row">
          <Button @click="confirmUpdate">{{ $t('common.confirm') }}</Button>
          <Button variant="secondary" @click="showConfirmation = false">{{ $t('common.cancel') }}</Button>
        </div>
      </div>
    </div>

    <div v-if="showNotFound" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm" @click.self="showNotFound = false">
      <div class="neo-raised w-full max-w-md p-6">
        <h2 class="mb-4 text-xl font-semibold text-white">{{ $t('update.notFoundTitle') }}</h2>
        <p class="mb-6 text-neo-muted">{{ $t('update.notFoundBody') }}</p>
        <div class="flex flex-col gap-3 sm:flex-row">
          <Button @click="confirmCreate">{{ $t('update.addNew') }}</Button>
          <Button variant="secondary" @click="showNotFound = false">{{ $t('common.cancel') }}</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useI18n } from 'vue-i18n'
import { updateResidentByPhone, createResident, searchResidents } from '../services/resident.service'
import Input from '../components/ui/Input.vue'
import Button from '../components/ui/Button.vue'
import Card from '../components/ui/Card.vue'
import Toast from '../components/ui/Toast.vue'

const { t } = useI18n()

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
    errors.firstName = t('validation.firstNameRequired')
    valid = false
  } else if (form.firstName.length > 128) {
    errors.firstName = t('validation.firstNameMax')
    valid = false
  }

  if (!form.lastName.trim()) {
    errors.lastName = t('validation.lastNameRequired')
    valid = false
  } else if (form.lastName.length > 128) {
    errors.lastName = t('validation.lastNameMax')
    valid = false
  }

  if (!form.mobilePhone.trim()) {
    errors.mobilePhone = t('validation.mobileRequired')
    valid = false
  } else if (!/^[+0-9()\-\s]{7,32}$/.test(form.mobilePhone)) {
    errors.mobilePhone = t('validation.phoneFormat')
    valid = false
  }

  if (form.homePhone && !/^[+0-9()\-\s]{7,32}$/.test(form.homePhone)) {
    errors.homePhone = t('validation.phoneFormat')
    valid = false
  }

  if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = t('validation.emailFormat')
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
    toast.message = t('update.updateSuccess')
    toast.type = 'success'
    resetForm()
  } catch (e: any) {
    error.value = e.response?.data?.detail || t('update.updateError')
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
    toast.message = t('update.createSuccess')
    toast.type = 'success'
    resetForm()
  } catch (e: any) {
    error.value = e.response?.data?.detail || t('update.createError')
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
