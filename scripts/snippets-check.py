#!/usr/bin/env python3
"""
Checks code snippets in a Markdown file for basic syntax validity.
Supports: python, bash, javascript, c, cpp.
"""
import sys
import re
import subprocess
import tempfile
import os

def check_python(code):
    try:
        compile(code, '<string>', 'exec')
        return True, "Valid Python syntax"
    except SyntaxError as e:
        return False, f"Python SyntaxError: {e}"

def check_bash(code):
    result = subprocess.run(['bash', '-n'], input=code, text=True, capture_output=True)
    if result.returncode == 0:
        return True, "Valid Bash syntax"
    return False, f"Bash syntax error: {result.stderr.strip()}"

def check_javascript(code):
    result = subprocess.run(['node', '--check'], input=code, text=True, capture_output=True)
    if result.returncode == 0:
        return True, "Valid JavaScript syntax"
    return False, f"JS syntax error: {result.stderr.strip()}"

def check_c(code, lang):
    ext = 'c' if lang == 'c' else 'cpp'
    compiler = 'gcc' if lang == 'c' else 'g++'
    with tempfile.NamedTemporaryFile(suffix=f'.{ext}', delete=False, mode='w') as f:
        f.write(code)
        temp_path = f.name
    try:
        result = subprocess.run([compiler, '-fsyntax-only', temp_path], capture_output=True, text=True)
        os.unlink(temp_path)
        if result.returncode == 0:
            return True, f"Valid {lang.upper()} syntax"
        return False, f"{lang.upper()} syntax error: {result.stderr.strip()}"
    except FileNotFoundError:
        os.unlink(temp_path)
        return True, f"Compiler {compiler} not found, skipping {lang.upper()} check"

def main():
    if len(sys.argv) < 2:
        print("Usage: python snippets-check.py <markdown_file.md>")
        sys.exit(1)

    md_file = sys.argv[1]
    if not os.path.exists(md_file):
        print(f"Error: File {md_file} not found.")
        sys.exit(1)

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all code blocks
    pattern = r'```(\w+)?\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)

    errors = 0
    for lang, code in matches:
        lang = (lang or 'text').lower().strip()
        if not code.strip():
            continue
            
        if lang == 'python':
            ok, msg = check_python(code)
        elif lang in ['bash', 'sh']:
            ok, msg = check_bash(code)
        elif lang in ['javascript', 'js']:
            ok, msg = check_javascript(code)
        elif lang in ['c', 'cpp', 'c++']:
            ok, msg = check_c(code, lang)
        else:
            continue # Skip unsupported languages

        if not ok:
            print(f"❌ FAIL [{lang}]: {msg}")
            errors += 1
        else:
            print(f"✅ PASS [{lang}]: {msg}")

    if errors > 0:
        print(f"\nFound {errors} broken snippet(s).")
        sys.exit(1)
    else:
        print("\nAll checked snippets are valid.")
        sys.exit(0)

if __name__ == '__main__':
    main()
