<template>
  <div class="mx-auto max-w-md space-y-6">
    <div class="neo-hero p-6 text-center">
      <p class="neo-label">{{ $t('login.label') }}</p>
      <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white">{{ $t('login.title') }}</h1>
      <p class="mt-2 text-neo-muted">{{ $t('login.subtitle') }}</p>
    </div>

    <Card>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="neo-label mb-2 block">{{ $t('login.usernameOrEmail') }}</label>
          <Input v-model="form.identifier" :class="{ 'ring-2 ring-red-500/50': errors.identifier }" />
          <p v-if="errors.identifier" class="mt-1 text-sm text-red-400">{{ errors.identifier }}</p>
        </div>

        <div>
          <label class="neo-label mb-2 block">{{ $t('login.password') }}</label>
          <Input v-model="form.password" type="password" :class="{ 'ring-2 ring-red-500/50': errors.password }" />
          <p v-if="errors.password" class="mt-1 text-sm text-red-400">{{ errors.password }}</p>
        </div>

        <Button type="submit" :disabled="loading" class="w-full">
          {{ loading ? $t('login.signingIn') : $t('login.signIn') }}
        </Button>

        <p v-if="error" class="text-center text-sm text-red-400">{{ error }}</p>
      </form>
    </Card>
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

const { t, locale } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const form = reactive({ identifier: '', password: '' })
const errors = reactive<Record<string, string>>({})
const loading = ref(false)
const error = ref('')

function validate() {
  Object.keys(errors).forEach((key) => delete errors[key])
  let valid = true
  if (!form.identifier.trim()) {
    errors.identifier = t('login.identifierRequired')
    valid = false
  }
  if (!form.password) {
    errors.password = t('login.passwordRequired')
    valid = false
  }
  return valid
}

async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  error.value = ''
  try {
    await auth.login({ username_or_email: form.identifier.trim(), password: form.password })
    const loc = (route.params.locale as string) ?? locale.value
    if (auth.mustChangePassword) {
      router.push({ name: 'ChangePassword', params: { locale: loc } })
    } else {
      router.push({ name: 'Home', params: { locale: loc } })
    }
  } catch (e: any) {
    error.value = e.response?.data?.detail || t('login.failed')
  } finally {
    loading.value = false
  }
}
</script>
