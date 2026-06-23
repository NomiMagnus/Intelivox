<template>
  <RouterLink
    :to="to"
    class="group flex flex-col items-center gap-1 rounded-neo px-2 py-2 text-center transition duration-200 lg:flex-row lg:gap-3 lg:px-4 lg:py-3 lg:text-start"
    active-class="lg:bg-neo-elevated"
  >
    <span
      :class="[
        'neo-nav-icon text-base',
        isActive ? 'neo-nav-icon-active' : 'group-hover:text-white',
      ]"
    >
      <i :class="icon" aria-hidden="true"></i>
    </span>
    <span class="text-[10px] font-medium text-neo-muted transition group-hover:text-white lg:text-sm" :class="{ 'text-white': isActive }">
      {{ label }}
    </span>
  </RouterLink>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps<{
  name: string
  labelKey: string
  icon: string
}>()

const route = useRoute()
const { t, locale } = useI18n()

// Fall back to the active locale when the route has no locale param yet
// (e.g. the initial `/` render before the redirect to `/he` resolves),
// otherwise resolving the named route throws "Missing required param 'locale'".
const to = computed(() => ({
  name: props.name,
  params: { locale: route.params.locale ?? locale.value },
}))
const label = computed(() => t(props.labelKey))
const isActive = computed(() => route.name === props.name)
</script>
