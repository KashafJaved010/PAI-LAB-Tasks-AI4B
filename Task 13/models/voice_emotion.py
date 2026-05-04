import librosa
import numpy as np

def detect_voice_emotion(audio_path, duration=5):
    try:
        # Load audio
        y, sr = librosa.load(audio_path, duration=duration, sr=16000)
        
        # Features
        rms = np.mean(librosa.feature.rms(y=y))
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        spec_cent = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfccs)
        mfcc_std = np.std(mfccs)
        
        # Pitch estimation (optional, but good)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch = np.mean(pitches[magnitudes > np.median(magnitudes)]) if np.any(magnitudes) else 0
        
        # Heuristic-based classification
        # High energy + high pitch + high ZCR -> excited/happy
        if rms > 0.08 and pitch > 200 and zcr > 0.1:
            return "Happy", 0.85
        # Very low energy + low pitch -> tired/sad
        elif rms < 0.02 and (pitch < 100 or mfcc_mean < -30):
            return "Tired", 0.78
        # High energy + high pitch + high MFCC variance -> stressed/anxious
        elif rms > 0.07 and pitch > 180 and mfcc_std > 50:
            return "Stressed", 0.75
        # High energy + high ZCR + high spectral centroid -> angry
        elif rms > 0.09 and zcr > 0.12 and spec_cent > 2000:
            return "Angry", 0.82
        # Very low rms + low spectral centroid -> sad
        elif rms < 0.03 and spec_cent < 1000:
            return "Sad", 0.79
        # Medium rms, low pitch -> neutral or tired
        elif rms < 0.05 and pitch < 120:
            return "Neutral", 0.65
        # Else fallback
        else:
            return "Neutral", 0.60
    except Exception as e:
        print("Voice Emotion Error:", e)
        return "No Voice", 0.0