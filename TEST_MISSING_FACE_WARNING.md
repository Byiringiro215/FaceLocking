# Testing Missing Face Warning (LOST State)

## How to Test

Run the face tracking module:
```powershell
python -m src.face_tracking --target "BYIRINGIRO.E" --camera 2
```

## Expected Behavior

### Phase 1: SEARCHING → LOCKED (5-10 seconds)
1. **Initial State**: "SEARCHING" message appears
2. **Position your face** in front of the camera
3. Expected output: Face detected, tracking locks on
4. **Visual**: GREEN BOX around face with "BYIRINGIRO.E | LOCKED"

### Phase 2: LOCKED State (Stable)
- Face is being tracked
- Expression info displayed on screen:
  - ✅ EAR value (green if > 0.21, red if < 0.21)
  - ✅ Eye state (EYES OPEN / CLOSING / CLOSED)
  - ✅ Smile score and status (SMILING / NEUTRAL)
  - ✅ Blink counter incrementing when you blink
- Status panel on right shows all tracking parameters

### Phase 3: Test LOST State (Orange Warning)
1. **Still visible but moving away**: Face becomes partially visible
2. **Expected**: "UNCERTAIN" message with ORANGE BOX
   - Orange frame border around video
   - Counter shows uncertain frames (e.g., "UNCERTAIN (1/5)")
   - Can last up to 5 frames with continuous position overlap

### Phase 4: Test LOST State (Red Warning)
1. **Move camera away completely** - turn away, look down, or move out of frame
2. **Expected immediate change**:
   - Large RED BOX with "FACE MISSING - SEARCHING" message
   - Red frame border around entire video
   - Counter shows "Lost for X/24 frames"
   - Status panel shows state: "LOST"

### Phase 5: Recovery from LOST
1. **Move back into frame** - face comes back
2. **Expected behavior**:
   - Face re-detected
   - Verification happens (checks if it's the target)
   - Returns to LOCKED state if verified
   - GREEN BOX reappears

## Visual Indicators

| State | Visual | Color | Message |
|-------|--------|-------|---------|
| SEARCHING | No box | N/A | "Searching for target" |
| LOCKED | GREEN BOX | Green (0, 200, 0) | "BYIRINGIRO.E \| LOCKED" |
| UNCERTAIN | ORANGE BOX | Orange (0, 165, 255) | "UNCERTAIN (X/5)" |
| LOST | RED BOX | Red (0, 0, 255) | "FACE MISSING - SEARCHING" |

## Expression Tracking Indicators

While tracking is LOCKED, watch for:

### Eye State (Color-coded)
```
EAR: 0.285 ← Value displayed in GREEN (eyes open)
EYES OPEN ← GREEN text

EAR: 0.185 ← Value displayed in RED (eyes closing)
EYES CLOSING ← ORANGE text

EAR: 0.150 ← Value displayed in RED (eyes closed)
EYES CLOSED ← RED text
```

### Blink Detection
```
BLINK DETECTED! ← MAGENTA text when you blink
Blinks: 5 ← Counter increments after each blink
```

### Smile Detection
```
Smile: 0.28 NEUTRAL ← GRAY text when neutral
Smile: 0.45 SMILING ← BLUE text when smiling
```

## Test Sequence (Full)

1. **Start tracking**: Run face_tracking command
2. **Establish lock** (5 sec): Position face center
   - Watch: GREEN BOX appears, state shows LOCKED
3. **Verify expressions** (10 sec): While locked
   - Blink 3-5 times → counter increments
   - Smile → see score increase, text turns BLUE
   - Close eyes → see EAR drop, text turns RED
4. **Test UNCERTAIN** (5 sec): Move face slowly
   - Should briefly show ORANGE BOX
   - Counter shows "UNCERTAIN (X/5)"
5. **Test LOST** (5 sec): Move completely out of frame
   - Should show RED BOX with "FACE MISSING"
   - Counter shows "Lost for X/24 frames"
6. **Recovery** (5 sec): Move face back
   - Face re-detected
   - Returns to LOCKED with GREEN BOX

## What Gets Logged

All tracking events are logged to: `data/logs/tracking_YYYYMMDDTHHMMSS_*.csv`

Each frame records:
- Timestamp
- Action Type (SESSION_START, TRACKING_SEARCHING, TRACKING_LOCKED, TRACKING_UNCERTAIN, TRACKING_LOST)
- Frame number
- Target name
- Tracking reason
- Detection confidence
- Match name and score
- Position (X, Y error)
- Expression data (smile, eye state, EAR, blink)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No face detected initially | Improve lighting, get closer to camera |
| Can't get to LOST state | Turn away slowly - face needs to disappear |
| Expression info not showing | Check that MediaPipe compatibility layer loaded |
| Red box not appearing | You may be in UNCERTAIN state - move further |
| Doesn't recover after LOST | Wait 24+ frames, then move face back in frame |

## Success Criteria

✅ Task passes if you can observe:
1. GREEN BOX when face is tracked (LOCKED)
2. ORANGE BOX when face briefly uncertain (UNCERTAIN)
3. RED BOX when face completely missing (LOST)
4. Expression data displayed (EAR, eyes, blink, smile)
5. Recovery back to LOCKED when face returns
