import { defineStore } from 'pinia'
import { DEFAULT_LOCALE, isSupportedLocale, type Locale } from '../i18n'

export const useLocaleStore = defineStore('locale', {
  state: () => ({
    // The user's last active locale. `null` until first resolved/chosen.
    locale: null as Locale | null,
  }),
  actions: {
    setLocale(locale: Locale) {
      this.locale = locale
    },
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'intelivox-locale',
        storage: localStorage,
        paths: ['locale'],
      },
    ],
  },
})

// Resolves the locale to use when the URL has no (valid) locale prefix:
// persisted choice first, then browser language, falling back to Hebrew.
export function resolvePreferredLocale(): Locale {
  const persisted = useLocaleStore().locale
  if (isSupportedLocale(persisted)) return persisted

  const browser = navigator.language?.toLowerCase() ?? ''
  if (browser.startsWith('en')) return 'en'

  return DEFAULT_LOCALE
}
