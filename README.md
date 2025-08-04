# yt-dlp Local Video Downloader

A simple Flask web application that provides a user-friendly interface for downloading videos using yt-dlp. This application allows users to paste video URLs and download videos directly through their web browser.

## Features

- Clean, responsive web interface using Bootstrap
- Support for YouTube, Vimeo, and many other video platforms (powered by yt-dlp)
- Direct file streaming to user's browser for download
- Error handling and user feedback
- Automatic cleanup of temporary files
- No frontend frameworks required - pure HTML with Bootstrap styling

## Requirements

- Python 3.7+
- Flask
- yt-dlp

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/rocket-todd/yt-dlp-local.git
   cd yt-dlp-local
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Paste a video URL in the form and click "Download Video"

4. The video will be processed and automatically downloaded to your browser's download folder

## How It Works

The application consists of two main routes:

- **`/` (GET)**: Displays the main form where users can paste video URLs
- **`/download` (POST)**: Handles the form submission, downloads the video using yt-dlp, and streams the file back to the user

### Technical Details

- Videos are downloaded to temporary directories that are automatically cleaned up
- The application prefers MP4 format when available, falling back to the best quality available
- Files are streamed directly to the user without being stored permanently on the server
- Error handling provides user-friendly feedback for common issues

## Supported Sites

Thanks to yt-dlp, this application supports hundreds of video sites including:

- YouTube
- Vimeo
- Dailymotion
- Twitch
- And many more...

For a complete list, see the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Configuration

The application runs on `0.0.0.0:5000` by default. You can modify the host and port in the `app.py` file:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Important**: Change the `secret_key` in production:

```python
app.secret_key = 'your-secret-key-here'  # Change this in production
```

## Security Considerations

- This application is intended for local/personal use
- Be cautious when exposing this to the internet, as it allows downloading from arbitrary URLs
- Always respect copyright laws and terms of service of video platforms
- Consider implementing authentication and rate limiting for production use

## File Structure

```
yt-dlp-local/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── LICENSE            # MIT License
└── .gitignore         # Git ignore rules
```

## Dependencies

- **Flask**: Web framework for the application
- **yt-dlp**: Video downloading library
- **Bootstrap**: CSS framework (loaded via CDN)

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and personal use only. Please respect copyright laws and the terms of service of video platforms. The developers are not responsible for any misuse of this software.
