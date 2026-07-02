#!/usr/bin/env python3
"""Debug script to check what characters are in the PDF text."""
import pdfplumber
import json
import os

pdf_path = 'C:/Users/86137/Desktop/中国近代史期末复习资料.pdf'
with pdfplumber.open(pdf_path) as pdf:
    text = pdf.pages[0].extract_text()

lines = text.split('\n')

# Check for explanation markers
for i, line in enumerate(lines):
    if '解析' in line or '题' in line:
        # Print hex codes of relevant characters
        for ch in line:
            if ord(ch) > 127:
                print(f"  Line {i}, char '{ch}' = U+{ord(ch):04X}")
        print(f"  Full line {i}: {repr(line[:150])}")
        print()
