# System Architecture Overview

## High-Level System Design

```mermaid
graph TB
    subgraph "Client Layer"
        Web[Web Browser<br/>React SPA]
        Mobile[Mobile App<br/>Future]
    end
    
    subgraph "CDN & Static Hosting"
        Azure[Azure Static Web Apps<br/>React Build + CDN]
    end
    
    subgraph "API Gateway"
        Gateway[Azure Application Gateway<br/>Load Balancer + SSL]
    end
    
    subgraph "Application Layer"
        FastAPI[FastAPI Server<br/>Azure Container Apps]
        subgraph "Services"
            RecEngine[Recommendation Engine]
            SearchSvc[Search Service]
            PDFSvc[PDF Generation]
            Analytics[Analytics Service]
        end
    end
    
    subgraph "Data Layer"
        MIND[MIND Dataset<br/>News + Behaviors]
        Embeddings[Entity/Relation<br/>Embeddings]
        Cache[Redis Cache<br/>Future]
    end
    
    Web --> Azure
    Mobile --> Azure
    Azure --> Gateway
    Gateway --> FastAPI
    FastAPI --> RecEngine
    FastAPI --> SearchSvc
    FastAPI --> PDFSvc
    FastAPI --> Analytics
    RecEngine --> MIND
    RecEngine --> Embeddings
    SearchSvc --> MIND
    PDFSvc --> MIND
    Analytics --> Cache
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API Gateway
    participant B as Backend
    participant ML as ML Engine
    participant D as Data Layer
    
    U->>F: Search/Browse Request
    F->>A: HTTP Request
    A->>B: Route to FastAPI
    B->>ML: Process Request
    ML->>D: Load Data
    D-->>ML: Return Data
    ML-->>B: Generate Recommendations
    B-->>A: JSON Response
    A-->>F: API Response
    F-->>U: Render Results
    
    Note over U,D: Real-time recommendation flow
```

## Component Interaction Diagram

```mermaid
graph LR
    subgraph "Frontend Components"
        Home[Home Component]
        Search[Search Container]
        Articles[Article Grid]
        PDF[PDF Export Button]
    end
    
    subgraph "API Layer"
        API[FastAPI Router]
        Adapters[Service Adapters]
    end
    
    subgraph "Business Logic"
        Recommender[Recommendation Engine]
        PDFGen[PDF Generator]
        DataLoader[Data Loader]
    end
    
    subgraph "Data Sources"
        News[News TSV]
        Behaviors[Behaviors TSV]
        Entities[Entity Embeddings]
    end
    
    Home --> Search
    Search --> Articles
    Home --> PDF
    
    Search --> API
    PDF --> API
    
    API --> Adapters
    Adapters --> Recommender
    Adapters --> PDFGen
    
    Recommender --> DataLoader
    PDFGen --> DataLoader
    
    DataLoader --> News
    DataLoader --> Behaviors
    DataLoader --> Entities
```

## Technology Stack Diagram

```mermaid
graph TB
    subgraph "Frontend Stack"
        React[React 18 + TypeScript]
        Vite[Vite Build Tool]
        StyledComponents[Styled Components]
        ReactQuery[React Query]
        FramerMotion[Framer Motion]
    end
    
    subgraph "Backend Stack"
        FastAPI[FastAPI Framework]
        Python[Python 3.11+]
        Pandas[Pandas + NumPy]
        Sklearn[Scikit-learn]
        ReportLab[ReportLab PDF]
    end
    
    subgraph "DevOps Stack"
        Docker[Docker Containers]
        Azure[Azure Cloud Platform]
        GitHub[GitHub Actions CI/CD]
        StaticApps[Azure Static Web Apps]
        ContainerApps[Azure Container Apps]
    end
    
    subgraph "Data Stack"
        MIND[Microsoft MIND Dataset]
        TSV[TSV File Format]
        Embeddings[Pre-trained Embeddings]
        FileSystem[Local File System]
    end
    
    React --> FastAPI
    FastAPI --> MIND
    Docker --> Azure
    GitHub --> Azure
```

## Deployment Pipeline

```mermaid
graph LR
    subgraph "Development"
        Dev[Local Development]
        Git[Git Repository]
    end
    
    subgraph "CI/CD Pipeline"
        Actions[GitHub Actions]
        Build[Build & Test]
        Deploy[Deploy to Azure]
    end
    
    subgraph "Production"
        Frontend[Azure Static Web Apps]
        Backend[Azure Container Apps]
        CDN[Global CDN]
    end
    
    Dev --> Git
    Git --> Actions
    Actions --> Build
    Build --> Deploy
    Deploy --> Frontend
    Deploy --> Backend
    Frontend --> CDN
```

## Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        SSL[SSL/TLS Encryption]
        CORS[CORS Policy]
        CSP[Content Security Policy]
        Validation[Input Validation]
        RateLimit[Rate Limiting]
    end
    
    subgraph "Application Security"
        Auth[Authentication Future]
        Authorization[Authorization Future]
        DataAnonymization[Data Anonymization]
        SecureHeaders[Security Headers]
    end
    
    subgraph "Infrastructure Security"
        AzureSecurity[Azure Security Center]
        NetworkSecurity[Network Security Groups]
        ContainerSecurity[Container Security]
        SecretManagement[Azure Key Vault Future]
    end
    
    SSL --> CORS
    CORS --> CSP
    CSP --> Validation
    Validation --> RateLimit
    
    Auth --> Authorization
    Authorization --> DataAnonymization
    DataAnonymization --> SecureHeaders
    
    AzureSecurity --> NetworkSecurity
    NetworkSecurity --> ContainerSecurity
    ContainerSecurity --> SecretManagement
```