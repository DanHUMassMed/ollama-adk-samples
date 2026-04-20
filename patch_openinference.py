# Automatically patching openinference-instrumentation-google-adk 
# due to prerelease string conversion bug: `invalid literal for int() with base 10: '0a3'`
# Run this script directly from the project root using standard python or `uv run python patch_openinference.py`

import os
import glob
import sys

def patch_openinference():
    # Find the python site-packages path within .venv
    venv_path = os.path.join(os.getcwd(), '.venv')
    if not os.path.exists(venv_path):
        print(f"Error: .venv not found at {venv_path}")
        print("Please run this script from the workspace root containing the .venv folder.")
        sys.exit(1)

    # Glob for python3.* dynamic paths in .venv
    adk_init_paths = glob.glob(os.path.join(venv_path, 'lib', 'python*', 'site-packages', 'openinference', 'instrumentation', 'google_adk', '__init__.py'))
    
    if not adk_init_paths:
        print("Error: Could not find openinference/instrumentation/google_adk/__init__.py in .venv")
        print("Make sure openinference-instrumentation-google-adk is installed via `uv sync` first.")
        sys.exit(1)
        
    target_file = adk_init_paths[0]
    print(f"Targeting: {target_file}")
    
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_line = 'version = cast(tuple[int, int, int], tuple(int(x) for x in __version__.split(".")[:3]))'
    patched_line = 'version = cast(tuple[int, int, int], tuple(int("".join(c for c in x if c.isdigit()) or 0) for x in __version__.split(".")[:3]))'

    if patched_line in content:
        print("✅ File is already patched! No changes needed.")
        sys.exit(0)
        
    if original_line not in content:
        print("⚠️ Warning: Could not find the exactly original line to patch.")
        print("The openinference package may have been updated upstream and the bug fixed.")
        sys.exit(1)

    content = content.replace(original_line, patched_line)
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("✅ Hot-patch safely applied to the .venv environment!")

if __name__ == "__main__":
    patch_openinference()
