"""
Main entry point for JavaScript ML Analyzer
Run with: python ml_analyzer.py
"""

import sys
from pathlib import Path
from typing import List, Dict
import json
from datetime import datetime
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config.settings import get_settings
from analyzers.js_analyzer import JavaScriptAnalyzer, BulkAnalyzer
from processors.batch_processor import BatchProcessor, StreamProcessor, MultiProjectProcessor
from models.js_classifier import JSCodeClassifier, FeatureExtractor, ModelEnsemble


class MLAnalyzerPipeline:
    """Main pipeline for analyzing JavaScript projects"""
    
    def __init__(self):
        self.config = get_settings()
        self.setup_logging()
        self.analyzer = BulkAnalyzer(self.config.get_file_extensions())
        self.batch_processor = BatchProcessor(self.config.batch_size)
        self.stream_processor = StreamProcessor(self.config.stream_chunk_size)
        self.project_processor = MultiProjectProcessor(self.config)
        self.model = None
        self.ensemble = None
    
    def setup_logging(self):
        """Setup logging"""
        logger.remove()
        logger.add(
            sys.stderr,
            level=self.config.log_level,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
        )
        logger.add(
            self.config.log_file,
            level=self.config.log_level,
            format="{time} | {level: <8} | {name}:{function} - {message}"
        )
        logger.info(f"ML Analyzer Pipeline initialized (Mode: {self.config.processing_mode})")
    
    def analyze_project(self, project_name: str, directory: str) -> Dict:
        """Analyze a project directory"""
        logger.info(f"Starting analysis of project: {project_name}")
        
        self.project_processor.register_project(
            project_name,
            {
                "type": self.config.project_type,
                "processing_mode": self.config.processing_mode
            }
        )
        
        # Perform analysis
        results = self.analyzer.analyze_directory(directory, recursive=True)
        
        # Generate report
        report = self.analyzer.generate_report(results)
        report["project"] = project_name
        report["timestamp"] = datetime.now().isoformat()
        report["detailed_results"] = results
        
        logger.info(f"Analysis complete. Processed {report['successful']} files, {report['failed']} failed")
        
        return report
    
    def batch_analyze(self, directory: str) -> Dict:
        """Analyze using batch processing"""
        logger.info(f"Starting batch analysis of: {directory}")
        
        all_results = []
        batch_num = 0
        
        path = Path(directory)
        files = []
        for ext in self.config.get_file_extensions():
            files.extend(path.rglob(f"*{ext}"))
        
        for file_path in files:
            result = self.analyzer.analyzer.analyze_file(str(file_path))
            self.batch_processor.add_file(str(file_path), self.config.project_name)
            all_results.append(result)
        
        # Flush remaining batch
        self.batch_processor.flush()
        
        logger.info(f"Batch analysis complete: {len(all_results)} files processed")
        
        return {
            "mode": "batch",
            "files_processed": len(all_results),
            "results": all_results,
            "timestamp": datetime.now().isoformat()
        }
    
    def stream_analyze(self, file_path: str) -> Dict:
        """Analyze using streaming mode"""
        logger.info(f"Starting stream analysis of: {file_path}")
        
        chunks_processed = 0
        for chunk in self.stream_processor.process_file_stream(file_path):
            chunks_processed += 1
        
        result = self.analyzer.analyzer.analyze_file(file_path)
        result["mode"] = "stream"
        result["chunks_processed"] = chunks_processed
        
        logger.info(f"Stream analysis complete: {chunks_processed} chunks processed")
        
        return result
    
    def extract_features_from_results(self, results: List[Dict]) -> List[List[float]]:
        """Extract ML features from analysis results"""
        features = []
        for result in results:
            if result.get("status") == "success":
                feature_vector = FeatureExtractor.extract_features(result)
                features.append(feature_vector)
        
        return features
    
    def save_results(self, results: Dict, filename: str = None):
        """Save analysis results to file"""
        if filename is None:
            filename = f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        output_path = Path(self.config.output_directory) / f"{filename}.{self.config.results_format}"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            if self.config.results_format == "json":
                json.dump(results, f, indent=2, default=str)
            else:
                # For other formats, default to JSON
                json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Results saved to: {output_path}")
        return str(output_path)
    
    def predict_code_quality(self, results: List[Dict]):
        """Use ML model to predict code quality"""
        logger.info("Making ML predictions on analysis results")
        
        # Extract features
        features = self.extract_features_from_results(results)
        
        if not features:
            logger.warning("No features to predict on")
            return None
        
        # Initialize and use model
        if self.model is None:
            self.model = JSCodeClassifier()
            self.model.build_model()
        
        # Make predictions
        predictions, confidences = self.model.predict(features)
        
        predictions_list = []
        for i, result in enumerate(results):
            if result.get("status") == "success" and i < len(predictions):
                predictions_list.append({
                    "file": result["file"],
                    "predicted_class": int(predictions[i]),
                    "confidence": float(confidences[i])
                })
        
        return predictions_list


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ML-based JavaScript Code Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ml_analyzer.py --project my_project --directory ./src --mode batch
  python ml_analyzer.py --directory ./data/input --mode stream
  python ml_analyzer.py --analyze-all
        """
    )
    
    parser.add_argument("--project", type=str, help="Project name")
    parser.add_argument("--directory", type=str, default="./", help="Directory to analyze")
    parser.add_argument("--mode", type=str, choices=["batch", "stream", "both"], help="Processing mode")
    parser.add_argument("--analyze-all", action="store_true", help="Analyze all files")
    parser.add_argument("--predict", action="store_true", help="Use ML model for predictions")
    parser.add_argument("--save", type=str, help="Save results to file")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = MLAnalyzerPipeline()
    
    # Perform analysis
    if args.analyze_all or args.directory:
        results = pipeline.batch_analyze(args.directory)
        
        # Make predictions if requested
        if args.predict and "results" in results:
            predictions = pipeline.predict_code_quality(results["results"])
            results["predictions"] = predictions
        
        # Save results
        if args.save:
            pipeline.save_results(results, args.save)
        else:
            print(json.dumps(results, indent=2, default=str))
    
    logger.info("Analysis complete!")


if __name__ == "__main__":
    main()
