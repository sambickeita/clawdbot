#!/usr/bin/env python3
"""
Fullstack Project Creator - NO MOCK DATA
Creates complete project structures with real configurations
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

class FullstackProjectCreator:
    def __init__(self):
        self.stacks = {
            "react-node": {
                "frontend": "react",
                "backend": "node",
                "database": "postgres"
            },
            "vue-python": {
                "frontend": "vue", 
                "backend": "python",
                "database": "postgres"
            },
            "nextjs": {
                "frontend": "nextjs",
                "backend": "nextjs-api",
                "database": "postgres"
            }
        }
    
    def create_project(self, name: str, stack: str, database: str = "postgres"):
        """Create complete fullstack project with real configuration"""
        project_path = Path(name)
        
        if project_path.exists():
            print(f"ERROR: Project {name} already exists")
            return False
        
        print(f"Creating fullstack project: {name}")
        print(f"Stack: {stack}, Database: {database}")
        
        # Create project structure
        self._create_structure(project_path, stack, database)
        
        # Initialize git
        subprocess.run(["git", "init"], cwd=project_path)
        
        # Install dependencies
        self._install_dependencies(project_path, stack)
        
        print(f"✅ Project {name} created successfully")
        print(f"📁 Location: {project_path.absolute()}")
        
        return True
    
    def _create_structure(self, path: Path, stack: str, database: str):
        """Create project directory structure"""
        path.mkdir()
        
        if stack == "nextjs":
            self._create_nextjs_structure(path, database)
        else:
            self._create_separated_structure(path, stack, database)
    
    def _create_nextjs_structure(self, path: Path, database: str):
        """Create Next.js fullstack structure"""
        # Next.js structure
        dirs = [
            "app", "app/api", "app/api/auth", "app/api/users",
            "components", "components/ui", "lib", "prisma",
            "public", "styles", "types"
        ]
        
        for dir_path in dirs:
            (path / dir_path).mkdir(parents=True)
        
        # Package.json
        package_json = {
            "name": path.name,
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint",
                "db:push": "prisma db push",
                "db:migrate": "prisma migrate dev"
            },
            "dependencies": {
                "next": "14.0.0",
                "react": "^18",
                "react-dom": "^18",
                "@prisma/client": "^5.0.0",
                "bcryptjs": "^2.4.3",
                "jsonwebtoken": "^9.0.0",
                "zod": "^3.22.0"
            },
            "devDependencies": {
                "typescript": "^5",
                "@types/node": "^20",
                "@types/react": "^18",
                "@types/react-dom": "^18",
                "prisma": "^5.0.0",
                "eslint": "^8",
                "eslint-config-next": "14.0.0"
            }
        }
        
        with open(path / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        
        # Prisma schema
        prisma_schema = f'''generator client {{
  provider = "prisma-client-js"
}}

datasource db {{
  provider = "postgresql"
  url      = env("DATABASE_URL")
}}

model User {{
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  password  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}}
'''
        
        with open(path / "prisma" / "schema.prisma", "w") as f:
            f.write(prisma_schema)
        
        # Environment file
        env_content = f'''DATABASE_URL="postgresql://user:password@localhost:5432/{path.name}"
NEXTAUTH_SECRET="your-secret-key"
NEXTAUTH_URL="http://localhost:3000"
'''
        
        with open(path / ".env.local", "w") as f:
            f.write(env_content)
    
    def _create_separated_structure(self, path: Path, stack: str, database: str):
        """Create separated frontend/backend structure"""
        # Create main directories
        (path / "client").mkdir()
        (path / "server").mkdir()
        (path / "shared").mkdir()
        
        # Frontend structure
        if "react" in stack:
            self._create_react_frontend(path / "client")
        elif "vue" in stack:
            self._create_vue_frontend(path / "client")
        
        # Backend structure
        if "node" in stack:
            self._create_node_backend(path / "server", database)
        elif "python" in stack:
            self._create_python_backend(path / "server", database)
        
        # Docker compose
        self._create_docker_compose(path, database)
    
    def _create_react_frontend(self, path: Path):
        """Create React frontend structure"""
        dirs = [
            "src", "src/components", "src/pages", "src/hooks",
            "src/utils", "src/styles", "src/types", "public"
        ]
        
        for dir_path in dirs:
            (path / dir_path).mkdir(parents=True)
        
        package_json = {
            "name": "client",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "vite",
                "build": "tsc && vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.8.0",
                "axios": "^1.3.0",
                "zustand": "^4.3.0"
            },
            "devDependencies": {
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0",
                "@vitejs/plugin-react": "^3.1.0",
                "typescript": "^4.9.0",
                "vite": "^4.1.0"
            }
        }
        
        with open(path / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
    
    def _create_node_backend(self, path: Path, database: str):
        """Create Node.js backend structure"""
        dirs = [
            "src", "src/routes", "src/models", "src/middleware",
            "src/utils", "src/config", "src/types"
        ]
        
        for dir_path in dirs:
            (path / dir_path).mkdir(parents=True)
        
        package_json = {
            "name": "server",
            "version": "1.0.0",
            "scripts": {
                "dev": "tsx watch src/index.ts",
                "build": "tsc",
                "start": "node dist/index.js"
            },
            "dependencies": {
                "express": "^4.18.0",
                "cors": "^2.8.5",
                "helmet": "^6.0.0",
                "bcryptjs": "^2.4.3",
                "jsonwebtoken": "^9.0.0",
                "zod": "^3.20.0",
                "prisma": "^5.0.0",
                "@prisma/client": "^5.0.0"
            },
            "devDependencies": {
                "@types/express": "^4.17.0",
                "@types/cors": "^2.8.0",
                "@types/bcryptjs": "^2.4.0",
                "@types/jsonwebtoken": "^9.0.0",
                "typescript": "^4.9.0",
                "tsx": "^3.12.0"
            }
        }
        
        with open(path / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
    
    def _create_docker_compose(self, path: Path, database: str):
        """Create Docker Compose configuration"""
        compose_content = f'''version: '3.8'

services:
  {database}:
    image: postgres:15
    environment:
      POSTGRES_DB: {path.name}
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
'''
        
        with open(path / "docker-compose.yml", "w") as f:
            f.write(compose_content)
    
    def _install_dependencies(self, path: Path, stack: str):
        """Install project dependencies"""
        if stack == "nextjs":
            subprocess.run(["npm", "install"], cwd=path)
        else:
            # Install frontend deps
            subprocess.run(["npm", "install"], cwd=path / "client")
            # Install backend deps
            subprocess.run(["npm", "install"], cwd=path / "server")

def main():
    if len(sys.argv) < 4:
        print("Usage: python create-project.py --name PROJECT_NAME --stack STACK [--database DB]")
        print("Stacks: react-node, vue-python, nextjs")
        sys.exit(1)
    
    creator = FullstackProjectCreator()
    
    # Parse arguments
    args = {}
    for i in range(1, len(sys.argv), 2):
        if i + 1 < len(sys.argv):
            args[sys.argv[i].lstrip('-')] = sys.argv[i + 1]
    
    name = args.get('name')
    stack = args.get('stack', 'react-node')
    database = args.get('database', 'postgres')
    
    if not name:
        print("ERROR: Project name is required")
        sys.exit(1)
    
    success = creator.create_project(name, stack, database)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()