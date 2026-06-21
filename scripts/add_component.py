#!/usr/bin/env python3
"""
Add a new React component to the frontend
"""
import argparse
import os
from pathlib import Path

def create_component(project_path, component_name, component_type="functional"):
    """Create a new React component"""
    frontend_path = Path(project_path) / "frontend" / "src" / "components"
    frontend_path.mkdir(parents=True, exist_ok=True)

    component_name = component_name[0].upper() + component_name[1:]

    if component_type == "functional":
        content = f"""import {{ useState }} from 'react'

function {component_name}({{ prop1, prop2 }}) {{
  const [state, setState] = useState({{}})

  return (
    <div>
      <h2>{component_name} Component</h2>
      {{/* Add your JSX here */}}
    </div>
  )
}}

export default {component_name}
"""
    elif component_type == "class":
        content = f"""import React, {{ Component }} from 'react'

class {component_name} extends Component {{
  constructor(props) {{
    super(props)
    this.state = {{}}
  }}

  render() {{
    return (
      <div>
        <h2>{component_name} Component</h2>
        {{/* Add your JSX here */}}
      </div>
    )
  }}
}}

export default {component_name}
"""

    file_path = frontend_path / f"{component_name}.jsx"
    with open(file_path, "w") as f:
        f.write(content)

    print(f"✅ Component created: {{file_path}}")
    return file_path

def main():
    parser = argparse.ArgumentParser(description='Add a new React component')
    parser.add_argument('project_path', help='Path to the project')
    parser.add_argument('component_name', help='Name of the component')
    parser.add_argument('--type', choices=['functional', 'class'], default='functional',
                        help='Component type (default: functional)')

    args = parser.parse_args()

    create_component(args.project_path, args.component_name, args.type)

if __name__ == "__main__":
    main()
