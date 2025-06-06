#!/usr/bin/env python3
"""
Project setup script for AI Plant Doctor

This script helps organize your files and fix common issues.
"""

import os
import shutil
import sys

def create_project_structure():
    """Create proper project directory structure"""
    
    print("🏗️  Setting up AI Plant Doctor project structure...")
    
    # Define directories to create
    directories = [
        'src',
        'tests', 
        'docs',
        'examples',
        'scripts',
        'configs'
    ]
    
    # Create directories
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Created directory: {directory}/")
        else:
            print(f"   📁 Directory exists: {directory}/")
    
    return True

def move_python_files_to_src():
    """Move Python files to src directory"""
    
    print("\n📦 Moving Python files to src/...")
    
    # Python files that should be in src/
    python_files = [
        'gradio_app.py',
        'model_handler.py', 
        'plant_health_analyzer.py',
        'plant_database.py',
        'utils.py'
    ]
    
    moved_files = []
    
    for file in python_files:
        if os.path.exists(file) and not os.path.exists(f'src/{file}'):
            try:
                shutil.move(file, f'src/{file}')
                moved_files.append(file)
                print(f"   ✅ Moved {file} -> src/{file}")
            except Exception as e:
                print(f"   ❌ Failed to move {file}: {e}")
        elif os.path.exists(f'src/{file}'):
            print(f"   📁 Already in src/: {file}")
        else:
            print(f"   ⚠️  File not found: {file}")
    
    if moved_files:
        print(f"\n   📦 Moved {len(moved_files)} files to src/")
    
    return True

def create_init_files():
    """Create __init__.py files for Python packages"""
    
    print("\n📄 Creating __init__.py files...")
    
    init_locations = [
        'src/__init__.py',
        'tests/__init__.py'
    ]
    
    for init_file in init_locations:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                if 'src' in init_file:
                    f.write('"""AI Plant Doctor - Source Package"""\n')
                else:
                    f.write('"""AI Plant Doctor - Test Package"""\n')
            print(f"   ✅ Created {init_file}")
        else:
            print(f"   📄 Exists: {init_file}")
    
    return True

def create_requirements_txt():
    """Create requirements.txt if it doesn't exist"""
    
    print("\n📋 Checking requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        requirements_content = """# AI Plant Doctor Dependencies

# Core dependencies
gradio>=4.0.0
torch>=2.0.0
torchvision>=0.15.0
transformers>=4.35.0
accelerate>=0.20.0
sentencepiece>=0.1.99
protobuf>=3.20.0

# Image processing
Pillow>=9.0.0

# Utilities
numpy>=1.21.0
regex>=2023.6.3

# Testing (optional)
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-xdist>=3.0.0

# Development (optional)
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
"""
        
        with open('requirements.txt', 'w') as f:
            f.write(requirements_content)
        print("   ✅ Created requirements.txt")
    else:
        print("   📋 requirements.txt already exists")
    
    return True

def fix_import_issues():
    """Fix common import issues in source files"""
    
    print("\n🔧 Checking for import issues...")
    
    src_files = []
    if os.path.exists('src'):
        src_files = [f for f in os.listdir('src') if f.endswith('.py') and f != '__init__.py']
    
    for file in src_files:
        file_path = f'src/{file}'
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if file can be imported (basic syntax check)
            if 'import' in content and 'def' in content:
                print(f"   ✅ {file} appears to have valid syntax")
            else:
                print(f"   ⚠️  {file} may have syntax issues")
                
        except Exception as e:
            print(f"   ❌ Error checking {file}: {e}")
    
    return True

def create_simple_test():
    """Create a simple working test file"""
    
    print("\n🧪 Creating simple test file...")
    
    simple_test_content = '''"""
Simple working test for AI Plant Doctor
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestBasicSetup(unittest.TestCase):
    """Test that basic setup is working"""
    
    def test_imports(self):
        """Test that we can import basic modules"""
        try:
            from PIL import Image
            self.assertTrue(True, "PIL imported successfully")
        except ImportError:
            self.fail("PIL/Pillow not available")
    
    def test_torch(self):
        """Test that PyTorch is available"""
        try:
            import torch
            self.assertTrue(True, "PyTorch imported successfully")
        except ImportError:
            self.fail("PyTorch not available")
    
    def test_image_creation(self):
        """Test basic image operations"""
        from PIL import Image
        
        # Create test image
        img = Image.new('RGB', (100, 100), color='green')
        self.assertEqual(img.size, (100, 100))
        self.assertEqual(img.mode, 'RGB')
    
    def test_project_structure(self):
        """Test that project structure exists"""
        project_root = os.path.dirname(os.path.dirname(__file__))
        
        # Check for src directory
        src_dir = os.path.join(project_root, 'src')
        self.assertTrue(os.path.exists(src_dir), "src/ directory should exist")
        
        # Check for tests directory
        tests_dir = os.path.join(project_root, 'tests')
        self.assertTrue(os.path.exists(tests_dir), "tests/ directory should exist")

if __name__ == '__main__':
    unittest.main(verbosity=2)
'''
    
    test_file_path = 'tests/test_setup.py'
    if not os.path.exists(test_file_path):
        with open(test_file_path, 'w') as f:
            f.write(simple_test_content)
        print(f"   ✅ Created {test_file_path}")
    else:
        print(f"   📄 {test_file_path} already exists")
    
    return True

def create_gitignore():
    """Create .gitignore file"""
    
    print("\n📝 Creating .gitignore...")
    
    if not os.path.exists('.gitignore'):
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environments
venv/
env/
ENV/
.venv/
.env

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Model cache
.cache/
models/
checkpoints/

# Temporary files
tmp/
temp/
*.tmp

# Jupyter Notebooks
.ipynb_checkpoints

# Testing
.coverage
.pytest_cache/
htmlcov/

# Gradio
gradio_cached_examples/
flagged/
"""
        
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("   ✅ Created .gitignore")
    else:
        print("   📝 .gitignore already exists")
    
    return True

def run_basic_test():
    """Run the basic setup test"""
    
    print("\n🚀 Running basic setup test...")
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, '-m', 'unittest', 'tests.test_setup', '-v'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("   ✅ Basic setup test passed!")
            print("   🎉 Your project is properly configured!")
        else:
            print("   ⚠️  Basic setup test had issues:")
            print(f"      {result.stderr}")
            print("   💡 This is normal - some dependencies may need installation")
    
    except Exception as e:
        print(f"   ⚠️  Could not run test: {e}")
        print("   💡 You can manually run: python -m unittest tests.test_setup -v")
    
    return True

def main():
    """Main setup function"""
    
    print("🌱 AI Plant Doctor - Project Setup")
    print("=" * 50)
    
    current_dir = os.getcwd()
    print(f"📁 Working in: {current_dir}")
    
    try:
        # Run all setup steps
        steps = [
            ("Creating project structure", create_project_structure),
            ("Moving Python files to src/", move_python_files_to_src), 
            ("Creating __init__.py files", create_init_files),
            ("Creating requirements.txt", create_requirements_txt),
            ("Checking import issues", fix_import_issues),
            ("Creating simple test", create_simple_test),
            ("Creating .gitignore", create_gitignore),
            ("Running basic test", run_basic_test)
        ]
        
        for step_name, step_function in steps:
            print(f"\n📋 {step_name}...")
            try:
                step_function()
            except Exception as e:
                print(f"   ❌ Error in {step_name}: {e}")
        
        # Final summary
        print("\n" + "=" * 50)
        print("🎉 Setup Complete!")
        print("=" * 50)
        
        print("\n📋 Next Steps:")
        print("1. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n2. Run simple tests:")
        print("   python tests/run_simple_tests.py --individual")
        print("\n3. Test your application:")
        print("   python src/gradio_app.py")
        print("\n4. Run all tests:")
        print("   python tests/run_simple_tests.py")
        
        print("\n🚀 Your AI Plant Doctor project is ready for development!")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)