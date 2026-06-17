# Neumorphism Redesign

## סיכום שיחה
המשתמש ביקש להעתיק את סגנון האפליקציה מהתמונה (Dark Neumorphism) ולהתאים לדסקטופ ולמובייל.

## תיאור
יישום מערכת עיצוב Neumorphic מרכזית: רקע כהה (#121212), כרטיסים מורמים עם צל כפול, שדות שקועים (inset), כפתורים עם glow כחול (#00A3FF), וניווט מותאם מובייל (סרגל תחתון עם אייקונים עגולים).

## Technical Log
- `tailwind.config.js` — צבעי neo, shadows, border-radius
- `style.css` — CSS variables + utility classes (neo-panel, neo-raised, neo-hero, neo-inset, neo-btn-*)
- `MainLayout.vue` — flex-col-reverse במובייל (ניווט למטה), neo-panel
- `Sidebar.vue` / `SidebarLink.vue` — ניווט אופקי במובייל, אייקונים עגולים עם glow בפעיל
- קומפוננטות UI: Card, Button, Input, Toast
- כל הדפים עודכנו לסגנון החדש

## קבצים שהשתנו
- frontend/tailwind.config.js
- frontend/src/style.css
- frontend/src/components/MainLayout.vue
- frontend/src/components/Sidebar.vue
- frontend/src/components/ui/*.vue
- frontend/src/pages/*.vue
