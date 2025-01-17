from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn, DownloadColumn, TransferSpeedColumn
from .api import MarketplaceAPI
from .models import Extension
import os


class ExtensionDownloader:
    def __init__(self, download_dir: Path):
        if download_dir:
            self.download_dir = download_dir
            self.download_dir.mkdir(parents=True, exist_ok=True)
        self.api = MarketplaceAPI()

    def download(self, extension: Extension) -> Path:
        metadata = self.api.get_extension_metadata(extension)
        download_url = self.api.get_download_url(extension, metadata)

        filename = f"{extension.full_name}-{metadata.version}"
        if extension.architecture:
            filename += f"-{extension.architecture}"
        filename += ".vsix"

        output_path = self.download_dir / filename

        if os.path.exists(output_path):
            return output_path

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            DownloadColumn(),
            TransferSpeedColumn(),
        ) as progress:
            task = progress.add_task(
                f"Downloading {extension.full_name}", total=None)

            response = self.api.session.get(download_url, stream=True)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    progress.advance(task)

        return output_path
