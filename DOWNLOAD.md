# Download Distribution Package

## 📦 Pre-built Executable Package

The Instagram Scraper is available as a pre-built, ready-to-use package.

### What's Included

The `instagram-scraper-dist.zip` file contains:

✅ **Compiled executable** - No Python installation required
✅ **Source code** - Full source for transparency
✅ **Sample data files** - Get started immediately  
✅ **Configuration templates** - Easy setup
✅ **Documentation** - Comprehensive guides
✅ **Run scripts** - One-click launch on all platforms

### Package Contents

```
instagram-scraper-dist/
├── instagram-scraper          # Executable (Linux/Mac)
├── instagram-scraper.exe      # Executable (Windows)
├── src/                       # Full source code
│   ├── scraper.py
│   └── cli.py
├── data/
│   └── input.csv             # Sample input file
├── requirements.txt          # Python dependencies
├── .env.example              # Configuration template
├── README.md                 # Main documentation
├── README.txt                # Quick start guide
├── LICENSE                   # MIT License
├── run.bat                   # Windows launcher
└── run.sh                    # Linux/Mac launcher
```

### File Size

**~62 MB** (compressed)

The package includes the Playwright browser automation framework and all dependencies.

### How to Get It

#### Method 1: Build Locally (Recommended for developers)

```bash
# Clone the repository
git clone https://github.com/xfdb88/vigilant-enigma1.git
cd vigilant-enigma1

# Install dependencies
pip install -r requirements.txt

# Build the distribution
python build.py

# Find the package at:
# ./instagram-scraper-dist.zip
```

#### Method 2: GitHub Releases

Check the [Releases](https://github.com/xfdb88/vigilant-enigma1/releases) page for pre-built packages (if available).

### After Download

1. **Extract the ZIP file**
   ```bash
   unzip instagram-scraper-dist.zip
   cd instagram-scraper-dist
   ```

2. **Run the application**
   
   **Windows:**
   ```cmd
   run.bat
   ```
   
   **Linux/Mac:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

3. **First-time setup**
   
   You may need to install Playwright browsers:
   ```bash
   playwright install chromium
   ```

### Verification

After extracting, verify the contents:

```bash
# Check executable exists
ls -lh instagram-scraper*

# Test the application (will show help/disclaimer)
./instagram-scraper --version
```

### System Requirements

- **OS**: Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)
- **RAM**: Minimum 2GB, Recommended 4GB+
- **Disk**: 500MB free space
- **Network**: Stable internet connection

### Security Note

⚠️ **Always verify downloads**

- Check file size (~62MB)
- Scan with antivirus
- Review included source code
- Only download from official sources

### Need Help?

- 📖 Read [INSTALLATION.md](INSTALLATION.md) for detailed setup
- 📚 Check [README.md](README.md) for usage guide
- 🐛 Report issues on [GitHub](https://github.com/xfdb88/vigilant-enigma1/issues)

---

## Quick Start After Download

1. Extract `instagram-scraper-dist.zip`
2. Edit `data/input.csv` with Instagram usernames
3. Run `run.bat` (Windows) or `./run.sh` (Linux/Mac)
4. Follow the on-screen instructions
5. Find results in `data/output.csv`

---

**License**: MIT  
**Version**: 1.0.0  
**Updated**: 2025-10-16
