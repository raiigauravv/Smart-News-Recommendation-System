# Smart News Recommendation System - Architecture

## 🏗️ System Overview

The Smart News Recommendation System is a modern, cloud-native application designed to deliver personalized news recommendations using multiple machine learning algorithms. The system follows a microservices architecture with clear separation of concerns between the frontend, backend, and data processing layers.

## 📐 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Client Layer                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Web Browser  │  Mobile App  │  Desktop App  │  API Clients  │  Third Party │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Presentation Layer                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                        React Frontend (TypeScript)                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │   Home Page     │  │ Recommend Page  │  │ Article Cards   │           │
│  │                 │  │                 │  │                 │           │
│  │ • Search        │  │ • Algorithm     │  │ • PDF Export    │           │
│  │ • Trending      │  │   Selection     │  │ • Category      │           │
│  │ • Categories    │  │ • User Input    │  │   Filter        │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                  HTTP/HTTPS
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Application Layer                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                          FastAPI Backend Server                             │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │   API Gateway   │  │   CORS Middleware │  │  Request/Response │         │
│  │                 │  │                 │  │   Validation    │           │
│  │ • Route Handling│  │ • Cross-Origin  │  │                 │           │
│  │ • Authentication│  │   Requests      │  │ • Pydantic     │           │
│  │ • Rate Limiting │  │ • Headers       │  │   Schemas       │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │   Adapters      │  │   Main App      │  │   Settings      │           │
│  │                 │  │                 │  │                 │           │
│  │ • Business Logic│  │ • Route         │  │ • Configuration │           │
│  │ • Data Transform│  │   Definitions   │  │ • Environment   │           │
│  │ • Error Handling│  │ • Dependency    │  │   Variables     │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                    Function Calls
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             Business Layer                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                        Recommendation Engine (utils/)                       │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │ BERT-based Rec  │  │ Hybrid System   │  │ Collaborative   │           │
│  │                 │  │                 │  │ Filtering       │           │
│  │ • Transformer   │  │ • Content +     │  │                 │           │
│  │   Models        │  │   Collaborative │  │ • User-Item     │           │
│  │ • Semantic      │  │ • Weighted      │  │   Matrix        │           │
│  │   Similarity    │  │   Scoring       │  │ • SVD           │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │ Content-based   │  │ Search Engine   │  │ PDF Generator   │           │
│  │ Filtering       │  │                 │  │                 │           │
│  │                 │  │ • Keyword       │  │ • ReportLab     │           │
│  │ • TF-IDF        │  │   Matching      │  │ • Custom        │           │
│  │ • Cosine        │  │ • Category      │  │   Templates     │           │
│  │   Similarity    │  │   Filtering     │  │ • User Reports  │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                    Data Access
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Data Layer                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                           MIND Dataset Storage                              │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │   News Data     │  │ User Behaviors  │  │   Embeddings    │           │
│  │                 │  │                 │  │                 │           │
│  │ • news.tsv      │  │ • behaviors.tsv │  │ • entity_       │           │
│  │ • Articles      │  │ • Click History │  │   embedding.vec │           │
│  │ • Categories    │  │ • Impressions   │  │ • relation_     │           │
│  │ • Metadata      │  │ • User Profiles │  │   embedding.vec │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │ Processed Data  │  │    Cache Layer  │  │  Temp Storage   │           │
│  │                 │  │                 │  │                 │           │
│  │ • TF-IDF        │  │ • In-Memory     │  │ • Generated     │           │
│  │   Matrices      │  │   Caching       │  │   PDFs          │           │
│  │ • User-Item     │  │ • Model Cache   │  │ • Session Data  │           │
│  │   Interactions  │  │ • Query Cache   │  │ • Logs          │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 Component Details

### Frontend Architecture (React + TypeScript)

#### Core Components
- **App.tsx**: Main application component with routing
- **Home.tsx**: Landing page with search and trending news
- **Recommend.tsx**: Personalized recommendations interface
- **ArticleCard.tsx**: Reusable article display component

#### State Management
- **TanStack Query**: Server state management and caching
- **React Hooks**: Local component state management
- **Context API**: Global application state

#### UI/UX Features
- **Responsive Design**: Mobile-first approach
- **Modern Styling**: CSS-in-JS with styled-components
- **Loading States**: Skeleton screens and spinners
- **Error Boundaries**: Graceful error handling

### Backend Architecture (FastAPI)

#### API Structure
```
server/
├── app/
│   ├── main.py          # FastAPI application and routes
│   ├── adapters.py      # Business logic adapters
│   ├── schemas.py       # Pydantic data models
│   └── settings.py      # Configuration management
└── requirements.txt     # Python dependencies
```

#### Key Endpoints
- `GET /health`: System health check
- `GET /trending`: Trending news articles
- `POST /recommend`: Personalized recommendations
- `POST /search`: Keyword and category search
- `POST /export/pdf`: PDF report generation

#### Middleware Stack
1. **CORS Middleware**: Cross-origin request handling
2. **Request Validation**: Pydantic schema validation
3. **Error Handling**: Custom exception handlers
4. **Logging**: Request/response logging

### Business Logic Layer

#### Recommendation Algorithms

##### 1. BERT-based Recommendations
```python
def bert_recommendations(user_id: str, articles: List[Dict]) -> List[Dict]:
    """
    Advanced transformer-based content understanding
    - Uses pre-trained BERT models for semantic analysis
    - Analyzes article content and user preferences
    - Provides contextually relevant recommendations
    """
```

##### 2. Hybrid Recommendations
```python
def hybrid_recommendations(user_id: str, alpha: float = 0.5) -> List[Dict]:
    """
    Combines collaborative and content-based filtering
    - Weighted combination of multiple algorithms
    - Balances popularity and personalization
    - Optimizes for both accuracy and diversity
    """
```

##### 3. Collaborative Filtering
```python
def collaborative_filtering(user_id: str, n_factors: int = 100) -> List[Dict]:
    """
    User behavior-based recommendations
    - Matrix factorization using SVD
    - Identifies similar users and their preferences
    - Effective for discovering trending content
    """
```

##### 4. Content-based Filtering
```python
def content_based_recommendations(user_id: str, articles: List[Dict]) -> List[Dict]:
    """
    Article similarity-based recommendations
    - TF-IDF vectorization of article content
    - Cosine similarity calculations
    - Recommends articles similar to user history
    """
```

## 🔄 Data Flow

### 1. User Request Flow
```
User Action → Frontend Component → API Call → FastAPI Route → 
Business Logic → Data Processing → Response → Frontend Update → UI Render
```

### 2. Recommendation Generation Flow
```
User ID Input → Algorithm Selection → Data Retrieval → 
Feature Engineering → Model Processing → Ranking → 
Response Formatting → Frontend Display
```

### 3. Search Flow
```
Search Query → Keyword Processing → Category Filtering → 
Data Matching → Relevance Scoring → Result Ranking → 
Response Return → Frontend Display
```

### 4. PDF Export Flow
```
Article Selection → PDF Request → Template Processing → 
Content Formatting → PDF Generation → File Response → 
Browser Download
```

## 📊 Data Models

### API Schemas (Pydantic)

```python
class Article(BaseModel):
    id: str
    title: str
    abstract: str
    category: str
    subcategory: Optional[str]
    url: Optional[str]
    published_date: Optional[datetime]

class RecommendationRequest(BaseModel):
    user_id: str
    algorithm: Literal["bert", "hybrid", "collaborative", "content"]
    limit: Optional[int] = 10

class SearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    limit: Optional[int] = 20

class PDFExportRequest(BaseModel):
    articles: List[Article]
    user_id: str
    title: str = "News Report"
```

### Database Schema (MIND Dataset)

#### News Articles (news.tsv)
- **NewsID**: Unique article identifier
- **Category**: Main category (e.g., sports, entertainment)
- **SubCategory**: Detailed subcategory
- **Title**: Article headline
- **Abstract**: Article summary
- **URL**: Original article link
- **TitleEntities**: Named entities in title
- **AbstractEntities**: Named entities in abstract

#### User Behaviors (behaviors.tsv)
- **ImpressionID**: Unique impression identifier
- **UserID**: Unique user identifier
- **Time**: Timestamp of interaction
- **History**: User's click history
- **Impressions**: Articles shown to user with click labels

## 🚀 Deployment Architecture

### Development Environment
```
Local Machine
├── Frontend (localhost:5173)
├── Backend (localhost:8000)
└── Dataset (local files)
```

### Production Environment
```
Azure Cloud
├── Static Web App (Frontend)
├── Container App (Backend)
├── Container Registry (Images)
└── Storage Account (Dataset)
```

## 🔒 Security Considerations

### Authentication & Authorization
- JWT token-based authentication (future enhancement)
- Role-based access control
- API rate limiting

### Data Security
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CORS configuration

### Infrastructure Security
- HTTPS encryption
- Environment variable management
- Secret management with Azure Key Vault
- Network security groups

## 📈 Performance Optimization

### Caching Strategy
- **Frontend**: Browser caching, service workers
- **Backend**: In-memory caching for models
- **Database**: Query result caching

### Scalability Features
- **Horizontal Scaling**: Multiple backend instances
- **Load Balancing**: Azure Load Balancer
- **Auto-scaling**: Based on CPU/memory metrics
- **CDN**: Static asset delivery optimization

### Performance Metrics
- **Response Time**: < 500ms for API calls
- **Throughput**: 1000+ requests per second
- **Availability**: 99.9% uptime SLA
- **Error Rate**: < 0.1% failed requests

## 🔧 Configuration Management

### Environment Variables
```bash
# Backend Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Dataset Configuration
MIND_DATASET_PATH=./MINDsmall_train/
MAX_ARTICLES=10000

# Model Configuration
TFIDF_MAX_FEATURES=5000
SVD_N_COMPONENTS=100
RECOMMENDATION_LIMIT=20

# Frontend Configuration
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=Smart News Recommendation System
```

### Feature Flags
- Algorithm selection toggle
- PDF export enable/disable
- Category filtering options
- Debug mode settings

## 🧪 Testing Strategy

### Unit Testing
- Frontend: Jest + React Testing Library
- Backend: pytest + FastAPI TestClient
- Business Logic: Algorithm-specific tests

### Integration Testing
- API endpoint testing
- Database integration tests
- Frontend-backend integration

### Performance Testing
- Load testing with Artillery
- Stress testing for peak loads
- Memory usage profiling
- Response time monitoring

## 📚 API Documentation

### OpenAPI Specification
FastAPI automatically generates OpenAPI documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Versioning
- Current version: v1
- Future versioning strategy: URL-based versioning
- Backward compatibility maintenance

## 🔮 Future Enhancements

### Planned Features
1. **Real-time Notifications**: WebSocket integration
2. **Social Features**: User comments and sharing
3. **Advanced Analytics**: User behavior tracking
4. **Mobile App**: React Native implementation
5. **Multi-language Support**: Internationalization

### Technical Improvements
1. **GraphQL API**: More efficient data fetching
2. **Microservices**: Service decomposition
3. **Event-driven Architecture**: Message queues
4. **AI/ML Enhancements**: Deep learning models
5. **Edge Computing**: CDN-based recommendations

## 📝 Maintenance & Monitoring

### Logging Strategy
- **Application Logs**: Structured JSON logging
- **Access Logs**: Request/response tracking
- **Error Logs**: Exception tracking and alerting
- **Performance Logs**: Metric collection

### Monitoring Tools
- **Azure Monitor**: Infrastructure monitoring
- **Application Insights**: Performance monitoring
- **Log Analytics**: Centralized log management
- **Alerts**: Automated incident response

### Backup & Recovery
- **Code Repository**: Git-based version control
- **Configuration**: Infrastructure as Code
- **Data Backup**: Regular dataset backups
- **Disaster Recovery**: Multi-region deployment

---

This architecture document provides a comprehensive overview of the Smart News Recommendation System's design, implementation, and operational considerations. The system is built with scalability, maintainability, and performance in mind, following modern cloud-native principles and best practices.