"""
CLI interface for Instagram Scraper with simple console GUI.
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import csv

# Handle imports for both script and frozen executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    import scraper
    InstagramScraper = scraper.InstagramScraper
else:
    # Running as script - add src to path
    sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
    from scraper import InstagramScraper

console = Console()


def display_banner():
    """Display application banner."""
    banner = """
[bold cyan]╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        Instagram Public Profile Scraper v1.0              ║
║                                                           ║
║        MIT License - Educational Use Only                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝[/bold cyan]
"""
    console.print(banner)
    
    disclaimer = """
[bold yellow]⚠️  LEGAL DISCLAIMER ⚠️[/bold yellow]

This tool is for [bold]educational purposes only[/bold].

By using this tool, you agree to:
• Only scrape [bold]publicly available[/bold] information
• Respect Instagram's Terms of Service
• Comply with applicable data protection laws (GDPR, CCPA, etc.)
• Not use this tool for harassment, spam, or unauthorized data collection
• Take full responsibility for your use of this tool

The developers are not responsible for any misuse of this software.
"""
    console.print(Panel(disclaimer, title="Important Notice", border_style="yellow"))
    
    if not Confirm.ask("\n[bold]Do you agree to these terms?[/bold]", default=False):
        console.print("[red]You must agree to the terms to use this tool.[/red]")
        sys.exit(0)


def show_menu():
    """Display main menu and get user choice."""
    console.print("\n[bold cyan]Main Menu:[/bold cyan]")
    console.print("1. Scrape profiles from CSV file")
    console.print("2. Scrape a single profile")
    console.print("3. View configuration")
    console.print("4. Exit")
    
    choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4"], default="1")
    return choice


def view_configuration():
    """Display current configuration."""
    console.print("\n[bold cyan]Current Configuration:[/bold cyan]\n")
    
    config_table = Table(show_header=True, header_style="bold magenta")
    config_table.add_column("Setting", style="cyan")
    config_table.add_column("Value", style="green")
    
    config_table.add_row("Input File", os.getenv('INPUT_FILE', 'data/input.csv'))
    config_table.add_row("Output File", os.getenv('OUTPUT_FILE', 'data/output.csv'))
    config_table.add_row("Request Timeout", f"{os.getenv('REQUEST_TIMEOUT', '30')} seconds")
    config_table.add_row("Max Retries", os.getenv('MAX_RETRIES', '3'))
    config_table.add_row("Retry Delay", f"{os.getenv('RETRY_DELAY', '5')} seconds")
    config_table.add_row("Rate Limit Delay", f"{os.getenv('RATE_LIMIT_DELAY', '2')} seconds")
    config_table.add_row("Proxy Configured", "Yes" if os.getenv('PROXY_SERVER') else "No")
    
    console.print(config_table)
    console.print("\n[dim]To change settings, edit the .env file[/dim]")


def scrape_single_profile():
    """Scrape a single Instagram profile."""
    username = Prompt.ask("\n[bold cyan]Enter Instagram username[/bold cyan]")
    
    if not username:
        console.print("[red]Username cannot be empty[/red]")
        return
    
    console.print(f"\n[cyan]Scraping profile: {username}[/cyan]")
    
    scraper = InstagramScraper()
    
    try:
        scraper.start_browser()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(description="Fetching profile data...", total=None)
            result = scraper.scrape_profile(username)
            progress.update(task, completed=True)
        
        # Display results
        console.print("\n[bold green]Profile Information:[/bold green]\n")
        
        result_table = Table(show_header=True, header_style="bold magenta")
        result_table.add_column("Field", style="cyan")
        result_table.add_column("Value", style="green")
        
        for key, value in result.items():
            if value:
                result_table.add_row(key.replace('_', ' ').title(), str(value))
        
        console.print(result_table)
        
        # Ask if user wants to save
        if Confirm.ask("\n[bold]Save to output.csv?[/bold]", default=True):
            output_file = 'data/output.csv'
            Path('data').mkdir(exist_ok=True)
            
            fieldnames = list(result.keys())
            file_exists = Path(output_file).exists()
            
            with open(output_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(result)
            
            console.print(f"[green]✓ Saved to {output_file}[/green]")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    
    finally:
        scraper.close_browser()


def scrape_from_csv():
    """Scrape profiles from CSV file."""
    input_file = Prompt.ask(
        "\n[bold cyan]Input CSV file path[/bold cyan]",
        default="data/input.csv"
    )
    
    if not Path(input_file).exists():
        console.print(f"[red]Error: File {input_file} not found[/red]")
        
        if Confirm.ask("Create sample input.csv?", default=True):
            Path('data').mkdir(exist_ok=True)
            with open('data/input.csv', 'w', encoding='utf-8') as f:
                f.write("username\ninstagram\nnatgeo\n")
            console.print("[green]✓ Created sample data/input.csv[/green]")
            input_file = 'data/input.csv'
        else:
            return
    
    # Show preview
    console.print(f"\n[cyan]Preview of {input_file}:[/cyan]")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            rows = list(reader)[:5]  # Show first 5
            
            preview_table = Table(show_header=False)
            preview_table.add_column("Username", style="cyan")
            
            for row in rows:
                if row and row[0].strip():
                    preview_table.add_row(row[0].strip())
            
            console.print(preview_table)
            
            total_count = len([r for r in rows if r and r[0].strip()])
            console.print(f"\n[dim]Total usernames: {total_count}[/dim]")
            
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        return
    
    if not Confirm.ask("\n[bold]Start scraping?[/bold]", default=True):
        return
    
    output_file = Prompt.ask(
        "[bold cyan]Output CSV file path[/bold cyan]",
        default="data/output.csv"
    )
    
    console.print("\n[cyan]Starting scraper...[/cyan]")
    
    try:
        scraper = InstagramScraper()
        scraper.scrape_from_csv(input_file, output_file)
        
        console.print(f"\n[bold green]✓ Scraping complete![/bold green]")
        console.print(f"[green]Results saved to: {output_file}[/green]")
        
    except Exception as e:
        console.print(f"\n[red]Error during scraping: {e}[/red]")


def main():
    """Main CLI application loop."""
    try:
        display_banner()
        
        while True:
            choice = show_menu()
            
            if choice == "1":
                scrape_from_csv()
            elif choice == "2":
                scrape_single_profile()
            elif choice == "3":
                view_configuration()
            elif choice == "4":
                console.print("\n[cyan]Goodbye! 👋[/cyan]\n")
                sys.exit(0)
            
            console.print("\n" + "─" * 60)
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
