#!/usr/bin/env python3
"""
Folder Structure Generator for TypeScript Output
"""

from pathlib import Path
from typing import List, Optional

from .models import JavaFileInfo
from .converter import JavaToTypeScriptConverter
from .llm_analyzer import LLMAnalyzer


class FolderStructureGenerator:
    """Creates organized TypeScript folder structure"""
    
    @staticmethod
    def create_structure(output_dir: str, files: List[JavaFileInfo], llm_analyzer: Optional[LLMAnalyzer] = None):
        """Create organized TypeScript folder structure"""
        base = Path(output_dir)
        base.mkdir(parents=True, exist_ok=True)
        
        print(f"\nCreating TypeScript files in: {output_dir}\n")
        
        # Initialize converter with LLM if available
        converter = JavaToTypeScriptConverter(llm_analyzer)
        
        for i, file in enumerate(files, 1):
            # Create category folder
            category_folder = base / file.category
            category_folder.mkdir(exist_ok=True)
            
            # Create package folder
            if file.package != 'unknown':
                package_folder = category_folder / file.package.replace('.', '/')
            else:
                package_folder = category_folder
            
            package_folder.mkdir(parents=True, exist_ok=True)
            
            # Create TypeScript file
            ts_file = package_folder / f"{file.class_name.lower()}.ts"
            
            # Read original Java file
            try:
                with open(file.path, 'r', encoding='utf-8', errors='ignore') as f:
                    java_code = f.read()
                ts_code = converter.convert_class(file, java_code)
            except Exception as e:
                print(f"    Error converting {file.class_name}: {str(e)}")
                ts_code = f"export class {file.class_name} {{}}\n"
            
            with open(ts_file, 'w') as f:
                f.write(ts_code)
            
            print(f"  [{i}/{len(files)}] ✓ {ts_file}")
        
        print(f"\n✓ Created TypeScript files in: {output_dir}\n")