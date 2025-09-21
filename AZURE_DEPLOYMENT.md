# Azure Deployment Guide - Smart News Recommendation System

## Prerequisites
- Azure CLI installed and logged in
- GitHub repository with the code
- Azure subscription with appropriate permissions

## A) Backend Deployment (Azure App Service + ACR)

### A1) Create Azure Resources

```bash
# Create resource group
az group create --name snr-rg --location eastus

# Create Azure Container Registry
az acr create --resource-group snr-rg --name snracr --sku Basic --location westus2

# Create App Service Plan (Free tier for students)
az appservice plan create --name snr-plan --resource-group snr-rg --sku F1 --is-linux --location eastus

# Create Web App for containers
az webapp create --resource-group snr-rg --plan snr-plan --name snr-api --deployment-container-image-name snracr.azurecr.io/smart-news-api:latest
```

### A2) Grant Web App ACR Pull Permissions

```bash
# Assign system identity to the web app
az webapp identity assign -g snr-rg -n snr-news-api

# Get resource IDs
ACR_ID=$(az acr show -n snracr -g snr-rg --query id -o tsv)
PRINCIPAL_ID=$(az webapp identity show -g snr-rg -n snr-news-api --query principalId -o tsv)

# Allow Web App to pull images from ACR
az role assignment create --assignee-object-id $PRINCIPAL_ID \
  --assignee-principal-type ServicePrincipal \
  --role "AcrPull" --scope $ACR_ID
```

### A3) Configure App Service Settings

```bash
# Set container port
az webapp config appsettings set -g snr-rg -n snr-news-api --settings WEBSITES_PORT=8000

# Configure container image
az webapp config container set -g snr-rg -n snr-news-api --docker-custom-image-name snracr.azurecr.io/smart-news-api:latest --docker-registry-server-url https://snracr.azurecr.io
```

### A4) Configure GitHub Secrets

In your GitHub repository, add these secrets (Settings → Secrets and variables → Actions):

1. **AZURE_CREDENTIALS**: Service principal credentials
```bash
# Create service principal
az ad sp create-for-rbac --name "snr-github-actions" --role contributor --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/snr-rg --sdk-auth
```

2. **AZURE_WEBAPP_NAME**: `snr-news-api`
3. **AZURE_RG**: `snr-rg`  
4. **AZURE_ACR_NAME**: `snracr`

### A5) Update GitHub Actions Workflow

The existing `.github/workflows/deploy.yml` should work. If needed, update the ACR name and other details.

### A6) Trigger Deployment

```bash
# Push to main branch to trigger deployment
git push origin feat/hardening-and-azure:main
```

### A7) Verify Backend

```bash
# Check deployment logs
az webapp log tail -g snr-rg -n snr-news-api

# Test API health
curl https://snr-news-api.azurewebsites.net/health
```

## B) Frontend Deployment (Azure Static Web Apps)

### B1) Create Static Web App

```bash
# Create SWA through Azure Portal:
# 1. Go to Azure Portal → Create Resource → Static Web App
# 2. Resource group: snr-rg
# 3. Name: snr-web
# 4. Plan: Free
# 5. Deployment source: GitHub
# 6. Repository: your-repo
# 7. Branch: main
# 8. App location: web
# 9. Build command: npm run build  
# 10. Output location: dist
```

### B2) Configure SWA Environment Variables

In Azure Portal → Static Web App → Configuration → Application settings:
- **Key**: `VITE_API_URL`
- **Value**: `https://snr-news-api.azurewebsites.net`

### B3) Configure GitHub Secrets for SWA

Add this secret to your GitHub repository:
- **AZURE_STATIC_WEB_APPS_API_TOKEN**: Get from SWA → Manage deployment token

### B4) Deploy Frontend

The `.github/workflows/swa.yml` workflow will automatically deploy when you push to main.

## C) Final Verification

### C1) Test API Endpoints

```bash
API="https://snr-api.azurewebsites.net"

# Health check
curl -s $API/health

# Trending articles
curl -s "$API/trending?k=3" | jq '.items'

# Search
curl -s -X POST "$API/search" \
  -H "content-type: application/json" \
  -d '{"q":"economy","k":5}' | jq '.items | length'

# Recommendations
curl -s -X POST "$API/recommend" \
  -H "content-type: application/json" \
  -d '{"user_id":"u123","k":5,"recent_clicks":["n101","n205"]}' | jq '.items[0]'
```

### C2) Test Frontend

1. Open SWA URL (e.g., `https://snr-web.azurestaticapps.net`)
2. Verify home page loads trending articles
3. Test search functionality  
4. Test recommendations
5. Check browser DevTools Network tab for API calls

## D) Troubleshooting

### Backend Issues

```bash
# Check container logs
az webapp log tail -g snr-rg -n snr-news-api

# Check app settings
az webapp config appsettings list -g snr-rg -n snr-news-api

# Restart app
az webapp restart -g snr-rg -n snr-news-api
```

### Frontend Issues

1. Check SWA logs in Azure Portal
2. Verify `VITE_API_URL` environment variable
3. Check CORS settings in backend
4. Clear SWA cache and redeploy if needed

### Common Issues

1. **CORS errors**: Ensure backend CORS includes your SWA domain
2. **Container won't start**: Check `WEBSITES_PORT=8000` setting
3. **403 pulling image**: Verify ACR permissions and managed identity
4. **Build failures**: Check GitHub Actions logs

## E) Cost Management

- **Free Tier Usage**: F1 App Service Plan, Basic ACR, Free SWA
- **Resource Monitoring**: Set up alerts for usage limits
- **Cleanup**: Delete resource group when done: `az group delete --name snr-rg`