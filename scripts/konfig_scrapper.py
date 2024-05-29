from pathlib import Path
import requests
from bs4 import BeautifulSoup
from requests import Response


class KonfigScraper:
    def __init__(self, output_path: Path):
        self.repository_url = r"https://github.com/konfig-sdks/openapi-examples"
        self.output_path = output_path
        self.dirs = set()
        self.cache = {}

    def reset(self):
        self.dirs = set()
        self.cache = {}

    def download_file(self, file_url: str, file_name: str) -> None:
        print(f"Downloading: {file_url}")

        # Make a request to download the file
        file_response = requests.get(file_url)
        # Check if the download request was successful (status code 200)
        if file_response.status_code == 200:
            self.cache[file_url] = {
                "file_name": file_name,
                "file_response": file_response,
            }
            # Save the file to the target directory
            with open(self.output_path / file_name, "wb") as file:
                file.write(file_response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(
                f"Failed to download {file_name}. Status code: {file_response.status_code}"
            )

    @staticmethod
    def _get_openapi_file(page: Response):
        soup = BeautifulSoup(page.content, "html.parser")
        return soup.find(
            "a",
            {
                "title": lambda x: x
                and x.lower() in {"openapi.yaml", "openapi.yml", "openapi.json"}
            },
        )

    @staticmethod
    def _get_dir_subdirectories(page: Response) -> list:
        soup = BeautifulSoup(page.content, "html.parser")
        return soup.find_all("a", {"aria-label": lambda x: x and "(Directory)" in x})

    def _explore_api(self, api_url: str, name: str) -> None:
        page = requests.get(api_url)
        openapi_spec_file = self._get_openapi_file(page)

        if openapi_spec_file:
            file_url = f"https://github.com/{openapi_spec_file['href']}".replace(
                "github.com", "raw.githubusercontent.com"
            ).replace("/blob", "")

            file_extension = file_url.split(".")[-1]
            file_name = f"{name}.{file_extension}"

            self.download_file(file_url, file_name)

        directories = self._get_dir_subdirectories(page)
        for directory in directories:
            directory_url = f"https://github.com/{directory['href']}"
            if directory_url in self.dirs:
                continue
            self.dirs.add(directory_url)
            directory_name = f"{name}_{directory_url.split('/')[-1]}"
            self._explore_api(directory_url, directory_name)

    def save_cache(self):
        for file_url, file_info in self.cache.items():
            with open(
                self.output_path / f"{file_info['file_name']}.cache", "wb"
            ) as file:
                file.write(file_info["file_response"].content)

    def scrap_repository(self) -> None:
        if self.cache:
            print(
                "Restoring from cache... to disable cache, delete the cache files by calling `reset` method."
            )
            for file_url, file_info in self.cache.items():
                with open(
                    self.output_path / f"{file_info['file_name']}.cache", "wb"
                ) as file:
                    file.write(file_info["file_response"].content)
            return

        page = requests.get(self.repository_url)

        # Create the output directory if it does not exist
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Find all the links in the page that has "(Directory)" in the aria-label attribute
        directories = self._get_dir_subdirectories(page)

        for directory in directories:
            directory_url = f"https://github.com/{directory['href']}"
            if directory_url in self.dirs:
                continue
            self.dirs.add(directory_url)
            directory_name = directory_url.split("/")[-1]
            self._explore_api(directory_url, directory_name)


if __name__ == "__main__":
    url = r"https://github.com/konfig-sdks/openapi-examples"
    output_dir = Path(__file__).parent.parent / "data" / "openapi-specifications"
    scraper = KonfigScraper(output_dir)
    scraper.scrap_repository()
