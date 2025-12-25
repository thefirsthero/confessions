# Confessions Admin Panel

Password-protected admin interface for managing confessions content generation.

## Features

- 🔐 **Password Protected** - Secure access with session-based authentication
- 📸 **Image Processing** - Upload confession images for OCR text extraction
- 📥 **Export Confessions** - Download MyConfessions.json for video generation
- 🎨 **Modern UI** - Built with shadcn/ui components
- 🔑 **API Key Authentication** - Secure backend communication

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```env
VITE_APP_NAME=Confessions Admin
VITE_API_URL=http://localhost:8000
VITE_API_KEY=your-api-key-from-backend
```

### 3. Run Development Server

```bash
npm run dev
```

Access at: http://localhost:5174

**Login with your existing database credentials** from the `public.users` table.

## Related

- **Backend API**: `../backend/` - FastAPI server with OCR
- **Client Frontend**: `../frontend-client/` - Public confession submission
