---
name: web-app-builder
description: "Full-stack web application scaffolding and development toolkit. Use when building complete web apps with frontend and backend, generating project scaffolding, creating REST APIs, setting up authentication, or deploying full-stack applications. Supports React plus Vite plus Tailwind CSS frontend and Node.js plus Express plus MongoDB backend."
agent_created: true
---

# Web App Builder Skill

Complete full-stack web application development toolkit with scaffolding generation, best practices, and deployment configurations.

## When to Use This Skill

Trigger this skill when the user requests:
- "Build me a full-stack app"
- "Create a web application with frontend and backend"
- "Generate a React + Express project"
- "Scaffold a new web app"
- "Set up authentication for my app"
- "Deploy my full-stack application"

## Tech Stack

**Frontend:**
- React 18+ with Vite
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls

**Backend:**
- Node.js with Express
- MongoDB with Mongoose (or PostgreSQL with Prisma)
- JWT authentication
- Express Validator for input validation

**Deployment:**
- Docker + Docker Compose
- Environment-based configuration

## Workflow

### 1. Project Scaffolding

To generate a new full-stack project, execute the scaffolding script:

```bash
python scripts/generate_scaffold.py <project-name> [--db mongodb|postgresql] [--auth jwt|session]
```

This script generates:
- Complete project structure
- Frontend boilerplate (React + Vite + Tailwind)
- Backend boilerplate (Express + Database)
- Docker configuration
- README with setup instructions

### 2. Frontend Development

Frontend templates are stored in `assets/frontend-template/`. To create a new frontend page/component:

1. Copy the component template from `assets/frontend-template/src/components/`
2. Follow the patterns in `references/frontend-patterns.md`
3. Use Tailwind CSS for styling (reference: `references/tailwind-cheatsheet.md`)

**Key templates available:**
- `assets/frontend-template/src/App.jsx` - Main app with router setup
- `assets/frontend-template/src/components/Navbar.jsx` - Navigation component
- `assets/frontend-template/src/pages/Home.jsx` - Example page
- `assets/frontend-template/src/context/AuthContext.jsx` - Authentication context

### 3. Backend Development

Backend templates are stored in `assets/backend-template/`. To create a new API endpoint:

1. Copy the route template from `assets/backend-template/src/routes/`
2. Follow the patterns in `references/backend-patterns.md`
3. Use the middleware from `assets/backend-template/src/middleware/`

**Key templates available:**
- `assets/backend-template/src/index.js` - Express app entry point
- `assets/backend-template/src/routes/auth.js` - Authentication routes
- `assets/backend-template/src/models/User.js` - User model (MongoDB)
- `assets/backend-template/src/middleware/auth.js` - JWT authentication middleware

### 4. Database Integration

To set up database models and connections:

- **MongoDB**: Use Mongoose models in `assets/backend-template/src/models/`
- **PostgreSQL**: Use Prisma schema in `assets/backend-template/prisma/`

Reference: `references/database-patterns.md`

### 5. Authentication

Authentication templates are pre-configured:

- **JWT-based**: `assets/backend-template/src/middleware/auth.js`
- **Frontend auth context**: `assets/frontend-template/src/context/AuthContext.jsx`
- **Login/Register pages**: `assets/frontend-template/src/pages/`

### 6. Deployment

To deploy the application:

1. Use the Docker configuration in `assets/docker/`
2. Follow the deployment guide in `references/deployment-guide.md`
3. Set up environment variables (reference: `references/env-variables.md`)

**Docker commands:**
```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

## File Structure

A generated project follows this structure:

```
<project-name>/
├── frontend/                 # React + Vite + Tailwind
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── context/        # React context (auth, etc.)
│   │   ├── hooks/          # Custom hooks
│   │   ├── utils/          # Utility functions
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── public/             # Static assets
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/                  # Express + MongoDB/PostgreSQL
│   ├── src/
│   │   ├── routes/         # API routes
│   │   ├── models/         # Database models
│   │   ├── middleware/     # Custom middleware
│   │   ├── controllers/    # Route controllers
│   │   ├── utils/          # Utility functions
│   │   └── index.js       # Entry point
│   ├── prisma/             # Prisma schema (if PostgreSQL)
│   ├── .env.example        # Environment variables template
│   └── package.json
│
├── docker-compose.yml       # Development Docker config
├── docker-compose.prod.yml # Production Docker config
├── .gitignore
└── README.md
```

## Best Practices

### Frontend
- Use functional components with hooks
- Implement proper error handling in API calls
- Use environment variables for API URLs
- Follow the component structure in `references/frontend-patterns.md`

### Backend
- Validate all inputs using Express Validator
- Use async/await with proper error handling
- Implement proper logging
- Follow the route structure in `references/backend-patterns.md`

### Security
- Never commit `.env` files
- Use HTTPS in production
- Implement rate limiting
- Sanitize user inputs
- Use secure headers (Helmet.js)

## Common Tasks

### Add a new page
1. Create page component in `frontend/src/pages/`
2. Add route in `frontend/src/App.jsx`
3. Add navigation link in `frontend/src/components/Navbar.jsx`

### Add a new API endpoint
1. Create route file in `backend/src/routes/`
2. Create controller in `backend/src/controllers/`
3. Add route to `backend/src/index.js`

### Add a new database model
1. Create model in `backend/src/models/` (MongoDB) or update `prisma/schema.prisma` (PostgreSQL)
2. Create corresponding routes and controllers
3. Update environment variables if needed

## Troubleshooting

**Frontend can't connect to backend:**
- Check CORS configuration in backend
- Verify API URL in frontend `.env`
- Ensure backend is running on correct port

**Database connection issues:**
- Verify MongoDB/PostgreSQL is running
- Check connection string in `.env`
- Ensure database credentials are correct

**Docker issues:**
- Run `docker-compose down -v` to clean volumes
- Check Docker logs: `docker-compose logs -f`
- Ensure ports are not already in use

## References

Load these reference files as needed:

- `references/frontend-patterns.md` - Frontend code patterns and best practices
- `references/backend-patterns.md` - Backend code patterns and best practices
- `references/database-patterns.md` - Database schemas and query patterns
- `references/deployment-guide.md` - Deployment instructions for various platforms
- `references/tailwind-cheatsheet.md` - Tailwind CSS utility classes reference
- `references/env-variables.md` - Environment variables configuration guide

## Scripts

- `scripts/generate_scaffold.py` - Generate complete project scaffolding
- `scripts/add_component.py` - Add a new frontend component
- `scripts/add_route.py` - Add a new backend route
- `scripts/setup_db.py` - Initialize database with seed data

## Assets

- `assets/frontend-template/` - Complete frontend boilerplate
- `assets/backend-template/` - Complete backend boilerplate
- `assets/docker/` - Docker configuration files
- `assets/example-requests/` - Example API requests (Postman/Insomnia)

---

**Tip:** When starting a new project, always run `generate_scaffold.py` first to create the proper project structure. Then customize the generated files based on the specific requirements.
