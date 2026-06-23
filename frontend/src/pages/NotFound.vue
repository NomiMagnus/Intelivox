<template>
  <div class="flex min-h-full flex-1 items-center justify-center py-12">
    <div class="neo-hero w-full max-w-xl p-8 text-center lg:p-12">
      <p class="neo-label">{{ content.label }}</p>
      <h1 class="mt-3 text-6xl font-semibold tracking-tight text-white lg:text-7xl">
        {{ content.code }}
      </h1>
      <h2 class="mt-4 text-xl font-semibold text-white lg:text-2xl">{{ content.title }}</h2>
      <p class="mx-auto mt-3 max-w-md text-neo-muted">{{ content.message }}</p>

      <div class="mt-8 flex flex-col justify-center gap-3 sm:flex-col">
        <Button @click="goHome">{{ $t('errors.backToHome') }}</Button>
        <Button variant="secondary" @click="goBack">{{ $t('errors.goBack') }}</Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import Button from '../components/ui/Button.vue'
import { resolvePreferredLocale } from '../stores/locale'
import { isSupportedLocale } from '../i18n'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const forbidden = computed(() => route.meta.forbidden === true)

const content = computed(() =>
  forbidden.value
    ? {
        label: t('errors.forbiddenLabel'),
        code: t('errors.forbiddenCode'),
        title: t('errors.forbiddenTitle'),
        message: t('errors.forbiddenBody'),
      }
    : {
        label: t('errors.notFoundLabel'),
        code: t('errors.notFoundCode'),
        title: t('errors.notFoundTitle'),
        message: t('errors.notFoundBody'),
      },
)

const locale = computed(() =>
  isSupportedLocale(route.params.locale) ? route.params.locale : resolvePreferredLocale(),
)

function goHome() {
  router.push({ name: 'Home', params: { locale: locale.value } })
}

function goBack() {
  if (window.history.length > 1) {
    router.back()
  } else {
    goHome()
  }
}
</script>
