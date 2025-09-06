# Ledgerly Development Guide

## Quick Start

1. **Prerequisites**
   - Docker Desktop installed and running
   - Git installed
   - 8GB+ RAM recommended

2. **Setup Development Environment**

   ```bash
   # Clone the repository (if needed)
   git clone <your-repo-url>
   cd fin-statement-processor

   # Run the setup script
   ./scripts/setup-dev-environment.sh
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - MinIO Console: http://localhost:9001 (admin/admin)

## Development Workflow

### Starting/Stopping Services

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f

# Restart specific service
docker compose restart backend
```

### Making Changes

**Backend Changes:**

- Edit files in `./backend/`
- FastAPI will auto-reload on changes
- View logs: `docker compose logs -f backend`

**Frontend Changes:**

- Edit files in `./frontend/`
- Vite will hot-reload on changes
- View logs: `docker compose logs -f frontend`

**Database Changes:**

- Edit files in `./database/`
- Restart postgres service: `docker compose restart postgres`

### Testing the Setup

1. **Backend Health Check**

   ```bash
   curl http://localhost:8000/health
   ```

2. **Frontend Accessibility**

   ```bash
   curl http://localhost:3000
   ```

3. **MinIO Access**

   ```bash
   curl http://localhost:9000/minio/health/live
   ```

4. **Database Connection**
   ```bash
   docker compose exec postgres psql -U postgres -d ledgerly -c "SELECT version();"
   ```

### Troubleshooting

**Port Conflicts:**

- If ports are in use, modify `docker-compose.yml` port mappings
- Common conflicts: 3000 (React), 8000 (FastAPI), 5432 (PostgreSQL)

**Build Issues:**

- Clean rebuild: `docker compose down && docker compose build --no-cache`
- Check Docker Desktop has enough memory allocated

**Service Not Starting:**

- Check logs: `docker compose logs <service-name>`
- Verify environment variables in `.env` files
- Ensure all required files exist

**File Permission Issues:**

- On Linux/Mac: `sudo chown -R $USER:$USER .`
- Ensure scripts are executable: `chmod +x scripts/*.sh`

## File Structure

```
/
├── backend/                 # FastAPI backend
│   ├── Dockerfile.dev      # Development container
│   ├── .env.development    # Backend environment vars
│   └── ...                 # Python application files
├── frontend/               # React frontend
│   ├── Dockerfile.dev      # Development container
│   ├── .env.development    # Frontend environment vars
│   └── ...                 # React application files
├── database/               # Database setup
│   ├── init.sql           # Database initialization
│   └── seeds/             # Seed data
├── scripts/               # Utility scripts
│   ├── setup-dev-environment.sh
│   └── minio/
├── docker-compose.yml     # Multi-service configuration
└── .env                  # Main environment configuration
```

## Next Steps

1. **Implement Backend API Endpoints** (see `docs/API_SPECIFICATION.md`)
2. **Connect Frontend to Backend**
3. **Add Authentication**
4. **Implement File Upload Processing**
5. **Add Transaction Parsing Logic**

## Production Considerations

This setup is for development only. For production:

- Use proper secrets management
- Enable SSL/TLS
- Configure proper backup strategies
- Use production-grade database hosting
- Implement proper logging and monitoring
