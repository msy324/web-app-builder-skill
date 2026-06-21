# Environment Variables Configuration Guide

This document provides a comprehensive guide for configuring environment variables in your full-stack application.

## Frontend Environment Variables

### Setup

1. Create `.env.local` file in the `frontend/` directory
2. Add variables prefixed with `VITE_` (required for Vite to expose them)

```bash
# frontend/.env.local
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=My App
VITE_GOOGLE_ANALYTICS_ID=UA-XXXXXXXXX
```

### Important Notes

- **Only variables prefixed with `VITE_` are exposed** to your Vite app
- `.env.local` should be added to `.gitignore` (already configured)
- Use `.env.example` to document required variables (committed to Git)

### Usage in Code

```jsx
// Access environment variables
const apiUrl = import.meta.env.VITE_API_URL
const appName = import.meta.env.VITE_APP_NAME

// In Vite config
export default defineConfig({
  plugins: [react()],
  define: {
    'process.env': process.env
  }
})
```

### Example .env.example

```bash
# frontend/.env.example
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=Your App Name
VITE_GOOGLE_ANALYTICS_ID=
```

## Backend Environment Variables

### Setup

1. Create `.env` file in the `backend/` directory
2. Use `dotenv` package to load variables (already configured)

```bash
# backend/.env
NODE_ENV=development
PORT=5000

# Database
MONGODB_URI=mongodb://localhost:27017/myapp
# Or for PostgreSQL:
# DATABASE_URL="postgresql://user:password@localhost:5432/myapp?schema=public"

# Authentication
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRES_IN=30d

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# File Upload (optional)
UPLOAD_DIR=uploads/
MAX_FILE_SIZE=5242880

# Third-party APIs (optional)
STRIPE_SECRET_KEY=sk_test_xxxxx
SENDGRID_API_KEY=SG.xxxxx
```

### Important Notes

- **Never commit `.env` to Git** (already in `.gitignore`)
- Use `.env.example` to document required variables
- Use strong, random values for secrets (JWT_SECRET, etc.)
- Different values for development, staging, and production

### Usage in Code

```javascript
// Load environment variables
import dotenv from 'dotenv'
dotenv.config()

// Access variables
const port = process.env.PORT || 5000
const jwtSecret = process.env.JWT_SECRET

// Validate required variables
if (!process.env.JWT_SECRET) {
  console.error('FATAL ERROR: JWT_SECRET is not defined')
  process.exit(1)
}
```

### Example .env.example

```bash
# backend/.env.example
NODE_ENV=development
PORT=5000

# Database
MONGODB_URI=your_mongodb_connection_string
# DATABASE_URL="postgresql://user:password@localhost:5432/dbname?schema=public"

# Authentication
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=30d

# Add other variables as needed
```

## Environment-Specific Configurations

### Development

```bash
# frontend/.env.development
VITE_API_URL=http://localhost:5000/api
VITE_DEBUG=true

# backend/.env.development
NODE_ENV=development
PORT=5000
MONGODB_URI=mongodb://localhost:27017/dev_db
```

### Production

```bash
# frontend/.env.production
VITE_API_URL=https://api.yourdomain.com
VITE_DEBUG=false

# backend/.env.production
NODE_ENV=production
PORT=5000
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/prod_db
JWT_SECRET=super-secure-production-secret
```

### Staging

```bash
# frontend/.env.staging
VITE_API_URL=https://staging-api.yourdomain.com
VITE_DEBUG=true

# backend/.env.staging
NODE_ENV=staging
PORT=5000
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/staging_db
```

## Generating Secure Secrets

### JWT Secret

```bash
# Node.js
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"

# Or use online generator (be careful)
# https://generate-secret.now.sh/64
```

### MongoDB Password

```bash
# Generate strong password
openssl rand -base64 32
```

## Docker Environment Variables

### Using Docker Compose

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - NODE_ENV=production
      - PORT=5000
      - MONGODB_URI=mongodb://mongodb:27017/myapp
      - JWT_SECRET=${JWT_SECRET}
    env_file:
      - ./backend/.env.production
```

### Using Docker Secrets

```yaml
# docker-compose.prod.yml
services:
  backend:
    secrets:
      - jwt_secret
      - mongo_password

secrets:
  jwt_secret:
    file: ./secrets/jwt_secret.txt
  mongo_password:
    file: ./secrets/mongo_password.txt
```

## CI/CD Environment Variables

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Deploy to production
        env:
          JWT_SECRET: ${{secrets.JWT_SECRET}}
          MONGODB_URI: ${{secrets.MONGODB_URI}}
        run: |
          # Deploy steps
```

### Adding Secrets to GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add your secrets (JWT_SECRET, MONGODB_URI, etc.)

## Best Practices

1. **Never commit `.env` files** - Always use `.gitignore`
2. **Use `.env.example`** - Document all required variables
3. **Validate environment variables** - Check required vars on startup
4. **Use strong secrets** - Generate secure random strings
5. **Different secrets per environment** - Dev, staging, production
6. **Rotate secrets regularly** - Especially in production
7. **Use environment variable management tools** - For team collaboration
   - [Doppler](https://www.doppler.com/)
   - [Infisical](https://infisical.com/)
   - [Vault by HashiCorp](https://www.vaultproject.io/)

## Troubleshooting

### Frontend can't access environment variables

- Ensure variables are prefixed with `VITE_`
- Restart dev server after changing `.env` files
- Check `import.meta.env` in browser console

### Backend can't read environment variables

- Ensure `dotenv.config()` is called at the top of `index.js`
- Check `.env` file exists and has correct format (no spaces around `=`)
- Restart the server after changing `.env`

### Docker containers can't access environment variables

- Check `docker-compose.yml` environment section
- Ensure `.env` file is in the correct location
- Use `docker-compose config` to verify configuration

## Useful Tools

- [dotenv](https://www.npmjs.com/package/dotenv) - Load environment variables from `.env`
- [cross-env](https://www.npmjs.com/package/cross-env) - Set environment variables cross-platform
- [env-cmd](https://www.npmjs.com/package/env-cmd) - Execute commands with environment variables
- [check-env](https://www.npmjs.com/package/check-env) - Validate environment variables

## Example: Complete Setup

### Frontend

```bash
# frontend/.env.local
VITE_API_URL=http://localhost:5000/api
VITE_GOOGLE_ANALYTICS_ID=UA-123456789-1
```

```jsx
// frontend/src/utils/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default api
```

### Backend

```bash
# backend/.env
NODE_ENV=development
PORT=5000
MONGODB_URI=mongodb://localhost:27017/myapp
JWT_SECRET=7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f
JWT_EXPIRES_IN=30d
```

```javascript
// backend/src/index.js
import dotenv from 'dotenv'
dotenv.config()

import express from 'express'
const app = express()

const PORT = process.env.PORT || 5000

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})
```
