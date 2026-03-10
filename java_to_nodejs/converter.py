#!/usr/bin/env python3
"""
Java to TypeScript Code Converter
"""

import re
from .models import JavaFileInfo
from .type_mapper import TypeMapper


class JavaToTypeScriptConverter:
    """Converts Java classes to TypeScript"""
    
    def __init__(self, llm_analyzer=None):
        """Initialize converter with optional LLM"""
        self.type_mapper = TypeMapper()
        self.llm = llm_analyzer
    
    def convert_class(self, java_file: JavaFileInfo, java_code: str) -> str:
        """Convert Java class to TypeScript"""
        
        # If LLM is available, use it to generate code
        if self.llm and self.llm.enabled:
            return self._convert_with_llm(java_file, java_code)
        else:
            return self._convert_pattern_based(java_file, java_code)
    
    def _convert_with_llm(self, java_file: JavaFileInfo, java_code: str) -> str:
        """Convert using LLM"""
        try:
            # Prepare the prompt for full code generation
            prompt = f"""Convert this Java class to TypeScript. Generate complete, production-ready code with:
1. Proper class declaration with export
2. All properties with TypeScript types
3. Constructor with initialization
4. All public methods with proper implementations (not just TODOs)
5. Proper error handling

Java Code:
{java_code[:2000]}

Generate ONLY TypeScript code, no explanations."""
            
            # Get LLM response
            result = self.llm.chain.run(code=java_code[:2000])
            
            if result and result.strip():
                # Clean up the response
                ts_code = result.strip()
                
                # Ensure it's valid TypeScript
                if 'export class' not in ts_code:
                    ts_code = f"export class {java_file.class_name} {{\n{ts_code}\n}}"
                
                return ts_code
        except Exception as e:
            print(f"    ⚠ LLM generation failed: {str(e)}, falling back to pattern-based")
        
        # Fallback to pattern-based if LLM fails
        return self._convert_pattern_based(java_file, java_code)
    
    def _convert_pattern_based(self, java_file: JavaFileInfo, java_code: str) -> str:
        """Pattern-based conversion (fallback)"""
        
        # Extract methods
        method_pattern = r'(?:public|private)\s+(\w+)\s+(\w+)\s*\(([^)]*)\)'
        methods = []
        
        for match in re.finditer(method_pattern, java_code):
            return_type = match.group(1)
            method_name = match.group(2)
            params_str = match.group(3)
            ts_return = self.type_mapper.map_type(return_type)
            
            if method_name not in ['equals', 'hashCode', 'toString']:
                # Parse parameters
                params = self._parse_parameters(params_str)
                param_str = ', '.join([f"{name}: {type_}" for name, type_ in params])
                
                methods.append(f"  {method_name}({param_str}): {ts_return} {{}}")
        
        # Extract fields
        field_pattern = r'(?:private|public|protected)?\s+(?:final)?\s+(\w+)\s+(\w+)\s*(?:=\s*([^;]+))?\s*;'
        fields = []
        
        for match in re.finditer(field_pattern, java_code):
            if self._is_class_level_field(java_code, match.start()):
                java_type = match.group(1)
                field_name = match.group(2)
                ts_type = self.type_mapper.map_type(java_type)
                fields.append(f"  {field_name}: {ts_type};")
        
        # Build TypeScript class
        decorator = ""
        if 'Controller' in java_file.annotations or 'RestController' in java_file.annotations:
            decorator = "@Injectable()\n"
        
        ts_code = f"""/**
 * {java_file.class_name}
 * {java_file.description}
 */

{decorator}export class {java_file.class_name} {{
"""
        
        if fields:
            ts_code += "\n  // Properties\n"
            ts_code += "\n".join(fields)
            ts_code += "\n"
        
        ts_code += f"""
  constructor() {{
    // Initialize properties
  }}

"""
        
        for method in methods[:20]:
            ts_code += f"{method}\n"
        
        ts_code += "}\n"
        
        return ts_code
    
    def _parse_parameters(self, params_str: str) -> list:
        """Parse method parameters"""
        if not params_str.strip():
            return []
        
        params = []
        # Split by comma, careful with generics
        param_parts = re.split(r',(?![^<>]*>)', params_str)
        
        for param in param_parts:
            param = param.strip()
            parts = param.split()
            if len(parts) >= 2:
                java_type = parts[0]
                param_name = parts[-1]
                ts_type = self.type_mapper.map_type(java_type)
                params.append((param_name, ts_type))
        
        return params
    
    def _is_class_level_field(self, code: str, position: int) -> bool:
        """Check if position is a class-level field (not inside a method)"""
        before = code[:position]
        # Count braces to see if we're inside a method
        brace_count = before.count('{') - before.count('}')
        return brace_count <= 1  # Class level or in class definition