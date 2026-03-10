"""
Java to TypeScript Converter Package
"""

from .models import JavaFileCategory, JavaFileInfo
from .analyzer import JavaCodebaseAnalyzer
from .converter import JavaToTypeScriptConverter
from .type_mapper import TypeMapper
from .llm_analyzer import LLMAnalyzer
from .reporters import ConsoleReporter, JSONReporter, CSVReporter, HTMLReporter
from .folder_structure import FolderStructureGenerator

__all__ = [
    'JavaFileCategory',
    'JavaFileInfo',
    'JavaCodebaseAnalyzer',
    'JavaToTypeScriptConverter',
    'TypeMapper',
    'LLMAnalyzer',
    'ConsoleReporter',
    'JSONReporter',
    'CSVReporter',
    'HTMLReporter',
    'FolderStructureGenerator',
]