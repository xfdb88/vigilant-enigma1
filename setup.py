"""
Setup script for Instagram Scraper.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
long_description = Path('README.md').read_text(encoding='utf-8')

setup(
    name='instagram-scraper',
    version='1.0.0',
    description='Instagram Public Profile Scraper - Educational Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='vigilant-enigma1',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'playwright==1.40.0',
        'httpx==0.25.2',
        'beautifulsoup4==4.12.2',
        'python-dotenv==1.0.0',
        'lxml==4.9.3',
        'rich==13.7.0',
    ],
    extras_require={
        'dev': [
            'PyInstaller==6.3.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'instagram-scraper=src.cli:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='instagram scraper playwright education',
    project_urls={
        'Source': 'https://github.com/xfdb88/vigilant-enigma1',
    },
)
