import streamlit as st
import streamlit.components.v1 as components
import base64
import io
from datetime import datetime

def audio_recorder_component(key="default", reset_trigger=None):
    """Audio recorder component using HTML/JS with improved compatibility"""
    
    st.markdown("#### 🎤 Audio Pronunciation (Optional)")
    st.markdown("Record yourself saying the name of this object in your local language.")
    
    # Create a unique key for this instance
    recorder_key = f"audio_recorder_{key}"
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .audio-recorder {{
                background: rgba(255, 255, 255, 0.1);
                padding: 1.5rem;
                border-radius: 10px;
                margin-bottom: 1rem;
                font-family: Arial, sans-serif;
                min-height: 200px;
                box-sizing: border-box;
            }}
            .recorder-title {{
                margin: 0 0 0.5rem 0;
                font-size: 16px;
                font-weight: bold;
            }}
            .recorder-instruction {{
                margin: 0 0 1rem 0;
                font-size: 14px;
                color: #666;
            }}
            .button-container {{
                margin-bottom: 1rem;
            }}
            .recorder-button {{
                background: #ff6b6b;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 5px;
                cursor: pointer;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
                font-size: 14px;
                display: inline-block;
            }}
            .recorder-button:hover {{
                background: #e55a5a;
            }}
            .recorder-button:disabled {{
                background: #ccc;
                cursor: not-allowed;
            }}
            .stop-button {{
                background: #6c757d;
            }}
            .play-button {{
                background: #28a745;
            }}
            .reset-button {{
                background: #ffc107;
                color: #333;
            }}
            .status {{
                margin: 1rem 0;
                font-weight: bold;
                font-size: 14px;
                min-height: 20px;
            }}
            .audio-player {{
                margin-top: 1rem;
                width: 100%;
                max-width: 100%;
            }}
            .download-link {{
                display: inline-block;
                background: #007bff;
                color: white;
                padding: 0.5rem 1rem;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 0.5rem;
            }}
            .download-link:hover {{
                background: #0056b3;
                color: white;
                text-decoration: none;
            }}
            .instructions {{
                background: rgba(255, 255, 255, 0.1);
                padding: 1rem;
                border-radius: 5px;
                margin-top: 1rem;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="audio-recorder">
            <h4 class="recorder-title">🎙️ Record Audio Directly</h4>
            <p class="recorder-instruction">Click the button below to record audio using your microphone:</p>
            
            <div class="button-container">
                <button id="recordBtn{recorder_key}" class="recorder-button">🎙️ Start Recording</button>
                <button id="stopBtn{recorder_key}" class="recorder-button stop-button" style="display: none;">⏹️ Stop Recording</button>
                <button id="playBtn{recorder_key}" class="recorder-button play-button" style="display: none;">▶️ Play Recording</button>
                <button id="resetBtn{recorder_key}" class="recorder-button reset-button" style="display: none;">🔄 Reset Recording</button>
            </div>
            
            <div id="status{recorder_key}" class="status"></div>
            <audio id="audioPlayer{recorder_key}" class="audio-player" controls style="display: none;"></audio>
            <div id="downloadContainer{recorder_key}" style="display: none;">
                <a id="downloadLink{recorder_key}" class="download-link" download="pronunciation.wav">📥 Download Audio</a>
            </div>
            
            <div class="instructions">
                <strong>Instructions:</strong><br>
                1. Click "Start Recording" and allow microphone access<br>
                2. Speak the pronunciation clearly<br>
                3. Click "Stop Recording" when done<br>
                4. Listen to your recording<br>
                5. Download the audio file<br>
                6. Upload the downloaded file using the file uploader below
            </div>
        </div>

        <script>
            let mediaRecorder{recorder_key};
            let audioChunks{recorder_key} = [];
            let audioBlob{recorder_key};
            let stream{recorder_key};
            let isRecording{recorder_key} = false;

            const recordBtn = document.getElementById('recordBtn{recorder_key}');
            const stopBtn = document.getElementById('stopBtn{recorder_key}');
            const playBtn = document.getElementById('playBtn{recorder_key}');
            const resetBtn = document.getElementById('resetBtn{recorder_key}');
            const status = document.getElementById('status{recorder_key}');
            const audioPlayer = document.getElementById('audioPlayer{recorder_key}');
            const downloadContainer = document.getElementById('downloadContainer{recorder_key}');
            const downloadLink = document.getElementById('downloadLink{recorder_key}');

            // Function to reset the recorder
            function resetRecorder{recorder_key}() {{
                // Stop any ongoing recording
                if (mediaRecorder{recorder_key} && mediaRecorder{recorder_key}.state !== 'inactive') {{
                    mediaRecorder{recorder_key}.stop();
                }}
                
                // Stop any active stream
                if (stream{recorder_key}) {{
                    stream{recorder_key}.getTracks().forEach(track => track.stop());
                }}
                
                // Reset variables
                audioChunks{recorder_key} = [];
                audioBlob{recorder_key} = null;
                isRecording{recorder_key} = false;
                
                // Reset UI
                recordBtn.style.display = 'inline-block';
                stopBtn.style.display = 'none';
                playBtn.style.display = 'none';
                resetBtn.style.display = 'none';
                audioPlayer.style.display = 'none';
                downloadContainer.style.display = 'none';
                status.textContent = '';
                
                console.log('Audio recorder reset for key: {recorder_key}');
            }}

            recordBtn.addEventListener('click', async () => {{
                try {{
                    stream{recorder_key} = await navigator.mediaDevices.getUserMedia({{ 
                        audio: {{
                            echoCancellation: true,
                            noiseSuppression: true,
                            sampleRate: 44100
                        }}
                    }});
                    
                    mediaRecorder{recorder_key} = new MediaRecorder(stream{recorder_key});
                    audioChunks{recorder_key} = [];
                    isRecording{recorder_key} = true;
                    
                    mediaRecorder{recorder_key}.ondataavailable = (event) => {{
                        audioChunks{recorder_key}.push(event.data);
                    }};
                    
                    mediaRecorder{recorder_key}.onstop = () => {{
                        audioBlob{recorder_key} = new Blob(audioChunks{recorder_key}, {{ type: 'audio/wav' }});
                        const audioUrl = URL.createObjectURL(audioBlob{recorder_key});
                        audioPlayer.src = audioUrl;
                        audioPlayer.style.display = 'block';
                        playBtn.style.display = 'inline-block';
                        resetBtn.style.display = 'inline-block';
                        downloadContainer.style.display = 'block';
                        
                        // Set up download link with timestamp
                        const timestamp = new Date().toISOString().slice(0,19).replace(/:/g, '-');
                        downloadLink.href = audioUrl;
                        downloadLink.download = 'pronunciation_{recorder_key}_' + timestamp + '.wav';
                        
                        // Stop all tracks
                        stream{recorder_key}.getTracks().forEach(track => track.stop());
                        isRecording{recorder_key} = false;
                    }};
                    
                    mediaRecorder{recorder_key}.start();
                    recordBtn.style.display = 'none';
                    stopBtn.style.display = 'inline-block';
                    status.textContent = '🔴 Recording...';
                    status.style.color = '#ff6b6b';
                    
                }} catch (error) {{
                    console.error('Error accessing microphone:', error);
                    status.textContent = '❌ Error: ' + error.message;
                    status.style.color = '#dc3545';
                    isRecording{recorder_key} = false;
                }}
            }});
            
            stopBtn.addEventListener('click', () => {{
                if (mediaRecorder{recorder_key} && mediaRecorder{recorder_key}.state !== 'inactive') {{
                    mediaRecorder{recorder_key}.stop();
                    recordBtn.style.display = 'inline-block';
                    stopBtn.style.display = 'none';
                    status.textContent = '✅ Recording saved!';
                    status.style.color = '#28a745';
                }}
            }});
            
            playBtn.addEventListener('click', () => {{
                audioPlayer.play();
            }});
            
            resetBtn.addEventListener('click', () => {{
                resetRecorder{recorder_key}();
                status.textContent = '🔄 Recording reset!';
                status.style.color = '#ffc107';
            }});
            
            // Cleanup on page unload
            window.addEventListener('beforeunload', () => {{
                if (stream{recorder_key}) {{
                    stream{recorder_key}.getTracks().forEach(track => track.stop());
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=450)
    
    # Add instructions for file upload
    st.markdown("**📁 Upload your recorded audio file:**")
    st.markdown("After recording and downloading your audio file, upload it here:")
    
    # Add a note about the workflow
    st.info("""
    **📋 Audio Recording Workflow:**
    1. 🎙️ **Record** - Use the audio recorder above to record your pronunciation
    2. 📥 **Download** - Click the download link to save the audio file
    3. 📁 **Upload** - Use the file uploader below to upload the downloaded file
    4. ✅ **Submit** - Your audio will be saved with your identification
    """)
    
    # Add a hidden text input to store the audio data (for backward compatibility)
    audio_data = st.text_input(
        "Audio Data (hidden)",
        key=f"audio_data_{key}",
        label_visibility="collapsed",
        help="Hidden field to store audio data"
    )
    
    return audio_data

def get_recorded_audio(key="default"):
    """Get recorded audio from sessionStorage via JavaScript"""
    # This will be handled by JavaScript injection
    return None

def has_recorded_audio(key="default"):
    """Check if audio has been recorded by checking session state"""
    return st.session_state.get(f"audio_recorded_{key}", False)

def clear_recorded_audio(key="default"):
    """Clear recorded audio from session state"""
    if f"audio_recorded_{key}" in st.session_state:
        del st.session_state[f"audio_recorded_{key}"]
    if f"audio_data_{key}" in st.session_state:
        del st.session_state[f"audio_data_{key}"]

def reset_audio_recorder(key="default"):
    """Reset the audio recorder by sending a message to the iframe"""
    reset_script = f"""
    <script>
        // Send reset message to audio recorder iframe
        const iframes = document.querySelectorAll('iframe');
        iframes.forEach(iframe => {{
            try {{
                iframe.contentWindow.postMessage({{
                    type: 'reset_audio_recorder',
                    key: 'audio_recorder_{key}'
                }}, '*');
            }} catch (e) {{
                console.log('Could not send reset message to iframe');
            }}
        }});
        
        // Also clear sessionStorage directly
        sessionStorage.removeItem('audio_data_{key}');
        sessionStorage.removeItem('audio_recorded_{key}');
        console.log('Audio recorder reset triggered for key: {key}');
    </script>
    """
    return reset_script

def save_recorded_audio_to_file(audio_data, filename):
    """Save recorded audio data to a file"""
    try:
        # Remove the data URL prefix to get just the base64 data
        if audio_data.startswith('data:audio/wav;base64,'):
            audio_base64 = audio_data.replace('data:audio/wav;base64,', '')
        else:
            audio_base64 = audio_data
        
        # Decode base64 to bytes
        audio_bytes = base64.b64decode(audio_base64)
        
        # Save to file
        with open(filename, 'wb') as f:
            f.write(audio_bytes)
        
        return True
    except Exception as e:
        print(f"Error saving recorded audio: {e}")
        return False 