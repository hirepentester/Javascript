"""JavaScript File Analyzer - Extract metrics and features"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Optional
import json


class JavaScriptAnalyzer:
    """Analyze JavaScript files for ML features"""
    
    def __init__(self):
        self.complexity_patterns = {
            "conditional": r"(if|else|switch|case)\s*[\(\{]",
            "loop": r"(for|while|do)\s*[\(\{]",
            "function": r"(function|\w+\s*=>|\w+\s*\()",
            "async": r"(async|await|Promise|\.then\()",
            "error_handling": r"(try|catch|throw|Error)",
            "security_issue": r"(eval|innerHTML|document\.write|setTimeout|setInterval)",
            "api_call": r"(fetch|axios|XMLHttpRequest|import|require)",
            "lazy_loading": r"(import\s*\(|dynamic\s*\(|require\.ensure)",
        }
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a single JavaScript file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {
                "file": file_path,
                "error": str(e),
                "status": "failed"
            }
        
        return {
            "file": file_path,
            "status": "success",
            "metrics": self._extract_metrics(content),
            "complexity": self._analyze_complexity(content),
            "security": self._analyze_security(content),
            "patterns": self._detect_patterns(content),
            "classification": self._classify_code(content),
        }
    
    def _extract_metrics(self, content: str) -> Dict:
        """Extract code metrics"""
        lines = content.split('\n')
        
        metrics = {
            "total_lines": len(lines),
            "non_empty_lines": len([l for l in lines if l.strip()]),
            "comment_lines": len([l for l in lines if l.strip().startswith('//')]),
            "characters": len(content),
            "imports": len(re.findall(r"(import|require)\s*[\(\{]", content)),
            "exports": len(re.findall(r"export\s+(default|const|function|class)", content)),
            "functions": len(re.findall(r"(function\s+\w+|const\s+\w+\s*=\s*\(|\w+\s*\(\s*\)\s*\{)", content)),
            "classes": len(re.findall(r"class\s+\w+", content)),
            "async_functions": len(re.findall(r"async\s+(function|\w+\s*=>|\w+\s*\()", content)),
        }
        
        return metrics
    
    def _analyze_complexity(self, content: str) -> Dict:
        """Analyze code complexity"""
        complexity = {}
        
        for pattern_name, pattern in self.complexity_patterns.items():
            matches = len(re.findall(pattern, content))
            complexity[pattern_name] = matches
        
        # Calculate cyclomatic complexity estimate
        cyclomatic = (
            complexity.get("conditional", 0) +
            complexity.get("loop", 0) +
            complexity.get("error_handling", 0) +
            1
        )
        
        complexity["cyclomatic_estimate"] = cyclomatic
        
        return complexity
    
    def _analyze_security(self, content: str) -> Dict:
        """Analyze security vulnerabilities"""
        security_issues = {}
        
        security_patterns = {
            "eval_usage": r"eval\s*\(",
            "innerHTML": r"\.innerHTML\s*=",
            "document_write": r"document\.write\s*\(",
            "unsafe_timing": r"(setTimeout|setInterval)\s*\(\s*\w+\s*,",
            "missing_validation": r"(\.split|\.replace|\.substring)\s*\(\s*\[0\]",
            "hardcoded_secrets": r"(password|api_key|secret|token)\s*[=:]\s*['\"]",
            "sql_injection": r"(SELECT|INSERT|UPDATE|DELETE)\s*\*\s*FROM",
            "xss_potential": r"(innerHTML|textContent)\s*=\s*[\w.]+",
        }
        
        for issue, pattern in security_patterns.items():
            count = len(re.findall(pattern, content, re.IGNORECASE))
            if count > 0:
                security_issues[issue] = count
        
        security_issues["risk_score"] = min(100, sum(security_issues.values()) * 10)
        security_issues["is_vulnerable"] = security_issues["risk_score"] > 30
        
        return security_issues
    
    def _detect_patterns(self, content: str) -> Dict:
        """Detect code patterns"""
        patterns = {
            "uses_react": len(re.findall(r"(from\s+['\"]react|import.*React|<.*>.*<\/.*>)", content)) > 0,
            "uses_async": len(re.findall(r"(async|await|Promise|\.then)", content)) > 0,
            "uses_arrow_functions": len(re.findall(r"=>\s*\{?", content)) > 0,
            "uses_classes": len(re.findall(r"class\s+\w+", content)) > 0,
            "uses_destructuring": len(re.findall(r"\{\s*\w+\s*[,}\]]*\s*\}", content)) > 0,
            "uses_spread_operator": len(re.findall(r"\.\.\.", content)) > 0,
            "uses_template_literals": len(re.findall(r"`[^`]*\${[^}]*}`", content)) > 0,
            "has_tests": len(re.findall(r"(describe|it|test)\s*\(", content)) > 0,
            "has_jsdoc": len(re.findall(r"/\*\*[\s\S]*?\*/", content)) > 0,
        }
        
        return patterns
    
    def _classify_code(self, content: str) -> Dict:
        """Classify code quality"""
        metrics = self._extract_metrics(content)
        complexity = self._analyze_complexity(content)
        security = self._analyze_security(content)
        patterns = self._detect_patterns(content)
        
        # Code quality score (0-100)
        quality_score = 100
        
        # Reduce score for complexity
        if complexity["cyclomatic_estimate"] > 10:
            quality_score -= 20
        elif complexity["cyclomatic_estimate"] > 5:
            quality_score -= 10
        
        # Reduce score for security issues
        quality_score -= security["risk_score"] / 5
        
        # Reduce score for poor patterns
        if not patterns["has_jsdoc"] and metrics["functions"] > 5:
            quality_score -= 10
        
        if not patterns["uses_async"] and "api_call" in complexity:
            quality_score -= 5
        
        # Boost score for good practices
        if patterns["has_tests"]:
            quality_score += 15
        if patterns["has_jsdoc"]:
            quality_score += 10
        if not security["is_vulnerable"]:
            quality_score += 10
        
        quality_score = max(0, min(100, quality_score))
        
        classification = {
            "quality_score": quality_score,
            "code_type": self._determine_code_type(content),
            "maintenance_level": self._determine_maintenance(quality_score),
            "refactor_needed": quality_score < 50,
            "security_issues_count": len([v for v in security.values() if isinstance(v, int) and v > 0]),
        }
        
        return classification
    
    def _determine_code_type(self, content: str) -> str:
        """Determine the type of code"""
        if re.search(r"(describe|it|test)\s*\(", content):
            return "test"
        if re.search(r"(from\s+['\"]react|import.*React)", content):
            return "react"
        if re.search(r"(vue|Vue|\.vue)", content):
            return "vue"
        if re.search(r"(angular|Angular)", content):
            return "angular"
        if re.search(r"(express|fastify|http\.createServer)", content):
            return "backend"
        return "generic"
    
    def _determine_maintenance(self, quality_score: float) -> str:
        """Determine maintenance level"""
        if quality_score >= 80:
            return "excellent"
        elif quality_score >= 60:
            return "good"
        elif quality_score >= 40:
            return "fair"
        else:
            return "poor"


class BulkAnalyzer:
    """Analyze multiple JavaScript files"""
    
    def __init__(self, extensions: List[str] = None):
        self.analyzer = JavaScriptAnalyzer()
        self.extensions = extensions or [".js", ".jsx", ".ts", ".tsx", ".mjs"]
    
    def analyze_directory(self, directory: str, recursive: bool = True) -> List[Dict]:
        """Analyze all JS files in a directory"""
        path = Path(directory)
        results = []
        
        if recursive:
            pattern = f"**/*{''.join(['[' + e[1:] + ']' if len(e) > 1 else e for e in self.extensions])}"
            files = list(path.glob(pattern))
        else:
            files = []
            for ext in self.extensions:
                files.extend(path.glob(f"*{ext}"))
        
        for file_path in files:
            if file_path.is_file():
                result = self.analyzer.analyze_file(str(file_path))
                results.append(result)
        
        return results
    
    def analyze_files(self, file_paths: List[str]) -> List[Dict]:
        """Analyze specific files"""
        results = []
        for file_path in file_paths:
            result = self.analyzer.analyze_file(file_path)
            results.append(result)
        return results
    
    def generate_report(self, results: List[Dict]) -> Dict:
        """Generate summary report"""
        successful = [r for r in results if r.get("status") == "success"]
        failed = [r for r in results if r.get("status") == "failed"]
        
        report = {
            "total_files": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "summary": {
                "avg_quality_score": sum(r["classification"]["quality_score"] for r in successful) / len(successful) if successful else 0,
                "files_needing_refactor": len([r for r in successful if r["classification"]["refactor_needed"]]),
                "vulnerable_files": len([r for r in successful if r["security"]["is_vulnerable"]]),
            }
        }
        
        return report
