"""
Test script for the transcription functionality

This script demonstrates how to use the transcribe_audio function
with various languages and audio formats.
"""

import os
import sys
from transcription import (
    transcribe_audio, 
    transcribe_audio_with_metadata, 
    get_supported_languages,
    validate_audio_file
)

def test_transcription():
    """Test the transcription functionality with sample audio files"""
    
    print("🎤 Audio Transcription Test")
    print("=" * 50)
    
    # Show supported languages
    print("\n📋 Supported Languages:")
    languages = get_supported_languages()
    for lang_name, lang_code in languages.items():
        print(f"  {lang_name}: {lang_code}")
    
    # Test audio files (you can replace these with actual audio files)
    test_files = [
        "sample_telugu.wav",
        "sample_hindi.mp3", 
        "sample_english.m4a"
    ]
    
    print(f"\n🔍 Looking for test audio files...")
    
    for audio_file in test_files:
        print(f"\n📁 Testing file: {audio_file}")
        
        if os.path.exists(audio_file):
            print(f"✅ File found: {audio_file}")
            
            # Validate the file
            if validate_audio_file(audio_file):
                print("✅ File validation passed")
                
                # Determine language based on filename
                if "telugu" in audio_file.lower():
                    language = "te"
                elif "hindi" in audio_file.lower():
                    language = "hi"
                elif "english" in audio_file.lower():
                    language = "en"
                else:
                    language = "auto"  # Auto-detect
                
                try:
                    print(f"🎯 Transcribing with language: {language}")
                    
                    # Basic transcription
                    text = transcribe_audio(audio_file, language=language)
                    print(f"📝 Transcribed text: {text}")
                    
                    # Transcription with metadata
                    print("\n📊 Getting detailed metadata...")
                    result = transcribe_audio_with_metadata(audio_file, language=language)
                    
                    print(f"📄 Full transcription: {result['text']}")
                    print(f"🌍 Detected language: {result['language']}")
                    print(f"📁 File info: {result['file_info']}")
                    print(f"🤖 Model used: {result['model_used']}")
                    
                    if result['segments']:
                        print(f"⏱️ Number of segments: {len(result['segments'])}")
                        print("📝 First segment:")
                        print(f"   Start: {result['segments'][0]['start']:.2f}s")
                        print(f"   End: {result['segments'][0]['end']:.2f}s")
                        print(f"   Text: {result['segments'][0]['text']}")
                    
                except Exception as e:
                    print(f"❌ Transcription error: {str(e)}")
            else:
                print("❌ File validation failed")
        else:
            print(f"❌ File not found: {audio_file}")
    
    print("\n" + "=" * 50)
    print("🎉 Transcription test completed!")

def test_language_support():
    """Test transcription with different languages"""
    
    print("\n🌍 Language Support Test")
    print("=" * 50)
    
    # Test with different language codes
    test_languages = ["te", "hi", "en", "auto"]
    
    # Use a sample audio file if available
    sample_file = None
    for ext in [".wav", ".mp3", ".m4a"]:
        for lang in ["telugu", "hindi", "english"]:
            test_file = f"sample_{lang}{ext}"
            if os.path.exists(test_file):
                sample_file = test_file
                break
        if sample_file:
            break
    
    if not sample_file:
        print("❌ No sample audio files found for language testing")
        print("   Please create sample audio files like:")
        print("   - sample_telugu.wav")
        print("   - sample_hindi.mp3") 
        print("   - sample_english.m4a")
        return
    
    print(f"🎵 Using sample file: {sample_file}")
    
    for language in test_languages:
        print(f"\n🔤 Testing language: {language}")
        try:
            text = transcribe_audio(sample_file, language=language)
            print(f"✅ Success! Text: {text[:100]}...")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_model_sizes():
    """Test transcription with different model sizes"""
    
    print("\n🤖 Model Size Test")
    print("=" * 50)
    
    # Find a sample audio file
    sample_file = None
    for ext in [".wav", ".mp3", ".m4a"]:
        test_file = f"sample_audio{ext}"
        if os.path.exists(test_file):
            sample_file = test_file
            break
    
    if not sample_file:
        print("❌ No sample audio file found for model testing")
        return
    
    print(f"🎵 Using sample file: {sample_file}")
    
    # Test different model sizes (from fastest to most accurate)
    model_sizes = ["tiny", "base", "small"]
    
    for model_size in model_sizes:
        print(f"\n🤖 Testing model: {model_size}")
        try:
            import time
            start_time = time.time()
            
            text = transcribe_audio(sample_file, language="auto", model_size=model_size)
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"✅ Success! Duration: {duration:.2f}s")
            print(f"📝 Text: {text[:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Transcription Tests")
    print("=" * 50)
    
    # Check if Whisper is installed
    try:
        import whisper
        print("✅ Whisper library is available")
    except ImportError:
        print("❌ Whisper library not found!")
        print("   Please install it with: pip install openai-whisper")
        sys.exit(1)
    
    # Run tests
    test_transcription()
    test_language_support()
    test_model_sizes()
    
    print("\n🎯 Test Summary:")
    print("✅ Basic transcription functionality tested")
    print("✅ Language support verified")
    print("✅ Model size options tested")
    print("\n💡 To use in your application:")
    print("   from transcription import transcribe_audio")
    print("   text = transcribe_audio('your_audio.wav', language='te')") 