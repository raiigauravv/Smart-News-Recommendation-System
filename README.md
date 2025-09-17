# Smart News Recommendation System 🗞️

A comprehensive, end-to-end personalized news recommendation system built using the Microsoft MIND dataset. Features multiple recommendation approaches including collaborative filtering, content-based filtering, hybrid models, and advanced BERT4Rec deep learning.

## 🎯 Features

- **Multiple Recommendation Engines**:
  - Collaborative Filtering (SVD-based)
  - Content-Based Filtering (TF-IDF + Cosine Similarity)
  - Hybrid Approach (Combining both with tunable weights)
  - BERT4Rec (Deep Learning Sequential Recommendations)
  - Keyword Search
  - Trending Articles

- **Interactive Web Interface**:
  - Streamlit-based user-friendly interface
  - Dark theme optimized
  - Multiple browsing modes
  - PDF and CSV export functionality
  - AI-powered article summaries

- **Advanced Features**:
  - Real-time recommendations
  - User behavior analysis
  - Category preference learning
  - Trending content detection
  - Comprehensive evaluation metrics

## 📁 Project Structure

```
Smart-News-Recommendation-System/
├── main.py                 # Streamlit web application
├── mind-ds.ipynb          # Comprehensive analysis notebook
├── utils/
│   ├── recommenders.py    # Core recommendation algorithms
│   └── pdf_utils.py       # PDF generation utilities
├── archive/
│   └── MINDsmall_train/   # MIND dataset
│       ├── news.tsv       # News articles metadata
│       ├── behaviors.tsv  # User interaction data
│       ├── entity_embedding.vec
│       └── relation_embedding.vec
├── temp/                  # Generated reports (auto-created)
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- 8GB+ RAM (for processing large dataset)
- 2GB+ free disk space

### Installation

1. **Clone or navigate to the project directory**

   ```bash
   cd Smart-News-Recommendation-System-main
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data (first time only)**

   ```python
   import nltk
   nltk.download('stopwords')
   ```

4. **Run the application**

   ```bash
   streamlit run main.py
   ```

5. **Open your browser** and go to `http://localhost:8501`

## 🔧 Configuration

### Environment Variables (.env)

- `NEWS_DATA_PATH`: Path to news.tsv file
- `BEHAVIORS_DATA_PATH`: Path to behaviors.tsv file
- `TFIDF_MAX_FEATURES`: Maximum features for TF-IDF (default: 5000)
- `SVD_LATENT_FACTORS`: SVD components (default: 100)
- `HYBRID_ALPHA_DEFAULT`: Default hybrid mixing parameter (default: 0.0)

### Model Parameters

- **Alpha Parameter**: Controls hybrid recommendation mixing
  - 0.0 = Pure collaborative filtering
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
