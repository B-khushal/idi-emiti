import streamlit as st
import streamlit.components.v1 as components

def audio_recorder_component(key="default", reset_trigger=None):
    """Audio recorder component using HTML/JS"""
    
    # Create a unique reset key for this instance
    reset_key = f"reset_{key}_{reset_trigger if reset_trigger else 'default'}"
    
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
                min-height: 280px;
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
        </style>
    </head>
    <body>
        <div class="audio-recorder">
            <h4 class="recorder-title">🎙️ Record Audio Directly</h4>
            <p class="recorder-instruction">Click the button below to record audio using your microphone:</p>
            
            <div class="button-container">
                <button id="recordBtn{key}" class="recorder-button">🎙️ Start Recording</button>
                <button id="stopBtn{key}" class="recorder-button stop-button" style="display: none;">⏹️ Stop Recording</button>
                <button id="playBtn{key}" class="recorder-button play-button" style="display: none;">▶️ Play Recording</button>
                <button id="resetBtn{key}" class="recorder-button reset-button" style="display: none;">🔄 Reset Recording</button>
            </div>
            
            <div id="status{key}" class="status"></div>
            <audio id="audioPlayer{key}" class="audio-player" controls style="display: none;"></audio>
        </div>

        <script>
            let mediaRecorder{key};
            let audioChunks{key} = [];
            let audioBlob{key};
            let stream{key};
            let isRecording{key} = false;

            const recordBtn = document.getElementById('recordBtn{key}');
            const stopBtn = document.getElementById('stopBtn{key}');
            const playBtn = document.getElementById('playBtn{key}');
            const resetBtn = document.getElementById('resetBtn{key}');
            const status = document.getElementById('status{key}');
            const audioPlayer = document.getElementById('audioPlayer{key}');

            // Function to reset the recorder
            function resetRecorder{key}() {{
                // Stop any ongoing recording
                if (mediaRecorder{key} && mediaRecorder{key}.state !== 'inactive') {{
                    mediaRecorder{key}.stop();
                }}
                
                // Stop any active stream
                if (stream{key}) {{
                    stream{key}.getTracks().forEach(track => track.stop());
                }}
                
                // Reset variables
                audioChunks{key} = [];
                audioBlob{key} = null;
                isRecording{key} = false;
                
                // Reset UI
                recordBtn.style.display = 'inline-block';
                stopBtn.style.display = 'none';
                playBtn.style.display = 'none';
                resetBtn.style.display = 'none';
                audioPlayer.style.display = 'none';
                status.textContent = '';
                
                // Clear sessionStorage
                sessionStorage.removeItem('recordedAudio{key}');
                
                console.log('Audio recorder reset for key: {key}');
            }}

            // Listen for reset messages from parent
            window.addEventListener('message', function(event) {{
                if (event.data.type === 'reset_audio_recorder' && event.data.key === '{key}') {{
                    resetRecorder{key}();
                }}
            }});

            recordBtn.addEventListener('click', async () => {{
                try {{
                    stream{key} = await navigator.mediaDevices.getUserMedia({{ 
                        audio: {{
                            echoCancellation: true,
                            noiseSuppression: true,
                            sampleRate: 44100
                        }}
                    }});
                    
                    mediaRecorder{key} = new MediaRecorder(stream{key});
                    audioChunks{key} = [];
                    isRecording{key} = true;
                    
                    mediaRecorder{key}.ondataavailable = (event) => {{
                        audioChunks{key}.push(event.data);
                    }};
                    
                    mediaRecorder{key}.onstop = () => {{
                        audioBlob{key} = new Blob(audioChunks{key}, {{ type: 'audio/wav' }});
                        const audioUrl = URL.createObjectURL(audioBlob{key});
                        audioPlayer.src = audioUrl;
                        audioPlayer.style.display = 'block';
                        playBtn.style.display = 'inline-block';
                        resetBtn.style.display = 'inline-block';
                        
                        // Store in sessionStorage
                        const reader = new FileReader();
                        reader.onload = function() {{
                            sessionStorage.setItem('recordedAudio{key}', reader.result);
                            console.log('Audio saved to sessionStorage for key: {key}');
                        }};
                        reader.readAsDataURL(audioBlob{key});
                        
                        // Stop all tracks
                        stream{key}.getTracks().forEach(track => track.stop());
                        isRecording{key} = false;
                    }};
                    
                    mediaRecorder{key}.start();
                    recordBtn.style.display = 'none';
                    stopBtn.style.display = 'inline-block';
                    status.textContent = '🔴 Recording...';
                    status.style.color = '#ff6b6b';
                    
                }} catch (error) {{
                    console.error('Error accessing microphone:', error);
                    status.textContent = '❌ Error: ' + error.message;
                    status.style.color = '#dc3545';
                    isRecording{key} = false;
                }}
            }});
            
            stopBtn.addEventListener('click', () => {{
                if (mediaRecorder{key} && mediaRecorder{key}.state !== 'inactive') {{
                    mediaRecorder{key}.stop();
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
                resetRecorder{key}();
                status.textContent = '🔄 Recording reset!';
                status.style.color = '#ffc107';
            }});
            
            // Cleanup on page unload
            window.addEventListener('beforeunload', () => {{
                if (stream{key}) {{
                    stream{key}.getTracks().forEach(track => track.stop());
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=350)

def get_recorded_audio(key="default"):
    """Get recorded audio from sessionStorage"""
    # This would need to be implemented with a callback mechanism
    # For now, we'll use a simple approach
    return None

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
                    key: '{key}'
                }}, '*');
            }} catch (e) {{
                console.log('Could not send reset message to iframe');
            }}
        }});
        
        // Also clear sessionStorage directly
        sessionStorage.removeItem('recordedAudio{key}');
        console.log('Audio recorder reset triggered for key: {key}');
    </script>
    """
    return reset_script 