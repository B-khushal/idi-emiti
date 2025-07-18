"""
Audio Transcription Utility using OpenAI's Whisper

This module provides functions to transcribe audio files using the Whisper library
with support for multiple languages and audio formats.
"""

import os
import logging
from typing import Optional, Dict, Any
import whisper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported language codes mapping
LANGUAGE_CODES = {
    "telugu": "te",
    "hindi": "hi", 
    "tamil": "ta",
    "kannada": "kn",
    "bengali": "bn",
    "malayalam": "ml",
    "marathi": "mr",
    "gujarati": "gu",
    "punjabi": "pa",
    "odia": "or",
    "assamese": "as",
    "english": "en",
    "auto": None  # For automatic language detection
}

def transcribe_audio(audio_path: str, language: str = "te", model_size: str = "base") -> str:
    """
    Transcribe an audio file into text using Whisper.
    
    Args:
        audio_path (str): Path to the input audio file.
        language (str): Language code (e.g., 'te' for Telugu, 'hi' for Hindi).
                       Use 'auto' for automatic language detection.
        model_size (str): Whisper model size ('tiny', 'base', 'small', 'medium', 'large').
                         Default is 'base' for balance of speed and accuracy.
    
    Returns:
        str: Transcribed text.
    
    Raises:
        FileNotFoundError: If the audio file doesn't exist.
        ValueError: If the language code is not supported.
        Exception: For other transcription errors.
    
    Example:
        >>> text = transcribe_audio("recording.wav", language="te")
        >>> print(text)
        "ఈ వస్తువు ఏమిటి?"
    """
    
    # Validate input parameters
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Normalize language code
    language = language.lower()
    if language in LANGUAGE_CODES:
        language_code = LANGUAGE_CODES[language]
    elif language in LANGUAGE_CODES.values():
        language_code = language
    else:
        raise ValueError(f"Unsupported language: {language}. Supported languages: {list(LANGUAGE_CODES.keys())}")
    
    # Validate model size
    valid_models = ['tiny', 'base', 'small', 'medium', 'large']
    if model_size not in valid_models:
        raise ValueError(f"Invalid model size: {model_size}. Valid options: {valid_models}")
    
    try:
        logger.info(f"Loading Whisper model: {model_size}")
        model = whisper.load_model(model_size)
        
        logger.info(f"Transcribing audio file: {audio_path}")
        logger.info(f"Language: {language_code if language_code else 'auto-detect'}")
        
        # Transcribe the audio
        result = model.transcribe(
            audio_path,
            language=language_code,
            task="transcribe"
        )
        
        transcribed_text = result["text"].strip()
        
        logger.info(f"Transcription completed successfully. Text length: {len(transcribed_text)} characters")
        
        return transcribed_text
        
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise Exception(f"Transcription failed: {str(e)}")

def transcribe_audio_with_metadata(audio_path: str, language: str = "te", model_size: str = "base") -> Dict[str, Any]:
    """
    Transcribe an audio file and return detailed metadata along with the text.
    
    Args:
        audio_path (str): Path to the input audio file.
        language (str): Language code (e.g., 'te' for Telugu, 'hi' for Hindi).
        model_size (str): Whisper model size.
    
    Returns:
        Dict[str, Any]: Dictionary containing transcription text and metadata.
    
    Example:
        >>> result = transcribe_audio_with_metadata("recording.wav", language="te")
        >>> print(result['text'])
        >>> print(result['language'])
        >>> print(result['segments'])
    """
    
    # Validate input parameters
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Normalize language code
    language = language.lower()
    if language in LANGUAGE_CODES:
        language_code = LANGUAGE_CODES[language]
    elif language in LANGUAGE_CODES.values():
        language_code = language
    else:
        raise ValueError(f"Unsupported language: {language}")
    
    try:
        logger.info(f"Loading Whisper model: {model_size}")
        model = whisper.load_model(model_size)
        
        logger.info(f"Transcribing audio file with metadata: {audio_path}")
        
        # Transcribe with detailed output
        result = model.transcribe(
            audio_path,
            language=language_code,
            task="transcribe",
            verbose=True
        )
        
        # Extract file information
        file_info = {
            "filename": os.path.basename(audio_path),
            "file_size": os.path.getsize(audio_path),
            "file_path": audio_path
        }
        
        # Prepare response
        response = {
            "text": result["text"].strip(),
            "language": result.get("language", language_code),
            "segments": result.get("segments", []),
            "file_info": file_info,
            "model_used": model_size,
            "transcription_time": result.get("transcription_time", 0)
        }
        
        logger.info(f"Transcription with metadata completed successfully")
        
        return response
        
    except Exception as e:
        logger.error(f"Error during transcription with metadata: {str(e)}")
        raise Exception(f"Transcription with metadata failed: {str(e)}")

def get_supported_languages() -> Dict[str, str]:
    """
    Get a dictionary of supported languages and their codes.
    
    Returns:
        Dict[str, str]: Dictionary mapping language names to their codes.
    """
    return LANGUAGE_CODES.copy()

def validate_audio_file(audio_path: str) -> bool:
    """
    Validate if the audio file exists and is accessible.
    
    Args:
        audio_path (str): Path to the audio file.
    
    Returns:
        bool: True if file is valid, False otherwise.
    """
    if not os.path.exists(audio_path):
        logger.error(f"Audio file not found: {audio_path}")
        return False
    
    if not os.path.isfile(audio_path):
        logger.error(f"Path is not a file: {audio_path}")
        return False
    
    # Check if file is readable
    try:
        with open(audio_path, 'rb') as f:
            f.read(1024)  # Read first 1KB to test access
        return True
    except Exception as e:
        logger.error(f"Cannot read audio file: {audio_path}, Error: {str(e)}")
        return False

def get_audio_duration(audio_path: str) -> Optional[float]:
    """
    Get the duration of an audio file in seconds.
    
    Args:
        audio_path (str): Path to the audio file.
    
    Returns:
        Optional[float]: Duration in seconds, or None if error.
    """
    try:
        import librosa
        duration = librosa.get_duration(path=audio_path)
        return duration
    except ImportError:
        logger.warning("librosa not installed. Cannot get audio duration.")
        return None
    except Exception as e:
        logger.error(f"Error getting audio duration: {str(e)}")
        return None

# Example usage and testing
if __name__ == "__main__":
    # Example usage
    try:
        # Test with a sample audio file (replace with actual path)
        audio_file = "sample_audio.wav"
        
        if os.path.exists(audio_file):
            # Basic transcription
            text = transcribe_audio(audio_file, language="te")
            print(f"Transcribed text: {text}")
            
            # Transcription with metadata
            result = transcribe_audio_with_metadata(audio_file, language="te")
            print(f"Full result: {result}")
        else:
            print(f"Sample audio file not found: {audio_file}")
            print("Please provide a valid audio file path for testing.")
            
    except Exception as e:
        print(f"Error: {str(e)}") 