import { RTL_LOCALES, type Locale } from './index'

// Applies the document direction and language for the given locale.
// Called from the router guard so direction always tracks the active URL locale.
export function applyDirection(locale: Locale) {
  const dir = RTL_LOCALES.includes(locale) ? 'rtl' : 'ltr'
  document.documentElement.dir = dir
  document.documentElement.lang = locale
}
