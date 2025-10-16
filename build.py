"""
Build script to create distributable package with PyInstaller.
"""

import os
import shutil
import subprocess
from pathlib import Path


def clean_build_dirs():
    """Clean previous build directories."""
    print("Cleaning previous builds...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")
    
    # Clean spec files
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"  Removed {spec_file}")


def create_executable():
    """Create executable using PyInstaller."""
    print("\nCreating executable with PyInstaller...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',  # Single executable file
        '--name=instagram-scraper',  # Name of executable
        '--add-data=.env.example:.', # Include .env.example
        '--hidden-import=playwright',
        '--hidden-import=httpx',
        '--hidden-import=bs4',
        '--hidden-import=rich',
        '--collect-all=playwright',
        'src/cli.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("  ✓ Executable created successfully")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error creating executable: {e}")
        return False
    
    return True


def create_distribution():
    """Create distribution package."""
    print("\nCreating distribution package...")
    
    dist_name = 'instagram-scraper-dist'
    dist_path = Path('dist') / dist_name
    
    # Create distribution directory
    if dist_path.exists():
        shutil.rmtree(dist_path)
    dist_path.mkdir(parents=True)
    
    # Copy executable
    exe_name = 'instagram-scraper.exe' if os.name == 'nt' else 'instagram-scraper'
    exe_path = Path('dist') / exe_name
    
    if exe_path.exists():
        shutil.copy2(exe_path, dist_path / exe_name)
        print(f"  ✓ Copied {exe_name}")
    
    # Copy source files
    src_dist = dist_path / 'src'
    src_dist.mkdir()
    for py_file in Path('src').glob('*.py'):
        shutil.copy2(py_file, src_dist / py_file.name)
    print("  ✓ Copied source files")
    
    # Copy data directory
    data_dist = dist_path / 'data'
    data_dist.mkdir()
    if Path('data/input.csv').exists():
        shutil.copy2('data/input.csv', data_dist / 'input.csv')
    print("  ✓ Copied data directory")
    
    # Copy configuration files
    files_to_copy = [
        'requirements.txt',
        '.env.example',
        'README.md',
        'LICENSE'
    ]
    
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, dist_path / file_name)
            print(f"  ✓ Copied {file_name}")
    
    # Create README for distribution
    create_dist_readme(dist_path)
    
    # Create run script
    create_run_script(dist_path)
    
    # Create zip file
    print("\nCreating ZIP archive...")
    zip_name = f'{dist_name}'
    shutil.make_archive(zip_name, 'zip', 'dist', dist_name)
    
    zip_file = Path(f'{zip_name}.zip')
    if zip_file.exists():
        size_mb = zip_file.stat().st_size / (1024 * 1024)
        print(f"  ✓ Created {zip_file} ({size_mb:.2f} MB)")
        return str(zip_file)
    
    return None


def create_dist_readme(dist_path):
    """Create README for distribution."""
    readme_content = """# Instagram Public Profile Scraper

## Quick Start

### Method 1: Run the executable (Recommended)
1. Run `instagram-scraper.exe` (Windows) or `./instagram-scraper` (Linux/Mac)
2. Follow the on-screen instructions

### Method 2: Run from source
1. Install Python 3.8 or higher
2. Install dependencies: `pip install -r requirements.txt`
3. Install Playwright browsers: `playwright install chromium`
4. Copy `.env.example` to `.env` and configure (optional)
5. Run: `python src/cli.py`

## Usage

1. Prepare your input file:
   - Edit `data/input.csv` with Instagram usernames (one per line)
   - Example:
     ```
     username
     instagram
     natgeo
     ```

2. Run the scraper:
   - Choose option 1 from the menu to scrape from CSV
   - Or choose option 2 to scrape a single profile

3. Results will be saved to `data/output.csv`

## Configuration

Edit the `.env` file to customize:
- Request timeout
- Retry settings
- Rate limiting
- Proxy settings (optional)

## Important Notes

⚠️ **Legal Disclaimer**: This tool is for educational purposes only.
- Only scrape publicly available information
- Respect Instagram's Terms of Service
- Comply with data protection laws (GDPR, CCPA, etc.)

## License

MIT License - See LICENSE file for details
"""
    
    with open(dist_path / 'README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("  ✓ Created distribution README.txt")


def create_run_script(dist_path):
    """Create convenience run scripts."""
    # Windows batch script
    batch_content = """@echo off
echo Starting Instagram Scraper...
echo.

REM Check if running executable or source
if exist instagram-scraper.exe (
    instagram-scraper.exe
) else (
    python src/cli.py
)

pause
"""
    
    with open(dist_path / 'run.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    # Linux/Mac shell script
    shell_content = """#!/bin/bash
echo "Starting Instagram Scraper..."
echo

# Check if running executable or source
if [ -f "./instagram-scraper" ]; then
    ./instagram-scraper
else
    python3 src/cli.py
fi

read -p "Press Enter to exit..."
"""
    
    script_path = dist_path / 'run.sh'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(shell_content)
    
    # Make shell script executable
    os.chmod(script_path, 0o755)
    
    print("  ✓ Created run scripts")


def main():
    """Main build process."""
    print("=" * 60)
    print("Instagram Scraper - Build Script")
    print("=" * 60)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create executable
    if not create_executable():
        print("\n✗ Build failed")
        return
    
    # Create distribution package
    zip_file = create_distribution()
    
    if zip_file:
        print("\n" + "=" * 60)
        print("✓ Build completed successfully!")
        print("=" * 60)
        print(f"\nDistribution package: {zip_file}")
        print("\nTo distribute:")
        print(f"  1. Share {zip_file}")
        print("  2. Recipients can extract and run immediately")
        print("\nNote: Recipients may need to install Playwright browsers:")
        print("  playwright install chromium")
    else:
        print("\n✗ Failed to create distribution package")


if __name__ == '__main__':
    main()
