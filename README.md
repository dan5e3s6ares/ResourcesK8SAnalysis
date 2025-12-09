# Kubernetes Resource Analysis Tool

🚀 AI-Powered Kubernetes Pod Resource Optimization

This application performs queries to Elasticsearch to download analytical data regarding RAM, CPU, Processor, and Hard Drive usage from your Kubernetes clusters. After downloading the data, comprehensive mathematical and AI analysis is performed to provide optimal resource configuration recommendations for your Pods.

## Features

- **FastAPI Backend**: High-performance REST API server
- **User Authentication**: Secure JWT-based authentication system
- **Configuration Management**: Store and manage multiple application configurations per user
- **Elasticsearch Integration**: Query resource metrics from your Elasticsearch clusters
- **Statistical Analysis**: Calculate mean, median, percentiles, and standard deviation
- **AI-Powered Recommendations**: Get intelligent suggestions using OpenAI GPT models
- **Web Interface**: Beautiful, responsive web frontend for easy interaction
- **Grafana Integration**: Store Grafana URLs and bearer tokens for easy dashboard access
- **Multi-User Support**: Each user has their own isolated configurations

## Architecture

```
ResourcesK8SAnalysis/
├── app/
│   ├── database/          # Database connection and configuration
│   ├── models/            # SQLAlchemy models and Pydantic schemas
│   ├── routers/           # FastAPI route handlers
│   ├── services/          # Business logic (Auth, ES, Analysis, AI)
│   ├── templates/         # HTML templates for web interface
│   └── main.py           # FastAPI application entry point
├── requirements.txt       # Python dependencies
├── run.py                # Application startup script
└── .env.example          # Environment variables template
```

## Prerequisites

- Python 3.8 or higher
- Elasticsearch cluster with Kubernetes metrics
- OpenAI API key (optional, for AI recommendations)
- Grafana instance (optional, for visualization)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dan5e3s6ares/ResourcesK8SAnalysis.git
   cd ResourcesK8SAnalysis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables (REQUIRED)**
   ```bash
   cp .env.example .env
   
   # Generate a secure SECRET_KEY
   openssl rand -hex 32
   
   # Edit .env and set your SECRET_KEY (REQUIRED)
   # Optionally add your OPENAI_API_KEY for AI features
   ```

   **Important:** The `SECRET_KEY` environment variable is **required** for security. The application will not start without it.

## Running the Application

### Development Mode

```bash
python run.py
```

The application will start on `http://localhost:8000`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Usage

### 1. Register/Login

Navigate to `http://localhost:8000` and create an account or login.

### 2. Create a Configuration

Go to the **Configurations** page and click "New Configuration". Fill in:

- **Application Name**: Name of your Kubernetes application
- **Namespace**: Kubernetes namespace
- **Elasticsearch URL**: Your Elasticsearch endpoint (e.g., `http://elasticsearch:9200`)
- **Elasticsearch Index**: Index pattern for metrics (e.g., `k8s-metrics-*`)
- **Grafana URL**: Your Grafana dashboard URL
- **Grafana Bearer Token**: API token for Grafana access
- **AI Model**: Choose GPT model for recommendations
- **Analysis Window**: Hours of historical data to analyze (1-168)

### 3. Run Analysis

- Navigate to the **Run Analysis** page
- Select a configuration
- Optionally specify a time range
- Click "Run Analysis"
- View statistical analysis and AI-powered recommendations

### 4. Apply Recommendations

The analysis provides:
- Recommended CPU requests and limits
- Recommended memory requests and limits
- Storage provisioning suggestions
- Optimization strategies
- Warning about concerning patterns

Apply these recommendations to your Kubernetes deployments.

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

#### Configurations
- `POST /configurations/` - Create new configuration
- `GET /configurations/` - List all configurations
- `GET /configurations/{id}` - Get specific configuration
- `PUT /configurations/{id}` - Update configuration
- `DELETE /configurations/{id}` - Delete configuration

#### Analysis
- `POST /analysis/run` - Run resource analysis
- `GET /analysis/test-connection/{id}` - Test Elasticsearch connection

## Elasticsearch Data Format

The application expects Elasticsearch documents with the following fields:

```json
{
  "@timestamp": "2024-01-01T00:00:00Z",
  "app_name": "my-app",
  "namespace": "production",
  "cpu_usage_percent": 45.2,
  "memory_usage_mb": 512,
  "disk_usage_mb": 1024,
  "cpu_cores": 2,
  "memory_total_mb": 2048,
  "disk_total_mb": 10240
}
```

## AI Recommendations

When OpenAI API key is configured, the system provides:
1. Pattern analysis of resource usage
2. Specific CPU/memory/disk recommendations
3. Optimization strategies
4. Warnings about anomalies or concerning patterns
5. Kubernetes YAML configuration examples

Without OpenAI API key, the system falls back to rule-based recommendations using statistical analysis.

## Security Considerations

- Store sensitive tokens (Grafana bearer tokens, etc.) securely
- Use HTTPS in production
- Change the default SECRET_KEY in production
- Keep your OpenAI API key secure
- Implement rate limiting for production deployments
- Regular security audits recommended

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
