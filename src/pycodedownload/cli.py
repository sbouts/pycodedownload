# src/vscode_ext_manager/cli.py
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from .config import load_config
from .downloader import ExtensionDownloader
from .compatibility import CompatibilityChecker
from .blacklist import BlacklistChecker
from .dependency import DependencyHandler

console = Console()

@click.group()
def cli():
    """VSCode Extension Manager"""
    pass

# Similar implementations for download-extensions and list-extensions commands...
@cli.command()
@click.argument('config_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output-dir', '-o', type=click.Path(path_type=Path), default='extensions')
def download_extensions(config_file, output_dir):
    """Download extensions specified in the config file"""
    extensions = load_config(config_file)
    downloader = ExtensionDownloader(output_dir)
    
    for ext in extensions:
        try:
            path = downloader.download(ext)
            console.print(f"[green]Downloaded {ext.full_name} to {path}")
        except Exception as e:
            console.print(f"[red]Failed to download {ext.full_name}: {e}")

@cli.command()
@click.argument('config_file', type=click.Path(exists=True, path_type=Path))
def list_extensions(config_file):
    """List all extensions in the config file"""
    extensions = load_config(config_file)
    
    table = Table(title="Configured Extensions")
    table.add_column("Name")
    table.add_column("Version")
    table.add_column("Architecture")
    
    for ext in extensions:
        table.add_row(ext.full_name, ext.version, ext.architecture or "any")
    
    console.print(table)

if __name__ == '__main__':
    cli()
