# Azure Deployment Guide - Smart News Recommendation System

## 🎯 Cost-Optimized Architecture ($0 Monthly Cost)

### Services Used:

- **Frontend**: Azure Static Web Apps (FREE forever)
- **Backend**: Azure App Service F1 Free Tier (FREE)
- **Storage**: GitHub repository (FREE)
- **CI/CD**: GitHub Actions (FREE)

---

## 📋 Prerequisites

1. **Azure Student Subscription** ($100 credit)
2. **GitHub Account** with this repository
3. **Azure CLI** installed locally

---

## 🚀 Step-by-Step Deployment

### Step 1: Azure Resource Group

```bash
# Login to Azure
az login

# Create resource group
az group create \
  --name smart-news-rg \
  --location eastus
```

### Step 2: Deploy Backend (Azure App Service)

```bash
# Create App Service Plan (F1 Free Tier)
az appservice plan create \
  --name smart-news-plan \
  --resource-group smart-news-rg \
  --sku F1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group smart-news-rg \
  --plan smart-news-plan \
  --name smart-news-backend \
  --deployment-container-image-name your-dockerhub/smart-news-backend:latest
```

### Step 3: Setup Container Registry (Optional)

```bash
# Create Azure Container Registry (Basic tier - $5/month)
# Skip this if using Docker Hub (FREE)
az acr create \
  --resource-group smart-news-rg \
  --name smartnewsacr \
  --sku Basic
```

### Step 4: Deploy Frontend (Azure Static Web Apps)

1. Go to [Azure Portal](https://portal.azure.com)
2. Create **Static Web App**
3. Connect to your GitHub repository
4. Set build configuration:
   - **App location**: `/web`
   - **Output location**: `dist`

### Step 5: Configure GitHub Secrets

Add these secrets to your GitHub repository:

```bash
# For Backend Deployment
AZUREAPPSERVICE_PUBLISHPROFILE  # Download from Azure Portal

# For Frontend Deployment
AZURE_STATIC_WEB_APPS_API_TOKEN  # Generated during Static Web App creation
```

### Step 6: Update CORS Settings

Update your backend's CORS origins with your Static Web App URL:

```python
# In server/app/settings.py
cors_origins = ["https://your-app-name.azurestaticapps.net"]
```

---

## 🔧 Configuration Files Created

### Backend Configuration:

- `server/Dockerfile` - Optimized for Azure App Service
- `server/azure-deploy.json` - ARM template
- `server/requirements-prod.txt` - Production dependencies
- `server/.env.production` - Production environment variables

### Frontend Configuration:

- `web/staticwebapp.config.json` - Static Web App routing
- `web/.env.production` - Production API URL

### CI/CD Configuration:

- `.github/workflows/azure-backend.yml` - Backend deployment
- `.github/workflows/azure-frontend.yml` - Frontend deployment

---

## 💰 Cost Breakdown

| Service               | Tier        | Monthly Cost |
| --------------------- | ----------- | ------------ |
| Azure Static Web Apps | Free        | $0           |
| Azure App Service     | F1 Free     | $0           |
| GitHub Actions        | Public repo | $0           |
| **Total**             |             | **$0**       |

### Free Tier Limitations:

- **App Service F1**: 1GB storage, 60 minutes/day CPU time
- **Static Web Apps**: 100GB bandwidth, 2 custom domains
- **Perfect for**: Development, demos, small-scale production

---

## 🔄 Deployment Process

1. **Push to main branch** → Triggers GitHub Actions
2. **Backend**: Builds container → Deploys to App Service
3. **Frontend**: Builds React app → Deploys to Static Web Apps
4. **Auto-update**: CORS settings, environment variables

---

## 📊 Monitoring & Scaling

### Free Tier Monitoring:

- Azure Portal dashboard
- Application Insights (Free tier available)
- GitHub Actions logs

### When to Upgrade:

- **More traffic**: Upgrade to Basic App Service ($13/month)
- **Custom domains**: Static Web Apps Standard ($9/month)
- **Better performance**: Premium tiers available

---

## 🛠️ Local Testing

Test deployment locally before Azure:

```bash
# Build and test with Docker Compose
docker-compose up --build

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:5173
```

---

## 🚨 Troubleshooting

### Common Issues:

1. **CORS errors**: Update backend CORS_ORIGINS
2. **Build failures**: Check GitHub Actions logs
3. **Cold starts**: F1 tier has slower cold starts
4. **Memory limits**: F1 tier has 1GB RAM limit

### Optimization Tips:

1. Use CPU-only PyTorch for smaller image size
2. Enable application caching
3. Optimize dataset loading
4. Use async/await in FastAPI endpoints

---

## 📞 Support

- Azure Documentation: [docs.microsoft.com](https://docs.microsoft.com/azure)
- GitHub Actions: [docs.github.com](https://docs.github.com/actions)
- FastAPI: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

Ready to deploy! 🚀
