<template>
  <div class="space-y-6">
    <div class="neo-hero p-6">
      <p class="neo-label">{{ $t('settings.label') }}</p>
      <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white">{{ $t('settings.title') }}</h1>
      <p class="mt-2 text-neo-muted">{{ $t('settings.subtitle') }}</p>
    </div>

    <div class="grid gap-4 lg:grid-cols-2 lg:gap-6">
      <Card>
        <h2 class="text-xl font-semibold text-white">{{ $t('settings.general') }}</h2>
        <div class="mt-4 space-y-4">
          <div class="space-y-2">
            <label class="neo-label">{{ $t('settings.language') }}</label>
            <select :value="currentLocale" @change="onLocaleChange" class="neo-select mt-1">
              <option v-for="loc in SUPPORTED_LOCALES" :key="loc" :value="loc">
                {{ $t(`common.languageName.${loc}`) }}
              </option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="neo-label">{{ $t('settings.themeMode') }}</label>
            <select class="neo-select mt-1">
              <option>{{ $t('settings.dark') }}</option>
              <option>{{ $t('settings.light') }}</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="neo-label">{{ $t('settings.dataRefresh') }}</label>
            <select class="neo-select mt-1">
              <option>{{ $t('settings.manual') }}</option>
              <option>{{ $t('settings.auto') }}</option>
            </select>
          </div>
        </div>
      </Card>

      <Card>
        <h2 class="text-xl font-semibold text-white">{{ $t('settings.notifications') }}</h2>
        <div class="mt-4 space-y-4">
          <label class="flex items-center gap-4 text-sm text-neo-muted">
            <input type="checkbox" class="h-5 w-5 rounded border-white/10 bg-neo-bg text-neo-accent focus:ring-neo-accent/30" checked />
            {{ $t('settings.enableAlerts') }}
          </label>
          <label class="flex items-center gap-4 text-sm text-neo-muted">
            <input type="checkbox" class="h-5 w-5 rounded border-white/10 bg-neo-bg text-neo-accent focus:ring-neo-accent/30" />
            {{ $t('settings.receiveEmail') }}
          </label>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import Card from '../components/ui/Card.vue'
import { SUPPORTED_LOCALES, isSupportedLocale, type Locale } from '../i18n'
import { useLocaleStore } from '../stores/locale'

const route = useRoute()
const router = useRouter()
const { locale } = useI18n()
const localeStore = useLocaleStore()

const currentLocale = computed(() => locale.value as Locale)

function onLocaleChange(event: Event) {
  const next = (event.target as HTMLSelectElement).value
  if (!isSupportedLocale(next) || next === currentLocale.value) return

  // Persist immediately; the router guard applies i18n + direction on navigation.
  localeStore.setLocale(next)
  router.push({
    name: (route.name as string) ?? 'UserArea',
    params: { ...route.params, locale: next },
    query: route.query,
  })
}
</script>
