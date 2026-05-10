#!/usr/bin/env python3
"""
Quick Start Example - ML JavaScript Analyzer
"""

from ml_analyzer import MLAnalyzerPipeline
from src.analyzers.js_analyzer import BulkAnalyzer
from src.models.js_classifier import FeatureExtractor, JSCodeClassifier
import json


def example_1_basic_analysis():
    """Example 1: Basic file analysis"""
    print("\n=== Example 1: Basic File Analysis ===\n")
    
    analyzer = BulkAnalyzer()
    
    # Analyze specific files
    results = analyzer.analyze_files([
        "./sample_good.js",
        "./sample_bad.js"
    ])
    
    # Print results
    for result in results:
        if result.get("status") == "success":
            print(f"File: {result['file']}")
            print(f"Quality Score: {result['classification']['quality_score']}")
            print(f"Code Type: {result['classification']['code_type']}")
            print(f"Security Issues: {result['security']['risk_score']}")
            print()


def example_2_batch_analysis():
    """Example 2: Batch analysis of directory"""
    print("\n=== Example 2: Batch Analysis ===\n")
    
    pipeline = MLAnalyzerPipeline()
    
    # Analyze directory
    results = pipeline.batch_analyze("./data/input")
    
    print(f"Files processed: {results['files_processed']}")
    print()


def example_3_with_predictions():
    """Example 3: Analysis with ML predictions"""
    print("\n=== Example 3: ML Predictions ===\n")
    
    pipeline = MLAnalyzerPipeline()
    
    # Analyze
    results = pipeline.batch_analyze("./src")
    
    # Extract features
    features = pipeline.extract_features_from_results(results['results'])
    
    if features:
        # Create and train model (normally would load pre-trained)
        model = JSCodeClassifier()
        model.build_model()
        
        # Make predictions
        predictions, confidences = model.predict(features)
        
        print(f"Made predictions for {len(predictions)} files")
        print(f"Average confidence: {confidences.mean():.2f}")
        print()


def example_4_multi_project():
    """Example 4: Multi-project analysis"""
    print("\n=== Example 4: Multi-Project Analysis ===\n")
    
    pipeline = MLAnalyzerPipeline()
    
    # Register projects
    pipeline.project_processor.register_project(
        "project_a",
        {"type": "react", "version": "1.0"}
    )
    
    pipeline.project_processor.register_project(
        "project_b",
        {"type": "backend", "version": "1.0"}
    )
    
    # Analyze projects
    results_a = pipeline.analyze_project("project_a", "./data/input")
    
    print(f"Project A - Files: {results_a['successful']}")
    print(f"Average Quality: {results_a['summary']['avg_quality_score']:.1f}")
    print()


def example_5_save_results():
    """Example 5: Save results to file"""
    print("\n=== Example 5: Save Results ===\n")
    
    pipeline = MLAnalyzerPipeline()
    
    # Analyze
    results = pipeline.batch_analyze("./src")
    
    # Save results
    output_path = pipeline.save_results(results, "my_analysis")
    print(f"Results saved to: {output_path}")
    print()


if __name__ == "__main__":
    print("ML JavaScript Analyzer - Quick Start Examples")
    print("=" * 50)
    
    # Run examples (comment out any you don't want to run)
    try:
        example_2_batch_analysis()
        example_5_save_results()
    except Exception as e:
        print(f"Error running examples: {e}")
        print("\nNote: Create sample JavaScript files in ./data/input/ first")
    
    print("\n" + "=" * 50)
    print("For more information, see ML_README.md")
