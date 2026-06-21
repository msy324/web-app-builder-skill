# Web App Builder Skill for WorkBuddy

🚀 **Full-stack web application development skill for WorkBuddy AI assistant**

This skill enables WorkBuddy to generate complete full-stack web applications with modern tech stack, best practices, and deployment configurations.

## ✨ Features

- **Complete Project Scaffolding** - Generate full-stack apps with one command
- **Modern Tech Stack** - React + Vite + Tailwind CSS (frontend), Node.js + Express + MongoDB (backend)
- **Authentication Built-in** - JWT-based auth system included
- **Docker Support** - Development and production Docker configurations
- **Best Practices** - Follows industry standards and patterns
- **Deployment Ready** - Guides for Vercel, Render, Railway, and VPS deployment

## 📦 Installation

### Option 1: Manual Installation (Recommended)

1. Download or clone this repository
2. Copy the `web-app-builder` folder to your WorkBuddy skills directory:
   ```bash
   # Linux/macOS
   cp -r web-app-builder ~/.workbuddy/skills/

   # Windows
   xcopy /E /I web-app-builder %USERPROFILE%\.workbuddy\skills\web-app-builder
   ```
3. Restart WorkBuddy

### Option 2: Install from Zip

1. Download `web-app-builder.zip` from the Releases page
2. Open WorkBuddy → Settings → Skills → Install Skill
3. Select the downloaded zip file

## 🚀 Usage

Once installed, use natural language to build web applications:

### Generate a New Project

```
"Build me a full-stack todo app"
"Create a React + Express project for a blog"
"Generate a web app with user authentication"
"Scaffold a new project with MongoDB"
```

### Add Features

```
"Add a login page to my app"
"Create a REST API for products"
"Add a dashboard page"
```

### Deployment

```
"Deploy my app to Vercel"
"How do I deploy the backend to Render?"
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + Tailwind CSS |
| Routing | React Router v6 |
| HTTP Client | Axios |
| Backend | Node.js + Express |
| Database | MongoDB (Mongoose) / PostgreSQL (Prisma) |
| Auth | JWT (jsonwebtoken) |
| Validation | express-validator |
| Security | helmet.js, cors, bcryptjs |
| DevOps | Docker + Docker Compose |

## 📁 File Structure

```
web-app-builder/
├── SKILL.md                          # Skill definition & instructions
├── scripts/                           # Executable Python scripts
│   ├── generate_scaffold.py         # Generate full project scaffolding
│   ├── add_component.py              # Add new React component
│   ├── add_route.py                  # Add new backend route + controller
│   └── setup_db.py                  # Create database seed data
└── references/                       # Reference documentation
    ├── frontend-patterns.md         # Component templates, hooks, patterns
    ├── backend-patterns.md          # Routes, middleware, DB queries
    ├── env-variables.md            # Environment config guide
    ├── deployment-guide.md         # Vercel/Render/Railway/VPS deploy
    └── tailwind-cheatsheet.md     # Tailwind CSS quick reference
```

## 🎯 Included Scripts

### `generate_scaffold.py`
Generate a complete full-stack project with one command:
```bash
python scripts/generate_scaffold.py my-app --db mongodb
python scripts/generate_scaffold.py my-blog --db postgresql
```

Generates:
- Frontend: React + Vite + Tailwind with auth pages, routing, context
- Backend: Express + Mongoose/Prisma with JWT auth, validation
- Docker: docker-compose.yml (dev + prod)
- README with setup instructions

### `add_component.py`
Quickly add a new React component:
```bash
python scripts/add_component.py my-app Button --type functional
```

### `add_route.py`
Add a new API endpoint with controller:
```bash
python scripts/add_route.py my-app products
# Creates route, controller, model template, updates index.js
```

### `setup_db.py`
Create database seed data:
```bash
python scripts/setup_db.py my-app --db mongodb
# Adds npm run seed command
```

## 🌟 Example Projects You Can Build

| Command | What You Get |
|---------|-------------|
| `"Build me a todo app"` | Full CRUD + auth + responsive UI |
| `"Create a blog platform"` | Posts, comments, rich text editor, admin panel |
| `"Scaffold an e-commerce admin"` | Products, orders, users, charts, file upload |
| `"Build a real-time chat app"` | WebSocket auth, rooms, message history |

## 📚 Documentation References

The `references/` folder contains comprehensive guides loaded on-demand:

- **Frontend Patterns** - Components, hooks, forms, custom hooks, error boundaries, testing
- **Backend Patterns** - Controllers, middleware, validation, MongoDB/Prisma queries, file uploads, rate limiting
- **Environment Variables** - Dev/staging/prod config, Docker secrets, CI/CD vars
- **Deployment Guide** - Step-by-step for Vercel, Netlify, Render, Railway, Heroku, VPS (Nginx)
- **Tailwind Cheatsheet** - Layout, typography, spacing, colors, components

## 🔧 Customization

After generating a project:
```bash
# Switch database to PostgreSQL
python scripts/generate_scaffold.py my-app --db postgresql

# Add more features via natural language in WorkBuddy
# "Add email verification"
# "Implement password reset"
# "Add admin dashboard"
```

## 🤝 Contributing

Contributions welcome! Fork, branch, commit, PR.

## 📄 License

MIT

---


