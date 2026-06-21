# Backend Development Patterns

This document provides code patterns and best practices for backend development in the web-app-builder skill.

## Express Route Structure

### Basic Route Template

```javascript
import { Router } from 'express'
import { body } from 'express-validator'
import { controllerFunction } from '../controllers/controllerName.js'
import { protect, authorize } from '../middleware/auth.js'

const router = Router()

// GET all items
router.get('/', controllerFunction)

// GET single item
router.get('/:id', controllerFunction)

// POST create item with validation
router.post('/', [
  body('field1').notEmpty().withMessage('Field1 is required'),
  body('field2').isEmail().withMessage('Please provide a valid email')
], controllerFunction)

// PUT update item
router.put('/:id', [
  body('field1').optional().notEmpty()
], controllerFunction)

// DELETE item
router.delete('/:id', protect, authorize('admin'), controllerFunction)

export default router
```

## Controller Patterns

### Controller with Async/Await

```javascript
import { validationResult } from 'express-validator'
import Model from '../models/Model.js'

export const getItems = async (req, res) => {
  try {
    const items = await Model.find()
    res.json(items)
  } catch (err) {
    console.error(err)
    res.status(500).json({ message: 'Server error' })
  }
}

export const createItem = async (req, res) => {
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() })
  }

  try {
    const newItem = new Model(req.body)
    await newItem.save()
    res.status(201).json(newItem)
  } catch (err) {
    console.error(err)
    res.status(500).json({ message: 'Server error' })
  }
}

export const updateItem = async (req, res) => {
  try {
    const updatedItem = await Model.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }
    )
    res.json(updatedItem)
  } catch (err) {
    console.error(err)
    res.status(500).json({ message: 'Server error' })
  }
}

export const deleteItem = async (req, res) => {
  try {
    await Model.findByIdAndDelete(req.params.id)
    res.json({ message: 'Item deleted' })
  } catch (err) {
    console.error(err)
    res.status(500).json({ message: 'Server error' })
  }
}
```

## Middleware Patterns

### Authentication Middleware (JWT)

```javascript
import jwt from 'jsonwebtoken'

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
```

### Authorization Middleware (Role-based)

```javascript
export const authorize = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ message: 'Not authorized' })
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ message: 'Not allowed' })
    }

    next()
  }
}
```

### Error Handling Middleware

```javascript
// Custom error class
export class AppError extends Error {
  constructor(message, statusCode) {
    super(message)
    this.statusCode = statusCode
    this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error'
    this.isOperational = true

    Error.captureStackTrace(this, this.constructor)
  }
}

// Global error handling middleware
export const errorHandler = (err, req, res, next) => {
  err.statusCode = err.statusCode || 500
  err.status = err.status || 'error'

  res.status(err.statusCode).json({
    status: err.status,
    message: err.message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  })
}

// Async handler wrapper
export const catchAsync = (fn) => {
  return (req, res, next) => {
    fn(req, res, next).catch(next)
  }
}
```

## Validation Patterns

### Using Express Validator

```javascript
import { body, param, query } from 'express-validator'

export const createUserValidation = [
  body('name')
    .notEmpty().withMessage('Name is required')
    .isLength({ min: 2, max: 50 }).withMessage('Name must be between 2 and 50 characters'),

  body('email')
    .isEmail().withMessage('Please provide a valid email')
    .normalizeEmail(),

  body('password')
    .isLength({ min: 6 }).withMessage('Password must be at least 6 characters')
    .matches(/\d/).withMessage('Password must contain a number'),

  body('confirmPassword')
    .custom((value, { req }) => {
      if (value !== req.body.password) {
        throw new Error('Passwords do not match')
      }
      return true
    })
]

export const idParamValidation = [
  param('id').isMongoId().withMessage('Invalid ID format')
]
```

## Database Patterns

### MongoDB (Mongoose) Patterns

**Model Definition:**

```javascript
import mongoose from 'mongoose'

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Name is required'],
    trim: true
  },
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: 6,
    select: false
  }
}, { timestamps: true })

// Pre-save middleware
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next()
  this.password = await bcrypt.hash(this.password, 10)
  next()
})

// Instance method
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password)
}

const User = mongoose.model('User', userSchema)
export default User
```

**Query Patterns:**

```javascript
// Basic queries
const users = await User.find({ active: true })
const user = await User.findById(id)
const user = await User.findOne({ email })

// Populate references
const user = await User.findById(id).populate('posts')

// Pagination
const page = parseInt(req.query.page) || 1
const limit = parseInt(req.query.limit) || 10
const skip = (page - 1) * limit

const users = await User.find().skip(skip).limit(limit)
const total = await User.countDocuments()

// Aggregation
const stats = await User.aggregate([
  { $match: { active: true } },
  { $group: { _id: '$role', count: { $sum: 1 } } }
])
```

### PostgreSQL (Prisma) Patterns

**Schema Definition:**

```prisma
model User {
  id        String   @id @default(uuid())
  name      String
  email     String   @unique
  password  String
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users")
}

model Post {
  id        String   @id @default(uuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("posts")
}
```

**Query Patterns:**

```javascript
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()

// Create
const user = await prisma.user.create({
  data: {
    name: 'John',
    email: 'john@example.com',
    posts: {
      create: { title: 'First Post' }
    }
  }
})

// Read
const users = await prisma.user.findMany({
  include: { posts: true }
})

const user = await prisma.user.findUnique({
  where: { email: 'john@example.com' }
})

// Update
const updatedUser = await prisma.user.update({
  where: { id: 'userId' },
  data: { name: 'Jane' }
})

// Delete
const deletedUser = await prisma.user.delete({
  where: { id: 'userId' }
})

// Pagination
const page = 1
const limit = 10
const users = await prisma.user.findMany({
  skip: (page - 1) * limit,
  take: limit
})
```

## Authentication Patterns

### JWT Token Generation

```javascript
import jwt from 'jsonwebtoken'

export const generateToken = (userId) => {
  return jwt.sign({ userId }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || '30d'
  })
}

export const verifyToken = (token) => {
  return jwt.verify(token, process.env.JWT_SECRET)
}
```

### Refresh Token Pattern

```javascript
// Generate refresh token
export const generateRefreshToken = (userId) => {
  return jwt.sign(
    { userId, type: 'refresh' },
    process.env.REFRESH_TOKEN_SECRET,
    { expiresIn: '90d' }
  )
}

// Refresh token endpoint
export const refreshToken = async (req, res) => {
  const { refreshToken } = req.body

  try {
    const decoded = jwt.verify(refreshToken, process.env.REFRESH_TOKEN_SECRET)

    if (decoded.type !== 'refresh') {
      return res.status(401).json({ message: 'Invalid token type' })
    }

    const newAccessToken = generateToken(decoded.userId)
    res.json({ token: newAccessToken })
  } catch (err) {
    res.status(401).json({ message: 'Invalid refresh token' })
  }
}
```

## Security Best Practices

1. **Use Helmet.js** - Set secure HTTP headers
2. **Enable CORS** - Configure Cross-Origin Resource Sharing
3. **Rate limiting** - Prevent brute-force attacks
4. **Input validation** - Always validate user input
5. **SQL/NoSQL injection prevention** - Use parameterized queries
6. **Password hashing** - Always hash passwords (bcryptjs)
7. **JWT secrets** - Use strong, random secrets
8. **Environment variables** - Never commit secrets to Git
9. **HTTPS** - Always use HTTPS in production
10. **Sanitize input** - Use libraries like `express-mongo-sanitize`

### Rate Limiting Example

```javascript
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later'
})

app.use('/api/', limiter)
```

## Logging Patterns

### Using Morgan

```javascript
import morgan from 'morgan'

// Development logging
if (process.env.NODE_ENV === 'development') {
  app.use(morgan('dev'))
}

// Production logging
app.use(morgan('combined'))
```

### Custom Logger

```javascript
export const logger = {
  info: (message, meta = {}) => {
    console.log(JSON.stringify({
      level: 'info',
      message,
      ...meta,
      timestamp: new Date().toISOString()
    }))
  },
  error: (message, error = null) => {
    console.error(JSON.stringify({
      level: 'error',
      message,
      error: error?.stack,
      timestamp: new Date().toISOString()
    }))
  }
}
```

## Testing Patterns

### API Testing with Jest and Supertest

```javascript
import request from 'supertest'
import app from '../src/index.js'
import User from '../src/models/User.js'

describe('Auth API', () => {
  beforeEach(async () => {
    await User.deleteMany({})
  })

  describe('POST /api/auth/register', () => {
    it('should register a new user', async () => {
      const res = await request(app)
        .post('/api/auth/register')
        .send({
          name: 'Test User',
          email: 'test@example.com',
          password: 'password123'
        })

      expect(res.statusCode).toBe(201)
      expect(res.body).toHaveProperty('token')
    })
  })
})
```

## File Upload Patterns

### Using Multer

```javascript
import multer from 'multer'
import path from 'path'

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/')
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`)
  }
})

const upload = multer({
  storage,
  limits: { fileSize: 1024 * 1024 * 5 }, // 5MB
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif/
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase())
    const mimetype = allowedTypes.test(file.mimetype)

    if (extname && mimetype) {
      return cb(null, true)
    } else {
      cb(new Error('Only image files are allowed'))
    }
  }
})

// Usage in route
router.post('/upload', upload.single('image'), async (req, res) => {
  res.json({ imageUrl: `/uploads/${req.file.filename}` })
})
```

## Best Practices

1. **Use environment variables** - For configuration and secrets
2. **Implement proper error handling** - Use try-catch and error middleware
3. **Validate all inputs** - Use express-validator or similar
4. **Use async/await** - Avoid callback hell
5. **Structure routes by resource** - Keep routes organized
6. **Use middleware for cross-cutting concerns** - Auth, logging, etc.
7. **Implement pagination** - For endpoints returning lists
8. **Use HTTP status codes correctly** - 200, 201, 400, 401, 403, 404, 500
9. **Document your API** - Use Swagger/OpenAPI or similar
10. **Write tests** - Unit and integration tests
