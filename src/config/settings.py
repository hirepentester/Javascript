"""Configuration management for ML JavaScript Analyzer"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file"""
    
    # Framework
    ml_framework: str = "tensorflow"
    model_path: str = "./models/js_analyzer_model.h5"
    model_version: str = "1.0"
    
    # Processing
    processing_mode: str = "batch"  # batch, stream, both
    batch_size: int = 32
    stream_chunk_size: int = 1024
    
    # JavaScript Analysis
    js_file_extensions: str = ".js,.jsx,.ts,.tsx,.mjs"
    max_file_size: int = 5242880  # 5MB
    analyze_security: bool = True
    analyze_complexity: bool = True
    analyze_patterns: bool = True
    analyze_classification: bool = True
    
    # Paths
    input_directory: str = "./data/input"
    output_directory: str = "./data/output"
    results_format: str = "json"  # json, csv, parquet
    
    # Training
    training_data_path: str = "./data/training"
    validation_split: float = 0.2
    test_split: float = 0.1
    epochs: int = 50
    learning_rate: float = 0.001
    
    # Performance
    use_gpu: bool = True
    num_workers: int = 4
    random_seed: int = 42
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/ml_analyzer.log"
    
    # Project Context
    project_name: str = "default"
    project_type: str = "mixed"  # web, mobile, desktop, backend, mixed
    analyze_multiple_projects: bool = True
    
    # Security
    remove_sensitive_data: bool = True
    anonymize_identifiers: bool = False
    store_raw_code: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_file_extensions(self) -> list:
        """Parse file extensions from config"""
        return [ext.strip() for ext in self.js_file_extensions.split(",")]
    
    def create_directories(self):
        """Ensure required directories exist"""
        dirs = [
            self.input_directory,
            self.output_directory,
            self.training_data_path,
            Path(self.log_file).parent,
            Path(self.model_path).parent,
        ]
        for directory in dirs:
            Path(directory).mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    """Load and return application settings"""
    # Load .env file
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Try to load from .env.example
        example_path = Path(".env.example")
        if example_path.exists():
            load_dotenv(example_path)
    
    settings = Settings()
    settings.create_directories()
    return settings


# Global settings instance
settings = get_settings()
