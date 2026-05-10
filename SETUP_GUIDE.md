# ML JavaScript Analyzer - Setup & Getting Started

## What Was Created

Your repository now has a complete **Machine Learning pipeline for analyzing JavaScript files in bulk**. Here's what's included:

### ✅ Core Components

1. **ml_analyzer.py** - Main entry point for the ML analyzer
2. **src/config/settings.py** - Configuration management using environment variables
3. **src/analyzers/js_analyzer.py** - JavaScript file analysis engine
4. **src/processors/batch_processor.py** - Batch, stream, and multi-project processing
5. **src/models/js_classifier.py** - TensorFlow ML models for code classification
6. **examples.py** - Quick start examples

### ✅ Features

- **Code Metrics**: Lines of code, functions, imports, async operations, complexity
- **Security Analysis**: Detects eval, innerHTML, hardcoded secrets, XSS, SQL injection
- **Pattern Detection**: React, Vue, Angular, async/await, destructuring, tests, JSDoc
- **Code Quality Classification**: Scores code on 0-100 scale (excellent, good, fair, poor)
- **Processing Modes**: Batch (fast), Stream (memory efficient), Hybrid (flexible)
- **ML Classification**: TensorFlow neural network for quality prediction
- **Multi-Project Support**: Analyze different projects with separate configurations
- **Environment-Based Configuration**: All settings in .env file

### ✅ Directory Structure

```
Javascript/
├── ml_analyzer.py              # Main entry point
├── examples.py                 # Quick start examples
├── .env.example                # Environment config template
├── ML_README.md                # Detailed documentation
├── requirements.txt            # ML dependencies
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration management
│   ├── analyzers/
│   │   ├── __init__.py
│   │   └── js_analyzer.py      # JavaScript analyzer
│   ├── processors/
│   │   ├── __init__.py
│   │   └── batch_processor.py  # Processing modes
│   ├── models/
│   │   ├── __init__.py
│   │   └── js_classifier.py    # ML models
│   └── utils/
│       └── __init__.py
├── data/
│   ├── input/                  # Input JavaScript files
│   ├── output/                 # Analysis results
│   └── training/               # Training data for ML
├── models/                     # Trained ML models
├── logs/                       # Application logs
└── .github/workflows/          # CI/CD pipelines
```

### ✅ Git Branches

Three-tier branching strategy already configured:

1. **working** - Development branch
   - CI pipeline: Lint → Test → Build
   - Push feature branches here first
   
2. **staging** - QA branch
   - Full CI pipeline runs
   - Test before production
   
3. **deploy** - Production branch
   - Automatic deployment pipeline
   - Only tested, stable code

---

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### 2. Configure .env

Edit `.env` with your settings:

```env
# Essential settings
ML_FRAMEWORK=tensorflow
PROCESSING_MODE=batch
BATCH_SIZE=32

# Analysis settings
ANALYZE_SECURITY=true
ANALYZE_COMPLEXITY=true
ANALYZE_PATTERNS=true
ANALYZE_CLASSIFICATION=true

# Paths
INPUT_DIRECTORY=./data/input
OUTPUT_DIRECTORY=./data/output

# For TensorFlow
USE_GPU=false  # Set to true if CUDA is installed
```

### 3. Add Test Data

Place JavaScript files to analyze in `./data/input/`

```bash
# Copy sample files
cp path/to/your/js/files ./data/input/
```

### 4. Run Analysis

```bash
# Basic analysis
python ml_analyzer.py --directory ./data/input --mode batch

# With ML predictions
python ml_analyzer.py --directory ./data/input --predict --save my_results

# Stream mode (for single files)
python ml_analyzer.py --directory ./data/input --mode stream

# Verbose output
python ml_analyzer.py --directory ./data/input --verbose
```

### 5. Check Results

Results are saved to `./data/output/` by default:

```bash
# View last analysis
cat ./data/output/analysis_results_*.json
```

---

## Usage Examples

### Example 1: Analyze a Project

```bash
python ml_analyzer.py --project my_project --directory ./src
```

### Example 2: With ML Predictions

```bash
python ml_analyzer.py \
  --directory ./src \
  --predict \
  --save project_analysis
```

### Example 3: Python API

```python
from ml_analyzer import MLAnalyzerPipeline

# Initialize
pipeline = MLAnalyzerPipeline()

# Analyze
results = pipeline.batch_analyze("./src")

# Make predictions
predictions = pipeline.predict_code_quality(results["results"])

# Save
pipeline.save_results(results, "my_analysis")
```

### Example 4: Run Examples

```bash
python examples.py
```

---

## What the Analyzer Reports

Each file analyzed generates:

### Metrics
- Total lines, comments, functions, classes
- Import/export counts
- Async operations

### Complexity
- Conditional branches (if/else)
- Loops (for/while)
- Cyclomatic complexity estimate

### Security Issues
- Dangerous API usage (eval, innerHTML)
- Hardcoded secrets (password, API keys)
- XSS vulnerabilities
- SQL injection patterns
- Risk score (0-100)

### Patterns Detected
- Framework detection (React, Vue, Angular)
- Modern JavaScript (async/await, arrow functions, destructuring)
- Code quality (JSDoc, tests present)

### Classification
- Overall quality score (0-100)
- Maintenance level (excellent, good, fair, poor)
- Refactoring needed
- Security issues count

---

## CI/CD Pipeline

### Automated Workflows

1. **ci.yml** - Runs on every push to working/staging
   - Linting (flake8, pylint)
   - Tests (pytest)
   - Build verification

2. **deploy.yml** - Runs on push to deploy branch
   - Deployment checks
   - Production deployment (when configured)

3. **branch-promotion.yml** - Tracks merges between branches
   - Notifies on successful promotions

### View Pipeline Status

```bash
# In GitHub: Settings → Branches
# Enable branch protection on staging and deploy
# Require status checks to pass before merging
```

---

## Next Steps

### 1. Prepare Data
- Add JavaScript files to `./data/input/`
- Run initial analysis: `python ml_analyzer.py --analyze-all`

### 2. Configure ML Model
- Edit `EPOCHS` and `LEARNING_RATE` in `.env`
- Prepare training data in `./data/training/`
- Train model: See ML_README.md for training details

### 3. Deploy Project
- Run tests: `pytest`
- Push to staging: `git checkout staging && git pull origin working`
- Push to production: `git checkout deploy && git pull origin staging`

### 4. Monitor Results
- Check logs in `./logs/`
- View analysis in `./data/output/`
- Monitor CI/CD in GitHub Actions

---

## Development Workflow

```bash
# Create feature branch
git checkout working
git checkout -b feature/my-feature

# Make changes and test
python ml_analyzer.py --analyze-all
pytest test_main.py

# Commit and push
git add .
git commit -m "Add my feature"
git push origin feature/my-feature

# Create PR to working on GitHub
# After approval: git checkout working && git merge origin/feature/my-feature

# Promote through stages
# working → (PR) → staging → (PR) → deploy → automatic deployment
```

---

## Troubleshooting

### ModuleNotFoundError

```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Verify virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### TensorFlow/GPU Issues

```bash
# If not using GPU, disable in .env
USE_GPU=false

# To use GPU, install CUDA:
# See: https://www.tensorflow.org/install/source_windows (for Windows)
```

### Out of Memory

```env
# In .env, reduce batch size
BATCH_SIZE=8  # Default is 32
```

### Analysis Takes Too Long

```bash
# Use streaming mode
python ml_analyzer.py --directory ./src --mode stream

# Or reduce analysis scope in .env:
ANALYZE_SECURITY=false
ANALYZE_PATTERNS=false
```

---

## Documentation

- **ML_README.md** - Complete ML analyzer documentation
- **BRANCHING_STRATEGY.md** - Git branching and CI/CD pipeline guide
- **requirements.txt** - All dependencies listed
- **examples.py** - Working code examples

---

## Key Technologies

- **TensorFlow** - Machine learning framework
- **NumPy/Pandas** - Data processing
- **Scikit-learn** - Additional ML algorithms
- **Python-dotenv** - Environment configuration
- **Loguru** - Advanced logging
- **pytest** - Testing framework
- **GitHub Actions** - CI/CD automation

---

## Support

For issues or questions:

1. Check **ML_README.md** for detailed documentation
2. Review **examples.py** for working code samples
3. Check **logs/** folder for error messages
4. See GitHub Issues for known problems

---

## Success Checklist

- ✅ Environment setup complete (virtual env + dependencies)
- ✅ .env file created and configured
- ✅ Test data in `./data/input/` (optional)
- ✅ First analysis ran successfully: `python ml_analyzer.py --analyze-all`
- ✅ Results visible in `./data/output/`
- ✅ CI/CD pipelines configured in GitHub
- ✅ Ready for development: feature branches working
- ✅ Ready to deploy: all branches synced

**You're ready to start analyzing JavaScript files with ML!** 🚀
