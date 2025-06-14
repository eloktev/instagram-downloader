#!/usr/bin/env python3
"""
Example script demonstrating how to use the InstagramDownloader class.
This script downloads content from an Instagram URL and displays the metadata.
"""

import os
import argparse
from instagram_downloader import InstagramDownloader


def main():
    """Main function to demonstrate InstagramDownloader usage."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Download Instagram content')
    parser.add_argument('url', help='Instagram URL to download')
    parser.add_argument('--cookies', help='Path to Instagram cookies file', default='instagram_cookies.txt')
    parser.add_argument('--proxy', help='Proxy server URL (e.g., http://127.0.0.1:10808)', default=None)
    parser.add_argument('--output', help='Output directory for downloaded files', default='downloads')
    parser.add_argument('--keep-files', action='store_true', help='Keep downloaded files (don\'t clean up)')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Initialize the downloader
    downloader = InstagramDownloader(
        cookies_path=args.cookies if os.path.exists(args.cookies) else None,
        proxy=args.proxy
    )
    
    try:
        # Validate the URL
        if not downloader.validate_instagram_url(args.url):
            print(f"Error: Invalid Instagram URL: {args.url}")
            return 1
        
        print(f"Downloading content from: {args.url}")
        print(f"Content type detected: {downloader.content_type}")
        
        # Download content
        metadata = downloader.download_content(args.url)
        
        # Display metadata
        print("\n=== Content Metadata ===")
        print(f"Content type: {metadata['content_type']}")
        
        # Check if content is private
        if metadata.get('is_private', False):
            print("\n=== PRIVATE CONTENT ===")
            print(f"This content appears to be private or not accessible.")
            if 'error' in metadata:
                print(f"Error: {metadata['error']}")
            print("\nTo access private content, make sure:")
            print("1. You are logged in (using a valid cookies file)")
            print("2. You have permission to view this content")
            print("3. The content still exists and hasn't been deleted")
        else:
            if metadata['owners']:
                print("\n=== Owners ===")
                for owner in metadata['owners']:
                    print(f"Username: {owner['username']}")
                    print(f"User ID: {owner['user_id']}")
            
            print(f"\nOriginal URL: {metadata['original_url']}")
            print(f"Cleaned URL: {metadata['cleaned_url']}")
            
            if metadata['caption']:
                print(f"\nCaption: {metadata['caption']}")
            
            if metadata['tagged_users']:
                print("\n=== Tagged Users ===")
                for user in metadata['tagged_users']:
                    print(f"Username: {user['username']}")
                    print(f"User ID: {user['user_id']}")
            
            # Display downloaded media files
            if downloader.media_files:
                print("\n=== Downloaded Media Files ===")
                for i, file_path in enumerate(downloader.media_files, 1):
                    file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                    print(f"{i}. {os.path.basename(file_path)} ({file_size:.2f} MB)")
                    
                    # Copy files to output directory if keep-files is specified
                    if args.keep_files:
                        import shutil
                        dest_path = os.path.join(args.output, os.path.basename(file_path))
                        shutil.copy2(file_path, dest_path)
                        print(f"   Saved to: {dest_path}")
                with open(os.path.join(args.output, f'{os.path.basename(file_path)}.json'), 'w') as f:
                    import json
                    f.write(json.dumps(metadata, indent=4))
                with open(os.path.join(args.output, f'raw_{os.path.basename(file_path)}.json'), 'w') as f:
                    import json
                    f.write(json.dumps(downloader.metadata, indent=4))
                        
            else:
                print("\nNo media files were downloaded.")
        
        return 0
        
    except Exception as e:
        import traceback
        print(f"Error: {e} {traceback.format_exc()}")
        return 1
    
    finally:
        # Clean up temporary files unless keep-files is specified
        downloader.cleanup()
        print("\nTemporary files cleaned up.")
        if args.keep_files:
            print(f"\nFiles saved to: {args.output}")
            # print(f"Temporary directory: {downloader.temp_dir}")


if __name__ == "__main__":
    exit(main())
