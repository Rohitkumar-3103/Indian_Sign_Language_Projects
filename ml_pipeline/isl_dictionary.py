"""
Indian Sign Language (ISL) Gesture Definitions, Metadata, and Guidance.
Synthesized according to standard Indian Sign Language (ISLRTC) conventions
with full support for 200+ video demonstration clips in Images/isl_videos/.
"""

ISL_CLASSES = {
    "A": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter A",
        "description": "Left hand open palm facing right; right hand index finger touches the tip of left thumb.",
        "tips": "Touch the right index fingertip to the left thumb tip while keeping left fingers spread.",
        "video_file": "a.mp4",
        "has_video": True
    },
    "B": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter B",
        "description": "Left hand open upright; right hand index and middle finger form a loop against left palm/thumb.",
        "tips": "Both hands form two loops resembling the letter 'B'.",
        "video_file": "b.mp4",
        "has_video": True
    },
    "C": {
        "category": "alphabet",
        "hands": 1,
        "name": "Letter C",
        "description": "Curved hand forming a 'C' shape with thumb and four fingers.",
        "tips": "Single hand held sideways, fingers and thumb curved like the letter C.",
        "video_file": "c.mp4",
        "has_video": True
    },
    "D": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter D",
        "description": "Left hand index pointing up; right hand curved into 'C' touching left index to form 'D'.",
        "tips": "Left index finger is the vertical stem; right curved hand creates the curved back of D.",
        "video_file": "d.mp4",
        "has_video": True
    },
    "E": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter E",
        "description": "Left hand open palm; right hand index finger touches left index fingertip.",
        "tips": "Right index touches the tip of the left index finger (representing vowel E).",
        "video_file": "e.mp4",
        "has_video": True
    },
    "F": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter F",
        "description": "Left index and middle finger horizontal; right index and middle finger placed across them.",
        "tips": "Cross two fingers of right hand over two horizontal fingers of left hand.",
        "video_file": "f.mp4",
        "has_video": True
    },
    "G": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter G",
        "description": "Both hands form closed fists placed one on top of the other.",
        "tips": "Right fist rested directly atop left fist.",
        "video_file": "g.mp4",
        "has_video": True
    },
    "H": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter H",
        "description": "Left hand flat palm horizontal; right hand flat palm swept across left palm.",
        "tips": "Right flat palm sweeps across the horizontal left palm.",
        "video_file": "h.mp4",
        "has_video": True
    },
    "I": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter I",
        "description": "Left hand open palm facing inward; right hand index finger touches left middle fingertip.",
        "tips": "Right index touches the tip of the left middle finger (representing vowel I).",
        "video_file": "i.mp4",
        "has_video": True
    },
    "J": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter J",
        "description": "Right index traces the letter 'J' starting from left middle fingertip down and curling up.",
        "tips": "Start at left middle fingertip, trace down into left palm with a hook.",
        "video_file": "j.mp4",
        "has_video": True
    },
    "K": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter K",
        "description": "Left index pointing up; right index finger bent at knuckle hooked onto left index.",
        "tips": "Right bent index finger hooks around the vertical left index finger.",
        "video_file": "k.mp4",
        "has_video": True
    },
    "L": {
        "category": "alphabet",
        "hands": 1,
        "name": "Letter L",
        "description": "Single hand with thumb and index finger extended at right angles forming an 'L'.",
        "tips": "Hold right hand up, thumb horizontal and index pointing straight up.",
        "video_file": "l.mp4",
        "has_video": True
    },
    "M": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter M",
        "description": "Right hand places three fingers (index, middle, ring) on the flat palm of left hand.",
        "tips": "Three fingertips of right hand rest on left open palm to represent three legs of M.",
        "video_file": "m.mp4",
        "has_video": True
    },
    "N": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter N",
        "description": "Right hand places two fingers (index and middle) on the flat palm of left hand.",
        "tips": "Two fingertips of right hand rest on left open palm to represent two legs of N.",
        "video_file": "n.mp4",
        "has_video": True
    },
    "O": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter O",
        "description": "Left hand open palm; right index touches the tip of left ring finger (vowel O).",
        "tips": "Right index touches left ring fingertip (representing vowel O).",
        "video_file": "o.mp4",
        "has_video": True
    },
    "P": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter P",
        "description": "Left hand index pointing up; right hand thumb and index form a small circle at the top.",
        "tips": "Left index forms stem; right thumb-index loop attaches to top to form P.",
        "video_file": "p.mp4",
        "has_video": True
    },
    "Q": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter Q",
        "description": "Left hand thumb and index form circle 'O'; right hand index placed through bottom as the tail.",
        "tips": "Left hand circle with right index finger protruding down diagonally.",
        "video_file": "q.mp4",
        "has_video": True
    },
    "R": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter R",
        "description": "Left hand flat; right hand index finger hooked like a shepherd's crook resting on left palm.",
        "tips": "Right curved/hooked index rests gently on the open left palm.",
        "video_file": "r.mp4",
        "has_video": True
    },
    "S": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter S",
        "description": "Both pinky fingers hooked together with fists closed.",
        "tips": "Interlock both little (pinky) fingers while keeping palms facing you.",
        "video_file": "s.mp4",
        "has_video": True
    },
    "T": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter T",
        "description": "Left hand index pointing right horizontally; right hand index touches midpoint from below forming 'T'.",
        "tips": "Left index is the horizontal bar; right index is the vertical stem touching the midpoint.",
        "video_file": "t.mp4",
        "has_video": True
    },
    "U": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter U",
        "description": "Left hand open palm; right hand index touches the tip of left pinky finger (vowel U).",
        "tips": "Right index touches left pinky fingertip (representing vowel U).",
        "video_file": "u.mp4",
        "has_video": True
    },
    "V": {
        "category": "alphabet",
        "hands": 1,
        "name": "Letter V",
        "description": "Single hand index and middle fingers extended apart in a 'V' shape (peace sign).",
        "tips": "Extend index and middle fingers apart while thumb holds ring and pinky.",
        "video_file": "v.mp4",
        "has_video": True
    },
    "W": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter W",
        "description": "Fingers of both hands interlocked and pointed upwards forming a 'W' shape.",
        "tips": "Interlock all fingers of both hands pointing upwards.",
        "video_file": "w.mp4",
        "has_video": True
    },
    "X": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter X",
        "description": "Both index fingers crossed over each other to form an 'X'.",
        "tips": "Cross right index over left index at 90 degrees.",
        "video_file": "x.mp4",
        "has_video": True
    },
    "Y": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter Y",
        "description": "Left index and thumb extended in 'V'; right index rests in the junction pointing down.",
        "tips": "Right index finger points between the left extended thumb and index finger.",
        "video_file": "y.mp4",
        "has_video": True
    },
    "Z": {
        "category": "alphabet",
        "hands": 2,
        "name": "Letter Z",
        "description": "Left hand held flat horizontally; right hand held vertical with fingertips touching to form angle of Z.",
        "tips": "Right fingertips touch left palm or right index traces 'Z' in the air.",
        "video_file": "z.mp4",
        "has_video": True
    },
    "0": {
        "category": "number",
        "hands": 1,
        "name": "Digit 0",
        "description": "Fingers curled touching thumb forming an oval '0'.",
        "tips": "Curl all fingers so fingertips meet thumb tip in a zero shape.",
        "video_file": "0.mp4",
        "has_video": True
    },
    "1": {
        "category": "number",
        "hands": 1,
        "name": "Digit 1",
        "description": "Single index finger extended upright, other fingers curled.",
        "tips": "Point index finger straight up.",
        "video_file": "1.mp4",
        "has_video": True
    },
    "2": {
        "category": "number",
        "hands": 1,
        "name": "Digit 2",
        "description": "Index and middle fingers extended upright together or slightly spread.",
        "tips": "Raise index and middle fingers.",
        "video_file": "2.mp4",
        "has_video": True
    },
    "3": {
        "category": "number",
        "hands": 1,
        "name": "Digit 3",
        "description": "Index, middle, and ring fingers extended upright.",
        "tips": "Raise index, middle, and ring fingers.",
        "video_file": "3.mp4",
        "has_video": True
    },
    "4": {
        "category": "number",
        "hands": 1,
        "name": "Digit 4",
        "description": "Four fingers (index, middle, ring, pinky) extended, thumb folded across palm.",
        "tips": "Four fingers held up, thumb tucked inward.",
        "video_file": "4.mp4",
        "has_video": True
    },
    "5": {
        "category": "number",
        "hands": 1,
        "name": "Digit 5",
        "description": "All five fingers fully spread and extended open.",
        "tips": "Open hand with all five fingers spread apart.",
        "video_file": "5.mp4",
        "has_video": True
    },
    "6": {
        "category": "number",
        "hands": 2,
        "name": "Digit 6",
        "description": "Left hand open with 5 fingers; right hand extends 1 index finger (5 + 1 = 6).",
        "tips": "Left hand shows 5, right hand shows 1 beside it.",
        "video_file": "6.mp4",
        "has_video": True
    },
    "7": {
        "category": "number",
        "hands": 2,
        "name": "Digit 7",
        "description": "Left hand open with 5 fingers; right hand extends 2 fingers (5 + 2 = 7).",
        "tips": "Left hand shows 5, right hand shows 2.",
        "video_file": "7.mp4",
        "has_video": True
    },
    "8": {
        "category": "number",
        "hands": 2,
        "name": "Digit 8",
        "description": "Left hand open with 5 fingers; right hand extends 3 fingers (5 + 3 = 8).",
        "tips": "Left hand shows 5, right hand shows 3.",
        "has_video": False
    },
    "9": {
        "category": "number",
        "hands": 2,
        "name": "Digit 9",
        "description": "Left hand open with 5 fingers; right hand extends 4 fingers (5 + 4 = 9).",
        "tips": "Left hand shows 5, right hand shows 4.",
        "video_file": "9.mp4",
        "has_video": True
    },
    "ACHE": {
        "category": "word",
        "hands": 1,
        "name": "Ache / Hurt",
        "description": "Index fingers pointing towards the affected area with twisted movement.",
        "tips": "Point and twist index finger indicating localized pain.",
        "video_file": "ache.mp4",
        "has_video": True
    },
    "AFRAID": {
        "category": "word",
        "hands": 2,
        "name": "Afraid / Scared",
        "description": "Both open hands held in front of chest, palms in, trembling slightly.",
        "tips": "Hands draw inward toward the chest with an expression of fear.",
        "video_file": "afraid.mp4",
        "has_video": True
    },
    "AFTER": {
        "category": "word",
        "hands": 2,
        "name": "After / Later",
        "description": "One flat hand slides forward past the other stationary flat hand.",
        "tips": "Dominant hand moves forward across the non-dominant hand.",
        "video_file": "after.mp4",
        "has_video": True
    },
    "AGAIN": {
        "category": "word",
        "hands": 2,
        "name": "Again / Repeat",
        "description": "Dominant bent hand arches over and taps onto the palm of non-dominant flat hand.",
        "tips": "Bend fingers at right angle and arc into the open palm.",
        "video_file": "again.mp4",
        "has_video": True
    },
    "AGE": {
        "category": "word",
        "hands": 1,
        "name": "Age / Old",
        "description": "Hand clasps chin and moves downward as if tugging on a beard.",
        "tips": "Gently stroke downward from chin with cupped hand.",
        "video_file": "age.mp4",
        "has_video": True
    },
    "AGREE": {
        "category": "word",
        "hands": 2,
        "name": "Agree / Concur",
        "description": "Both index fingers start near temple/chest and move forward together in affirmation.",
        "tips": "Both hands move forward simultaneously and nod together.",
        "video_file": "agree.mp4",
        "has_video": True
    },
    "ALL": {
        "category": "word",
        "hands": 2,
        "name": "All / Whole",
        "description": "Both flat palms sweep outward in a full horizontal circle meeting together.",
        "tips": "Enclose an imaginary circle with both hands.",
        "video_file": "all.mp4",
        "has_video": True
    },
    "ALWAYS": {
        "category": "word",
        "hands": 1,
        "name": "Always / Forever",
        "description": "Index finger extended upright tracing continuous small circular motion in the air.",
        "tips": "Rotate index finger in a steady circular loop.",
        "video_file": "always.mp4",
        "has_video": True
    },
    "ANGRY": {
        "category": "word",
        "hands": 1,
        "name": "Angry / Mad",
        "description": "Curved claw hand held in front of face pulling slightly outward with tension.",
        "tips": "Form a claw shape with fingers tense in front of face.",
        "video_file": "angry.mp4",
        "has_video": True
    },
    "ANSWER": {
        "category": "word",
        "hands": 2,
        "name": "Answer / Reply",
        "description": "Index fingers at lips move forward and point outward toward the person.",
        "tips": "Start with index near mouth and direct it towards the listener.",
        "video_file": "answer.mp4",
        "has_video": True
    },
    "ASK": {
        "category": "word",
        "hands": 1,
        "name": "Ask / Inquire",
        "description": "Index finger bent like a hook moving from body outward toward the listener.",
        "tips": "Curl index finger forward in a questioning gesture.",
        "video_file": "ask.mp4",
        "has_video": True
    },
    "BAD": {
        "category": "word",
        "hands": 1,
        "name": "Bad",
        "description": "Flat hand placed at chin and swept abruptly downward turning palm face down.",
        "tips": "Touch chin with flat hand and twist palm down abruptly.",
        "video_file": "bad.mp4",
        "has_video": True
    },
    "BE_BRAVE": {
        "category": "word",
        "hands": 2,
        "name": "Be Brave",
        "description": "Fists held at chest moving firmly outward with strength and courage.",
        "tips": "Thrust closed fists forward from chest resolutely.",
        "video_file": "be_brave.mp4",
        "has_video": True
    },
    "BE_BRAVE_ENOUGH": {
        "category": "word",
        "hands": 2,
        "name": "Be Brave Enough",
        "description": "Both hands form firm fists at chest with determined forward posture.",
        "tips": "Solid chest posture with forward chin lift.",
        "video_file": "be_brave_enough.mp4",
        "has_video": True
    },
    "BEFORE": {
        "category": "word",
        "hands": 2,
        "name": "Before / Prior",
        "description": "Dominant hand moves backward over the shoulder or back over stationary hand.",
        "tips": "Pull hand backward indicating earlier in time.",
        "video_file": "before.mp4",
        "has_video": True
    },
    "BEHAVIOUR": {
        "category": "word",
        "hands": 2,
        "name": "Behaviour / Conduct",
        "description": "Both 'B' hands move alternately side to side in front of the chest.",
        "tips": "Wave flat hands in gentle alternating horizontal sweeps.",
        "video_file": "behaviour.mp4",
        "has_video": True
    },
    "BEST": {
        "category": "word",
        "hands": 1,
        "name": "Best",
        "description": "Thumbs-up hand moved from chin diagonally upwards into the air.",
        "tips": "Start thumbs-up near mouth and elevate it high with pride.",
        "video_file": "best.mp4",
        "has_video": True
    },
    "BRAVE": {
        "category": "word",
        "hands": 2,
        "name": "Brave / Courage",
        "description": "Both open hands at shoulders pull into strong clenched fists.",
        "tips": "Grasp air into strong fists pulled down near torso.",
        "video_file": "brave.mp4",
        "has_video": True
    },
    "BREAK": {
        "category": "word",
        "hands": 2,
        "name": "Break / Snap",
        "description": "Both hands hold an imaginary stick and snap it downward simultaneously.",
        "tips": "Twist both fists downward as if snapping a twig.",
        "video_file": "break.mp4",
        "has_video": True
    },
    "BYE": {
        "category": "word",
        "hands": 1,
        "name": "Bye / Goodbye",
        "description": "Open hand held up waving fingers back and forth smoothly.",
        "tips": "Standard friendly hand wave with fingers moving together.",
        "video_file": "bye.mp4",
        "has_video": True
    },
    "CALL": {
        "category": "word",
        "hands": 1,
        "name": "Call / Phone",
        "description": "Hand in 'Y' shape (thumb and pinky extended) held to the ear like a phone.",
        "tips": "Thumb at ear and pinky near mouth mimicking telephone handset.",
        "video_file": "call.mp4",
        "has_video": True
    },
    "CALM": {
        "category": "word",
        "hands": 2,
        "name": "Calm / Peaceful",
        "description": "Both flat hands start at chest level and press gently downward together.",
        "tips": "Lower both open palms smoothly to convey calmness.",
        "video_file": "calm.mp4",
        "has_video": True
    },
    "CAREFUL": {
        "category": "word",
        "hands": 2,
        "name": "Careful / Cautious",
        "description": "Two 'V' hands placed one on top of the other, tapping twice.",
        "tips": "Rest dominant V-fingers on top of non-dominant V-fingers.",
        "video_file": "careful.mp4",
        "has_video": True
    },
    "CHAT": {
        "category": "word",
        "hands": 2,
        "name": "Chat / Conversation",
        "description": "Both hands open and close in an alternating talking beak motion.",
        "tips": "Alternate opening and pinching fingertips of both hands.",
        "video_file": "chat.mp4",
        "has_video": True
    },
    "CHOCOLATE": {
        "category": "word",
        "hands": 2,
        "name": "Chocolate",
        "description": "'C' hand circles gently on the back of the non-dominant closed fist.",
        "tips": "Rub 'C' shape over the back of the opposite hand.",
        "video_file": "chocolate.mp4",
        "has_video": True
    },
    "COLLEGE": {
        "category": "word",
        "hands": 2,
        "name": "College / University",
        "description": "Flat dominant hand slides off flat non-dominant hand and arches upward.",
        "tips": "Slide dominant palm across opposite palm and sweep up in an arc.",
        "video_file": "college.mp4",
        "has_video": True
    },
    "COME": {
        "category": "word",
        "hands": 2,
        "name": "Come / Approach",
        "description": "Both index fingers curled inward beckoning toward the body.",
        "tips": "Beckon with both index fingers pulling toward yourself.",
        "video_file": "come.mp4",
        "has_video": True
    },
    "COMPREHEND": {
        "category": "word",
        "hands": 1,
        "name": "Comprehend / Understand",
        "description": "Flick index finger upward from closed fist next to the forehead.",
        "tips": "Flick index up near temple like a lightbulb turning on.",
        "video_file": "comprehend.mp4",
        "has_video": True
    },
    "COMPUTER": {
        "category": "word",
        "hands": 2,
        "name": "Computer",
        "description": "Fingers of both hands wiggle rhythmically as if typing on a keyboard.",
        "tips": "Mimic fluid two-handed keyboard typing motion.",
        "video_file": "computer.mp4",
        "has_video": True
    },
    "CONCUR": {
        "category": "word",
        "hands": 2,
        "name": "Concur / Agree",
        "description": "Both index fingers come forward and meet in parallel alignment.",
        "tips": "Bring both index fingers parallel and move down together in agreement.",
        "video_file": "concur.mp4",
        "has_video": True
    },
    "CONDUCT": {
        "category": "word",
        "hands": 2,
        "name": "Conduct / Manners",
        "description": "Both flat hands sweep side to side alternately in front of torso.",
        "tips": "Gentle alternating side-to-side sweeping motion.",
        "video_file": "conduct.mp4",
        "has_video": True
    },
    "CONFUSED": {
        "category": "word",
        "hands": 2,
        "name": "Confused / Puzzled",
        "description": "Both claw hands rotate in opposing circles near the temples.",
        "tips": "Circle clawed hands near sides of forehead.",
        "video_file": "confused.mp4",
        "has_video": True
    },
    "CONGRATULATIONS": {
        "category": "word",
        "hands": 2,
        "name": "Congratulations",
        "description": "Both hands clasp together and shake, or clap in sign language ovation.",
        "tips": "Clasp own hands together shaking joyfully near shoulder.",
        "video_file": "congratulations.mp4",
        "has_video": True
    },
    "CONSENT": {
        "category": "word",
        "hands": 2,
        "name": "Consent / Permission",
        "description": "Both open palms start at chest facing up and rise forward together.",
        "tips": "Lift both cupped palms gently upward in approval.",
        "video_file": "consent.mp4",
        "has_video": True
    },
    "CRY": {
        "category": "word",
        "hands": 2,
        "name": "Cry / Weep",
        "description": "Both index fingers trace teardrop paths downward from eyes across cheeks.",
        "tips": "Trace lines down cheeks with index fingers repeatedly.",
        "video_file": "cry.mp4",
        "has_video": True
    },
    "DISAGREE": {
        "category": "word",
        "hands": 2,
        "name": "Disagree / Oppose",
        "description": "Index fingers touch temple then pull apart sharply with a head shake.",
        "tips": "Touch forehead and pull both hands apart in opposite directions.",
        "video_file": "disagree.mp4",
        "has_video": True
    },
    "DISSENT": {
        "category": "word",
        "hands": 2,
        "name": "Dissent / Disapproval",
        "description": "Hands cross at wrists and push outward in refusal.",
        "tips": "Cross forearms and swing outward dismissing.",
        "video_file": "dissent.mp4",
        "has_video": True
    },
    "DO": {
        "category": "word",
        "hands": 2,
        "name": "Do / Action",
        "description": "Both 'C' or pinch hands move side to side rhythmically together.",
        "tips": "Move both hands side to side synchronously in front of waist.",
        "video_file": "do.mp4",
        "has_video": True
    },
    "DRINK": {
        "category": "word",
        "hands": 1,
        "name": "Drink / Beverage",
        "description": "Hand forms 'C' cup shape and tilts toward mouth as if drinking.",
        "tips": "Mimic tipping a cup up to lips.",
        "video_file": "drink.mp4",
        "has_video": True
    },
    "EARLY": {
        "category": "word",
        "hands": 2,
        "name": "Early",
        "description": "Middle finger of dominant hand flicks forward over non-dominant fist.",
        "tips": "Flick middle finger across the back of opposite wrist.",
        "video_file": "early.mp4",
        "has_video": True
    },
    "EAT": {
        "category": "word",
        "hands": 1,
        "name": "Eat / Food",
        "description": "Fingertips brought together into a bunched shape tapping at mouth.",
        "tips": "Tap bunched fingers gently at lips twice.",
        "video_file": "eat.mp4",
        "has_video": True
    },
    "EVERY_TIME": {
        "category": "word",
        "hands": 2,
        "name": "Every Time / Always",
        "description": "Index finger repeatedly taps non-dominant index in regular intervals.",
        "tips": "Tap index finger repeatedly moving forward.",
        "video_file": "every_time.mp4",
        "has_video": True
    },
    "EXCUSE_ME": {
        "category": "word",
        "hands": 2,
        "name": "Excuse Me / Pardon",
        "description": "Fingertips of dominant hand slide across non-dominant palm twice.",
        "tips": "Brush dominant fingertips across flat palm toward yourself.",
        "video_file": "excuse_me.mp4",
        "has_video": True
    },
    "EXHAUSTED": {
        "category": "word",
        "hands": 2,
        "name": "Exhausted / Depleted",
        "description": "Curved hands at chest drop downward limp and heavy with shoulders slumping.",
        "tips": "Drop hands down from chest with tired posture.",
        "video_file": "exhausted.mp4",
        "has_video": True
    },
    "EXPLAIN": {
        "category": "word",
        "hands": 2,
        "name": "Explain / Describe",
        "description": "Both 'F' hands move alternately forward and back smoothly.",
        "tips": "Pinch thumb and index on both hands, slide back and forth alternately.",
        "video_file": "explain.mp4",
        "has_video": True
    },
    "FATHER": {
        "category": "word",
        "hands": 1,
        "name": "Father / Dad",
        "description": "Thumb of open hand rests on forehead or temple, fingers spread.",
        "tips": "Tap thumb against center of forehead with open palm.",
        "video_file": "father.mp4",
        "has_video": True
    },
    "FATIGUED": {
        "category": "word",
        "hands": 2,
        "name": "Fatigued / Worn Out",
        "description": "Hands bent at chest sag downward limply.",
        "tips": "Let hands and shoulders drop together.",
        "video_file": "fatigued.mp4",
        "has_video": True
    },
    "FEAR": {
        "category": "word",
        "hands": 2,
        "name": "Fear / Fright",
        "description": "Both hands shake slightly pulling in front of chest.",
        "tips": "Pull trembling hands toward chest defensively.",
        "video_file": "fear.mp4",
        "has_video": True
    },
    "FINE": {
        "category": "word",
        "hands": 1,
        "name": "Fine / Alright",
        "description": "Thumb of open five-hand touches center of chest with fingers spread.",
        "tips": "Tap thumb tip gently against sternum with fingers wiggling.",
        "video_file": "fine.mp4",
        "has_video": True
    },
    "FOLLOW": {
        "category": "word",
        "hands": 2,
        "name": "Follow / Accompany",
        "description": "Dominant fist trails closely behind non-dominant fist moving forward.",
        "tips": "One fist pursues the other in forward motion.",
        "video_file": "follow.mp4",
        "has_video": True
    },
    "FOOD": {
        "category": "word",
        "hands": 1,
        "name": "Food / Meal",
        "description": "Bunched fingertips tap lips twice.",
        "tips": "Tap bunched fingertips against mouth.",
        "video_file": "food.mp4",
        "has_video": True
    },
    "FRIEND": {
        "category": "word",
        "hands": 2,
        "name": "Friend / Companion",
        "description": "Both index fingers hook together once, then flip and hook reverse.",
        "tips": "Interlock curved index fingers warmly.",
        "video_file": "friend.mp4",
        "has_video": True
    },
    "FRUSTRATED": {
        "category": "word",
        "hands": 1,
        "name": "Frustrated / Annoyed",
        "description": "Back of flat hand taps chin or forehead abruptly with tension.",
        "tips": "Back of fingers tap chin sharply with tense expression.",
        "video_file": "frustrated.mp4",
        "has_video": True
    },
    "GO": {
        "category": "word",
        "hands": 2,
        "name": "Go / Leave",
        "description": "Both index fingers point down then arc forward and away from body.",
        "tips": "Fling index fingers forward in an outward arc.",
        "video_file": "go.mp4",
        "has_video": True
    },
    "GOD": {
        "category": "word",
        "hands": 1,
        "name": "God / Divine",
        "description": "Open flat hand held high pointing upward toward heaven.",
        "tips": "Raise open hand up above eye level pointing skyward.",
        "video_file": "god.mp4",
        "has_video": True
    },
    "GOOD": {
        "category": "word",
        "hands": 1,
        "name": "Good / Well",
        "description": "Flat hand touches chin and moves outward into open flat palm.",
        "tips": "Touch fingertips to chin and move forward into palm.",
        "video_file": "good.mp4",
        "has_video": True
    },
    "GOOD_AFTERNOON": {
        "category": "word",
        "hands": 2,
        "name": "Good Afternoon",
        "description": "Sign for 'Good' followed by sun position at midday (flat forearm resting horizontal).",
        "tips": "Sign Good, then rest right elbow on left palm with arm tilted at 45 degrees.",
        "video_file": "good_afternoon.mp4",
        "has_video": True
    },
    "GOOD_MORNING": {
        "category": "word",
        "hands": 2,
        "name": "Good Morning",
        "description": "Sign for 'Good' followed by right hand rising from horizontal left arm like the sunrise.",
        "tips": "Sign Good, then bring right hand up from behind left horizontal arm.",
        "video_file": "good_morning.mp4",
        "has_video": True
    },
    "GOOD_NIGHT": {
        "category": "word",
        "hands": 2,
        "name": "Good Night",
        "description": "Sign for 'Good' followed by right bent hand curving down over horizontal left hand (sunset).",
        "tips": "Sign Good, then curve right hand down over left forearm like setting sun.",
        "video_file": "good_night.mp4",
        "has_video": True
    },
    "HALT": {
        "category": "word",
        "hands": 2,
        "name": "Halt / Stop",
        "description": "Dominant flat hand chops firmly down onto open non-dominant palm.",
        "tips": "Vertical flat palm chops into horizontal open palm.",
        "video_file": "halt.mp4",
        "has_video": True
    },
    "HAPPY": {
        "category": "word",
        "hands": 2,
        "name": "Happy / Joyful",
        "description": "Both flat hands brush upward on chest in cheerful repeated strokes.",
        "tips": "Sweep both palms upward across chest with a smile.",
        "video_file": "happy.mp4",
        "has_video": True
    },
    "HAVE_COURAGE": {
        "category": "word",
        "hands": 2,
        "name": "Have Courage",
        "description": "Hands pull from shoulders into strong forward-facing fists.",
        "tips": "Clench fists firmly in front of chest.",
        "video_file": "have_courage.mp4",
        "has_video": True
    },
    "HE": {
        "category": "word",
        "hands": 1,
        "name": "He / Him",
        "description": "Index finger points to the side towards an imaginary male person.",
        "tips": "Point index finger to the right side.",
        "video_file": "he.mp4",
        "has_video": True
    },
    "HEAR": {
        "category": "word",
        "hands": 1,
        "name": "Hear / Audio",
        "description": "Index finger points directly to or taps the ear.",
        "tips": "Point index finger at ear canal.",
        "video_file": "hear.mp4",
        "has_video": True
    },
    "HELLO": {
        "category": "word",
        "hands": 1,
        "name": "Hello / Namaste",
        "description": "Open flat hand salutes outward from temple, or palms together in Namaste.",
        "tips": "Salute outward from brow or press palms in Namaste.",
        "video_file": "hello.mp4",
        "has_video": True
    },
    "HELP": {
        "category": "word",
        "hands": 2,
        "name": "Help / Support",
        "description": "Dominant thumbs-up fist sits atop non-dominant flat palm and lifts up.",
        "tips": "Lift thumbs-up fist with open palm underneath.",
        "video_file": "help.mp4",
        "has_video": True
    },
    "HELPLESS": {
        "category": "word",
        "hands": 2,
        "name": "Helpless",
        "description": "Both open hands held limp with palms facing up, shoulders shrug.",
        "tips": "Hold open hands out helplessly with palms up.",
        "video_file": "helpless.mp4",
        "has_video": True
    },
    "HERE": {
        "category": "word",
        "hands": 2,
        "name": "Here / Present",
        "description": "Both flat hands held in front with palms facing up, circling gently.",
        "tips": "Palms face upward dropping slightly to indicate this spot.",
        "video_file": "here.mp4",
        "has_video": True
    },
    "HOME": {
        "category": "word",
        "hands": 2,
        "name": "Home / House",
        "description": "Fingertips of both flat hands touch together forming a roof peak.",
        "tips": "Fingertips meet at 45-degree angle forming a triangle roof.",
        "video_file": "home.mp4",
        "has_video": True
    },
    "HOW_MANY": {
        "category": "word",
        "hands": 2,
        "name": "How Many / Quantity",
        "description": "Both closed fists held palm-up flick all fingers open upward.",
        "tips": "Flick fingers open from fists moving upward with questioning face.",
        "video_file": "how_many.mp4",
        "has_video": True
    },
    "HUNGRY": {
        "category": "word",
        "hands": 1,
        "name": "Hungry",
        "description": "'C' hand traces downward from neck to stomach.",
        "tips": "Slide 'C' shape down the center of chest.",
        "video_file": "hungry.mp4",
        "has_video": True
    },
    "IN": {
        "category": "word",
        "hands": 2,
        "name": "In / Inside",
        "description": "Dominant hand tucks fingertips into non-dominant 'C' or curled hand.",
        "tips": "Insert bunched dominant fingers into opposite curled hand.",
        "video_file": "in.mp4",
        "has_video": True
    },
    "INCORRECT": {
        "category": "word",
        "hands": 1,
        "name": "Incorrect / Wrong",
        "description": "'Y' hand or crooked index knocks against chin.",
        "tips": "Knock middle knuckles against chin firmly.",
        "video_file": "incorrect.mp4",
        "has_video": True
    },
    "INDIA": {
        "category": "word",
        "hands": 1,
        "name": "India / Bharat",
        "description": "Thumb touches forehead between eyebrows (like applying bindi/tilak).",
        "tips": "Touch center of forehead with thumb tip.",
        "video_file": "india.mp4",
        "has_video": True
    },
    "INDIAN": {
        "category": "word",
        "hands": 1,
        "name": "Indian",
        "description": "Thumb touches forehead center representing cultural tilak.",
        "tips": "Touch middle of brow with thumb.",
        "video_file": "indian.mp4",
        "has_video": True
    },
    "INVITE": {
        "category": "word",
        "hands": 2,
        "name": "Invite / Welcome",
        "description": "Both open palms start outward and sweep inward toward body.",
        "tips": "Gather both hands inward warmly with palms up.",
        "video_file": "invite.mp4",
        "has_video": True
    },
    "LANGUAGE": {
        "category": "word",
        "hands": 2,
        "name": "Language",
        "description": "Both 'L' hands start touching at thumbs and pull apart with undulating motion.",
        "tips": "Form 'L' shapes with both hands and snake them apart horizontally.",
        "video_file": "language.mp4",
        "has_video": True
    },
    "LATE": {
        "category": "word",
        "hands": 1,
        "name": "Late / Delayed",
        "description": "Hand flaps backward at the wrist several times near hip.",
        "tips": "Flap downward-facing hand backward at the wrist.",
        "video_file": "late.mp4",
        "has_video": True
    },
    "LEARN": {
        "category": "word",
        "hands": 2,
        "name": "Learn / Study",
        "description": "Dominant fingertips take imaginary knowledge from non-dominant palm to forehead.",
        "tips": "Gather from open left palm and touch to forehead.",
        "video_file": "learn.mp4",
        "has_video": True
    },
    "LIKE": {
        "category": "word",
        "hands": 1,
        "name": "Like / Fond Of",
        "description": "Thumb and middle finger pull outward from chest pinching together.",
        "tips": "Pinch thumb and middle finger together while drawing away from chest.",
        "video_file": "like.mp4",
        "has_video": True
    },
    "LISTEN": {
        "category": "word",
        "hands": 1,
        "name": "Listen / Pay Attention",
        "description": "Cupped hand placed behind ear leaning forward.",
        "tips": "Cup hand behind right ear attentively.",
        "video_file": "listen.mp4",
        "has_video": True
    },
    "LITTLE": {
        "category": "word",
        "hands": 1,
        "name": "Little / Small",
        "description": "Thumb and index finger held close together showing small gap.",
        "tips": "Pinch index and thumb close showing tiny space.",
        "video_file": "little.mp4",
        "has_video": True
    },
    "MANNER": {
        "category": "word",
        "hands": 2,
        "name": "Manner / Etiquette",
        "description": "Both hands move gracefully side to side.",
        "tips": "Smooth rhythmic wave of both hands.",
        "video_file": "manner.mp4",
        "has_video": True
    },
    "ME": {
        "category": "word",
        "hands": 1,
        "name": "Me / I",
        "description": "Index finger points directly to own chest.",
        "tips": "Point index finger at center of your chest.",
        "video_file": "me.mp4",
        "has_video": True
    },
    "MEAGER": {
        "category": "word",
        "hands": 1,
        "name": "Meager / Tiny",
        "description": "Index finger and thumb show narrow slit.",
        "tips": "Hold thumb and index in a very narrow pinch.",
        "video_file": "meager.mp4",
        "has_video": True
    },
    "MEET": {
        "category": "word",
        "hands": 2,
        "name": "Meet / Encounter",
        "description": "Both index fingers upright move towards each other until knuckles meet.",
        "tips": "Bring two upright index fingers together until they touch.",
        "video_file": "meet.mp4",
        "has_video": True
    },
    "MOTHER": {
        "category": "word",
        "hands": 1,
        "name": "Mother / Mom",
        "description": "Thumb of open five-hand taps chin or side of jaw twice.",
        "tips": "Tap thumb tip against chin twice with open palm.",
        "video_file": "mother.mp4",
        "has_video": True
    },
    "MUST": {
        "category": "word",
        "hands": 1,
        "name": "Must / Need",
        "description": "Bent index finger moves downward firmly and decisively.",
        "tips": "Hook index finger and press down firmly.",
        "video_file": "must.mp4",
        "has_video": True
    },
    "MY": {
        "category": "word",
        "hands": 1,
        "name": "My / Mine",
        "description": "Flat open hand placed firmly over center of chest.",
        "tips": "Press flat palm against chest over heart.",
        "video_file": "my.mp4",
        "has_video": True
    },
    "NAME": {
        "category": "word",
        "hands": 2,
        "name": "Name",
        "description": "Two fingers (index and middle) of right hand tap across left two fingers twice.",
        "tips": "Tap right 'H' fingers crosswise on left 'H' fingers.",
        "video_file": "name.mp4",
        "has_video": True
    },
    "NERVOUS": {
        "category": "word",
        "hands": 2,
        "name": "Nervous / Anxious",
        "description": "Both hands held in front with fingers pointing down, trembling visibly.",
        "tips": "Tremble fingers of both hands nervously.",
        "video_file": "nervous.mp4",
        "has_video": True
    },
    "NEVER": {
        "category": "word",
        "hands": 1,
        "name": "Never",
        "description": "Flat hand draws a question mark or downward wave in the air.",
        "tips": "Swipe flat hand down in an 'S' curve or chop across.",
        "video_file": "never.mp4",
        "has_video": True
    },
    "NEW": {
        "category": "word",
        "hands": 2,
        "name": "New / Fresh",
        "description": "Back of dominant hand scoops across the palm of non-dominant hand.",
        "tips": "Scoop right fingertips across left palm upward.",
        "video_file": "new.mp4",
        "has_video": True
    },
    "NICE_TO_MEET_YOU": {
        "category": "word",
        "hands": 2,
        "name": "Nice To Meet You",
        "description": "Sign for 'Good/Nice' followed by two index fingers meeting together.",
        "tips": "Slide right palm across left palm, then bring both index fingers together.",
        "video_file": "nice_to_meet_you.mp4",
        "has_video": True
    },
    "NO": {
        "category": "word",
        "hands": 1,
        "name": "No / Deny",
        "description": "Index and middle finger snap closed against thumb tip.",
        "tips": "Snap index and middle down onto thumb firmly.",
        "video_file": "no.mp4",
        "has_video": True
    },
    "NOW": {
        "category": "word",
        "hands": 2,
        "name": "Now / Present",
        "description": "Both bent hands drop down simultaneously in front of body.",
        "tips": "Drop both hands with bent fingers downward at waist.",
        "video_file": "now.mp4",
        "has_video": True
    },
    "OFFICE": {
        "category": "word",
        "hands": 2,
        "name": "Office / Workplace",
        "description": "Two 'O' hands form imaginary box walls in front of torso.",
        "tips": "Outline four walls of a room with flat hands.",
        "video_file": "office.mp4",
        "has_video": True
    },
    "OK": {
        "category": "word",
        "hands": 1,
        "name": "OK / Okay",
        "description": "Fingers spell 'O' then 'K' in rapid succession, or form OK loop.",
        "tips": "Thumb and index form loop with other three fingers upright.",
        "video_file": "ok.mp4",
        "has_video": True
    },
    "OKAY": {
        "category": "word",
        "hands": 1,
        "name": "Okay / Fine",
        "description": "Thumb and index form circular loop with remaining fingers extended.",
        "tips": "Standard OK ring hand shape held up.",
        "video_file": "okay.mp4",
        "has_video": True
    },
    "ON": {
        "category": "word",
        "hands": 2,
        "name": "On / Upon",
        "description": "Dominant flat hand placed squarely on top of non-dominant flat hand.",
        "tips": "Place right palm flat onto the back of left hand.",
        "video_file": "on.mp4",
        "has_video": True
    },
    "OUT": {
        "category": "word",
        "hands": 2,
        "name": "Out / Outside",
        "description": "Dominant hand pulls out from inside non-dominant curled hand.",
        "tips": "Pull bunched fingertips out of the opposite hand.",
        "video_file": "out.mp4",
        "has_video": True
    },
    "OUTSIDE": {
        "category": "word",
        "hands": 1,
        "name": "Outside",
        "description": "Hand pulls from near shoulder and opens outward away from body.",
        "tips": "Flick open hand outward past shoulder.",
        "video_file": "outside.mp4",
        "has_video": True
    },
    "PAIN": {
        "category": "word",
        "hands": 2,
        "name": "Pain / Hurt",
        "description": "Both index fingers point at each other and twist in opposite directions.",
        "tips": "Jab both index fingers toward each other with a twist.",
        "video_file": "pain.mp4",
        "has_video": True
    },
    "PAUSE": {
        "category": "word",
        "hands": 2,
        "name": "Pause / Intermission",
        "description": "Both index fingers held upright parallel, like the pause icon '||'.",
        "tips": "Hold two vertical index fingers side by side.",
        "video_file": "pause.mp4",
        "has_video": True
    },
    "PEOPLE": {
        "category": "word",
        "hands": 2,
        "name": "People / Public",
        "description": "Both 'P' hands pedal in alternating forward circles.",
        "tips": "Alternate circular bicycle motion with both 'P' hand shapes.",
        "video_file": "people.mp4",
        "has_video": True
    },
    "PERSON": {
        "category": "word",
        "hands": 2,
        "name": "Person / Individual",
        "description": "Both flat hands move downward parallel along sides of torso.",
        "tips": "Trace sides of body straight down with flat palms.",
        "video_file": "person.mp4",
        "has_video": True
    },
    "PLAY": {
        "category": "word",
        "hands": 2,
        "name": "Play / Game",
        "description": "Both 'Y' hands (thumb and pinky extended) shake side to side playfully.",
        "tips": "Shake both 'Y' hands with wrists rotating joyfully.",
        "video_file": "play.mp4",
        "has_video": True
    },
    "PLEASE": {
        "category": "word",
        "hands": 1,
        "name": "Please",
        "description": "Flat open hand rubbed in a circular motion over the chest.",
        "tips": "Rub flat palm clockwise on center of chest.",
        "video_file": "please.mp4",
        "has_video": True
    },
    "PRESSURED": {
        "category": "word",
        "hands": 2,
        "name": "Pressured / Stressed",
        "description": "Dominant palm presses downward heavily against opposite fist.",
        "tips": "Push down on top of fist with flat palm demonstrating pressure.",
        "video_file": "pressured.mp4",
        "has_video": True
    },
    "PROUD": {
        "category": "word",
        "hands": 1,
        "name": "Proud / Pride",
        "description": "Thumb of 'A' fist traces up the center of chest with chin held high.",
        "tips": "Stroke thumb up sternum with an upright posture.",
        "video_file": "proud.mp4",
        "has_video": True
    },
    "QUESTION": {
        "category": "word",
        "hands": 1,
        "name": "Question / Ask",
        "description": "Index finger draws question mark in air then dots the bottom.",
        "tips": "Trace question mark curve with index finger.",
        "video_file": "question.mp4",
        "has_video": True
    },
    "READY": {
        "category": "word",
        "hands": 2,
        "name": "Ready / Prepared",
        "description": "Both 'R' hands start together and swing outward simultaneously.",
        "tips": "Cross fingers into 'R' and sweep both hands outward.",
        "video_file": "ready.mp4",
        "has_video": True
    },
    "RELAX": {
        "category": "word",
        "hands": 2,
        "name": "Relax / Calm Down",
        "description": "Forearms cross gently over chest then lower smoothly.",
        "tips": "Cross arms over chest and exhale lowering hands.",
        "video_file": "relax.mp4",
        "has_video": True
    },
    "REPEAT": {
        "category": "word",
        "hands": 2,
        "name": "Repeat / Again",
        "description": "Dominant bent hand arches and taps opposite palm.",
        "tips": "Arc fingertips onto opposite open palm.",
        "video_file": "repeat.mp4",
        "has_video": True
    },
    "REQUEST": {
        "category": "word",
        "hands": 2,
        "name": "Request / Ask",
        "description": "Both flat palms pressed together moving inward toward chest.",
        "tips": "Press palms together in prayer position moving slightly forward.",
        "video_file": "request.mp4",
        "has_video": True
    },
    "RIGHT_NOW": {
        "category": "word",
        "hands": 2,
        "name": "Right Now / Immediately",
        "description": "Both hands drop down sharply at waist with emphasis.",
        "tips": "Drop both hands with bent fingers sharply for immediate time.",
        "video_file": "right_now.mp4",
        "has_video": True
    },
    "SCARED": {
        "category": "word",
        "hands": 2,
        "name": "Scared / Frightened",
        "description": "Both open hands pull backward to chest with trembling motion.",
        "tips": "Pull trembling hands toward chest with fearful look.",
        "video_file": "scared.mp4",
        "has_video": True
    },
    "SCHOOL": {
        "category": "word",
        "hands": 2,
        "name": "School",
        "description": "Dominant flat hand claps down onto non-dominant flat palm twice.",
        "tips": "Clap right palm horizontally onto left palm twice.",
        "video_file": "school.mp4",
        "has_video": True
    },
    "SEE_YOU_TOMORROW": {
        "category": "word",
        "hands": 2,
        "name": "See You Tomorrow",
        "description": "'V' hand from eye moves forward, followed by thumb flick for Tomorrow.",
        "tips": "Sign 'See' then flick thumb forward from jaw for tomorrow.",
        "video_file": "see_you_tomorrow.mp4",
        "has_video": True
    },
    "SHE": {
        "category": "word",
        "hands": 1,
        "name": "She / Her",
        "description": "Index finger points to the left side towards an imaginary female person.",
        "tips": "Point index finger to the side indicating female individual.",
        "video_file": "she.mp4",
        "has_video": True
    },
    "SHOULD": {
        "category": "word",
        "hands": 1,
        "name": "Should / Ought To",
        "description": "Bent index finger nods downward firmly twice.",
        "tips": "Nod curved index finger downward two times.",
        "video_file": "should.mp4",
        "has_video": True
    },
    "SIGN": {
        "category": "word",
        "hands": 2,
        "name": "Sign / Signing",
        "description": "Both index fingers circle alternately backward towards chest.",
        "tips": "Alternate rolling circles with both index fingers.",
        "video_file": "sign.mp4",
        "has_video": True
    },
    "SISTER": {
        "category": "word",
        "hands": 2,
        "name": "Sister",
        "description": "Thumb strokes chin (female), then right 'L' hand taps on left 'L' hand.",
        "tips": "Touch jaw then bring two L-hands together.",
        "video_file": "sister.mp4",
        "has_video": True
    },
    "SLEEP": {
        "category": "word",
        "hands": 1,
        "name": "Sleep / Rest",
        "description": "Open hand over face draws down into bunched fingers, eyes close.",
        "tips": "Pull open hand down over face while letting head tilt.",
        "video_file": "sleep.mp4",
        "has_video": True
    },
    "SMILE": {
        "category": "word",
        "hands": 2,
        "name": "Smile / Grin",
        "description": "Index fingers point to corners of mouth and draw upward curves.",
        "tips": "Trace smiling curves up from mouth corners.",
        "video_file": "smile.mp4",
        "has_video": True
    },
    "SOB": {
        "category": "word",
        "hands": 2,
        "name": "Sob / Weep",
        "description": "Both hands wipe tears from eyes repeatedly with slumped posture.",
        "tips": "Draw fingers down cheeks repeatedly showing heavy crying.",
        "video_file": "sob.mp4",
        "has_video": True
    },
    "SOMETIMES": {
        "category": "word",
        "hands": 2,
        "name": "Sometimes / Occasionally",
        "description": "Dominant index finger circles and taps non-dominant palm repeatedly.",
        "tips": "Tap index finger on open palm in intermittent arcs.",
        "video_file": "sometimes.mp4",
        "has_video": True
    },
    "SORRY": {
        "category": "word",
        "hands": 1,
        "name": "Sorry / Apology",
        "description": "'A' fist rubbed in circular motion over the center of chest.",
        "tips": "Rub closed fist in clockwise circle on chest with remorseful face.",
        "video_file": "sorry.mp4",
        "has_video": True
    },
    "SPEAK": {
        "category": "word",
        "hands": 1,
        "name": "Speak / Talk",
        "description": "Four extended fingers tap against chin/mouth twice.",
        "tips": "Tap four index fingers near lips moving outward.",
        "video_file": "speak.mp4",
        "has_video": True
    },
    "SPEECH": {
        "category": "word",
        "hands": 1,
        "name": "Speech / Oratory",
        "description": "Bent index and middle fingers rotate outward from mouth.",
        "tips": "Move curled fingers forward from mouth like spoken words.",
        "video_file": "speech.mp4",
        "has_video": True
    },
    "STAY": {
        "category": "word",
        "hands": 2,
        "name": "Stay / Remain",
        "description": "Both 'Y' hands push downward firmly and hold position.",
        "tips": "Press both 'Y' hands downward together locking in place.",
        "video_file": "stay.mp4",
        "has_video": True
    },
    "STOP": {
        "category": "word",
        "hands": 2,
        "name": "Stop / Cease",
        "description": "Dominant flat hand chops sharply down onto open palm.",
        "tips": "Vertical palm chops into open horizontal palm decisively.",
        "video_file": "stop.mp4",
        "has_video": True
    },
    "STRESSED": {
        "category": "word",
        "hands": 2,
        "name": "Stressed / Overwhelmed",
        "description": "Clawed hands tense at temples or chest pressing down.",
        "tips": "Hold tense claw hands near head showing mental strain.",
        "video_file": "stressed.mp4",
        "has_video": True
    },
    "STUDENT": {
        "category": "word",
        "hands": 2,
        "name": "Student / Learner",
        "description": "Sign for 'Learn' followed by 'Person' sign (hands sliding down sides).",
        "tips": "Sign Learn, then drop both flat hands down like individual.",
        "video_file": "student.mp4",
        "has_video": True
    },
    "STUDY": {
        "category": "word",
        "hands": 2,
        "name": "Study / Academics",
        "description": "Dominant fingers wiggle toward non-dominant open flat palm (book).",
        "tips": "Flutter right fingertips toward left flat palm intently.",
        "video_file": "study.mp4",
        "has_video": True
    },
    "TALK": {
        "category": "word",
        "hands": 2,
        "name": "Talk / Speak",
        "description": "Index fingers alternate moving forward and back near chin.",
        "tips": "Alternate index fingers moving back and forth from lips.",
        "video_file": "talk.mp4",
        "has_video": True
    },
    "TEACHER": {
        "category": "word",
        "hands": 2,
        "name": "Teacher / Instructor",
        "description": "Bunched hands at temples move forward opening, followed by 'Person' sign.",
        "tips": "Take ideas from head forward, then drop flat hands for person.",
        "video_file": "teacher.mp4",
        "has_video": True
    },
    "THANK_YOU": {
        "category": "word",
        "hands": 1,
        "name": "Thank You / Grateful",
        "description": "Fingertips touch chin/lips and move forward towards listener with flat palm.",
        "tips": "Touch fingertips to chin and extend open palm outward with gratitude.",
        "video_file": "thank_you.mp4",
        "has_video": True
    },
    "THERE": {
        "category": "word",
        "hands": 1,
        "name": "There / That Place",
        "description": "Index finger points distinctly outward away from speaker.",
        "tips": "Point index finger straight toward distant location.",
        "video_file": "there.mp4",
        "has_video": True
    },
    "THEY": {
        "category": "word",
        "hands": 1,
        "name": "They / Them",
        "description": "Index finger points and sweeps across horizontally to the side.",
        "tips": "Sweep index finger horizontally indicating a group.",
        "video_file": "they.mp4",
        "has_video": True
    },
    "THIRSTY": {
        "category": "word",
        "hands": 1,
        "name": "Thirsty",
        "description": "Index finger traces down center of throat.",
        "tips": "Draw index finger straight down front of throat.",
        "video_file": "thirsty.mp4",
        "has_video": True
    },
    "TIME_OUT": {
        "category": "word",
        "hands": 2,
        "name": "Time Out / Pause",
        "description": "One flat hand placed perpendicular on top of the other forming a 'T'.",
        "tips": "Form 'T' shape with one flat hand on top of another.",
        "video_file": "time_out.mp4",
        "has_video": True
    },
    "TIRED": {
        "category": "word",
        "hands": 2,
        "name": "Tired / Weary",
        "description": "Bent fingertips on chest roll outward and drop down heavily.",
        "tips": "Rest fingertips on chest and let hands roll down limply.",
        "video_file": "tired.mp4",
        "has_video": True
    },
    "TODAY": {
        "category": "word",
        "hands": 2,
        "name": "Today / This Day",
        "description": "Both 'Y' hands drop downward twice in front of body.",
        "tips": "Bounce both 'Y' hands downward twice.",
        "video_file": "today.mp4",
        "has_video": True
    },
    "TOMORROW": {
        "category": "word",
        "hands": 1,
        "name": "Tomorrow",
        "description": "Thumb of 'A' fist flicks forward from the cheek/jaw.",
        "tips": "Touch cheek with thumb and roll forward into the air.",
        "video_file": "tomorrow.mp4",
        "has_video": True
    },
    "UNDER": {
        "category": "word",
        "hands": 2,
        "name": "Under / Below",
        "description": "Dominant thumbs-up hand passes beneath non-dominant flat palm.",
        "tips": "Sweep right hand under the horizontal left palm.",
        "video_file": "under.mp4",
        "has_video": True
    },
    "UNDERSTAND": {
        "category": "word",
        "hands": 1,
        "name": "Understand / Got It",
        "description": "Index finger flicks upward from closed fist next to forehead.",
        "tips": "Flick index finger up near temple like a realization.",
        "video_file": "understand.mp4",
        "has_video": True
    },
    "WAIT": {
        "category": "word",
        "hands": 2,
        "name": "Wait / Hold On",
        "description": "Both open palms facing up wiggle fingers rhythmically.",
        "tips": "Hold palms up in front and wiggle fingers waiting.",
        "video_file": "wait.mp4",
        "has_video": True
    },
    "WE": {
        "category": "word",
        "hands": 1,
        "name": "We / Us",
        "description": "Index finger touches right shoulder, arcs forward, and touches left shoulder.",
        "tips": "Touch dominant shoulder and sweep in an arc to opposite shoulder.",
        "video_file": "we.mp4",
        "has_video": True
    },
    "WELCOME": {
        "category": "word",
        "hands": 2,
        "name": "Welcome / Greeting",
        "description": "Both open palms start outward and sweep inward toward body with a smile.",
        "tips": "Sweep both palms inward toward torso in welcoming embrace.",
        "video_file": "welcome.mp4",
        "has_video": True
    },
    "WHAT": {
        "category": "word",
        "hands": 2,
        "name": "What / Question",
        "description": "Both open hands held palm-up shake gently side to side.",
        "tips": "Hold palms up and wiggle side to side with questioning brow.",
        "video_file": "what.mp4",
        "has_video": True
    },
    "WHAT_HAPPENED": {
        "category": "word",
        "hands": 2,
        "name": "What Happened?",
        "description": "Both open hands turn over from palms-down to palms-up.",
        "tips": "Flip hands over from palms-down to palms-up with puzzled face.",
        "video_file": "what_happened.mp4",
        "has_video": True
    },
    "WHAT_TIME": {
        "category": "word",
        "hands": 2,
        "name": "What Time?",
        "description": "Index finger taps repeatedly on opposite wrist where watch is worn.",
        "tips": "Tap the back of opposite wrist with index finger.",
        "video_file": "what_time.mp4",
        "has_video": True
    },
    "WHEN": {
        "category": "word",
        "hands": 2,
        "name": "When?",
        "description": "Dominant index circles around non-dominant index and touches its tip.",
        "tips": "Circle right index finger around left index and land on its tip.",
        "video_file": "when.mp4",
        "has_video": True
    },
    "WHERE": {
        "category": "word",
        "hands": 1,
        "name": "Where?",
        "description": "Upright index finger wiggles side to side repeatedly.",
        "tips": "Wiggle upright index finger back and forth inquiry.",
        "video_file": "where.mp4",
        "has_video": True
    },
    "WHO": {
        "category": "word",
        "hands": 1,
        "name": "Who?",
        "description": "Thumb rests on chin while index finger wiggles up and down.",
        "tips": "Rest thumb on chin and waggle index finger.",
        "video_file": "who.mp4",
        "has_video": True
    },
    "WHOM": {
        "category": "word",
        "hands": 1,
        "name": "Whom?",
        "description": "Thumb rests on chin while index finger points toward person.",
        "tips": "Place thumb on chin and extend index finger outward.",
        "video_file": "whom.mp4",
        "has_video": True
    },
    "WHY": {
        "category": "word",
        "hands": 1,
        "name": "Why?",
        "description": "Fingertips touch forehead and pull down into 'Y' hand shape.",
        "tips": "Touch forehead with flat hand and pull away forming 'Y'.",
        "video_file": "why.mp4",
        "has_video": True
    },
    "WIFE": {
        "category": "word",
        "hands": 2,
        "name": "Wife / Spouse",
        "description": "Thumb touches chin (female) then both hands clasp together.",
        "tips": "Touch chin, then clasp hands together indicating marriage.",
        "video_file": "wife.mp4",
        "has_video": True
    },
    "WORK": {
        "category": "word",
        "hands": 2,
        "name": "Work / Job",
        "description": "Dominant fist taps wrist of non-dominant fist twice.",
        "tips": "Tap heel of right fist on back of left wrist twice.",
        "video_file": "work.mp4",
        "has_video": True
    },
    "WORRY": {
        "category": "word",
        "hands": 2,
        "name": "Worry / Concerned",
        "description": "Both 'B' hands alternate crossing in front of forehead.",
        "tips": "Flap flat hands across forehead with concerned expression.",
        "video_file": "worry.mp4",
        "has_video": True
    },
    "WRONG": {
        "category": "word",
        "hands": 1,
        "name": "Wrong / Error",
        "description": "'Y' hand knocks middle knuckles against chin.",
        "tips": "Tap chin with middle fingers of 'Y' hand shape.",
        "video_file": "wrong.mp4",
        "has_video": True
    },
    "YEAR": {
        "category": "word",
        "hands": 2,
        "name": "Year / Annual",
        "description": "Dominant fist orbits completely around non-dominant fist and lands on top.",
        "tips": "Orbit right fist around left fist like the Earth orbiting the sun.",
        "video_file": "year.mp4",
        "has_video": True
    },
    "YES": {
        "category": "word",
        "hands": 1,
        "name": "Yes / Affirm",
        "description": "'S' fist nods up and down like a head nodding yes.",
        "tips": "Nod closed fist up and down gently.",
        "video_file": "yes.mp4",
        "has_video": True
    },
    "YESTERDAY": {
        "category": "word",
        "hands": 1,
        "name": "Yesterday",
        "description": "Thumb of 'Y' or 'A' hand touches chin then moves backward to touch ear.",
        "tips": "Touch chin with thumb and sweep backward to touch ear.",
        "video_file": "yesterday.mp4",
        "has_video": True
    },
    "YOU": {
        "category": "word",
        "hands": 1,
        "name": "You",
        "description": "Index finger points directly at the listener.",
        "tips": "Point index finger directly at the person you are speaking with.",
        "video_file": "you.mp4",
        "has_video": True
    },
    "YOUR": {
        "category": "word",
        "hands": 1,
        "name": "Your / Yours",
        "description": "Flat open palm pushes forward towards the listener.",
        "tips": "Push flat palm forward toward the listener respectfully.",
        "video_file": "your.mp4",
        "has_video": True
    },
    "YOURSELF": {
        "category": "word",
        "hands": 1,
        "name": "Yourself",
        "description": "'A' fist with thumb pointing forward pushes towards the listener.",
        "tips": "Thrust thumbs-up fist forward toward the listener.",
        "video_file": "yourself.mp4",
        "has_video": True
    },
}

def get_class_list():
    """Return ordered list of class labels."""
    return sorted(list(ISL_CLASSES.keys()))

def get_class_info(label):
    """Retrieve metadata for a specific class label."""
    key = str(label).upper()
    return ISL_CLASSES.get(key, {
        "category": "custom",
        "hands": 1,
        "name": key,
        "description": "User defined sign",
        "tips": "Hold steady in front of camera",
        "has_video": False
    })
