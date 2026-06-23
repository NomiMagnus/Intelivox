<template>
  <div class="mx-auto max-w-md space-y-6">
    <div class="neo-hero p-6">
      <p class="neo-label">{{ $t('changePassword.label') }}</p>
      <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white">{{ $t('changePassword.title') }}</h1>
      <p class="mt-2 text-neo-muted">
        {{ auth.mustChangePassword ? $t('changePassword.firstLoginSubtitle') : $t('changePassword.subtitle') }}
      </p>
    </div>

    <Card>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="neo-label mb-2 block">{{ $t('changePassword.currentPassword') }}</label>
          <Input v-model="form.oldPassword" type="password" :class="{ 'ring-2 ring-red-500/50': errors.oldPassword }" />
          <p v-if="errors.oldPassword" class="mt-1 text-sm text-red-400">{{ errors.oldPassword }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">{{ $t('changePassword.newPassword') }}</label>
          <Input v-model="form.newPassword" type="password" :class="{ 'ring-2 ring-red-500/50': errors.newPassword }" />
          <p v-if="errors.newPassword" class="mt-1 text-sm text-red-400">{{ errors.newPassword }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">{{ $t('changePassword.confirmPassword') }}</label>
          <Input v-model="form.confirmPassword" type="password" :class="{ 'ring-2 ring-red-500/50': errors.confirmPassword }" />
          <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-400">{{ errors.confirmPassword }}</p>
        </div>

        <Button type="submit" :disabled="loading" class="w-full">
          {{ loading ? $t('changePassword.saving') : $t('changePassword.submit') }}
        </Button>

        <p v-if="error" class="text-center text-sm text-red-400">{{ error }}</p>
      </form>
    </Card>

    <Toast v-if="toast.message" :message="toast.message" :type="toast.type" />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Input from '../components/ui/Input.vue'
import Button from '../components/ui/Button.vue'
import Card from '../components/ui/Card.vue'
import Toast from '../components/ui/Toast.vue'

const { t, locale } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const form = reactive({ oldPassword: '', newPassword: '', confirmPassword: '' })
const errors = reactive<Record<string, string>>({})
const loading = ref(false)
const error = ref('')
const toast = reactive({ message: '', type: 'info' as 'success' | 'error' | 'info' })

function validate() {
  Object.keys(errors).forEach((key) => delete errors[key])
  let valid = true
  if (!form.oldPassword) {
    errors.oldPassword = t('changePassword.currentRequired')
    valid = false
  }
  if (form.newPassword.length < 8) {
    errors.newPassword = t('changePassword.minLength')
    valid = false
  }
  if (form.newPassword !== form.confirmPassword) {
    errors.confirmPassword = t('changePassword.mismatch')
    valid = false
  }
  return valid
}

async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  error.value = ''
  try {
    await auth.changePassword({ old_password: form.oldPassword, new_password: form.newPassword })
    toast.message = t('changePassword.success')
    toast.type = 'success'
    const loc = (route.params.locale as string) ?? locale.value
    router.push({ name: 'Home', params: { locale: loc } })
  } catch (e: any) {
    error.value = e.response?.data?.detail || t('changePassword.failed')
  } finally {
    loading.value = false
  }
}
</script>
