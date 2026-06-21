# Frontend Development Patterns

This document provides code patterns and best practices for frontend development in the web-app-builder skill.

## Component Structure

### Functional Component Template

```jsx
import { useState, useEffect } from 'react'
import PropTypes from 'prop-types'

function ComponentName({ prop1, prop2 }) {
  const [state, setState] = useState(initialValue)

  useEffect(() => {
    // Side effects here
    return () => {
      // Cleanup
    }
  }, [dependencies])

  return (
    <div className="container">
      {/* JSX content */}
    </div>
  )
}

ComponentName.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.func
}

export default ComponentName
```

## Common Patterns

### Data Fetching

```jsx
import { useState, useEffect } from 'react'
import axios from 'axios'

function DataFetchingComponent() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/endpoint')
        setData(response.data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      {/* Render data */}
    </div>
  )
}
```

### Form Handling

```jsx
import { useState } from 'react'

function FormComponent() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await axios.post('/api/submit', formData)
      console.log('Success:', response.data)
    } catch (err) {
      console.error('Error:', err)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        className="border p-2 rounded"
      />
      {/* More inputs */}
      <button type="submit">Submit</button>
    </form>
  )
}
```

### Custom Hook Example

```jsx
import { useState, useEffect } from 'react'
import axios from 'axios'

function useFetch(url) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(url)
        setData(response.data)
      } catch (err) {
        setError(err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [url])

  return { data, loading, error }
}

// Usage
function Component() {
  const { data, loading, error } = useFetch('/api/data')

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error</div>

  return <div>{/* Render data */}</div>
}
```

## Styling with Tailwind CSS

### Responsive Design

```jsx
<div className="
  w-full          /* Full width on mobile */
  md:w-1/2       /* Half width on medium screens */
  lg:w-1/3       /* One-third width on large screens */
  px-4            /* Horizontal padding */
  py-2            /* Vertical padding */
">
  Content
</div>
```

### Common Tailwind Patterns

**Flexbox布局:**
```jsx
<div className="flex items-center justify-between">
  <div>Left</div>
  <div>Right</div>
</div>
```

**Grid布局:**
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

**Card组件:**
```jsx
<div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
  <h3 className="text-xl font-semibold mb-2">Card Title</h3>
  <p className="text-gray-600">Card content</p>
</div>
```

**Button样式:**
```jsx
<button className="
  px-4 py-2
  bg-blue-600 hover:bg-blue-700
  text-white font-semibold
  rounded-lg
  transition duration-200
  disabled:opacity-50 disabled:cursor-not-allowed
">
  Click Me
</button>
```

## State Management

### Using Context for Global State

```jsx
// context/AppContext.jsx
import { createContext, useContext, useState } from 'react'

const AppContext = createContext()

export function AppProvider({ children }) {
  const [state, setState] = useState({})

  return (
    <AppContext.Provider value={{ state, setState }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)
```

### Redux Toolkit (if needed)

```jsx
// store/counterSlice.js
import { createSlice } from '@reduxjs/toolkit'

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => {
      state.value += 1
    },
    decrement: (state) => {
      state.value -= 1
    }
  }
})

export const { increment, decrement } = counterSlice.actions
export default counterSlice.reducer
```

## Routing Patterns

### Protected Routes

```jsx
// components/PrivateRoute.jsx
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function PrivateRoute({ component: Component }) {
  const { user, loading } = useAuth()

  if (loading) return <div>Loading...</div>

  return user ? <Component /> : <Navigate to="/login" />
}

export default PrivateRoute
```

### Nested Routes

```jsx
// App.jsx
<Routes>
  <Route path="/" element={<Layout />}>
    <Route index element={<Home />} />
    <Route path="about" element={<About />} />
    <Route path="dashboard" element={<PrivateRoute component={Dashboard} />}>
      <Route path="profile" element={<Profile />} />
      <Route path="settings" element={<Settings />} />
    </Route>
  </Route>
</Routes>
```

## Performance Optimization

### Code Splitting

```jsx
import { lazy, Suspense } from 'react'

const LazyComponent = lazy(() => import('./LazyComponent'))

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  )
}
```

### Memoization

```jsx
import { useMemo, useCallback } from 'react'

function ExpensiveComponent({ data }) {
  const processedData = useMemo(() => {
    return data.map(item => expensiveCalculation(item))
  }, [data])

  const handleClick = useCallback(() => {
    console.log('Clicked')
  }, [])

  return <div>{/* Render with processedData */}</div>
}
```

## Error Handling

### Error Boundary

```jsx
import { Component } from 'react'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>
    }

    return this.props.children
  }
}

// Usage
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

## Testing Patterns

### Component Testing (Jest + React Testing Library)

```jsx
import { render, screen, fireEvent } from '@testing-library/react'
import Button from './Button'

test('button click handler is called', () => {
  const handleClick = jest.fn()
  render(<Button onClick={handleClick}>Click me</Button>)

  fireEvent.click(screen.getByText('Click me'))
  expect(handleClick).toHaveBeenCalledTimes(1)
})
```

## Best Practices

1. **Keep components small and focused** - Single responsibility principle
2. **Use TypeScript** - For better type safety (optional)
3. **Destructure props** - For cleaner code
4. **Use default parameters** - For optional props
5. **Memoize expensive calculations** - Use useMemo and useCallback
6. **Handle errors gracefully** - Always wrap API calls in try-catch
7. **Use environment variables** - For API URLs and sensitive data
8. **Follow naming conventions** - PascalCase for components, camelCase for functions
