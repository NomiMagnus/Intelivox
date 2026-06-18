# Intelivox Frontend

Modern resident management UI built with Vue 3, TypeScript, and Vite. Features a clean sidebar navigation with real-time search and CRUD operations.

## Features
- 🔍 **Search Residents** - Real-time search by name, phone, or email
- 📝 **Update Residents** - Edit resident information
- 👤 **User Management** - User area and settings
- 🎨 **Modern UI** - Dark theme with TailwindCSS and PrimeVue components
- 📱 **Responsive Design** - Mobile-friendly layout
- 🚀 **Fast Development** - Hot module replacement with Vite

## Tech Stack
- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool
- **Vue Router** - Client-side routing
- **Pinia** - State management with persistence
- **PrimeVue** - UI component library
- **TailwindCSS** - Utility-first CSS
- **Axios** - HTTP client

## Run Locally

### Prerequisites
- Node.js 20+
- npm

### Setup
1. Install dependencies:
   ```bash
   npm install
   ```

2. Create `.env` file:
   ```bash
   copy .env.example .env
   ```
   
   Default configuration:
   ```
   VITE_API_BASE_URL=http://localhost:8000
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

4. Open: http://localhost:5173

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run type-check` - Run TypeScript type checking

## Docker

### Run with Docker Compose (Recommended)
From project root directory:

```bash
cd ..
docker-compose up --build
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

### Run Frontend Only with Docker

1. Build the image:
   ```bash
   docker build -t intelivox-frontend .
   ```

2. Run the container:
   ```bash
   docker run -p 5173:5173 -e VITE_API_BASE_URL=http://localhost:8000 intelivox-frontend
   ```

## Project Structure
```
src/
├── components/
│   ├── ui/                # Reusable UI components
│   └── MainLayout.vue     # Main app layout
├── pages/
│   ├── Home.vue           # Dashboard
│   ├── SearchResidents.vue
│   ├── UpdateResident.vue
│   ├── Settings.vue
│   └── UserArea.vue
├── router/
│   └── index.ts           # Route definitions
├── stores/
│   └── residents.ts       # Pinia state management
├── services/
│   └── api.ts             # API integration
├── composables/
│   └── useResidents.ts    # Reusable logic
├── types/
│   └── index.ts           # TypeScript types
└── main.ts                # App entry point
```

## Environment Variables

- `VITE_API_BASE_URL` - Backend API base URL (default: http://localhost:8000)

## Development

The frontend communicates with the FastAPI backend. Make sure the backend is running on the configured `VITE_API_BASE_URL` before starting development.
