#!/usr/bin/env python3
"""
Fix odd-length hex strings in genesis.json alloc.code fields
"""
import json
import sys
import os
import re

def fix_hex_string(hex_str):
    """Fix odd-length hex string by padding with leading zero"""
    if not hex_str.startswith('0x'):
        return hex_str
    
    hex_part = hex_str[2:]
    if len(hex_part) % 2 != 0:
        # Pad with leading zero to make it even length
        fixed = '0x0' + hex_part
        print(f"Fixed odd-length hex: {len(hex_part)} -> {len(hex_part) + 1} chars")
        return fixed
    return hex_str

def check_and_report(input_file):
    """Check for odd-length hex strings and report"""
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    alloc = data.get('alloc', {})
    errors = []
    
    for addr, account in alloc.items():
        if 'code' in account and isinstance(account['code'], str):
            code = account['code']
            if code.startswith('0x'):
                hex_part = code[2:]
                if len(hex_part) % 2 != 0:
                    errors.append({
                        'addr': addr,
                        'length': len(hex_part),
                        'last_50': code[-50:]
                    })
    
    if errors:
        print(f"Found {len(errors)} odd-length hex strings:")
        for err in errors:
            print(f"  Address: {err['addr']}")
            print(f"  Hex length: {err['length']} (odd)")
            print(f"  Last 50 chars: {err['last_50']}")
            print()
        return True
    return False

def fix_genesis_file(input_file, output_file):
    """Fix odd-length hex strings in genesis.json"""
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Parse JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return False
    
    # Fix alloc.code fields
    alloc = data.get('alloc', {})
    fixed_count = 0
    
    for addr, account in alloc.items():
        if 'code' in account and isinstance(account['code'], str):
            original = account['code']
            fixed = fix_hex_string(original)
            if fixed != original:
                account['code'] = fixed
                fixed_count += 1
                print(f"Fixed code for address {addr}")
    
    if fixed_count > 0:
        # Write fixed JSON
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\nFixed {fixed_count} odd-length hex strings")
        print(f"Output written to {output_file}")
        return True
    else:
        print("No odd-length hex strings found")
        return False

if __name__ == '__main__':
    # Get script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
    genesis_path = os.path.join(project_root, 'script', 'genesis.json')
    output_file = os.path.join(project_root, 'script', 'genesis.json.fixed')
    
    # First check and report
    print("Checking for odd-length hex strings...")
    has_errors = check_and_report(genesis_path)
    
    if has_errors:
        if fix_genesis_file(genesis_path, output_file):
            print(f"\nTo apply the fix, run:")
            print(f"  mv {output_file} {genesis_path}")
        else:
            sys.exit(1)
    else:
        print("No odd-length hex strings found. Genesis file is valid.")

