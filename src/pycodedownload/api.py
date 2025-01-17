# src/vscode_ext_manager/api.py
import requests
from typing import Dict
from .models import Extension, ExtensionMetadata

class MarketplaceAPI:
    BASE_URL = "https://marketplace.visualstudio.com/_apis/public/gallery"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json;api-version=3.0-preview.1',
            'Content-Type': 'application/json'
        })

    def get_extension_metadata(self, extension: Extension) -> ExtensionMetadata:
        url = f"{self.BASE_URL}/extensionquery"
        query = {
            "filters": [{
                "criteria": [{
                    "filterType": 7,
                    "value": extension.full_name
                }]
            }],
            "flags": 914
        }
        
        response = self.session.post(url, json=query)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('results', []):
            raise ValueError(f"Extension not found: {extension.full_name}")
            
        ext_data = data['results'][0]['extensions'][0]
        return ExtensionMetadata(
            id=ext_data['extensionId'],
            version=ext_data['versions'][0]['version'],
            dependencies=ext_data.get('dependencies', []),
            engine=ext_data['versions'][0].get('engine', {}),
            asset_uri=ext_data['versions'][0]['assetUri']
        )

    def get_download_url(self, extension: Extension, metadata: ExtensionMetadata) -> str:
        url = f"{metadata.asset_uri}/Microsoft.VisualStudio.Services.VSIXPackage"
        
        if extension.architecture:
            url += f"?targetPlatform={extension.architecture}"
        
        return url
