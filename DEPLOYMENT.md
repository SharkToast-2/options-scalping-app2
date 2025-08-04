# Deployment Guide

## GitHub Repository Setup

### 1. Initialize Git Repository
```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Options Scalping Application"

# Add remote repository (replace with your GitHub repo URL)
git remote add origin https://github.com/yourusername/options-scalping-app.git

# Push to GitHub
git push -u origin main
```

### 2. GitHub Repository Creation
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name: `options-scalping-app`
4. Description: "Automated options scalping application with real-time market data analysis"
5. Make it Public or Private
6. Don't initialize with README (we already have one)
7. Click "Create repository"

### 3. Repository Structure
```
options-scalping-app/
├── README.md
├── requirements.txt
├── main.py
├── config/
│   ├── settings.py
│   └── env_example.txt
├── data/
│   └── data_fetcher.py
├── signals/
│   ├── technical_indicators.py
│   └── sentiment_analysis.py
├── trading/
│   ├── risk_manager.py
│   └── signal_processor.py
├── ui/
│   └── streamlit_app.py
├── utils/
│   └── logger.py
├── tos_api.py
├── oauth_callback.py
├── setup_tos_auth.py
├── alternative_data_sources.py
├── config.json.example
├── tos_config.py.example
├── .gitignore
└── docs/
    ├── RATE_LIMITING_GUIDE.md
    ├── TOS_SETUP.md
    └── SCHWAB_API_SETUP.md
```

## Environment Setup

### 1. Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/options-scalping-app.git
cd options-scalping-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy configuration files
cp config.json.example config.json
cp tos_config.py.example tos_config.py

# Edit configuration files with your API keys
nano config.json
nano tos_config.py

# Run the application
python main.py
```

### 2. Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build and run with Docker
docker build -t options-scalping-app .
docker run -p 8501:8501 options-scalping-app
```

### 3. Cloud Deployment

#### Heroku
```bash
# Create Procfile
echo "web: streamlit run ui/streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

#### Railway
```bash
# Connect to Railway
railway login
railway init
railway up
```

#### Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Deploy automatically

## Configuration

### 1. API Keys Setup
```bash
# Copy example config
cp config.json.example config.json

# Edit with your API keys
nano config.json
```

### 2. ThinkOrSwim Setup
```bash
# Copy example config
cp tos_config.py.example tos_config.py

# Edit with your credentials
nano tos_config.py

# Run OAuth setup
python setup_tos_auth.py
```

### 3. Environment Variables
```bash
# Create .env file
cat > .env << EOF
ALPACA_API_KEY=your_alpaca_key
ALPACA_SECRET_KEY=your_alpaca_secret
NEWS_API_KEY=your_newsapi_key
ALPHA_VANTAGE_API_KEY=your_alphavantage_key
EOF
```

## Security Considerations

### 1. API Key Protection
- Never commit API keys to Git
- Use environment variables in production
- Rotate keys regularly
- Use least privilege access

### 2. Data Privacy
- Don't store sensitive trading data
- Use encrypted databases
- Implement proper logging
- Follow GDPR/CCPA compliance

### 3. Rate Limiting
- Monitor API usage
- Implement exponential backoff
- Use caching strategies
- Respect API limits

## Monitoring and Logging

### 1. Application Logs
```python
# Configure logging in main.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('options_scalping.log'),
        logging.StreamHandler()
    ]
)
```

### 2. Performance Monitoring
```python
# Add performance metrics
import time
import psutil

def monitor_performance():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    logger.info(f"CPU: {cpu_usage}%, Memory: {memory_usage}%")
```

### 3. Error Tracking
```python
# Add error tracking
import traceback

try:
    # Your code here
    pass
except Exception as e:
    logger.error(f"Error: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")
```

## Backup and Recovery

### 1. Database Backup
```bash
# Backup SQLite databases
cp trades.db trades.db.backup
cp performance.db performance.db.backup
```

### 2. Configuration Backup
```bash
# Backup configuration
cp config.json config.json.backup
cp tos_config.py tos_config.py.backup
```

### 3. Code Backup
```bash
# Create release tags
git tag v1.0.0
git push origin v1.0.0
```

## Troubleshooting

### 1. Common Issues
- **Rate Limiting**: Check RATE_LIMITING_GUIDE.md
- **API Errors**: Verify API keys and permissions
- **Streamlit Issues**: Check port availability
- **Import Errors**: Verify virtual environment

### 2. Debug Mode
```bash
# Run with debug logging
python -u main.py --debug

# Check logs
tail -f options_scalping.log
```

### 3. Health Checks
```bash
# Test API connections
python -c "from data.data_fetcher import DataFetcher; df = DataFetcher(); print(df.get_data_source_info())"

# Test Streamlit app
streamlit run ui/streamlit_app.py --server.port 8501
```

## Support and Documentation

### 1. Documentation
- README.md: Main documentation
- RATE_LIMITING_GUIDE.md: API rate limiting
- TOS_SETUP.md: ThinkOrSwim setup
- SCHWAB_API_SETUP.md: Schwab API setup

### 2. Issues and Support
- GitHub Issues: Report bugs and feature requests
- Discussions: Community support
- Wiki: Additional documentation

### 3. Contributing
- Fork the repository
- Create feature branch
- Submit pull request
- Follow coding standards 