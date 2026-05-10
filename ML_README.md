# JavaScript ML Analyzer

A machine learning-based system for analyzing JavaScript code in bulk, extracting metrics, detecting security vulnerabilities, identifying patterns, and classifying code quality.

## Overview

This project provides:

- **Bulk Analysis**: Analyze multiple JavaScript files efficiently
- **Security Scanning**: Detect vulnerabilities and code smells
- **Complexity Metrics**: Calculate cyclomatic complexity and other metrics
- **Pattern Detection**: Identify code patterns and frameworks used
- **ML Classification**: Use TensorFlow to classify code quality
- **Flexible Processing**: Support for batch, stream, and hybrid processing modes
- **Multi-Project Support**: Handle different projects with separate configurations

## Architecture

```
ml_analyzer.py (Main Entry Point)
│
├── src/config/
│   └── settings.py (Environment & config management)
│
├── src/analyzers/
│   └── js_analyzer.py (JavaScript analysis engine)
│
├── src/processors/
│   └── batch_processor.py (Batch/Stream/Multi-project processing)
│
├── src/models/
│   └── js_classifier.py (TensorFlow ML models)
│
└── src/utils/
    └── (Utility modules)
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repo>
   cd Javascript
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Configuration

### Environment Variables (.env)

Key configuration options:

```env
# ML Framework
ML_FRAMEWORK=tensorflow
MODEL_PATH=./models/js_analyzer_model.h5

# Processing Mode
PROCESSING_MODE=batch  # Options: batch, stream, both
BATCH_SIZE=32
STREAM_CHUNK_SIZE=1024

# Analysis Settings
ANALYZE_SECURITY=true
ANALYZE_COMPLEXITY=true
ANALYZE_PATTERNS=true
ANALYZE_CLASSIFICATION=true

# Paths
INPUT_DIRECTORY=./data/input
OUTPUT_DIRECTORY=./data/output

# Training
EPOCHS=50
LEARNING_RATE=0.001
VALIDATION_SPLIT=0.2
```

## Usage

### Basic Analysis

Analyze a directory:
```bash
python ml_analyzer.py --directory ./src --mode batch
```

### Advanced Options

```bash
# Analyze with ML predictions
python ml_analyzer.py --directory ./src --predict --save results

# Analyze all files
python ml_analyzer.py --analyze-all

# Stream mode (process one file at a time)
python ml_analyzer.py --directory ./src --mode stream

# Verbose output
python ml_analyzer.py --directory ./src --verbose
```

### Python API

```python
from ml_analyzer import MLAnalyzerPipeline

# Initialize
pipeline = MLAnalyzerPipeline()

# Analyze project
results = pipeline.analyze_project("my_project", "./src")

# Make ML predictions
predictions = pipeline.predict_code_quality(results["detailed_results"])

# Save results
pipeline.save_results(results, "my_analysis")
```

## Analysis Features

### Metrics Extracted

- **Lines of Code**: Total, non-empty, comments
- **Code Structure**: Functions, classes, exports, imports
- **Async Operations**: Async functions, promises, callbacks
- **Complexity**: Conditionals, loops, error handling

### Security Analysis

Detects:
- `eval()` usage
- Unsafe DOM manipulation (`innerHTML`)
- Hardcoded secrets
- XSS vulnerabilities
- SQL injection patterns
- Timing attacks

### Pattern Detection

Identifies:
- React/Vue/Angular usage
- Async/await patterns
- Arrow functions
- Destructuring
- Template literals
- Test files (Jest, Mocha)
- JSDoc documentation

### Code Quality Classification

Scores code on:
- Complexity
- Security issues
- Documentation
- Test coverage
- Best practices

Quality levels: `excellent`, `good`, `fair`, `poor`

## Processing Modes

### Batch Processing
- Process multiple files together
- Efficient for large codebases
- Default: 32 files per batch
- Configuration: `BATCH_SIZE`

### Stream Processing
- Process files one at a time
- Memory-efficient
- Better for limited resources
- Configuration: `STREAM_CHUNK_SIZE`

### Hybrid Mode
- Combine batch and stream processing
- Flexible for different scenarios
- Configuration: `PROCESSING_MODE=both`

## ML Models

### JSCodeClassifier

TensorFlow neural network for code quality classification:
- Input: 50 features from JavaScript analysis
- Hidden layers: 128 → 64 → 32 → 16
- Output: 5 classes (quality levels)
- Optimizer: Adam with learning rate decay
- Regularization: Dropout, BatchNormalization

### ModelEnsemble

Robust predictions using multiple models:
- Trains 3+ independent models
- Uses majority voting for predictions
- Combines confidence scores
- Better generalization

## Output Formats

### JSON Output (Default)
```json
{
  "total_files": 45,
  "successful": 44,
  "failed": 1,
  "summary": {
    "avg_quality_score": 72.5,
    "files_needing_refactor": 12,
    "vulnerable_files": 3
  },
  "detailed_results": [...]
}
```

### CSV/Parquet
Export results for data analysis in Excel or Python.

## Multi-Project Support

Analyze multiple projects with different configurations:

```python
pipeline.project_processor.register_project(
    "frontend",
    {"type": "react", "analyze_tests": True}
)

pipeline.project_processor.register_project(
    "backend",
    {"type": "backend", "analyze_tests": True}
)

# Process each project
pipeline.analyze_project("frontend", "./apps/frontend")
pipeline.analyze_project("backend", "./apps/backend")
```

## Development

### Running Tests
```bash
pytest test_main.py -v
```

### Creating New Analyzers

1. Add analyzer module to `src/analyzers/`
2. Inherit from base analyzer patterns
3. Implement `analyze_file()` method
4. Register in config

### Adding ML Models

1. Create model in `src/models/`
2. Inherit from `JSCodeClassifier`
3. Override `build_model()` for custom architecture
4. Register in pipeline

## Performance Tips

1. **Use Batch Mode**: Faster than stream for large codebases
2. **Enable GPU**: Set `USE_GPU=true` for TensorFlow
3. **Adjust Batch Size**: Increase for more RAM, decrease for constraints
4. **Parallel Processing**: Set `NUM_WORKERS` to CPU count
5. **Disable Unused Analysis**: Turn off unneeded analysis types

## Branching Strategy

This project uses a three-tier branching strategy:

- **working**: Development branch (CI pipeline: Lint → Test → Build)
- **staging**: QA branch (full CI pipeline)
- **deploy**: Production branch (automatic deployment)

See [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md) for details.

## CI/CD Pipeline

GitHub Actions workflows:
- **ci.yml**: Lint, test, build on working/staging
- **deploy.yml**: Automatic deploy from deploy branch
- **branch-promotion.yml**: Track merges between branches

## Troubleshooting

### Memory Issues
- Reduce `BATCH_SIZE`
- Enable `STREAM_CHUNK_SIZE`
- Set `USE_GPU=false` to free RAM

### Slow Analysis
- Increase `BATCH_SIZE`
- Set `NUM_WORKERS` to CPU count
- Disable unused analysis types

### TensorFlow Errors
- Ensure CUDA is installed (if using GPU)
- Check TensorFlow version compatibility
- Try: `pip install --upgrade tensorflow`

## Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -am "Add feature"`
3. Push to working: `git push origin feature/my-feature`
4. Create PR to working branch
5. After approval, merge and promote through staging → deploy

## License

See [LICENSE](LICENSE) file

## Support

For issues, questions, or suggestions, please open an issue in the repository.
