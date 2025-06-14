# Instagram Downloader

A Python library for downloading and processing Instagram content using gallery-dl.

## Features

- Download content from Instagram posts, reels, stories, and highlights
- Extract metadata including owner information, captions, and tagged users
- Process and reformat video files using ffmpeg
- Support for private content with cookies authentication
- Proxy support for accessing region-restricted content
- Clean and well-documented API

## Installation

```bash
pip install instagram-downloader
```

### Requirements

- Python 3.6+
- [gallery-dl](https://github.com/mikf/gallery-dl) 1.29.0+
- [ffmpeg](https://ffmpeg.org/) (for video reformatting)
- [httpx](https://www.python-httpx.org/) (for HTTP requests)

## Usage

### Basic Usage

```python
from instagram_downloader import InstagramDownloader

# Initialize the downloader
downloader = InstagramDownloader(
    cookies_path="instagram_cookies.txt",  # Optional
    proxy="http://127.0.0.1:10808"         # Optional
)

# Download content
url = "https://www.instagram.com/p/EXAMPLE/"
metadata = downloader.download_content(url)

# Process the metadata
print(f"Content type: {metadata['content_type']}")
print(f"Caption: {metadata['caption']}")
print(f"Owner: {metadata['owners'][0]['username']}")

# Clean up temporary files
downloader.cleanup()
```

### Command Line Example

The package includes an example script that demonstrates how to use the InstagramDownloader class from the command line:

```bash
python example.py https://www.instagram.com/p/EXAMPLE/ --cookies instagram_cookies.txt --proxy http://127.0.0.1:10808 --output downloads --keep-files
```

### Handling Private Content

To access private content, you need to provide a cookies file from a logged-in Instagram session:

```python
downloader = InstagramDownloader(cookies_path="instagram_cookies.txt")
```

### Using a Proxy

For region-restricted content or to avoid rate limiting, you can use a proxy:

```python
downloader = InstagramDownloader(proxy="http://127.0.0.1:10808")
```

## Content Types

The library supports the following Instagram content types:

- **Posts**: Regular Instagram posts (single image, video, or carousel)
- **Reels**: Instagram reels (short videos)
- **Stories**: User stories
- **Highlights**: Story highlights

## Metadata

The metadata returned by `download_content()` includes:

- `content_type`: Type of content (post, reel, highlight, stories)
- `owners`: List of content owners (username, user_id)
- `original_url`: Original Instagram URL
- `cleaned_url`: URL without query parameters
- `caption`: Content caption
- `tagged_users`: List of tagged users
- `media_files`: List of media files with URLs and types
- `is_private`: Whether the content is private
- `id`: Content ID
- `shortcode`: Content shortcode
- `taken_at`: Timestamp when the content was posted

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [gallery-dl](https://github.com/mikf/gallery-dl) for the core Instagram API interaction
- [ffmpeg](https://ffmpeg.org/) for video processing
