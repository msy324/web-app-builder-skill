# Tailwind CSS Cheatsheet

Quick reference for common Tailwind CSS utility classes.

## Spacing (Margin & Padding)

### Format: `{property}{side?}-{size}`

- **Property:** `m` (margin), `p` (padding)
- **Side:** `t` (top), `r` (right), `b` (bottom), `l` (left), `x` (horizontal), `y` (vertical), `` (all)
- **Size:** `0`, `1` (0.25rem), `2` (0.5rem), `4` (1rem), `8` (2rem), etc.

```jsx
<div className="m-4">Margin all sides 1rem</div>
<div className="mt-8">Margin top 2rem</div>
<div className="px-4">Padding left & right 1rem</div>
<div className="py-2">Padding top & bottom 0.5rem</div>
```

## Width & Height

```jsx
<div className="w-full">100% width</div>
<div className="w-1/2">50% width</div>
<div className="w-64">16rem width</div>
<div className="h-screen">100vh height</div>
<div className="min-h-screen">Minimum 100vh</div>
```

## Colors

### Text Colors

```jsx
<p className="text-red-500">Red text</p>
<p className="text-blue-600">Blue text</p>
<p className="text-gray-900">Dark gray text</p>
<p className="text-white">White text</p>
```

### Background Colors

```jsx
<div className="bg-blue-500">Blue background</div>
<div className="bg-gray-100">Light gray background</div>
<div className="bg-white">White background</div>
<div className="bg-gradient-to-r from-purple-400 to-pink-400">
  Gradient background
</div>
```

## Typography

```jsx
<h1 className="text-4xl font-bold">Large bold text</h1>
<p className="text-base font-normal">Normal text</p>
<p className="text-sm font-light">Small light text</p>
<p className="text-center">Centered text</p>
<p className="uppercase tracking-wide">Uppercase</p>
<p className="leading-relaxed">Relaxed line height</p>
```

## Flexbox

```jsx
<div className="flex">Flex container</div>
<div className="flex-row">Horizontal (default)</div>
<div className="flex-col">Vertical</div>
<div className="items-center">Align items center</div>
<div className="justify-center">Justify content center</div>
<div className="justify-between">Space between</div>
<div className="flex-1">Flex grow</div>
<div className="flex-shrink-0">Don't shrink</div>
```

## Grid

```jsx
<div className="grid grid-cols-3">3 columns</div>
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  Responsive columns
</div>
<div className="gap-4">Gap between items</div>
<div className="col-span-2">Span 2 columns</div>
```

## Position & Display

```jsx
<div className="block">Display block</div>
<div className="inline-block">Display inline-block</div>
<div className="hidden">Display none</div>
<div className="relative">Position relative</div>
<div className="absolute">Position absolute</div>
<div className="fixed">Position fixed</div>
<div className="sticky">Position sticky</div>
```

## Borders & Radius

```jsx
<div className="border">1px solid border</div>
<div className="border-2">2px border</div>
<div className="border-gray-300">Gray border</div>
<div className="rounded">Border radius 0.25rem</div>
<div className="rounded-lg">Large radius</div>
<div className="rounded-full">Full circle/oval</div>
<div className="border-t-0">No top border</div>
```

## Shadows

```jsx
<div className="shadow">Small shadow</div>
<div className="shadow-md">Medium shadow</div>
<div className="shadow-lg">Large shadow</div>
<div className="shadow-xl">Extra large shadow</div>
<div className="shadow-none">No shadow</div>
```

## Hover, Focus & Active States

```jsx
<button className="bg-blue-500 hover:bg-blue-700">
  Hover effect
</button>
<input className="border focus:border-blue-500 focus:outline-none" />
<button className="active:bg-blue-800">Active effect</button>
```

## Responsive Design

### Breakpoints

- `sm` (640px+)
- `md` (768px+)
- `lg` (1024px+)
- `xl` (1280px+)
- `2xl` (1536px+)

```jsx
<div className="w-full md:w-1/2 lg:w-1/3">
  Full width on mobile, half on tablet, third on desktop
</div>
<div className="hidden md:block">
  Hidden on mobile, visible on tablet+
</div>
```

## Common Patterns

### Button

```jsx
<button className="
  px-4 py-2
  bg-blue-600 hover:bg-blue-700
  text-white font-semibold
  rounded-lg
  shadow-md hover:shadow-lg
  transition duration-200
  disabled:opacity-50 disabled:cursor-not-allowed
">
  Click Me
</button>
```

### Card

```jsx
<div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
  <h3 className="text-xl font-semibold mb-2">Card Title</h3>
  <p className="text-gray-600">Card content goes here.</p>
</div>
```

### Input

```jsx
<input
  type="text"
  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
  placeholder="Enter text..."
/>
```

### Navbar

```jsx
<nav className="bg-white shadow-lg">
  <div className="container mx-auto px-4">
    <div className="flex justify-between items-center h-16">
      <div>Logo</div>
      <div className="flex space-x-4">
        <a href="#" className="text-gray-700 hover:text-blue-600">Home</a>
        <a href="#" className="text-gray-700 hover:text-blue-600">About</a>
      </div>
    </div>
  </div>
</nav>
```

### Alert

```jsx
<div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
  <strong className="font-bold">Success!</strong>
  <span className="block sm:inline"> Your action was completed.</span>
</div>
```

## Advanced Techniques

### Dark Mode

```jsx
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
  Dark mode supported!
</div>
```

### Arbitrary Values

```jsx
<div className="w-[32rem]">32rem width</div>
<div className="bg-[#bada55]">Custom color</div>
<div className="grid-cols-[1fr_500px_2fr]">Custom grid</div>
```

### Group Hover

```jsx
<div className="group">
  <div className="text-black group-hover:text-red-500">
    Hover me!
  </div>
</div>
```

## Tips

1. **Use `@apply` in CSS for repeated patterns:**
   ```css
   .btn {
     @apply px-4 py-2 bg-blue-600 text-white rounded;
   }
   ```

2. **Check class order** - Tailwind uses consistent ordering

3. **Use official extension** - VS Code Tailwind CSS IntelliSense

4. **Purge unused classes** - Configure `content` in `tailwind.config.js`

## Resources

- [Official Docs](https://tailwindcss.com/docs)
- [Tailwind UI](https://tailwindui.com/) - Pre-built components
- [Tailwind Play](https://play.tailwindcss.com/) - Online playground
- [Heroicons](https://heroicons.com/) - Free icons from Tailwind team
