# Smart News Recommendation System - System Diagrams

This document provides comprehensive visual representations of the Smart News Recommendation System architecture and data flows.

## 1. High-Level System Architecture

```mermaid
flowchart TB
    subgraph Client["Client Layer"]
        Web["Web Browser<br/>React SPA"]
        Mobile["Mobile App<br/>Future"]
        APIClient["API Clients<br/>Third Party"]
    end
    
    subgraph CDN["CDN & Static Hosting"]
        Vite["Vite Dev Server<br/>localhost:5173"]
        Azure["Azure Static Web Apps<br/>Production CDN"]
    end
    
    subgraph Gateway["API Gateway"]
        FastAPI["FastAPI Server<br/>localhost:8000"]
        CORS["CORS Middleware<br/>Cross-Origin Support"]
    end
    
    subgraph AppLayer["Application Layer"]
        subgraph CoreServices["Core Services"]
            RecEngine["Recommendation Engine<br/>4 ML Algorithms"]
            SearchSvc["Search Service<br/>Keyword + Category"]
            PDFSvc["PDF Generation<br/>ReportLab"]
            HealthSvc["Health Check<br/>System Status"]
        end
        
        subgraph BusinessLogic["Business Logic"]
            Adapters["Service Adapters<br/>Data Processing"]
            Schemas["Pydantic Schemas<br/>Validation"]
            Settings["Configuration<br/>Environment"]
        end
    end
    
    subgraph DataLayer["Data Layer"]
        MIND["MIND Dataset<br/>News + Behaviors"]
        NewsData["news.tsv<br/>51k+ Articles"]
        BehaviorData["behaviors.tsv<br/>User Interactions"]
        Embeddings["Entity/Relation<br/>Embeddings.vec"]
        TempStorage["Temporary Storage<br/>PDFs + Cache"]
    end
    
    Web --> Vite
    Mobile --> Azure
    APIClient --> FastAPI
    Vite --> FastAPI
    Azure --> FastAPI
    FastAPI --> CORS
    CORS --> RecEngine
    CORS --> SearchSvc
    CORS --> PDFSvc
    CORS --> HealthSvc
    
    RecEngine --> Adapters
    SearchSvc --> Adapters
    PDFSvc --> Adapters
    Adapters --> Schemas
    Adapters --> Settings
    Adapters --> MIND
    
    MIND --> NewsData
    MIND --> BehaviorData
    MIND --> Embeddings
    PDFSvc --> TempStorage
```

## 2. Recommendation Engine Architecture

```mermaid
flowchart TB
    subgraph Input["Input Layer"]
        UserID["User ID"]
        RecentClicks["Recent Clicks<br/>Array of News IDs"]
        NumRecs["Number of Recommendations<br/>K Parameter"]
        Locale["User Locale<br/>Language Preference"]
    end
    
    subgraph Engine["Recommendation Engine Core"]
        subgraph Algorithms["ML Algorithms"]
            BERT["BERT4Rec<br/>Sequential Modeling"]
            Hybrid["Hybrid Filtering<br/>Content + Collaborative"]
            Collaborative["Collaborative Filtering<br/>User Similarity"]
            ContentBased["Content-Based<br/>Article Features"]
        end
        
        subgraph Processing["Processing Layer"]
            Aggregator["Score Aggregation<br/>Weighted Combination"]
            Deduplicator["Deduplication<br/>Remove Duplicates"]
            Personalizer["Personalization<br/>User Preferences"]
        end
    end
    
    subgraph Data["Data Sources"]
        NewsCorpus["News Corpus<br/>51k+ Articles"]
        UserBehavior["User Behaviors<br/>Click History"]
        EntityEmbed["Entity Embeddings<br/>Knowledge Graph"]
        RelationEmbed["Relation Embeddings<br/>Semantic Links"]
    end
    
    subgraph Output["Output Layer"]
        RankedList["Ranked Article List<br/>Personalized Results"]
        Explanations["Recommendation Reasons<br/>Transparency"]
        Confidence["Confidence Scores<br/>Quality Metrics"]
    end
    
    UserID --> Engine
    RecentClicks --> Engine
    NumRecs --> Engine
    Locale --> Engine
    
    Engine --> BERT
    Engine --> Hybrid
    Engine --> Collaborative
    Engine --> ContentBased
    
    BERT --> Aggregator
    Hybrid --> Aggregator
    Collaborative --> Aggregator
    ContentBased --> Aggregator
    
    Aggregator --> Deduplicator
    Deduplicator --> Personalizer
    
    NewsCorpus --> Engine
    UserBehavior --> Engine
    EntityEmbed --> Engine
    RelationEmbed --> Engine
    
    Personalizer --> RankedList
    Personalizer --> Explanations
    Personalizer --> Confidence
```

## 3. Data Flow Sequence

```mermaid
sequenceDiagram
    participant Client as React Client
    participant API as FastAPI Server
    participant Engine as Recommendation Engine
    participant Data as MIND Dataset
    participant PDF as PDF Service
    
    Note over Client,PDF: User Request Flow
    
    Client->>API: POST /recommend
    Note right of Client: {user_id, recent_clicks, k, locale}
    
    API->>API: Validate Request Schema
    API->>Engine: Process Recommendation Request
    
    Engine->>Data: Load News Articles
    Engine->>Data: Load User Behaviors
    Engine->>Data: Load Embeddings
    
    Note over Engine: ML Algorithm Processing
    Engine->>Engine: BERT4Rec Sequential Analysis
    Engine->>Engine: Hybrid Filtering
    Engine->>Engine: Collaborative Filtering
    Engine->>Engine: Content-Based Filtering
    
    Engine->>Engine: Aggregate & Rank Results
    Engine->>API: Return Ranked Articles
    
    API->>Client: JSON Response with Recommendations
    
    Note over Client,PDF: PDF Export Flow
    
    Client->>API: POST /export/pdf
    Note right of Client: {articles: [selected recommendations]}
    
    API->>PDF: Generate PDF Report
    PDF->>PDF: Create PDF with ReportLab
    PDF->>API: Return PDF Binary
    
    API->>Client: PDF File Download
```

## 4. Component Interaction Model

```mermaid
flowchart LR
    subgraph Frontend["Frontend Components"]
        HomePage["Home Page<br/>Article Discovery"]
        RecommendPage["Recommend Page<br/>Personalized Feed"]
        ArticleCard["Article Cards<br/>Interactive Display"]
        ExportBtn["Export Button<br/>PDF Generation"]
    end
    
    subgraph API["API Endpoints"]
        HealthAPI["/health<br/>System Status"]
        TrendingAPI["/trending<br/>Popular Articles"]
        RecommendAPI["/recommend<br/>Personalized Feed"]
        ExportAPI["/export/pdf<br/>PDF Generation"]
    end
    
    subgraph Services["Backend Services"]
        RecommendSvc["Recommendation Service<br/>ML Processing"]
        SearchSvc["Search Service<br/>Query Processing"]
        PDFSvc["PDF Service<br/>Document Generation"]
        DataSvc["Data Service<br/>MIND Dataset Access"]
    end
    
    subgraph Storage["Data Storage"]
        NewsDB["News Articles<br/>51k+ Items"]
        BehaviorDB["User Behaviors<br/>Interaction History"]
        EmbeddingDB["ML Embeddings<br/>Vector Representations"]
        TempFiles["Temporary Files<br/>PDF Cache"]
    end
    
    HomePage --> TrendingAPI
    RecommendPage --> RecommendAPI
    ArticleCard --> RecommendAPI
    ExportBtn --> ExportAPI
    
    HealthAPI --> DataSvc
    TrendingAPI --> SearchSvc
    RecommendAPI --> RecommendSvc
    ExportAPI --> PDFSvc
    
    RecommendSvc --> DataSvc
    SearchSvc --> DataSvc
    PDFSvc --> TempFiles
    DataSvc --> NewsDB
    DataSvc --> BehaviorDB
    DataSvc --> EmbeddingDB
```

## 5. Technology Stack Overview

```mermaid
flowchart TB
    subgraph FrontendStack["Frontend Technology Stack"]
        React["React 18<br/>Component Library"]
        TypeScript["TypeScript<br/>Type Safety"]
        Vite["Vite<br/>Build Tool & Dev Server"]
        TailwindCSS["Tailwind CSS<br/>Styling Framework"]
    end
    
    subgraph BackendStack["Backend Technology Stack"]
        FastAPI["FastAPI<br/>Python Web Framework"]
        Pydantic["Pydantic<br/>Data Validation"]
        Uvicorn["Uvicorn<br/>ASGI Server"]
        Python["Python 3.9+<br/>Runtime Environment"]
    end
    
    subgraph MLStack["Machine Learning Stack"]
        Transformers["Transformers<br/>BERT Models"]
        NumPy["NumPy<br/>Numerical Computing"]
        Pandas["Pandas<br/>Data Manipulation"]
        SciKitLearn["Scikit-learn<br/>ML Algorithms"]
    end
    
    subgraph DataStack["Data & Storage Stack"]
        TSV["TSV Files<br/>MIND Dataset Format"]
        Embeddings["Vector Embeddings<br/>.vec Files"]
        ReportLab["ReportLab<br/>PDF Generation"]
        JSON["JSON<br/>API Communication"]
    end
    
    subgraph DevOpsStack["DevOps & Deployment Stack"]
        Docker["Docker<br/>Containerization"]
        AzureStaticApps["Azure Static Web Apps<br/>Frontend Hosting"]
        AzureContainerApps["Azure Container Apps<br/>Backend Hosting"]
        GitHub["GitHub Actions<br/>CI/CD Pipeline"]
    end
    
    React --> TypeScript
    TypeScript --> Vite
    Vite --> TailwindCSS
    
    FastAPI --> Pydantic
    Pydantic --> Uvicorn
    Uvicorn --> Python
    
    Transformers --> NumPy
    NumPy --> Pandas
    Pandas --> SciKitLearn
    
    TSV --> Embeddings
    Embeddings --> ReportLab
    ReportLab --> JSON
    
    Docker --> AzureStaticApps
    AzureStaticApps --> AzureContainerApps
    AzureContainerApps --> GitHub
```

## 6. Deployment Architecture

```mermaid
flowchart TB
    subgraph Development["Development Environment"]
        DevFrontend["Vite Dev Server<br/>localhost:5173"]
        DevBackend["Uvicorn Server<br/>localhost:8000"]
        LocalData["Local MIND Dataset<br/>File System"]
    end
    
    subgraph Production["Production Environment"]
        subgraph AzureFrontend["Azure Static Web Apps"]
            CDN["Global CDN<br/>Content Distribution"]
            StaticFiles["Static Assets<br/>React Build"]
            CustomDomain["Custom Domain<br/>SSL/TLS"]
        end
        
        subgraph AzureBackend["Azure Container Apps"]
            APIContainer["FastAPI Container<br/>Auto-scaling"]
            LoadBalancer["Load Balancer<br/>High Availability"]
            HealthCheck["Health Monitoring<br/>Auto-recovery"]
        end
        
        subgraph AzureStorage["Azure Storage"]
            BlobStorage["Blob Storage<br/>MIND Dataset"]
            FileShare["File Share<br/>Embeddings"]
            TempStorage["Temp Storage<br/>PDF Cache"]
        end
    end
    
    subgraph CICD["CI/CD Pipeline"]
        GitHubActions["GitHub Actions<br/>Automated Deployment"]
        BuildProcess["Build & Test<br/>Quality Gates"]
        DeploymentSlots["Deployment Slots<br/>Blue-Green Deployment"]
    end
    
    DevFrontend --> GitHubActions
    DevBackend --> GitHubActions
    LocalData --> GitHubActions
    
    GitHubActions --> BuildProcess
    BuildProcess --> DeploymentSlots
    
    DeploymentSlots --> CDN
    DeploymentSlots --> APIContainer
    
    CDN --> StaticFiles
    StaticFiles --> CustomDomain
    
    APIContainer --> LoadBalancer
    LoadBalancer --> HealthCheck
    
    APIContainer --> BlobStorage
    APIContainer --> FileShare
    APIContainer --> TempStorage
```

## 7. Security Architecture

```mermaid
flowchart TB
    subgraph Client["Client Security"]
        HTTPS["HTTPS Encryption<br/>TLS 1.3"]
        CSP["Content Security Policy<br/>XSS Protection"]
        CORS["CORS Headers<br/>Cross-Origin Security"]
    end
    
    subgraph APIGateway["API Gateway Security"]
        RateLimit["Rate Limiting<br/>DDoS Protection"]
        InputValidation["Input Validation<br/>Pydantic Schemas"]
        RequestLogging["Request Logging<br/>Audit Trail"]
    end
    
    subgraph Application["Application Security"]
        DataSanitization["Data Sanitization<br/>SQL Injection Prevention"]
        ErrorHandling["Secure Error Handling<br/>Information Disclosure Prevention"]
        SessionManagement["Session Management<br/>User State Security"]
    end
    
    subgraph Infrastructure["Infrastructure Security"]
        AzureAD["Azure Active Directory<br/>Identity Management"]
        NetworkSecurity["Network Security Groups<br/>Firewall Rules"]
        Monitoring["Security Monitoring<br/>Threat Detection"]
    end
    
    subgraph Data["Data Security"]
        Encryption["Data Encryption<br/>At Rest & In Transit"]
        AccessControl["Access Control<br/>Principle of Least Privilege"]
        DataPrivacy["Data Privacy<br/>GDPR Compliance"]
    end
    
    HTTPS --> RateLimit
    CSP --> InputValidation
    CORS --> RequestLogging
    
    RateLimit --> DataSanitization
    InputValidation --> ErrorHandling
    RequestLogging --> SessionManagement
    
    DataSanitization --> AzureAD
    ErrorHandling --> NetworkSecurity
    SessionManagement --> Monitoring
    
    AzureAD --> Encryption
    NetworkSecurity --> AccessControl
    Monitoring --> DataPrivacy
```

## 8. ML Algorithm Flow

```mermaid
flowchart TB
    subgraph Input["Input Processing"]
        UserProfile["User Profile<br/>ID + Preferences"]
        ClickHistory["Click History<br/>Recent Interactions"]
        NewsCorpus["News Corpus<br/>Article Database"]
    end
    
    subgraph BERT["BERT4Rec Algorithm"]
        BERTPreprocess["Sequence Preprocessing<br/>Tokenization"]
        BERTModel["Transformer Model<br/>Sequential Patterns"]
        BERTScoring["Sequence Scoring<br/>Next Item Prediction"]
    end
    
    subgraph Hybrid["Hybrid Filtering"]
        ContentFeatures["Content Features<br/>Article Attributes"]
        UserSimilarity["User Similarity<br/>Collaborative Signals"]
        HybridScoring["Hybrid Scoring<br/>Combined Approach"]
    end
    
    subgraph Collaborative["Collaborative Filtering"]
        UserMatrix["User-Item Matrix<br/>Interaction Patterns"]
        SimilarityCalc["Similarity Calculation<br/>Cosine/Pearson"]
        CollabPrediction["Collaborative Prediction<br/>Neighborhood-based"]
    end
    
    subgraph ContentBased["Content-Based Filtering"]
        ArticleVectors["Article Vectors<br/>TF-IDF Features"]
        UserPreferences["User Preferences<br/>Profile Building"]
        ContentScoring["Content Scoring<br/>Cosine Similarity"]
    end
    
    subgraph Aggregation["Score Aggregation"]
        WeightedSum["Weighted Combination<br/>Algorithm Fusion"]
        Normalization["Score Normalization<br/>Range Adjustment"]
        Ranking["Final Ranking<br/>Top-K Selection"]
    end
    
    UserProfile --> BERT
    ClickHistory --> BERT
    NewsCorpus --> BERT
    
    UserProfile --> Hybrid
    ClickHistory --> Hybrid
    NewsCorpus --> Hybrid
    
    UserProfile --> Collaborative
    ClickHistory --> Collaborative
    NewsCorpus --> Collaborative
    
    UserProfile --> ContentBased
    ClickHistory --> ContentBased
    NewsCorpus --> ContentBased
    
    BERTPreprocess --> BERTModel
    BERTModel --> BERTScoring
    
    ContentFeatures --> HybridScoring
    UserSimilarity --> HybridScoring
    
    UserMatrix --> SimilarityCalc
    SimilarityCalc --> CollabPrediction
    
    ArticleVectors --> ContentScoring
    UserPreferences --> ContentScoring
    
    BERTScoring --> WeightedSum
    HybridScoring --> WeightedSum
    CollabPrediction --> WeightedSum
    ContentScoring --> WeightedSum
    
    WeightedSum --> Normalization
    Normalization --> Ranking
```

## 9. Error Handling & Recovery

```mermaid
flowchart TB
    subgraph ErrorTypes["Error Categories"]
        ClientErrors["Client Errors<br/>4xx Status Codes"]
        ServerErrors["Server Errors<br/>5xx Status Codes"]
        SystemErrors["System Errors<br/>Infrastructure Issues"]
        DataErrors["Data Errors<br/>Corruption/Missing"]
    end
    
    subgraph Detection["Error Detection"]
        HealthChecks["Health Check Endpoints<br/>Proactive Monitoring"]
        LoggingSystem["Centralized Logging<br/>Error Aggregation"]
        Monitoring["Real-time Monitoring<br/>Alert System"]
    end
    
    subgraph Handling["Error Handling"]
        GracefulDegradation["Graceful Degradation<br/>Fallback Mechanisms"]
        RetryLogic["Retry Logic<br/>Exponential Backoff"]
        CircuitBreaker["Circuit Breaker<br/>Failure Isolation"]
    end
    
    subgraph Recovery["Recovery Strategies"]
        AutoRecovery["Auto Recovery<br/>Self-healing"]
        ManualIntervention["Manual Intervention<br/>Admin Actions"]
        DataRecovery["Data Recovery<br/>Backup Restoration"]
    end
    
    subgraph UserExperience["User Experience"]
        ErrorMessages["User-friendly Messages<br/>Clear Communication"]
        FallbackContent["Fallback Content<br/>Default Recommendations"]
        ProgressIndicators["Progress Indicators<br/>Loading States"]
    end
    
    ClientErrors --> HealthChecks
    ServerErrors --> LoggingSystem
    SystemErrors --> Monitoring
    DataErrors --> HealthChecks
    
    HealthChecks --> GracefulDegradation
    LoggingSystem --> RetryLogic
    Monitoring --> CircuitBreaker
    
    GracefulDegradation --> AutoRecovery
    RetryLogic --> ManualIntervention
    CircuitBreaker --> DataRecovery
    
    AutoRecovery --> ErrorMessages
    ManualIntervention --> FallbackContent
    DataRecovery --> ProgressIndicators
```

---

## Summary

This system architecture provides:

- **Scalable Architecture**: Microservices-based design with clear separation of concerns
- **Modern Technology Stack**: React frontend with FastAPI backend and advanced ML algorithms
- **Robust Data Pipeline**: Efficient processing of the MIND dataset with multiple recommendation strategies
- **Production-Ready Deployment**: Azure-based cloud infrastructure with CI/CD automation
- **Security First**: Comprehensive security measures across all layers
- **Error Resilience**: Robust error handling and recovery mechanisms
- **User-Centric Design**: Focus on performance, usability, and transparency

The system is designed to handle real-world usage patterns while maintaining high performance, reliability, and user satisfaction.