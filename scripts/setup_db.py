#!/usr/bin/env python3
"""
Setup database with seed data
"""
import argparse
import os
from pathlib import Path

def create_seed_data(project_path, db_type="mongodb"):
    """Create database seed data script"""

    backend_path = Path(project_path) / "backend"
    scripts_path = backend_path / "scripts"
    scripts_path.mkdir(parents=True, exist_ok=True)

    if db_type == "mongodb":
        seed_content = """import mongoose from 'mongoose'
import dotenv from 'dotenv'
import User from '../src/models/User.js'
import bcrypt from 'bcryptjs'

dotenv.config()

const seedUsers = [
  {
    name: 'Admin User',
    email: 'admin@example.com',
    password: 'admin123',
    role: 'admin'
  },
  {
    name: 'Test User',
    email: 'test@example.com',
    password: 'test123',
    role: 'user'
  }
]

const seedDatabase = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI)
    console.log('Connected to MongoDB')

    // Clear existing data
    await User.deleteMany({})
    console.log('Cleared users')

    // Hash passwords and insert users
    for (let userData of seedUsers) {
      const hashedPassword = await bcrypt.hash(userData.password, 10)
      userData.password = hashedPassword
    }

    await User.insertMany(seedUsers)
    console.log('Seed users inserted')

    console.log('Database seeded successfully!')
    process.exit(0)
  } catch (err) {
    console.error('Error seeding database:', err)
    process.exit(1)
  }
}

seedDatabase()
"""

        seed_file = scripts_path / "seed.js"
        with open(seed_file, "w") as f:
            f.write(seed_content)

        # Add seed script to package.json
        package_json_path = backend_path / "package.json"
        if package_json_path.exists():
            import json
            with open(package_json_path, "r") as f:
                package_data = json.load(f)

            if "scripts" not in package_data:
                package_data["scripts"] = {}

            package_data["scripts"]["seed"] = "node scripts/seed.js"

            with open(package_json_path, "w") as f:
                json.dump(package_data, f, indent=2)

        print(f"✅ Seed script created: {seed_file}")
        print(f"✅ Added 'npm run seed' command to package.json")

    elif db_type == "postgresql":
        seed_content = """import {{ PrismaClient }} from '@prisma/client'
const prisma = new PrismaClient()

const seedUsers = [
  {{
    name: 'Admin User',
    email: 'admin@example.com',
    password: '$2b$10$hashedpasswordhere', // admin123
    role: 'admin'
  }},
  {{
    name: 'Test User',
    email: 'test@example.com',
    password: '$2b$10$hashedpasswordhere', // test123
    role: 'user'
  }}
]

async function main() {{
  console.log('Start seeding...')

  await prisma.user.deleteMany({})
  console.log('Cleared users')

  for (const user of seedUsers) {{
    const createdUser = await prisma.user.create({{
      data: user
    }})
    console.log(`Created user with id: ${{createdUser.id}}`)
  }}

  console.log('Seeding finished.')
}}

main()
  .catch((e) => {{
    console.error(e)
    process.exit(1)
  }})
  .finally(async () => {{
    await prisma.$disconnect()
  }})
"""

        seed_file = scripts_path / "seed.js"
        with open(seed_file, "w") as f:
            f.write(seed_content)

        # Update package.json
        package_json_path = backend_path / "package.json"
        if package_json_path.exists():
            import json
            with open(package_json_path, "r") as f:
                package_data = json.load(f)

            if "scripts" not in package_data:
                package_data["scripts"] = {}

            package_data["scripts"]["seed"] = "node scripts/seed.js"
            package_data["scripts"]["postinstall"] = "prisma generate"

            with open(package_json_path, "w") as f:
                json.dump(package_data, f, indent=2)

        print(f"✅ Seed script created: {seed_file}")
        print(f"✅ Added 'npm run seed' command to package.json")

def main():
    parser = argparse.ArgumentParser(description='Setup database with seed data')
    parser.add_argument('project_path', help='Path to the project')
    parser.add_argument('--db', choices=['mongodb', 'postgresql'], default='mongodb',
                        help='Database type (default: mongodb)')

    args = parser.parse_args()

    create_seed_data(args.project_path, args.db)

if __name__ == "__main__":
    main()
