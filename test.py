import json
from gallery_dl.job import DownloadJob
from gallery_dl import config





def download_with_metadata_postprocessor(url, cookies_path=None, download_path=None, proxy=None):
    """
    Download Instagram metadata using gallery-dl with postprocessor,
    custom download path, and proxy support
    
    Args:
        url (str): Instagram post URL
        cookies_path (str): Path to cookies file (optional)
        download_path (str): Custom download directory path (optional)
        proxy (str): Proxy server URL (optional)
    
    Returns:
        int: Exit status (0 for success)
    """
    headers = {
        'X-IG-App-ID': '936619743392459',
        'X-ASBD-ID': '198387', 
        'X-IG-WWW-Claim': '0',
        'Origin': 'https://www.instagram.com',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Referer': 'https://www.instagram.com/',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    # Configure postprocessor for metadata
    config.set(('extractor',), 'postprocessors', [
        {
            'name': 'metadata',
            'event': 'post',
            'mode': 'json'
        }
    ])
    config.set(('extractor', 'instagram'), 'cookies', headers)
    # Set custom download path if provided
    if download_path:
        config.set(('extractor',), 'base-directory', download_path)
    
    # Set cookies if provided
    if cookies_path:
        config.set(('extractor', 'instagram'), 'cookies', cookies_path)
    
    # Set proxy if provided
    if proxy:
        config.set(('extractor', 'instagram'), 'proxy', proxy)
    
    # Enable skip to avoid downloading actual files
    config.set(('extractor',), 'skip', True)
    
    job = DownloadJob(url)
    
    job.run()
    with open(f'{download_path}/{download_path}.json', 'w') as f:
        f.write(json.dumps(list(job.extractor.posts()), indent=4))
    # print()


if __name__ == "__main__":
    download_with_metadata_postprocessor('https://www.instagram.com/p/DGGG8RPoQnbajDftLU-bwYsTQ9fhxs-XySvuN40/?igsh=MTg1aGlncjZya2VvMg==', 
                                         cookies_path='instagram_cookies.txt',
                                         download_path='private',
                                         proxy='http://127.0.0.1:10808'
                                         )
    # print(meta)