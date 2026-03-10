#!/usr/bin/env python3
"""
Java Codebase Analyzer & Converter with optional LLM
Main entry point
"""

import sys
from pathlib import Path

from java_to_nodejs import (
    JavaCodebaseAnalyzer,
    LLMAnalyzer,
    ConsoleReporter,
    JSONReporter,
    CSVReporter,
    HTMLReporter,
    FolderStructureGenerator,
)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Java Codebase Analyzer & Converter with optional LLM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_java_codebase.py ./my-java-project
  python analyze_java_codebase.py ./my-java-project --convert-ts
  python analyze_java_codebase.py ./my-java-project --llm --provider ollama --convert-ts
  python analyze_java_codebase.py ./my-java-project --llm --convert-ts -j report.json -c report.csv --html report.html
        """
    )
    
    parser.add_argument('directory', help='Java project directory')
    parser.add_argument('--llm', action='store_true', help='Enable LLM enhancement')
    parser.add_argument('--provider', default='openai', choices=['openai', 'ollama'], help='LLM provider')
    parser.add_argument('--model', help='Model name')
    parser.add_argument('--convert-ts', action='store_true', help='Convert to TypeScript')
    parser.add_argument('-o', '--output', default='./typescript-output', help='TypeScript output directory')
    parser.add_argument('-j', '--json', help='Export JSON report')
    parser.add_argument('-c', '--csv', help='Export CSV report')
    parser.add_argument('--html', help='Export HTML report')
    parser.add_argument('-d', '--detailed', action='store_true', help='Detailed output')
    
    args = parser.parse_args()
    
    # Validate
    path = Path(args.directory)
    if not path.exists():
        print(f"✗ Directory not found: {args.directory}")
        sys.exit(1)
    
    java_files = list(path.rglob("*.java"))
    if not java_files:
        print(f"✗ No Java files found")
        sys.exit(1)
    
    # Initialize LLM if requested
    llm = None
    if args.llm:
        print(f"\nInitializing LLM ({args.provider})...")
        llm = LLMAnalyzer(provider=args.provider, model=args.model)
        print()
    
    # Analyze
    print(f"\n{'='*120}")
    print("Java Codebase Analyzer")
    print(f"{'='*120}\n")
    
    print(f"Analyzing: {args.directory}\n")
    analyzer = JavaCodebaseAnalyzer(llm)
    files = analyzer.analyze_directory(str(path))
    
    # Report
    ConsoleReporter.print_report(files, args.detailed)
    
    # Export
    if args.json:
        JSONReporter.export(files, args.json)
    if args.csv:
        CSVReporter.export(files, args.csv)
    if args.html:
        HTMLReporter.export(files, args.html)
    
    # Convert
    if args.convert_ts:
        print(f"\n{'='*120}")
        print("Converting to TypeScript")
        print(f"{'='*120}")
        
        FolderStructureGenerator.create_structure(args.output, files, llm)
    
    print(f"{'='*120}")
    print("✓ Analysis complete!")
    print(f"{'='*120}\n")


if __name__ == '__main__':
    main()
    