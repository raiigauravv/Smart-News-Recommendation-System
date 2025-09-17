# 🚀 Deployment Verification Guide

## Quick Verification Checklist

### ✅ Step 1: Check GitHub Actions Status
1. **Open GitHub Actions**: https://github.com/raiigauravv/Smart-News-Recommendation-System/actions
2. **Look for**:
   - ✅ Green checkmarks for successful deployments
   - 🔄 Yellow circles for in-progress deployments
   - ❌ Red X marks for failed deployments

### ✅ Step 2: Verify Backend API (Azure App Service)
```bash
# Test health endpoint
curl https://snr-news-api.azurewebsites.net/health

# Expected response: {"status": "healthy"}
```

**Backend URL**: https://snr-news-api.azurewebsites.net

### ✅ Step 3: Verify Frontend (Azure Static Web Apps)
Your frontend should be deployed to a URL like:
```
https://polite-grass-0129f300f.1.azurestaticapps.net
```

**To find your exact URL**:
1. Go to: https://portal.azure.com
2. Navigate to: Resource Groups → `snr-system-rg` → Azure Static Web Apps
3. Look for the **URL** field in the overview

### ✅ Step 4: Test Full Integration
Once both are live, test these endpoints:

#### Backend API Tests:
```bash
# 1. Health check
curl https://snr-news-api.azurewebsites.net/health

# 2. Get news articles
curl "https://snr-news-api.azurewebsites.net/api/news?category=technology&limit=5"

# 3. Get user recommendations
curl "https://snr-news-api.azurewebsites.net/api/recommendations/U82271"
```

#### Frontend Tests:
1. **Visit your frontend URL**
2. **Check functionality**:
   - Category dropdown works
   - News articles load
   - PDF export works
   - No console errors

## 🔍 Troubleshooting Common Issues

### Backend Issues
**Problem**: API returns 500 error or "Application Error"
**Solutions**:
1. Check Azure App Service logs:
   ```bash
   # View recent logs
   az webapp log tail --name snr-news-api --resource-group snr-system-rg
   ```

2. Restart the Azure App Service:
   ```bash
   az webapp restart --name snr-news-api --resource-group snr-system-rg
   ```

### Frontend Issues
**Problem**: Static Web App shows 404 or build errors
**Solutions**:
1. Check GitHub Actions for build failures
2. Verify Node.js version compatibility (should be 18+)
3. Check if `dist/` folder is being generated correctly

### Integration Issues
**Problem**: Frontend can't connect to backend
**Solutions**:
1. Check CORS settings in backend
2. Verify API base URL in frontend config
3. Check network requests in browser dev tools

## 📱 Manual Testing Checklist

### Frontend Functionality:
- [ ] Page loads without errors
- [ ] Category dropdown populated
- [ ] News articles display correctly
- [ ] PDF export button works
- [ ] Responsive design works on mobile
- [ ] No console errors in browser dev tools

### Backend API:
- [ ] `/health` endpoint responds
- [ ] `/api/news` returns articles
- [ ] `/api/recommendations/{user_id}` returns recommendations
- [ ] CORS headers allow frontend domain
- [ ] Response times are reasonable (< 5s)

### End-to-End:
- [ ] Frontend successfully fetches data from backend
- [ ] PDF export includes real data
- [ ] Error handling works (try invalid category)
- [ ] Loading states work properly

## 🔗 Important URLs

- **GitHub Repository**: https://github.com/raiigauravv/Smart-News-Recommendation-System
- **GitHub Actions**: https://github.com/raiigauravv/Smart-News-Recommendation-System/actions
- **Azure Portal**: https://portal.azure.com
- **Backend API**: https://snr-news-api.azurewebsites.net
- **Frontend App**: Check Azure Static Web Apps in portal for exact URL

## 🚨 If Something's Not Working

1. **Check GitHub Actions first** - most issues show up here
2. **Review the logs** - both GitHub Actions and Azure App Service logs
3. **Test locally** - make sure your code works locally first
4. **Check Azure portal** - verify resources are running and configured correctly

## 📞 Quick Commands for Status Check

```bash
# Check if both services are responding
echo "🔍 Checking Backend..."
curl -s https://snr-news-api.azurewebsites.net/health | head -1

echo "🔍 Checking GitHub Actions..."
echo "Visit: https://github.com/raiigauravv/Smart-News-Recommendation-System/actions"

echo "🔍 Find your frontend URL:"
echo "Visit Azure Portal → snr-system-rg → Static Web Apps"
```

---
*Last updated: Deployment verification guide for Smart News Recommendation System*