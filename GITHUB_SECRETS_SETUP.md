# 🔑 GitHub Secrets Setup Guide

## Step 1: Add GitHub Secrets

Go to your GitHub repository: https://github.com/raiigauravv/Smart-News-Recommendation-System

1. **Navigate to**: Settings → Secrets and variables → Actions → New repository secret

2. **Add these 4 secrets:**

### AZURE_CREDENTIALS
```json
{
  "clientId": "YOUR_CLIENT_ID",
  "clientSecret": "YOUR_CLIENT_SECRET", 
  "subscriptionId": "YOUR_SUBSCRIPTION_ID",
  "tenantId": "YOUR_TENANT_ID",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

**Note**: The actual values for this secret have been provided to you separately. Use those values when adding to GitHub secrets.

### AZURE_WEBAPP_NAME
```
snr-news-api
```

### AZURE_RG
```
snr-rg
```

### AZURE_ACR_NAME
```
snracr
```

## Step 2: Create Azure Static Web Apps

1. **Go to Azure Portal**: https://portal.azure.com
2. **Create Resource** → Search "Static Web Apps"
3. **Fill in details**:
   - Resource group: `snr-rg`
   - Name: `snr-web`
   - Plan: Free
   - Deployment source: GitHub
   - Organization: raiigauravv
   - Repository: Smart-News-Recommendation-System
   - Branch: main
   - App location: `web`
   - Output location: `dist`

4. **After creation**, go to SWA → Configuration → Application settings
5. **Add environment variable**:
   - Name: `VITE_API_URL`
   - Value: `https://snr-news-api.azurewebsites.net`

6. **Get deployment token**: SWA → Manage deployment token
7. **Add to GitHub secrets**: `AZURE_STATIC_WEB_APPS_API_TOKEN`

## Step 3: Push to Main Branch

Once secrets are added, run these commands:

```bash
# Push to main to trigger deployment
git push origin main

# Monitor deployment at:
# https://github.com/raiigauravv/Smart-News-Recommendation-System/actions
```

## Step 4: Test Deployment

After deployment completes:

```bash
# Make the test script executable
chmod +x test_deployment.sh

# Run the verification script
./test_deployment.sh
```

## 🎯 Expected Results

- **Backend**: https://snr-news-api.azurewebsites.net/health → `{"status":"ok"}`
- **Frontend**: Your SWA URL (e.g., https://snr-web-abc123.azurestaticapps.net)
- **Integration**: Frontend calls backend with no CORS errors

## 📋 Checklist

- [x] Add 4 GitHub secrets
- [x] Create Azure Static Web Apps
- [x] Add SWA environment variable  
- [x] Add SWA deployment token to GitHub
- [ ] Push to main branch
- [ ] Monitor GitHub Actions
- [ ] Run test_deployment.sh
- [ ] Verify frontend-backend integration

## 🆘 If Something Fails

```bash
# Check backend logs
az webapp log tail -g snr-rg -n snr-news-api

# Check GitHub Actions logs
# Go to: https://github.com/raiigauravv/Smart-News-Recommendation-System/actions

# Restart web app if needed
az webapp restart -g snr-rg -n snr-news-api
```