# Deployment Guide

This guide covers various deployment options for your full-stack web application.

## Pre-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database connection strings updated
- [ ] CORS settings updated for production domain
- [ ] JWT_SECRET changed to secure value
- [ ] `.env` files added to `.gitignore`
- [ ] Build scripts tested
- [ ] API endpoints documented
- [ ] Error handling implemented
- [ ] Logs configured

## Deployment Options

### Option 1: Docker Deployment (Recommended)

#### Step 1: Build and Run with Docker Compose

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

#### Step 2: Deploy to Cloud with Docker

**Railway:**
1. Connect your GitHub repository
2. Railway auto-detects Docker Compose
3. Add environment variables in Railway dashboard
4. Deploy!

**Render:**
1. Connect your GitHub repository
2. Select "Deploy with Docker Compose"
3. Configure environment variables
4. Deploy!

### Option 2: Separate Frontend/Backend Deployment

#### Frontend Deployment

**Vercel (Recommended for React+Vite):**

1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Configure build settings:
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`
   - Install Command: `npm install`
5. Add environment variables:
   - `VITE_API_URL`: Your backend API URL
6. Deploy!

**Netlify:**

1. Push code to GitHub
2. Go to [netlify.com](https://netlify.com)
3. Import your repository
4. Configure build settings:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`
5. Add environment variables
6. Deploy!

#### Backend Deployment

**Render (Recommended for Node.js):**

1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Build Command: `cd backend && npm install`
   - Start Command: `cd backend && npm start`
5. Add environment variables:
   - `NODE_ENV`: `production`
   - `PORT`: `1000` (Render assigns port)
   - `MONGODB_URI`: Your MongoDB connection string
   - `JWT_SECRET`: Your secret key
6. Deploy!

**Railway:**

1. Go to [railway.app](https://railway.app)
2. Create new project
3. Connect GitHub repository
4. Configure:
   - Root Directory: `backend`
   - Build Command: `npm install`
   - Start Command: `npm start`
5. Add environment variables
6. Deploy!

**Heroku (Legacy but still used):**

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add MongoDB addon: `heroku addons:create mongodb:sandbox`
5. Set environment variables:
   ```bash
   heroku config:set JWT_SECRET=your-secret
   heroku config:set NODE_ENV=production
   ```
6. Deploy: `git push heroku main`

### Option 3: VPS Deployment (DigitalOcean, Linode, AWS EC2)

#### Step 1: Set up Server

```bash
# SSH into your server
ssh user@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install MongoDB (or use MongoDB Atlas)
sudo apt install -y mongodb

# Install Nginx
sudo apt install -y nginx

# Install PM2 (process manager)
sudo npm install -g pm2
```

#### Step 2: Clone and Configure

```bash
# Clone repository
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Install dependencies
cd backend && npm install --production
cd ../frontend && npm install && npm run build

# Configure environment variables
cd ../backend
cp .env.example .env
nano .env  # Edit with production values

cd ../frontend
cp .env.example .env.production
nano .env.production  # Edit with production values
```

#### Step 3: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/your-app
```

Add configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/your-app/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/your-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 4: Start Applications

```bash
# Start backend with PM2
cd /var/www/your-app/backend
pm2 start src/index.js --name "your-app-backend"

# Save PM2 configuration
pm2 save
pm2 startup
```

#### Step 5: SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Database Deployment

### MongoDB Atlas (Recommended)

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas/database)
2. Create free account
3. Create new cluster
4. Configure network access (add your IP or `0.0.0.0/0` for all IPs)
5. Create database user
6. Get connection string
7. Update `MONGODB_URI` in your backend environment variables

### PostgreSQL on Neon (Recommended)

1. Go to [Neon](https://neon.tech)
2. Create free account
3. Create new project
4. Get connection string
5. Update `DATABASE_URL` in your backend environment variables

## CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd backend && npm install && npm test
      - run: cd frontend && npm install && npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        uses: easingthemes/ssh-deploy@v2.1.5
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
          remote-host: ${{ secrets.HOST }}
          remote-user: ${{ secrets.USER }}
          source: "."
          target: "/var/www/your-app"
```

## Monitoring and Logging

### PM2 Monitoring

```bash
# Monitor applications
pm2 monit

# View logs
pm2 logs your-app-backend

# Restart application
pm2 restart your-app-backend
```

### Logging Services

- **Sentry** - Error tracking
- **LogRocket** - Frontend monitoring
- **Papertrail** - Log management
- **Datadog** - Full-stack monitoring

## Performance Optimization

### Frontend

- Enable gzip compression in Nginx
- Use CDN for static assets
- Optimize images
- Lazy load components
- Use code splitting

### Backend

- Enable compression middleware
- Use Redis for caching
- Optimize database queries
- Use PM2 cluster mode
- Enable rate limiting

## Security Checklist

- [ ] HTTPS enabled (SSL certificate)
- [ ] Security headers set (Helmet.js)
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] SQL/NoSQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Secure cookies
- [ ] JWT secrets rotated regularly

## Rollback Strategy

```bash
# Using PM2
pm2 rollback your-app-backend

# Using Git
git revert HEAD
git push origin main

# Using Docker
docker-compose down
docker-compose up -d --build
```

## Troubleshooting

### Application won't start

- Check logs: `pm2 logs` or `docker logs container-name`
- Verify environment variables
- Check port availability: `netstat -tulpn | grep 5000`

### Database connection issues

- Verify connection string
- Check IP whitelist (MongoDB Atlas)
- Test connection locally

### Frontend can't connect to backend

- Check CORS configuration
- Verify API URL in frontend environment variables
- Check Nginx proxy configuration

## Useful Resources

- [Vercel Deployment Docs](https://vercel.com/docs)
- [Render Deployment Guide](https://render.com/docs)
- [PM2 Documentation](https://pm2.keymetrics.io/docs/usage/quick-start/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Let's Encrypt Docs](https://letsencrypt.org/docs/)
