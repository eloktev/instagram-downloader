#!/usr/bin/env python3
"""
Unit tests for the InstagramDownloader class.
"""

import os
import unittest
from unittest.mock import patch, MagicMock, Mock
import tempfile
import shutil
import json
import sys

# Mock the gallery_dl module before importing InstagramDownloader
sys.modules['gallery_dl'] = MagicMock()
sys.modules['gallery_dl.job'] = MagicMock()
sys.modules['gallery_dl.config'] = MagicMock()

# Create mock classes for gallery-dl
class MockConfig:
    @staticmethod
    def set(*args):
        pass

class MockExtractor:
    def __init__(self, posts_data=None, exception=None):
        self.posts_data = posts_data or []
        self.exception = exception
        
    def posts(self):
        if self.exception:
            raise self.exception
        return self.posts_data

class MockDownloadJob:
    def __init__(self, posts_data=None, exception=None):
        self.extractor = MockExtractor(posts_data, exception)
        
    def run(self):
        pass

# Set up the mocks in the modules
sys.modules['gallery_dl.config'].set = MockConfig.set
sys.modules['gallery_dl.job'].DownloadJob = MockDownloadJob

# Now import InstagramDownloader
from instagram_downloader import InstagramDownloader


class TestInstagramDownloader(unittest.TestCase):
    """Test cases for the InstagramDownloader class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp(prefix="test_instagram_")
        self.downloader = InstagramDownloader(
            cookies_path=None,
            proxy=None
        )
        
        # Create a mock image file
        self.mock_image_path = os.path.join(self.test_dir, "mock_image.jpg")
        with open(self.mock_image_path, "wb") as f:
            f.write(b"mock image data")
        
        # Create a mock video file
        self.mock_video_path = os.path.join(self.test_dir, "mock_video.mp4")
        with open(self.mock_video_path, "wb") as f:
            f.write(b"mock video data")

    def tearDown(self):
        """Tear down test fixtures."""
        self.downloader.cleanup()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_validate_instagram_url(self):
        """Test URL validation."""
        # Valid URLs
        self.assertTrue(self.downloader.validate_instagram_url("https://www.instagram.com/p/ABC123/"))
        self.assertEqual(self.downloader.content_type, "post")
        
        self.assertTrue(self.downloader.validate_instagram_url("https://instagram.com/reel/ABC123/"))
        self.assertEqual(self.downloader.content_type, "reel")
        
        self.assertTrue(self.downloader.validate_instagram_url("https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTQ3Mzk2NDQ0OTYyNDI5"))
        self.assertEqual(self.downloader.content_type, "highlight")
        
        self.assertTrue(self.downloader.validate_instagram_url("https://www.instagram.com/stories/highlights/123456789/"))
        self.assertEqual(self.downloader.content_type, "highlights")
        
        # Invalid URLs
        self.assertFalse(self.downloader.validate_instagram_url("https://www.example.com"))
        self.assertFalse(self.downloader.validate_instagram_url("https://www.instagram.com/username"))
        self.assertFalse(self.downloader.validate_instagram_url("not a url"))

    def test_clean_url(self):
        """Test URL cleaning."""
        url = "https://www.instagram.com/p/ABC123/?utm_source=ig_web_copy_link"
        cleaned_url = self.downloader.clean_url(url)
        self.assertEqual(cleaned_url, "https://www.instagram.com/p/ABC123")
        
        url = "https://www.instagram.com/reel/ABC123/?igshid=123456789"
        cleaned_url = self.downloader.clean_url(url)
        self.assertEqual(cleaned_url, "https://www.instagram.com/reel/ABC123")

    def test_create_temp_directory(self):
        """Test temporary directory creation."""
        temp_dir = self.downloader.create_temp_directory()
        self.assertTrue(os.path.exists(temp_dir))
        self.assertEqual(temp_dir, self.downloader.temp_dir)

    @patch('gallery_dl.config.set')
    def test_download_content_post(self, mock_config_set):
        """Test downloading post content."""
        # Sample post data
        mock_post_data = [{
            'owner': {
                'username': 'test_user',
                'id': '12345'
            },
            'post_url': 'https://www.instagram.com/p/ABC123/',
            'caption': {
                'text': 'Test caption'
            },
            'tagged_users': [
                {
                    'username': 'tagged_user',
                    'id': '67890'
                }
            ],
            'content': [
                {
                    'url': 'https://example.com/image.jpg',
                    'type': 'image',
                    'filename': 'image.jpg'
                }
            ]
        }]
        
        # Use our MockDownloadJob class
        with patch('gallery_dl.job.DownloadJob', return_value=MockDownloadJob(mock_post_data)):
            # Set up the downloader
            self.downloader.temp_dir = self.test_dir
            self.downloader.content_type = 'post'
            self.downloader.media_files = [self.mock_image_path]
            
            # Call the method
            metadata = self.downloader.download_content('https://www.instagram.com/p/ABC123/')
        
        # Verify the results
        self.assertEqual(metadata['content_type'], 'post')
        self.assertEqual(len(metadata['owners']), 1)
        self.assertEqual(metadata['owners'][0]['username'], 'test_user')
        self.assertEqual(metadata['owners'][0]['user_id'], '12345')
        self.assertEqual(metadata['original_url'], 'https://www.instagram.com/p/ABC123/')
        self.assertEqual(metadata['cleaned_url'], 'https://www.instagram.com/p/ABC123')
        self.assertEqual(metadata['caption'], 'Test caption')
        self.assertEqual(len(metadata['tagged_users']), 1)
        self.assertEqual(metadata['tagged_users'][0]['username'], 'tagged_user')
        self.assertEqual(metadata['tagged_users'][0]['user_id'], '67890')

    @patch('gallery_dl.config.set')
    def test_download_content_highlight(self, mock_config_set):
        """Test downloading highlight content."""
        # Sample highlight data
        mock_highlight_data = [{
            'user': {
                'username': 'test_user',
                'id': '12345'
            },
            'highlight_url': 'https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTQ3Mzk2NDQ0OTYyNDI5',
            'items': [
                {
                    'id': 'item123',
                    'caption': 'Test caption',
                    'image_versions2': {
                        'candidates': [
                            {
                                'url': 'https://example.com/image.jpg'
                            }
                        ]
                    }
                }
            ]
        }]
        
        # Use our MockDownloadJob class
        with patch('gallery_dl.job.DownloadJob', return_value=MockDownloadJob(mock_highlight_data)):
            # Set up the downloader
            self.downloader.temp_dir = self.test_dir
            self.downloader.content_type = 'highlight'
            self.downloader.media_files = [self.mock_image_path]
            
            # Call the method
            metadata = self.downloader.download_content('https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTQ3Mzk2NDQ0OTYyNDI5')
        
        # Verify the results
        self.assertEqual(metadata['content_type'], 'highlight')
        self.assertEqual(len(metadata['owners']), 1)
        self.assertEqual(metadata['owners'][0]['username'], 'test_user')
        self.assertEqual(metadata['owners'][0]['user_id'], '12345')
        self.assertEqual(metadata['original_url'], 'https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTQ3Mzk2NDQ0OTYyNDI5')
        self.assertEqual(metadata['cleaned_url'], 'https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTQ3Mzk2NDQ0OTYyNDI5')
        self.assertEqual(metadata['caption'], 'Test caption')

    @patch('subprocess.run')
    def test_reformat_video(self, mock_subprocess_run):
        """Test video reformatting."""
        # Set up the mock
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        
        # Call the method
        self.downloader._reformat_video(self.mock_video_path)
        
        # Verify the subprocess call
        mock_subprocess_run.assert_called_once()
        args, kwargs = mock_subprocess_run.call_args
        
        # Check that ffmpeg command is correct
        self.assertEqual(args[0][0], 'ffmpeg')
        self.assertEqual(args[0][1], '-i')
        self.assertEqual(args[0][2], self.mock_video_path)
        self.assertEqual(args[0][3], '-c:v')
        self.assertEqual(args[0][4], 'libx264')

    def test_cleanup(self):
        """Test cleanup method."""
        # Create a temp directory
        self.downloader.temp_dir = tempfile.mkdtemp(prefix="test_cleanup_")
        self.assertTrue(os.path.exists(self.downloader.temp_dir))
        
        # Call cleanup
        self.downloader.cleanup()
        
        # Verify the directory is gone
        self.assertFalse(os.path.exists(self.downloader.temp_dir))
        self.assertIsNone(self.downloader.temp_dir)
        
    @patch('gallery_dl.config.set')
    def test_private_content_handling(self, mock_config_set):
        """Test handling of private content."""
        # Create a mock exception for private content
        private_exception = Exception("400 Bad Request for 'https://www.instagram.com/api/v1/media/12345/info/'")
        
        # Use our MockDownloadJob class with an exception
        with patch('gallery_dl.job.DownloadJob', return_value=MockDownloadJob(exception=private_exception)):
            # Set up the downloader
            self.downloader.temp_dir = self.test_dir
            self.downloader.content_type = 'post'
            
            # Call the method
            metadata = self.downloader.download_content('https://www.instagram.com/p/PRIVATE/')
        
        # Verify the results for private content
        self.assertEqual(metadata['content_type'], 'post')
        self.assertTrue(metadata['is_private'])
        self.assertEqual(metadata['original_url'], 'https://www.instagram.com/p/PRIVATE/')
        self.assertEqual(metadata['cleaned_url'], 'https://www.instagram.com/p/PRIVATE')
        self.assertIn('error', metadata)
        self.assertEqual(len(metadata['media_files']), 0)
        
    @patch('gallery_dl.config.set')
    def test_empty_posts_private_content(self, mock_config_set):
        """Test handling of private content that returns empty posts list."""
        # Use our MockDownloadJob class with empty posts list
        with patch('gallery_dl.job.DownloadJob', return_value=MockDownloadJob(posts_data=[])):
            # Set up the downloader
            self.downloader.temp_dir = self.test_dir
            self.downloader.content_type = 'post'
            
            # Call the method
            metadata = self.downloader.download_content('https://www.instagram.com/p/PRIVATE/')
        
        # Verify the results for private content
        self.assertEqual(metadata['content_type'], 'post')
        self.assertTrue(metadata['is_private'])
        self.assertEqual(metadata['original_url'], 'https://www.instagram.com/p/PRIVATE/')
        self.assertEqual(metadata['cleaned_url'], 'https://www.instagram.com/p/PRIVATE')
        self.assertIn('error', metadata)
        self.assertEqual(len(metadata['media_files']), 0)


if __name__ == '__main__':
    unittest.main()
