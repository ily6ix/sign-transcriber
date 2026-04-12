#!/usr/bin/env python
"""
MediaPipe Installation Verification Script

Run this script to verify that MediaPipe and all dependencies are properly
installed and functional for the sign-transcriber app.

Usage:
    python verify_mediapipe.py
"""

import sys
import os

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_installation():
    """Verify MediaPipe installation"""
    print_section("MediaPipe Installation Check")
    
    # Check 1: pip installed packages
    print("1️⃣  Checking installed packages...")
    try:
        import mediapipe as mp
        print(f"   ✓ MediaPipe installed")
    except ImportError:
        print("   ❌ MediaPipe not installed")
        return False
    
    # Check 2: Python import
    print("\n2️⃣  Testing Python imports...")
    try:
        import mediapipe
        print(f"   ✓ MediaPipe version: {mediapipe.__version__}")
    except ImportError as e:
        print(f"   ❌ Failed to import MediaPipe: {e}")
        return False
    
    # Check 3: Vision module
    try:
        from mediapipe.tasks.python import vision
        print(f"   ✓ Vision module available")
    except ImportError as e:
        print(f"   ❌ Vision module not available: {e}")
        return False
    
    # Check 4: Required components
    try:
        from mediapipe.tasks.python.core.base_options import BaseOptions
        from mediapipe.tasks.python.vision.core.image import Image, ImageFormat
        print(f"   ✓ All required components available")
    except ImportError as e:
        print(f"   ❌ Missing components: {e}")
        return False
    
    return True

def check_model_file():
    """Verify model file availability"""
    print_section("Model File Check")
    
    model_path = "models/hand_landmarker.task"
    
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"✓ Model file found: {model_path}")
        print(f"  Size: {size_mb:.1f} MB")
        print(f"  Status: Ready for use")
        return True
    else:
        print(f"❌ Model file not found: {model_path}")
        print(f"\nTo download the model:")
        print(f"  mkdir -p models")
        print(f"  curl -L https://storage.googleapis.com/mediapipe-assets/hand_landmarker.task \\")
        print(f"    -o models/hand_landmarker.task")
        return False

def check_hand_landmarker():
    """Test Hand Landmarker initialization"""
    print_section("Hand Landmarker Initialization")
    
    try:
        from mediapipe.tasks.python import vision
        from mediapipe.tasks.python.core.base_options import BaseOptions
        import os
        
        model_path = "models/hand_landmarker.task"
        
        if not os.path.exists(model_path):
            print(f"❌ Model file not found: {model_path}")
            return False
        
        print("Initializing HandLandmarker...")
        base_options = BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=2,
            min_hand_detection_confidence=0.3,
            min_hand_presence_confidence=0.5
        )
        hand_detector = vision.HandLandmarker.create_from_options(options)
        
        print(f"✓ HandLandmarker initialized successfully")
        print(f"  Mode: IMAGE (real-time frame processing)")
        print(f"  Max hands: 2")
        print(f"  Detection confidence: 0.3 (permissive)")
        print(f"  Presence confidence: 0.5")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize HandLandmarker:")
        print(f"  {e}")
        import traceback
        traceback.print_exc()
        return False

def check_sign_detector():
    """Test SignDetector initialization"""
    print_section("SignDetector Integration Check")
    
    try:
        from sign_detector import initialize_detector, MEDIAPIPE_AVAILABLE
        
        print(f"MediaPipe available: {MEDIAPIPE_AVAILABLE}")
        
        if not MEDIAPIPE_AVAILABLE:
            print("❌ MediaPipe not available to sign_detector")
            return False
        
        print("\nInitializing SignDetector...")
        detector = initialize_detector()
        
        if not detector or not detector.is_model_loaded:
            print("❌ SignDetector failed to load model")
            return False
        
        print(f"✓ SignDetector initialized successfully")
        print(f"  Model loaded: {detector.is_model_loaded}")
        print(f"  Hand detector ready: {detector.hand_detector is not None}")
        print(f"  Confidence threshold: {detector.confidence_threshold}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize SignDetector:")
        print(f"  {e}")
        import traceback
        traceback.print_exc()
        return False

def check_dependencies():
    """Check optional dependencies"""
    print_section("Optional Dependencies")
    
    dependencies = {
        'cv2': 'OpenCV (image processing)',
        'numpy': 'NumPy (numerical computing)',
        'PIL': 'Pillow (image handling)',
        'flask': 'Flask (web framework)',
        'sqlalchemy': 'SQLAlchemy (database ORM)',
        'flask_login': 'Flask-Login (authentication)',
    }
    
    all_available = True
    for module_name, description in dependencies.items():
        try:
            __import__(module_name)
            print(f"✓ {module_name:15} - {description}")
        except ImportError:
            print(f"❌ {module_name:15} - {description} [MISSING]")
            all_available = False
    
    return all_available

def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("  MediaPipe + Sign-Transcriber Verification")
    print("="*60)
    
    results = {
        'Installation': check_installation(),
        'Model File': check_model_file(),
        'Hand Landmarker': check_hand_landmarker(),
        'SignDetector': check_sign_detector(),
        'Dependencies': check_dependencies(),
    }
    
    # Summary
    print_section("Summary")
    
    all_passed = all(results.values())
    
    for check_name, passed in results.items():
        status = "✓" if passed else "❌"
        print(f"{status} {check_name}")
    
    print()
    
    if all_passed:
        print("✅ All checks passed! MediaPipe is fully functional.")
        print("\nYour sign-transcriber app is ready to:")
        print("  • Detect hand gestures from webcam")
        print("  • Recognize ASL signs in real-time")
        print("  • Train and save custom gestures")
        print("  • Process video frames with high accuracy")
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print("\nTroubleshooting:")
        print("  1. Make sure you're in the correct virtual environment")
        print("  2. Run: pip install -r requirements.txt")
        print("  3. If model file is missing, download it (see instructions above)")
        print("  4. Check your Python version (3.8+ required)")
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
