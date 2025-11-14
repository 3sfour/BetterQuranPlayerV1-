import requests
import os 
directory_path = (f"{os.getcwd()}/audio")
def download_zip(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    

# Example:
download_zip(
    "https://everyayah.com/data/warsh/warsh_ibrahim_aldosary_128kbps/000_versebyverse.zip",
        "reciter.zip"
)
