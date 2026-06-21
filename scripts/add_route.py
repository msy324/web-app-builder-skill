#!/usr/bin/env python3
"""
Add a new backend route to the Express app
"""
import argparse
import os
from pathlib import Path

def create_route(project_path, route_name, include_controller=True):
    """Create a new backend route with optional controller"""

    backend_path = Path(project_path) / "backend" / "src"

    # Create route file
    routes_path = backend_path / "routes"
    routes_path.mkdir(parents=True, exist_ok=True)

    route_content = f"""import {{ Router }} from 'express'
import {{ body }} from 'express-validator'
"""

    if include_controller:
        controller_name = f"{route_name}Controller"
        route_content += f"import {{ get{route_name.capitalize()}s, create{route_name.capitalize()}, update{route_name.capitalize()}, delete{route_name.capitalize()} }} from '../controllers/{route_name}Controller.js'\n"

    route_content += f"""
const router = Router()

// GET all {route_name}s
router.get('/', {controller_name}.get{route_name.capitalize()}s)

// GET single {route_name}
router.get('/:id', {controller_name}.get{route_name.capitalize()})

// POST create {route_name}
router.post('/', [
  body('name').notEmpty().withMessage('Name is required')
], {controller_name}.create{route_name.capitalize()})

// PUT update {route_name}
router.put('/:id', [
  body('name').optional().notEmpty()
], {controller_name}.update{route_name.capitalize()})

// DELETE {route_name}
router.delete('/:id', {controller_name}.delete{route_name.capitalize()})

export default router
"""

    route_file = routes_path / f"{route_name}.js"
    with open(route_file, "w") as f:
        f.write(route_content)

    print(f"✅ Route created: {route_file}")

    # Create controller file
    if include_controller:
        controllers_path = backend_path / "controllers"
        controllers_path.mkdir(parents=True, exist_ok=True)

        controller_content = f"""import {{ validationResult }} from 'express-validator'
import {route_name} from '../models/{route_name}.js'

export const get{route_name.capitalize()}s = async (req, res) => {{
  try {{
    const {route_name}s = await {route_name}.find()
    res.json({route_name}s)
  }} catch (err) {{
    console.error(err)
    res.status(500).json({{ message: 'Server error' }})
  }}
}}

export const create{route_name.capitalize()} = async (req, res) => {{
  const errors = validationResult(req)
  if (!errors.isEmpty()) {{
    return res.status(400).json({{ errors: errors.array() }})
  }}

  try {{
    const new{route_name.capitalize()} = new {route_name}(req.body)
    await new{route_name.capitalize()}.save()
    res.status(201).json(new{route_name.capitalize()})
  }} catch (err) {{
    console.error(err)
    res.status(500).json({{ message: 'Server error' }})
  }}
}}

export const update{route_name.capitalize()} = async (req, res) => {{
  try {{
    const updated{route_name.capitalize()} = await {route_name}.findByIdAndUpdate(
      req.params.id,
      req.body,
      {{ new: true }}
    )
    res.json(updated{route_name.capitalize()})
  }} catch (err) {{
    console.error(err)
    res.status(500).json({{ message: 'Server error' }})
  }}
}}

export const delete{route_name.capitalize()} = async (req, res) => {{
  try {{
    await {route_name}.findByIdAndDelete(req.params.id)
    res.json({{ message: '{route_name} deleted' }})
  }} catch (err) {{
    console.error(err)
    res.status(500).json({{ message: 'Server error' }})
  }}
}}
"""

        controller_file = controllers_path / f"{route_name}Controller.js"
        with open(controller_file, "w") as f:
            f.write(controller_content)

        print(f"✅ Controller created: {controller_file}")

    # Update index.js to include the new route
    index_file = backend_path / "index.js"
    if index_file.exists():
        with open(index_file, "r") as f:
            content = f.read()

        # Add import
        import_line = f"import {route_name}Routes from './routes/{route_name}.js'\n"
        if import_line not in content:
            # Find the last import line
            lines = content.split('\n')
            last_import_idx = 0
            for i, line in enumerate(lines):
                if line.startswith('import'):
                    last_import_idx = i

            lines.insert(last_import_idx + 1, import_line.strip())
            content = '\n'.join(lines)

        # Add route usage
        route_line = f"app.use('/api/{route_name}s', {route_name}Routes)\n"
        if route_line not in content:
            # Find the line with existing routes
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "app.use('/api" in line:
                    lines.insert(i + 1, f"app.use('/api/{route_name}s', {route_name}Routes)")
                    break
            content = '\n'.join(lines)

        with open(index_file, "w") as f:
            f.write(content)

        print(f"✅ Updated index.js to include {route_name} routes")

    return route_file

def main():
    parser = argparse.ArgumentParser(description='Add a new backend route')
    parser.add_argument('project_path', help='Path to the project')
    parser.add_argument('route_name', help='Name of the route (e.g., products, users)')
    parser.add_argument('--no-controller', action='store_true', help='Do not create controller file')

    args = parser.parse_args()

    create_route(args.project_path, args.route_name, not args.no_controller)

if __name__ == "__main__":
    main()
