import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import he from './locales/he.json'

// Single source of truth for supported languages.
// To add a language: create `locales/<code>.json`, import it, add it to
// `messages` below, and push its code into `SUPPORTED_LOCALES`.
export const SUPPORTED_LOCALES = ['he', 'en'] as const
export type Locale = (typeof SUPPORTED_LOCALES)[number]

export const DEFAULT_LOCALE: Locale = 'he'

// Locales that render right-to-left.
export const RTL_LOCALES: readonly Locale[] = ['he']

export function isSupportedLocale(value: unknown): value is Locale {
  return typeof value === 'string' && (SUPPORTED_LOCALES as readonly string[]).includes(value)
}

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: DEFAULT_LOCALE,
  fallbackLocale: 'en',
  messages: { en, he },
})

export default i18n
