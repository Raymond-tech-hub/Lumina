import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)          
print("Working directory set to:", os.getcwd())

def list_files(base_path, indent=0):
    """Recursively lists files and directories with indentation for structure."""
    for entry in sorted(os.listdir(base_path)):
        path = os.path.join(base_path, entry)
        print('    ' * indent + '|-- ' + entry)
        if os.path.isdir(path):
            list_files(path, indent + 1)

# Replace this with the path to your folder or extracted zip
directory_path = dname

print(f"File structure of: {directory_path}")
list_files(directory_path)
