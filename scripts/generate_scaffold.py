#!/usr/bin/env python3
"""
Web App Builder - Scaffold Generator
Generates complete full-stack web application scaffolding.
"""
import argparse
import os
import sys
from pathlib import Path
import shutil

def create_frontend(project_path, project_name):
    """Create React + Vite + Tailwind frontend"""
    frontend_path = Path(project_path) / "frontend"

    # Create directory structure
    dirs = [
        "src/components",
        "src/pages",
        "src/context",
        "src/hooks",
        "src/utils",
        "public"
    ]

    for dir_name in dirs:
        (frontend_path / dir_name).mkdir(parents=True, exist_ok=True)

    # package.json
    package_json = {
        "name": f"{project_name}-frontend",
        "private": True,
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview",
            "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0",
            "axios": "^1.6.0",
            "react-hot-toast": "^2.4.1"
        },
        "devDependencies": {
            "@types/react": "^18.2.37",
            "@types/react-dom": "^18.2.15",
            "@vitejs/plugin-react": "^4.2.0",
            "autoprefixer": "^10.4.16",
            "postcss": "^8.4.31",
            "tailwindcss": "^3.3.5",
            "vite": "^5.0.0"
        }
    }

    import json
    with open(frontend_path / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)

    # vite.config.js
    vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})
"""

    with open(frontend_path / "vite.config.js", "w") as f:
        f.write(vite_config)

    # tailwind.config.js
    tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""

    with open(frontend_path / "tailwind.config.js", "w") as f:
        f.write(tailwind_config)

    # postcss.config.js
    postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

    with open(frontend_path / "postcss.config.js", "w") as f:
        f.write(postcss_config)

    # index.html
    index_html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_name.title()} App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""

    with open(frontend_path / "index.html", "w") as f:
        f.write(index_html)

    # src/main.jsx
    main_jsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
"""

    with open(frontend_path / "src/main.jsx", "w") as f:
        f.write(main_jsx)

    # src/index.css
    index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
"""

    with open(frontend_path / "src/index.css", "w") as f:
        f.write(index_css)

    # src/App.jsx
    app_jsx = """import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import PrivateRoute from './components/PrivateRoute'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<PrivateRoute component={Dashboard} />} />
        </Routes>
      </div>
    </div>
  )
}

export default App
"""

    with open(frontend_path / "src/App.jsx", "w") as f:
        f.write(app_jsx)

    # src/components/Navbar.jsx
    navbar = """import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function Navbar() {
  const { user, logout } = useAuth()

  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-xl font-bold text-blue-600">
            Logo
          </Link>

          <div className="flex space-x-4">
            <Link to="/" className="text-gray-700 hover:text-blue-600">
              Home
            </Link>
            {user ? (
              <>
                <Link to="/dashboard" className="text-gray-700 hover:text-blue-600">
                  Dashboard
                </Link>
                <button
                  onClick={logout}
                  className="text-gray-700 hover:text-blue-600"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700 hover:text-blue-600">
                  Login
                </Link>
                <Link to="/register" className="text-gray-700 hover:text-blue-600">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
"""

    with open(frontend_path / "src/components/Navbar.jsx", "w") as f:
        f.write(navbar)

    # src/components/PrivateRoute.jsx
    private_route = """import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function PrivateRoute({ component: Component }) {
  const { user, loading } = useAuth()

  if (loading) {
    return <div>Loading...</div>
  }

  return user ? <Component /> : <Navigate to="/login" />
}

export default PrivateRoute
"""

    with open(frontend_path / "src/components/PrivateRoute.jsx", "w") as f:
        f.write(private_route)

    # src/context/AuthContext.jsx
    auth_context = """import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const res = await axios.get('/api/auth/me')
      setUser(res.data)
    } catch (err) {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    const res = await axios.post('/api/auth/login', { email, password })
    localStorage.setItem('token', res.data.token)
    setUser(res.data.user)
    return res.data
  }

  const register = async (name, email, password) => {
    const res = await axios.post('/api/auth/register', { name, email, password })
    localStorage.setItem('token', res.data.token)
    setUser(res.data.user)
    return res.data
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
"""

    with open(frontend_path / "src/context/AuthContext.jsx", "w") as f:
        f.write(auth_context)

    # src/pages/Home.jsx
    home = """export default function Home() {
  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        Welcome to Our App
      </h1>
      <p className="text-xl text-gray-600">
        Build amazing things with our full-stack template
      </p>
    </div>
  )
}
"""

    with open(frontend_path / "src/pages/Home.jsx", "w") as f:
        f.write(home)

    # src/pages/Login.jsx
    login = """import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import toast from 'react-hot-toast'

export default function Login() {
  const [formData, setFormData] = useState({ email: '', password: '' })
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await login(formData.email, formData.password)
      toast.success('Login successful!')
      navigate('/dashboard')
    } catch (err) {
      toast.error(err.response?.data?.message || 'Login failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-8">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
        >
          Login
        </button>
      </form>
      <p className="mt-4 text-center">
        Don't have an account? <Link to="/register" className="text-blue-600">Register</Link>
      </p>
    </div>
  )
}
"""

    with open(frontend_path / "src/pages/Login.jsx", "w") as f:
        f.write(login)

    # src/pages/Register.jsx
    register = """import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import toast from 'react-hot-toast'

export default function Register() {
  const [formData, setFormData] = useState({ name: '', email: '', password: '' })
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await register(formData.name, formData.email, formData.password)
      toast.success('Registration successful!')
      navigate('/dashboard')
    } catch (err) {
      toast.error(err.response?.data?.message || 'Registration failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-8">
      <h2 className="text-2xl font-bold mb-4">Register</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Name</label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
        >
          Register
        </button>
      </form>
      <p className="mt-4 text-center">
        Already have an account? <Link to="/login" className="text-blue-600">Login</Link>
      </p>
    </div>
  )
}
"""

    with open(frontend_path / "src/pages/Register.jsx", "w") as f:
        f.write(register)

    # src/pages/Dashboard.jsx
    dashboard = """export default function Dashboard() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Dashboard</h1>
      <p className="text-gray-600">Welcome to your dashboard!</p>
    </div>
  )
}
"""

    with open(frontend_path / "src/pages/Dashboard.jsx", "w") as f:
        f.write(dashboard)

    # .env.example
    env_example = """VITE_API_URL=http://localhost:5000/api
"""

    with open(frontend_path / ".env.example", "w") as f:
        f.write(env_example)

    # .gitignore
    gitignore = """# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

.env
.env.local
"""

    with open(frontend_path / ".gitignore", "w") as f:
        f.write(gitignore)

    print(f"✅ Frontend created at {frontend_path}")

def create_backend(project_path, project_name, db_type="mongodb"):
    """Create Node.js + Express backend"""
    backend_path = Path(project_path) / "backend"

    # Create directory structure
    dirs = [
        "src/routes",
        "src/models",
        "src/middleware",
        "src/controllers",
        "src/utils"
    ]

    for dir_name in dirs:
        (backend_path / dir_name).mkdir(parents=True, exist_ok=True)

    # package.json
    package_json = {
        "name": f"{project_name}-backend",
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js",
            "test": "jest"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "bcryptjs": "^2.4.3",
            "jsonwebtoken": "^9.0.2",
            "express-validator": "^7.0.1",
            "helmet": "^7.1.0",
            "morgan": "^1.10.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.1",
            "jest": "^29.7.0"
        }
    }

    if db_type == "mongodb":
        package_json["dependencies"]["mongoose"] = "^8.0.0"
    elif db_type == "postgresql":
        package_json["dependencies"]["@prisma/client"] = "^5.7.0"
        package_json["devDependencies"]["prisma"] = "^5.7.0"

    import json
    with open(backend_path / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)

    # src/index.js
    index_js = """import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import dotenv from 'dotenv'
"""

    if db_type == "mongodb":
        index_js += """import mongoose from 'mongoose'
"""

    index_js += """
dotenv.config()

const app = express()
const PORT = process.env.PORT || 5000

// Middleware
app.use(express.json())
app.use(cors())
app.use(helmet())
app.use(morgan('dev'))

// Routes
import authRoutes from './routes/auth.js'
app.use('/api/auth', authRoutes)

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).json({ message: 'Something went wrong!' })
})
"""

    if db_type == "mongodb":
        index_js += """
// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('✅ MongoDB connected'))
  .catch(err => console.error('❌ MongoDB connection error:', err))

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`)
})
"""
    else:
        index_js += """
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`)
})
"""

    with open(backend_path / "src/index.js", "w") as f:
        f.write(index_js)

    # src/routes/auth.js
    auth_routes = """import { Router } from 'express'
import { body } from 'express-validator'
import { register, login, getMe } from '../controllers/authController.js'
import { protect } from '../middleware/auth.js'

const router = Router()

router.post('/register', [
  body('name').notEmpty().withMessage('Name is required'),
  body('email').isEmail().withMessage('Please include a valid email'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters')
], register)

router.post('/login', [
  body('email').isEmail().withMessage('Please include a valid email'),
  body('password').notEmpty().withMessage('Password is required')
], login)

router.get('/me', protect, getMe)

export default router
"""

    with open(backend_path / "src/routes/auth.js", "w") as f:
        f.write(auth_routes)

    # src/controllers/authController.js
    auth_controller = """import bcrypt from 'bcryptjs'
import jwt from 'jsonwebtoken'
import { validationResult } from 'express-validator'

// User model - import based on db type
"""

    if db_type == "mongodb":
        auth_controller += """import User from '../models/User.js'
"""
    else:
        auth_controller += """import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()
"""

    auth_controller += """
export const register = async (req, res) => {
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() })
  }

  const { name, email, password } = req.body

  try {
"""

    if db_type == "mongodb":
        auth_controller += """    let user = await User.findOne({ email })
    if (user) {
      return res.status(400).json({ message: 'User already exists' })
    }

    user = new User({ name, email, password })
    await user.save()

    const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '30d' })

    res.status(201).json({
      token,
      user: { id: user._id, name: user.name, email: user.email }
    })
"""
    else:
        auth_controller += """    let user = await prisma.user.findUnique({ where: { email } })
    if (user) {
      return res.status(400).json({ message: 'User already exists' })
    }

    const hashedPassword = await bcrypt.hash(password, 10)

    user = await prisma.user.create({
      data: { name, email, password: hashedPassword }
    })

    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: '30d' })

    res.status(201).json({
      token,
      user: { id: user.id, name: user.name, email: user.email }
    })
"""

    auth_controller += """
  } catch (err) {
    console.error(err)
    res.status(500).json({ message: 'Server error' })
  }
}

export const login = async (req, res) => {
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() })
  }

  const { email, password } = req.body

  try {
"""

    if db_type == "mongodb":
        auth_controller += """    const user = await User.findOne({ email })
    if (!user) {
      return res.status(400).json({ message: 'Invalid credentials' })
    }

    const isMatch = await bcrypt.compare(password, user.password)
    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid credentials' })
    }

    const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '30d' })

    res.json({
      token,
      user: { id: user._id, name: user.name, email: user.email }
    })
"""
    else:
        auth_controller += """    const user = await prisma.user.findUnique({ where: { email } })
    if (!user) {
      return res.status(400).json({ message: 'Invalid credentials' })
    }

    const isMatch = await bcrypt.compare(password, user.password)
    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid credentials' })
    }

    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: '30d' })

    res.json({
      token,
      user: { id: user.id, name: user.name, email: user.email }
    })
"""

    auth_controller += """
  } catch (err) {
    console.error(err)
    res.status(500).json({ message: 'Server error' })
  }
}

export const getMe = async (req, res) => {
  try {
"""

    if db_type == "mongodb":
        auth_controller += """    const user = await User.findById(req.user.userId).select('-password')
    res.json(user)
"""
    else:
        auth_controller += """    const user = await prisma.user.findUnique({
      where: { id: req.user.userId },
      select: { id: true, name: true, email: true, createdAt: true }
    })
    res.json(user)
"""

    auth_controller += """
  } catch (err) {
    console.error(err)
    res.status(500).json({ message: 'Server error' })
  }
}
"""

    with open(backend_path / "src/controllers/authController.js", "w") as f:
        f.write(auth_controller)

    # src/middleware/auth.js
    auth_middleware = """import jwt from 'jsonwebtoken'

export const protect = async (req, res, next) => {
  let token

  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    try {
      token = req.headers.authorization.split(' ')[1]
      const decoded = jwt.verify(token, process.env.JWT_SECRET)
      req.user = decoded
      next()
    } catch (err) {
      res.status(401).json({ message: 'Not authorized, token failed' })
    }
  }

  if (!token) {
    res.status(401).json({ message: 'Not authorized, no token' })
  }
}
"""

    with open(backend_path / "src/middleware/auth.js", "w") as f:
        f.write(auth_middleware)

    if db_type == "mongodb":
        # src/models/User.js
        user_model = """import mongoose from 'mongoose'
import bcrypt from 'bcryptjs'

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true,
    unique: true
  },
  password: {
    type: String,
    required: true
  }
}, { timestamps: true })

userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) {
    next()
  }
  const salt = await bcrypt.genSalt(10)
  this.password = await bcrypt.hash(this.password, salt)
})

const User = mongoose.model('User', userSchema)

export default User
"""

        with open(backend_path / "src/models/User.js", "w") as f:
            f.write(user_model)

    # .env.example
    env_example = """PORT=5000
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
"""

    if db_type == "mongodb":
        env_example += "MONGODB_URI=mongodb://localhost:27017/" + project_name + "\n"
    elif db_type == "postgresql":
        env_example += "DATABASE_URL=\"postgresql://user:password@localhost:5432/" + project_name + "?schema=public\"\n"

    with open(backend_path / ".env.example", "w") as f:
        f.write(env_example)

    # .gitignore
    gitignore = """# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
build

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Prisma
.prisma/client

# IDE
.vscode
.idea
"""

    with open(backend_path / ".gitignore", "w") as f:
        f.write(gitignore)

    if db_type == "postgresql":
        # Create Prisma schema
        prisma_dir = backend_path / "prisma"
        prisma_dir.mkdir(exist_ok=True)

        prisma_schema = """generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  name      String
  email     String   @unique
  password  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users")
}
"""

        with open(prisma_dir / "schema.prisma", "w") as f:
            f.write(prisma_schema)

    print(f"✅ Backend created at {backend_path} (database: {db_type})")

def create_docker_config(project_path, project_name):
    """Create Docker configuration files"""
    # docker-compose.yml
    docker_compose = f"""version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:5000/api
    command: npm run dev

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
      - /app/node_modules
    environment:
      - PORT=5000
      - MONGODB_URI=mongodb://mongodb:27017/{project_name}
      - JWT_SECRET=dev-secret-key
    depends_on:
      - mongodb

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
"""

    with open(Path(project_path) / "docker-compose.yml", "w") as f:
        f.write(docker_compose)

    # docker-compose.prod.yml
    docker_compose_prod = f"""version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=production
      - PORT=5000
      - MONGODB_URI=${{secrets.MONGODB_URI}}
      - JWT_SECRET=${{secrets.JWT_SECRET}}

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${{secrets.MONGO_USERNAME}}
      - MONGO_INITDB_ROOT_PASSWORD=${{secrets.MONGO_PASSWORD}}

volumes:
  mongodb_data:
"""

    with open(Path(project_path) / "docker-compose.prod.yml", "w") as f:
        f.write(docker_compose_prod)

    # Frontend Dockerfile.dev
    dockerfile_dev_frontend = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
"""

    with open(Path(project_path) / "frontend/Dockerfile.dev", "w") as f:
        f.write(dockerfile_dev_frontend)

    # Frontend Dockerfile.prod
    dockerfile_prod_frontend = """FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
"""

    with open(Path(project_path) / "frontend/Dockerfile.prod", "w") as f:
        f.write(dockerfile_prod_frontend)

    # Backend Dockerfile.dev
    dockerfile_dev_backend = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5000

CMD ["npm", "run", "dev"]
"""

    with open(Path(project_path) / "backend/Dockerfile.dev", "w") as f:
        f.write(dockerfile_dev_backend)

    # Backend Dockerfile.prod
    dockerfile_prod_backend = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install --production

COPY . .

EXPOSE 5000

CMD ["npm", "start"]
"""

    with open(Path(project_path) / "backend/Dockerfile.prod", "w") as f:
        f.write(dockerfile_prod_backend)

    print(f"✅ Docker configuration created")

def create_readme(project_path, project_name):
    """Create README.md with setup instructions"""
    readme = f"""# {project_name.title()} App

Full-stack web application built with React + Vite + Tailwind CSS (frontend) and Node.js + Express + MongoDB (backend).

## Features

- 🔐 Authentication (JWT)
- 🎨 Modern UI with Tailwind CSS
- 🚀 Fast development with Vite
- 🐳 Docker support
- 📱 Responsive design

## Tech Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- React Router
- Axios

### Backend
- Node.js
- Express
- MongoDB (Mongoose)
- JWT Authentication
- Express Validator

## Getting Started

### Prerequisites
- Node.js 18+
- MongoDB (local or Atlas)
- npm or yarn

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd {project_name}
```

2. Install dependencies
```bash
# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
npm install
```

3. Environment setup
```bash
# Frontend
cd frontend
cp .env.example .env
# Edit .env if needed

# Backend
cd ../backend
cp .env.example .env
# Edit .env and add your MongoDB URI and JWT secret
```

4. Run the development servers
```bash
# Terminal 1 - Frontend
cd frontend
npm run dev

# Terminal 2 - Backend
cd backend
npm run dev
```

The frontend will be available at `http://localhost:3000`
The backend API will be available at `http://localhost:5000`

## Docker Deployment

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

## Project Structure

```
{project_name}/
├── frontend/          # React + Vite + Tailwind
├── backend/           # Express + MongoDB
├── docker-compose.yml
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user (protected)

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000/api
```

### Backend (.env)
```
PORT=5000
MONGODB_URI=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret
```

## Scripts

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Backend
- `npm run dev` - Start development server with nodemon
- `npm start` - Start production server

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License - feel free to use this project for your own purposes.
"""

    with open(Path(project_path) / "README.md", "w") as f:
        f.write(readme)

    print(f"✅ README.md created")

def create_gitignore(project_path):
    """Create root .gitignore"""
    gitignore = """# Dependencies
node_modules/
package-lock.json
yarn.lock
pnpm-lock.yaml

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Build outputs
dist/
build/
*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Testing
coverage/
.nyc_output

# Misc
.cache/
"""

    with open(Path(project_path) / ".gitignore", "w") as f:
        f.write(gitignore)

    print(f"✅ .gitignore created")

def main():
    parser = argparse.ArgumentParser(description='Generate full-stack web app scaffolding')
    parser.add_argument('project_name', help='Name of the project')
    parser.add_argument('--db', choices=['mongodb', 'postgresql'], default='mongodb', help='Database type (default: mongodb)')
    parser.add_argument('--path', help='Project path (default: current directory)')

    args = parser.parse_args()

    project_name = args.project_name.lower().replace(' ', '-')
    project_path = args.path if args.path else os.path.join(os.getcwd(), project_name)

    # Create project directory
    Path(project_path).mkdir(parents=True, exist_ok=True)

    print(f"🚀 Generating full-stack project: {project_name}")
    print(f"📁 Location: {project_path}")
    print(f"🗄️  Database: {args.db}")
    print()

    # Generate components
    create_frontend(project_path, project_name)
    create_backend(project_path, project_name, args.db)
    create_docker_config(project_path, project_name)
    create_readme(project_path, project_name)
    create_gitignore(project_path)

    print()
    print(f"✨ Project {project_name} generated successfully!")
    print()
    print("Next steps:")
    print(f"  1. cd {project_name}")
    print("  2. Set up environment variables (copy .env.example to .env)")
    print("  3. Install dependencies: cd frontend && npm install && cd ../backend && npm install")
    print("  4. Start development servers: npm run dev (in both frontend and backend)")
    print()

if __name__ == "__main__":
    main()
"""

Skill development - creating scaffold generator script."""