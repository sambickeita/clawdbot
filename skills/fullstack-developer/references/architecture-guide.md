# Fullstack Architecture Guide

## Project Structure Patterns

### Monorepo Structure (Recommended)
```
project/
├── apps/
│   ├── web/              # Next.js frontend
│   ├── api/              # Backend API
│   └── mobile/           # React Native (optional)
├── packages/
│   ├── ui/               # Shared UI components
│   ├── types/            # Shared TypeScript types
│   └── utils/            # Shared utilities
├── docker-compose.yml
└── package.json
```

### Separated Structure
```
project/
├── client/               # Frontend application
├── server/               # Backend API
├── shared/               # Shared code/types
├── database/             # Migrations, seeds
└── docker-compose.yml
```

## Technology Stack Decisions

### Frontend Framework Selection
- **Next.js**: SSR/SSG, API routes, optimized performance
- **React + Vite**: SPA, maximum flexibility, fast development
- **Vue + Nuxt**: Gentle learning curve, excellent DX
- **Angular**: Enterprise features, opinionated structure

### Backend Framework Selection
- **Next.js API Routes**: Fullstack React, serverless-ready
- **Express**: Minimal, flexible, huge ecosystem
- **FastAPI**: Modern Python, automatic docs, type safety
- **NestJS**: Enterprise Node.js, decorators, modular

### Database Selection
- **PostgreSQL**: ACID compliance, complex queries, JSON support
- **MongoDB**: Document-based, flexible schema
- **SQLite**: Embedded, zero-config, prototyping
- **Redis**: Caching, sessions, real-time features

## Authentication Patterns

### JWT-based Authentication
```typescript
// Token structure
interface JWTPayload {
  userId: string;
  email: string;
  role: string;
  exp: number;
}

// Middleware pattern
const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token provided' });
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

### Session-based Authentication
```typescript
// Session configuration
app.use(session({
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,
  store: new RedisStore({ client: redisClient }),
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
  }
}));
```

## Database Patterns

### Prisma Schema Design
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  password  String
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  @@map("users")
}

model Post {
  id        String   @id @default(cuid())
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

### Connection Pooling
```typescript
import { Pool } from 'pg';

class DatabaseManager {
  private pool: Pool;
  
  constructor() {
    this.pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
  }
  
  async query<T>(text: string, params?: any[]): Promise<T[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(text, params);
      return result.rows;
    } finally {
      client.release();
    }
  }
}
```

## API Design Patterns

### RESTful API Structure
```
GET    /api/users           # List users
POST   /api/users           # Create user
GET    /api/users/:id       # Get user
PUT    /api/users/:id       # Update user
DELETE /api/users/:id       # Delete user

GET    /api/users/:id/posts # Get user's posts
POST   /api/users/:id/posts # Create post for user
```

### Error Handling Pattern
```typescript
// Result pattern for consistent error handling
type Result<T, E = Error> = 
  | { success: true; data: T }
  | { success: false; error: E };

// API response wrapper
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Error middleware
const errorHandler = (err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  
  if (err instanceof ValidationError) {
    return res.status(400).json({
      success: false,
      error: 'Validation failed',
      details: err.details
    });
  }
  
  res.status(500).json({
    success: false,
    error: 'Internal server error'
  });
};
```

## State Management Patterns

### Zustand Store Pattern
```typescript
interface AppState {
  user: User | null;
  loading: boolean;
  error: string | null;
  
  // Actions
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  // Async actions
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}

const useAppStore = create<AppState>((set, get) => ({
  user: null,
  loading: false,
  error: null,
  
  setUser: (user) => set({ user }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  
  login: async (credentials) => {
    set({ loading: true, error: null });
    try {
      const response = await api.login(credentials);
      set({ user: response.user, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
  
  logout: () => {
    localStorage.removeItem('token');
    set({ user: null });
  }
}));
```

### React Query Pattern
```typescript
// Custom hooks for data fetching
const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => api.getUsers(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

const useCreateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (userData: CreateUserData) => api.createUser(userData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};
```

## Security Best Practices

### Input Validation
```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(50),
  password: z.string().min(8).regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
});

const validateCreateUser = (req: Request, res: Response, next: NextFunction) => {
  try {
    CreateUserSchema.parse(req.body);
    next();
  } catch (error) {
    res.status(400).json({ error: 'Invalid input', details: error.errors });
  }
};
```

### Rate Limiting
```typescript
import rateLimit from 'express-rate-limit';

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  message: 'Too many authentication attempts',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/auth', authLimiter);
```

## Performance Optimization

### Database Optimization
```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_author_id ON posts(author_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);

-- Composite indexes for complex queries
CREATE INDEX idx_posts_author_published ON posts(author_id, published, created_at DESC);
```

### Caching Strategy
```typescript
import Redis from 'ioredis';

class CacheManager {
  private redis: Redis;
  
  constructor() {
    this.redis = new Redis(process.env.REDIS_URL);
  }
  
  async get<T>(key: string): Promise<T | null> {
    const cached = await this.redis.get(key);
    return cached ? JSON.parse(cached) : null;
  }
  
  async set(key: string, value: any, ttl: number = 3600): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }
  
  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
}
```

## Testing Strategies

### Unit Testing Pattern
```typescript
// Service layer testing
describe('UserService', () => {
  let userService: UserService;
  let mockRepository: jest.Mocked<UserRepository>;
  
  beforeEach(() => {
    mockRepository = {
      findById: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    } as any;
    
    userService = new UserService(mockRepository);
  });
  
  it('should create user with hashed password', async () => {
    const userData = { email: 'test@example.com', password: 'password123' };
    const expectedUser = { id: '1', email: 'test@example.com', password: 'hashed' };
    
    mockRepository.create.mockResolvedValue(expectedUser);
    
    const result = await userService.createUser(userData);
    
    expect(mockRepository.create).toHaveBeenCalledWith({
      email: userData.email,
      password: expect.not.stringMatching(userData.password)
    });
    expect(result).toEqual(expectedUser);
  });
});
```

### Integration Testing Pattern
```typescript
// API endpoint testing
describe('POST /api/users', () => {
  it('should create user and return 201', async () => {
    const userData = {
      email: 'test@example.com',
      name: 'Test User',
      password: 'Password123!'
    };
    
    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);
    
    expect(response.body).toMatchObject({
      success: true,
      data: {
        id: expect.any(String),
        email: userData.email,
        name: userData.name
      }
    });
    
    // Verify user was created in database
    const user = await db.user.findUnique({ where: { email: userData.email } });
    expect(user).toBeTruthy();
  });
});
```

## Deployment Patterns

### Docker Multi-stage Build
```dockerfile
# Frontend build stage
FROM node:18-alpine AS frontend-builder
WORKDIR /app/client
COPY client/package*.json ./
RUN npm ci --only=production
COPY client/ ./
RUN npm run build

# Backend build stage
FROM node:18-alpine AS backend-builder
WORKDIR /app/server
COPY server/package*.json ./
RUN npm ci --only=production
COPY server/ ./
RUN npm run build

# Production stage
FROM node:18-alpine AS runner
WORKDIR /app

# Copy built applications
COPY --from=frontend-builder /app/client/dist ./public
COPY --from=backend-builder /app/server/dist ./
COPY --from=backend-builder /app/server/node_modules ./node_modules

EXPOSE 3000
CMD ["node", "index.js"]
```

### Environment Configuration
```typescript
// Environment validation
const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().transform(Number),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  REDIS_URL: z.string().url().optional(),
});

export const env = envSchema.parse(process.env);
```