from flask import Flask, request, render_template_string, send_file, flash, redirect, url_for
import yt_dlp
import os
import tempfile
import threading
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# HTML template for the form
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Downloader</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <h1 class="text-center mb-4">Video Downloader</h1>
                
                {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-danger" role="alert">
                                {{ message }}
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
                
                <div class="card">
                    <div class="card-body">
                        <form action="/download" method="post">
                            <div class="mb-3">
                                <label for="video_url" class="form-label">Video URL</label>
                                <input type="url" class="form-control" id="video_url" name="video_url" 
                                       placeholder="Paste your video URL here..." required>
                                <div class="form-text">Supports YouTube, Vimeo, and many other video platforms.</div>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Download Video</button>
                        </form>
                    </div>
                </div>
                
                <div class="mt-4 text-center">
                    <small class="text-muted">
                        Powered by yt-dlp | Please respect copyright and terms of service
                    </small>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/')
def index():
    """Display the main form for entering video URLs."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download_video():
    """Handle video download requests."""
    video_url = request.form.get('video_url')
    
    if not video_url:
        flash('Please provide a video URL.')
        return redirect(url_for('index'))
    
    try:
        # Create a temporary directory for downloads
        temp_dir = tempfile.mkdtemp()
        
        # Configure yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'format': 'best[ext=mp4]/best',  # Prefer mp4, fallback to best quality
            'noplaylist': True,  # Download single video only
        }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info to get the filename
            info = ydl.extract_info(video_url, download=False)
            filename = ydl.prepare_filename(info)
            
            # Download the actual file
            ydl.download([video_url])
            
            # Find the downloaded file
            downloaded_file = None
            for file in os.listdir(temp_dir):
                if os.path.isfile(os.path.join(temp_dir, file)):
                    downloaded_file = os.path.join(temp_dir, file)
                    break
            
            if downloaded_file and os.path.exists(downloaded_file):
                # Get a safe filename for download
                safe_filename = secure_filename(os.path.basename(downloaded_file))
                
                # Clean up the temp directory after a delay
                def cleanup_temp_dir():
                    time.sleep(60)  # Wait 60 seconds before cleanup
                    try:
                        import shutil
                        shutil.rmtree(temp_dir, ignore_errors=True)
                    except:
                        pass
                
                cleanup_thread = threading.Thread(target=cleanup_temp_dir)
                cleanup_thread.daemon = True
                cleanup_thread.start()
                
                # Send the file to the user
                return send_file(
                    downloaded_file,
                    as_attachment=True,
                    download_name=safe_filename
                )
            else:
                flash('Failed to download the video. Please check the URL and try again.')
                return redirect(url_for('index'))
                
    except yt_dlp.DownloadError as e:
        flash(f'Download error: {str(e)}')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))
    finally:
        # Cleanup temp directory if something went wrong
        try:
            if 'temp_dir' in locals():
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
