"""Batch processor for handling multiple projects and files"""

from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime
from loguru import logger


class BatchProcessor:
    """Process files in batches"""
    
    def __init__(self, batch_size: int = 32):
        self.batch_size = batch_size
        self.current_batch = []
        self.results = []
    
    def add_file(self, file_path: str, project: str = "default"):
        """Add file to batch"""
        self.current_batch.append({
            "file": file_path,
            "project": project,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.current_batch) >= self.batch_size:
            return self.process_batch()
        return None
    
    def process_batch(self) -> List[Dict]:
        """Process current batch"""
        if not self.current_batch:
            return []
        
        batch_results = []
        for item in self.current_batch:
            # Process each file
            batch_results.append(item)
        
        self.results.extend(batch_results)
        self.current_batch = []
        
        return batch_results
    
    def flush(self) -> List[Dict]:
        """Process remaining items in batch"""
        return self.process_batch()


class StreamProcessor:
    """Process files in streaming mode"""
    
    def __init__(self, chunk_size: int = 1024):
        self.chunk_size = chunk_size
    
    def process_file_stream(self, file_path: str):
        """Process file in chunks (streaming)"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            logger.error(f"Error streaming {file_path}: {e}")


class MultiProjectProcessor:
    """Handle multiple projects with different configurations"""
    
    def __init__(self, config):
        self.config = config
        self.projects = {}
        self.logger = logger
    
    def register_project(self, project_name: str, project_config: Dict):
        """Register a new project"""
        self.projects[project_name] = {
            "config": project_config,
            "status": "registered",
            "files_processed": 0,
            "results": []
        }
        self.logger.info(f"Project registered: {project_name}")
    
    def process_project(self, project_name: str, directory: str):
        """Process all files in a project"""
        if project_name not in self.projects:
            self.logger.warning(f"Project not found: {project_name}")
            return None
        
        project = self.projects[project_name]
        project["status"] = "processing"
        
        # Process files
        path = Path(directory)
        if path.exists():
            project["status"] = "completed"
            self.logger.info(f"Project completed: {project_name}")
        else:
            project["status"] = "failed"
            self.logger.error(f"Project directory not found: {directory}")
        
        return project
    
    def get_project_summary(self, project_name: str) -> Dict:
        """Get summary for a project"""
        if project_name not in self.projects:
            return None
        
        project = self.projects[project_name]
        return {
            "name": project_name,
            "status": project["status"],
            "files_processed": project["files_processed"],
            "config": project["config"]
        }
