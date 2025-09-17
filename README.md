# Smart News Recommendation System 🗞️

A comprehensive news recommendation system with FastAPI backend and React frontend, featuring multiple ML algorithms and PDF export functionality.

## 🚀 How to run locally (two terminals)

### Terminal 1 - Backend
```bash
cd server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend  
```bash
cd web
npm install
npm run dev
```

Visit: http://localhost:5173 (frontend) and http://localhost:8000/docs (API docs)

## 🐳 How to run with Docker Compose

```bash
docker compose up --build
```

Visit: http://localhost:5173 (frontend) and http://localhost:8000 (API)

## 📡 API endpoints

- `GET /health` - Health check
- `GET /trending?k={number}` - Get trending articles  
- `POST /recommend` - Get personalized recommendations
- `POST /search` - Keyword search articles
- `POST /export/pdf` - Export articles to PDF

## ⚙️ Frontend .env.local note

Create `web/.env.local` with:
```
VITE_API_URL=http://localhost:8000
```

## 📁 Project Structure

```
repo-root/
├─ server/            # FastAPI backend
├─ web/               # React (Vite + TS) frontend  
├─ utils/             # Business logic (recommendation algorithms)
├─ docker-compose.yml # One-command development
└─ README.md          # This file
```

## 🧪 Running Tests

```bash
cd server
source .venv/bin/activate
pip install -r requirements.txt pytest
pytest -q
```

## 📊 Features

- **Multiple Recommendation Engines**: Collaborative filtering, content-based, hybrid approaches
- **Real-time API**: FastAPI with automatic OpenAPI documentation
- **Modern Frontend**: React with TypeScript and Vite
- **PDF Export**: Download recommendations as formatted PDF reports
- **Docker Support**: One-command development environment

## ☁️ Azure Deployment

### What to deploy
- Deploy only the **backend** to Azure App Service using ACR (small Python slim image)
- Deploy **frontend** to Azure Static Web Apps or Vercel/Netlify (free)
- Point VITE_API_URL to the App Service URL

### Backend commands (once)
```bash
# login
az login

# create RG
az group create -n snr-rg -l canadacentral

# create ACR (Basic)
az acr create -g snr-rg -n snracr --sku Basic

# app service plan + webapp (container)
az appservice plan create -g snr-rg -n snr-asp --is-linux --sku B1
az webapp create -g snr-rg -p snr-asp -n snr-api --deployment-container-image-name mcr.microsoft.com/azure-app-service/samples/aspnethelloworld:latest
```

### GitHub secrets (repo → Settings → Secrets and variables → Actions)
- `AZURE_CREDENTIALS` (output from `az ad sp create-for-rbac --name snr-sp --sdk-auth --role contributor --scopes /subscriptions/<SUB_ID>/resourceGroups/snr-rg`)
- `AZURE_WEBAPP_NAME = snr-api`
- `AZURE_RG = snr-rg`
- `AZURE_ACR_NAME = snracr`

### Why this saves space
- Python slim base, no transformers/torch
- Static frontend hosted elsewhere (no App Service disk usage)
- No dataset baked into the image; your utils load minimal data at runtime
  - 1.0 = Pure content-based filtering
  - 0.5 = Balanced hybrid approach

## 📊 Dataset Information

### MIND Dataset (Microsoft News Dataset)

- **News Articles**: 51,282+ articles with metadata
- **User Interactions**: 50,000+ users with behavior data
- **Categories**: news, sports, entertainment, finance, lifestyle, etc.
- **Features**: Title, Abstract, Category, Subcategory, Entities

### Data Processing Pipeline

1. **News Data Cleaning**: Remove articles without title/abstract
2. **Behavior Parsing**: Extract user click histories and impressions
3. **Interaction Matrix**: Create user-item interaction matrix
4. **Feature Engineering**: TF-IDF vectorization, SVD decomposition
5. **Model Training**: Train recommendation models

## 🎮 Usage Guide

### Web Interface Modes

#### 1. Browse by Keyword 🔍

- Enter keywords like "Sports", "Health", "Finance"
- Get content-based recommendations
- View AI-generated summaries
- Export results as PDF/CSV

#### 2. Personalized Recommendations 👤

- **User-Based Tab**: Collaborative filtering recommendations
- **Hybrid Tab**: Combined collaborative + content-based
- **Keyword + Hybrid Tab**: Keyword-guided personalized recommendations
- **Daily Trends Tab**: Most popular articles

### Sample User IDs for Testing

- `U13740` - Sports and entertainment enthusiast
- `U91836` - News and business focused
- `U73700` - Health and lifestyle interested
- `U34670` - General news consumer
- `U8125` - Finance and technology focused

## 🧪 Jupyter Notebook Analysis

The `mind-ds.ipynb` notebook contains:

1. **Data Exploration & Preprocessing**
2. **Content-Based Filtering Implementation**
3. **Collaborative Filtering (SVD)**
4. **Hybrid Model Development**
5. **BERT4Rec Deep Learning Model**
6. **Comprehensive Evaluation Metrics**
7. **Visualization and Analysis**

### Key Findings

- Best hybrid parameter: α = 0.0 (collaborative filtering dominant)
- SVD with 100 latent factors achieves good performance
- Content-based filtering works well for cold-start scenarios
- BERT4Rec shows promise for sequential recommendations

## 📈 Performance Metrics

### Evaluation Results

- **Collaborative Filtering**:
  - Precision: 1.0, Recall: 0.090, F1: 0.166
- **Content-Based**:
  - Precision: 1.0, Recall: 0.002, F1: 0.004
- **Hybrid (α=0.0)**:
  - Precision: 1.0, Recall: 0.090, F1: 0.166

## 🔧 Technical Implementation

### Algorithms Used

1. **TF-IDF Vectorization**: For content similarity
2. **Cosine Similarity**: Content-based recommendations
3. **Singular Value Decomposition (SVD)**: Collaborative filtering
4. **BERT4Rec**: Sequential deep learning recommendations
5. **Hybrid Scoring**: Weighted combination of methods

### Libraries & Technologies

- **Frontend**: Streamlit
- **ML/Data**: pandas, numpy, scikit-learn, scipy
- **NLP**: transformers, nltk
- **Visualization**: matplotlib, seaborn
- **PDF**: reportlab
- **Deep Learning**: torch, datasets

## 🎯 Use Cases

1. **News Publishers**: Increase user engagement and retention
2. **Content Platforms**: Improve content discovery
3. **Research**: Study recommendation system approaches
4. **Education**: Learn ML/NLP implementation

## 🚨 Troubleshooting

### Common Issues

1. **Memory Error**: Reduce `TFIDF_MAX_FEATURES` or `SVD_LATENT_FACTORS`
2. **Slow Loading**: Large dataset processing takes time initially
3. **Missing Packages**: Install all requirements.txt dependencies
4. **Path Errors**: Ensure data files are in correct archive/ location

### Performance Tips

- First run takes 2-3 minutes to load and process data
- Subsequent runs are faster due to model caching
- Use smaller top_n values for faster response

## 📝 Development Notes

### Model Training Time

- TF-IDF fitting: ~30 seconds
- SVD training: ~10 seconds
- Initial data loading: ~2 minutes

### Memory Usage

- Peak memory: ~4-6GB during initial processing
- Runtime memory: ~2-3GB

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Implement improvements
4. Add tests if applicable
5. Submit pull request

## 📄 License

This project uses the Microsoft MIND dataset under Microsoft's terms of use.

## 🙏 Acknowledgments

- Microsoft for the MIND dataset
- Hugging Face for transformer models
- Streamlit team for the web framework
- Open source ML community

---

**Happy Recommending! 🎉**
