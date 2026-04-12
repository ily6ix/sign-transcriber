"""
DEBUG SNIPPET - Paste this into your /api/transcribe route to log detection pipeline
Replace the detection = sign_detector.detect_signs(frame_data) call with this code
"""

# ============================================================================
# DIAGNOSTIC DEBUG SNIPPET FOR /api/transcribe ENDPOINT
# ============================================================================
# Paste this INSIDE your api_transcribe() function, replace the existing
# sign_detector.detect_signs() call with this code block
#
# This will output detailed logs to help diagnose frame conversion and
# gesture classification issues

import json
import sys

# LOG FUNCTION - sends to both stdout and to response
debug_logs = []

def debug_log(message):
    """Add to debug log"""
    timestamp = datetime.utcnow().isoformat()
    log_entry = f"[{timestamp}] {message}"
    print(log_entry, file=sys.stderr)  # stderr for Gunicorn/deployment visibility
    print(log_entry)  # stdout for local debugging
    debug_logs.append(message)

# ============================================================================
# FRAME PIPELINE DEBUGGING
# ============================================================================

debug_log(f"=== FRAME RECEIVED ===")
debug_log(f"Frame data type: {type(frame_data)}")
debug_log(f"Frame data size: {len(frame_data) if isinstance(frame_data, bytes) else 'N/A'} bytes")

# Check if frame is valid image data (JPEG/PNG magic numbers)
if isinstance(frame_data, bytes):
    if frame_data[:2] == b'\xff\xd8':  # JPEG
        debug_log("✓ Frame is JPEG format")
    elif frame_data[:8] == b'\x89PNG\r\n\x1a\n':  # PNG
        debug_log("✓ Frame is PNG format")
    elif frame_data[:4] == b'RIFF':  # WebP or WAV
        debug_log("✓ Frame is RIFF format (WebP possible)")
    else:
        debug_log(f"⚠️  UNKNOWN frame format. Magic bytes: {frame_data[:8].hex()}")

# ============================================================================
# MEDIAPIPE DETECTOR STATE CHECK
# ============================================================================

debug_log(f"=== DETECTOR STATE ===")
debug_log(f"Detector initialized: {sign_detector.hand_detector is not None}")
debug_log(f"Model loaded flag: {sign_detector.is_model_loaded}")
debug_log(f"MediaPipe available: {sign_detector.MEDIAPIPE_AVAILABLE if hasattr(sign_detector, 'MEDIAPIPE_AVAILABLE') else 'N/A'}")
debug_log(f"Confidence threshold: {sign_detector.confidence_threshold}")

# ============================================================================
# RUN DETECTION WITH LOGGING
# ============================================================================

debug_log(f"=== RUNNING DETECTION ===")
detection = sign_detector.detect_signs(frame_data)

# ============================================================================
# DETECTION RESULTS LOGGING
# ============================================================================

debug_log(f"=== DETECTION RESULTS ===")
debug_log(f"Has hands: {detection['has_hands']}")
debug_log(f"Hands detected: {detection['hands_detected']}")
debug_log(f"Confidence: {detection['confidence']:.3f}")
debug_log(f"Detected sign: {detection['detected_sign']}")
debug_log(f"All gestures: {detection['gestures']}")

if detection['hand_positions']:
    for i, pos in enumerate(detection['hand_positions']):
        debug_log(f"  Hand {i}: {pos['label']} (confidence: {pos['confidence']:.3f})")

# ============================================================================
# HAND LANDMARKS LOGGING (first hand only, to keep output manageable)
# ============================================================================

if detection['landmarks']:
    first_hand = detection['landmarks'][0]
    debug_log(f"First hand has {len(first_hand)} landmarks")
    
    # Log only critical landmarks (palm, fingertips)
    if len(first_hand) >= 21:
        palm = first_hand[0]
        index_tip = first_hand[8]
        middle_tip = first_hand[12]
        ring_tip = first_hand[16]
        pinky_tip = first_hand[20]
        thumb_tip = first_hand[4]
        
        debug_log(f"Palm position: x={palm['x']:.3f}, y={palm['y']:.3f}, z={palm['z']:.3f}")
        debug_log(f"Index tip: x={index_tip['x']:.3f}, y={index_tip['y']:.3f}, z={index_tip['z']:.3f}")
        debug_log(f"Thumb extended check: tip_y={thumb_tip['y']:.3f} < (should be for extended)")

# ============================================================================
# HAND SHAPE ANALYSIS (diagnostic only)
# ============================================================================

if detection['landmarks']:
    first_landmarks = detection['landmarks'][0]
    hand_shape = sign_detector._get_hand_shape(first_landmarks)
    hand_position = sign_detector._get_hand_position(first_landmarks)
    palm_facing = sign_detector._get_palm_orientation(first_landmarks)
    
    debug_log(f"=== HAND SHAPE FEATURES ===")
    debug_log(f"Fingers up: index={hand_shape['index_up']}, middle={hand_shape['middle_up']}, "
              f"ring={hand_shape['ring_up']}, pinky={hand_shape['pinky_up']}")
    debug_log(f"Thumb extended: {hand_shape['thumb_extended']}")
    debug_log(f"Fingers spread: {hand_shape['fingers_spread']}")
    debug_log(f"Closed fist: {hand_shape['closed_fist']}")
    
    debug_log(f"=== HAND POSITION FEATURES ===")
    debug_log(f"Height: {hand_position['height']}, Side: {hand_position['side']}, Distance: {hand_position['distance']}")
    debug_log(f"Focus area: {hand_position.get('focus_area', 'N/A')}")
    debug_log(f"Palm facing: {palm_facing}")

# ============================================================================
# DEBUG INFO FROM DETECTION (if available)
# ============================================================================

if 'debug_info' in detection:
    debug_log(f"=== DEBUG INFO ===")
    for key, value in detection['debug_info'].items():
        debug_log(f"{key}: {value}")

debug_log(f"=== END DEBUG LOG ===\n")

# Return all detection data + debug logs
response_data = {
    'status': 'hand_detected' if detection['has_hands'] else 'no_hand',
    'hands_detected': detection['hands_detected'],
    'detected_sign': detection['detected_sign'],
    'gestures': detection['gestures'],
    'confidence': detection['confidence'],
    'hand_positions': detection['hand_positions'],
    'landmarks': detection['landmarks'],
    'keypoints': detection.get('hand_keypoints', []),
    'debug_logs': debug_logs  # ← Include logs in response for frontend inspection
}

# Return with debug logs
return jsonify(response_data), 200


# ============================================================================
# HOW TO USE THIS DEBUG SNIPPET
# ============================================================================
#
# 1. Find this line in your app.py api_transcribe() function:
#        detection = sign_detector.detect_signs(frame_data)
#
# 2. Replace it with the code above (starting from "debug_logs = []")
#
# 3. Run your app and send a frame to /api/transcribe via your webcam
#
# 4. Check the logs. You'll see:
#    - Frame format and size
#    - Detector state (loaded or not)
#    - Hand detection results
#    - Hand shape features (fingers, thumb, spread)
#    - Hand position (height, side, distance)
#    - Palm orientation
#
# 5. The debug_logs are also returned in the JSON response, so you can
#    view them in the browser console (if you log response.debug_logs)
#
# 6. Use these logs to answer:
#    - Is the frame arriving as valid image data?
#    - Is the detector initialized?
#    - Are hands being detected?
#    - What hand shape features are being extracted?
#    - Why is the gesture not matching?
#
# Once fixed, remove this debug code and use the normal detection path.
# ============================================================================
