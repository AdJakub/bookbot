import re
import time
from pathlib import Path

import requests

DOWNLOAD_DIR = Path(r"./books")

LIMIT = 1000

API_URL = "https://gutendex.com/books/"

MIRROR_BASE = "https://gutenberg.pglaf.org/cache/epub"

RETRY_STATUSES = {429, 500, 502, 503, 504}

session = requests.Session()
session.headers.update({"User-Agent": "PersonalGutenbergDownloader/1.0"})


def get_with_retry(
    url: str,
    params: dict | None = None,
    stream: bool = False,
    timeout: tuple[int, int] = (10, 120),
    attempts: int = 8,
) -> requests.Response:

    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    for attempt in range(attempts):
        try:
            response = session.get(url, params=params, stream=stream, timeout=timeout)
            response.raise_for_status()
            return response

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
        ) as error:
            if isinstance(error, requests.exceptions.HTTPError):
                if error.response.status_code not in RETRY_STATUSES:
                    raise

            if attempt == attempts - 1:
                raise

            delay = min(2 ** (attempt + 1), 60)
            print(
                f"Request failed ({error.__class__.__name__}). "
                f"Retrying in {delay} seconds ({attempt + 2}/{attempts})..."
            )
            time.sleep(delay)

    raise RuntimeError("Request failed after all retry attempts")


def clean_filename(title):
    title = title.split(";", 1)[0].strip()

    title = "".join(character.lower() for character in title if character.isalnum())
    return title or "Untitled"


def download_book(book):
    book_id = book["id"]
    title = book["title"]

    filename = DOWNLOAD_DIR / (f"{clean_filename(title)}.txt")

    if filename.exists() and filename.stat().st_size > 0:
        return "skipped", f"already exists: {filename.name}"

    url = f"{MIRROR_BASE}/{book_id}/pg{book_id}.txt"
    temp_file = filename.with_suffix(".txt.part")

    try:
        with get_with_retry(url, stream=True, timeout=(10, 120)) as response:
            with temp_file.open("wb") as file:
                for chunk in response.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        file.write(chunk)
            if temp_file.stat().st_size == 0:
                raise ValueError("The downloaded file was empty")

        temp_file.replace(filename)
        return "downloaded", f"Downloaded: {filename.name}"

    except (requests.RequestException, OSError, ValueError) as error:
        if temp_file.exists():
            temp_file.unlink()

        return "failed", f"Failed: {title} (ID {book_id}): {error}"


def download_top_books():
    url = API_URL

    params = {"languages": "en", "sort": "popular", "mime_type": "text/plain"}

    downloaded = 0

    while url and downloaded < LIMIT:
        with get_with_retry(url, params=params, timeout=(10, 120)) as response:
            data = response.json()

        for book in data["results"]:
            if downloaded >= LIMIT:
                break

            success, message = download_book(book)
            print(message)

            if success:
                downloaded += 1
                print(f"Progress: {downloaded}/{LIMIT}")

            time.sleep(1)

        url = data["next"]

        params = None

    print(f"\nFinished. {downloaded} books available")
    print(f"Folder: {DOWNLOAD_DIR.resolve()}")


download_top_books()
