#!/usr/bin/env python3
"""
Data Models for Java Analysis
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class JavaFileCategory(Enum):
    """Java file categories"""
    CONTROLLER = "controller"
    SERVICE = "service"
    REPOSITORY = "repository"
    ENTITY = "entity"
    DTO = "dto"
    UTIL = "utility"
    CONFIG = "config"
    TEST = "test"
    UNKNOWN = "unknown"


@dataclass
class JavaFileInfo:
    """Information about a Java file"""
    path: str
    filename: str
    class_name: str
    package: str
    category: str
    lines: int
    size: int
    confidence: float
    description: str = ""
    annotations: List[str] = None
    
    def __post_init__(self):
        if self.annotations is None:
            self.annotations = []