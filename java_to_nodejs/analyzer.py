#!/usr/bin/env python3
"""
Java Codebase Analyzer
"""

import re
from pathlib import Path
from typing import List, Optional

from .models import JavaFileInfo
from .llm_analyzer import LLMAnalyzer
from .converter import JavaToTypeScriptConverter


class JavaCodebaseAnalyzer:
    """Analyzes Java codebase"""
    
    def __init__(self, llm_analyzer: Optional[LLMAnalyzer] = None):
        """Initialize analyzer"""
        self.categories = {
            'controller': ['Controller', 'controller'],
            'service': ['Service', 'service'],
            'repository': ['Repository', 'repository'],
            'entity': ['Entity', 'entity'],
            'dto': ['DTO', 'Dto', 'dto'],
            'config': ['Config', 'config'],
            'util': ['Util', 'Helper', 'util'],
            'test': ['Test', 'test'],
        }
        self.llm = llm_analyzer
        self.converter = JavaToTypeScriptConverter(llm_analyzer)
    
    def extract_class_name(self, content: str) -> str:
        """Extract class name from Java code"""
        match = re.search(r'(?:public\s+)?class\s+(\w+)', content)
        return match.group(1) if match else "Unknown"
    
    def extract_package(self, content: str) -> str:
        """Extract package from Java code"""
        match = re.search(r'package\s+([\w.]+)', content)
        return match.group(1) if match else "unknown"
    
    def extract_annotations(self, content: str) -> List[str]:
        """Extract annotations from Java code"""
        return re.findall(r'@(\w+)', content)
    
    def categorize_file(self, filename: str, content: str) -> tuple:
        """Categorize Java file - returns (category, confidence)"""
        filename_lower = filename.lower()
        
        # Check filename patterns
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in filename_lower:
                    return category, 0.95
        
        # Check content patterns
        if '@Controller' in content or '@RestController' in content:
            return 'controller', 0.9
        if '@Service' in content:
            return 'service', 0.9
        if '@Repository' in content:
            return 'repository', 0.9
        if '@Entity' in content:
            return 'entity', 0.9
        
        return 'unknown', 0.5
    
    def analyze_file(self, file_path: Path) -> JavaFileInfo:
        """Analyze single Java file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        class_name = self.extract_class_name(content)
        package = self.extract_package(content)
        category, confidence = self.categorize_file(file_path.name, content)
        annotations = self.extract_annotations(content)
        
        # Get LLM description if available
        description = ""
        if self.llm and self.llm.enabled:
            description = self.llm.analyze(content)
        
        return JavaFileInfo(
            path=str(file_path),
            filename=file_path.name,
            class_name=class_name,
            package=package,
            category=category,
            lines=content.count('\n'),
            size=len(content),
            confidence=confidence,
            description=description,
            annotations=annotations
        )
    
    def analyze_directory(self, directory: str) -> List[JavaFileInfo]:
        """Analyze entire directory"""
        root = Path(directory).resolve()
        files = []
        java_files = list(root.rglob("*.java"))
        total = len(java_files)
        
        print(f"Found {total} Java files\n")
        
        for i, java_file in enumerate(java_files, 1):
            try:
                file_info = self.analyze_file(java_file)
                files.append(file_info)
                
                if i % 10 == 0 or i == total:
                    print(f"  Progress: {i}/{total} files processed...")
            except Exception as e:
                print(f"  Error processing {java_file}: {str(e)}")
        
        return files