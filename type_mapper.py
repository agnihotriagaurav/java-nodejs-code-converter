#!/usr/bin/env python3
"""
Java to TypeScript Type Mapper
"""


class TypeMapper:
    """Maps Java types to TypeScript types"""
    
    BASIC_TYPES = {
        'int': 'number',
        'long': 'number',
        'float': 'number',
        'double': 'number',
        'boolean': 'boolean',
        'String': 'string',
        'void': 'void',
        'List': 'Array',
        'Set': 'Set',
        'Map': 'Map',
        'Date': 'Date',
    }
    
    @staticmethod
    def map_type(java_type: str) -> str:
        """Map Java type to TypeScript type"""
        if not java_type:
            return 'any'
        
        java_type = java_type.strip()
        
        if java_type in TypeMapper.BASIC_TYPES:
            return TypeMapper.BASIC_TYPES[java_type]
        
        if 'List<' in java_type:
            inner = java_type.split('<')[1].split('>')[0]
            mapped = TypeMapper.map_type(inner)
            return f'Array<{mapped}>'
        
        if java_type.endswith('[]'):
            base = java_type[:-2]
            return f'Array<{TypeMapper.map_type(base)}>'
        
        return java_type