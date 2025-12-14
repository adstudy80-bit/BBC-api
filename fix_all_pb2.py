import os
import re

def fix_pb2_file(filepath):
    print(f"\n=== Fixing {os.path.basename(filepath)} ===")
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    changes = 0
    
    for i, line in enumerate(lines):
        original = line
        stripped = line.strip()
        
        # Rule 1: Fix number-only lines (like "6," "30," "0,")
        if re.match(r'^\d+,?\s*$', stripped) and line != stripped:
            line = stripped + '\n'
            changes += 1
            print(f"  Line {i+1}: Fixed number indentation")
        
        # Rule 2: Fix runtime_version import
        elif 'from google.protobuf import runtime_version' in line:
            if not line.startswith('#'):
                line = '# ' + line
                changes += 1
                print(f"  Line {i+1}: Commented runtime_version import")
        
        # Rule 3: Add _runtime_version = None after commented import
        elif line.strip() == '_runtime_version = None':
            # Already there, keep it
            pass
        
        # Rule 4: Comment ValidateProtobufRuntimeVersion calls
        elif '_runtime_version.ValidateProtobufRuntimeVersion' in line:
            if not line.strip().startswith('#'):
                line = '# ' + line.lstrip()
                changes += 1
                print(f"  Line {i+1}: Commented ValidateProtobufRuntimeVersion")
        
        fixed_lines.append(line)
    
    # Ensure _runtime_version = None exists after the import
    for i in range(len(fixed_lines)):
        if 'from google.protobuf import runtime_version' in fixed_lines[i]:
            # Check next line
            if i+1 < len(fixed_lines) and fixed_lines[i+1].strip() != '_runtime_version = None':
                fixed_lines.insert(i+1, '_runtime_version = None\n')
                changes += 1
                print(f"  Added _runtime_version = None at line {i+2}")
            break
    
    if changes > 0:
        with open(filepath, 'w') as f:
            f.writelines(fixed_lines)
        print(f"  Total changes: {changes}")
    else:
        print("  No changes needed")
    
    return changes

# Fix all pb2 files
pb2_dir = "Pb2"
total_changes = 0
for filename in os.listdir(pb2_dir):
    if filename.endswith('_pb2.py'):
        total_changes += fix_pb2_file(os.path.join(pb2_dir, filename))

print(f"\n=== Total files changed: {total_changes} ===")
print("\nNow running main.py...")
os.system("python main.py")
