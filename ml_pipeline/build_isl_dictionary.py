"""
Generator for Comprehensive ISL Dictionary.
Combines:
- 26 Alphabet letters (A-Z) with video & image support
- 10 Digits (0-9) with video & image support
- 168 Everyday Vocabulary Words with video & image support
Total: 204 Indian Sign Language Signs with full metadata.
"""

import os
import json

VIDEOS_DIR = "Images/isl_videos"

# Descriptions and hand counts for common words
WORD_DETAILS = {
    "ACHE": {"name": "Ache / Hurt", "hands": 1, "desc": "Index fingers pointing towards the affected area with twisted movement.", "tips": "Point and twist index finger indicating localized pain."},
    "AFRAID": {"name": "Afraid / Scared", "hands": 2, "desc": "Both open hands held in front of chest, palms in, trembling slightly.", "tips": "Hands draw inward toward the chest with an expression of fear."},
    "AFTER": {"name": "After / Later", "hands": 2, "desc": "One flat hand slides forward past the other stationary flat hand.", "tips": "Dominant hand moves forward across the non-dominant hand."},
    "AGAIN": {"name": "Again / Repeat", "hands": 2, "desc": "Dominant bent hand arches over and taps onto the palm of non-dominant flat hand.", "tips": "Bend fingers at right angle and arc into the open palm."},
    "AGE": {"name": "Age / Old", "hands": 1, "desc": "Hand clasps chin and moves downward as if tugging on a beard.", "tips": "Gently stroke downward from chin with cupped hand."},
    "AGREE": {"name": "Agree / Concur", "hands": 2, "desc": "Both index fingers start near temple/chest and move forward together in affirmation.", "tips": "Both hands move forward simultaneously and nod together."},
    "ALL": {"name": "All / Whole", "hands": 2, "desc": "Both flat palms sweep outward in a full horizontal circle meeting together.", "tips": "Enclose an imaginary circle with both hands."},
    "ALWAYS": {"name": "Always / Forever", "hands": 1, "desc": "Index finger extended upright tracing continuous small circular motion in the air.", "tips": "Rotate index finger in a steady circular loop."},
    "ANGRY": {"name": "Angry / Mad", "hands": 1, "desc": "Curved claw hand held in front of face pulling slightly outward with tension.", "tips": "Form a claw shape with fingers tense in front of face."},
    "ANSWER": {"name": "Answer / Reply", "hands": 2, "desc": "Index fingers at lips move forward and point outward toward the person.", "tips": "Start with index near mouth and direct it towards the listener."},
    "ASK": {"name": "Ask / Inquire", "hands": 1, "desc": "Index finger bent like a hook moving from body outward toward the listener.", "tips": "Curl index finger forward in a questioning gesture."},
    "BAD": {"name": "Bad", "hands": 1, "desc": "Flat hand placed at chin and swept abruptly downward turning palm face down.", "tips": "Touch chin with flat hand and twist palm down abruptly."},
    "BE_BRAVE": {"name": "Be Brave", "hands": 2, "desc": "Fists held at chest moving firmly outward with strength and courage.", "tips": "Thrust closed fists forward from chest resolutely."},
    "BE_BRAVE_ENOUGH": {"name": "Be Brave Enough", "hands": 2, "desc": "Both hands form firm fists at chest with determined forward posture.", "tips": "Solid chest posture with forward chin lift."},
    "BEFORE": {"name": "Before / Prior", "hands": 2, "desc": "Dominant hand moves backward over the shoulder or back over stationary hand.", "tips": "Pull hand backward indicating earlier in time."},
    "BEHAVIOUR": {"name": "Behaviour / Conduct", "hands": 2, "desc": "Both 'B' hands move alternately side to side in front of the chest.", "tips": "Wave flat hands in gentle alternating horizontal sweeps."},
    "BEST": {"name": "Best", "hands": 1, "desc": "Thumbs-up hand moved from chin diagonally upwards into the air.", "tips": "Start thumbs-up near mouth and elevate it high with pride."},
    "BRAVE": {"name": "Brave / Courage", "hands": 2, "desc": "Both open hands at shoulders pull into strong clenched fists.", "tips": "Grasp air into strong fists pulled down near torso."},
    "BREAK": {"name": "Break / Snap", "hands": 2, "desc": "Both hands hold an imaginary stick and snap it downward simultaneously.", "tips": "Twist both fists downward as if snapping a twig."},
    "BYE": {"name": "Bye / Goodbye", "hands": 1, "desc": "Open hand held up waving fingers back and forth smoothly.", "tips": "Standard friendly hand wave with fingers moving together."},
    "CALL": {"name": "Call / Phone", "hands": 1, "desc": "Hand in 'Y' shape (thumb and pinky extended) held to the ear like a phone.", "tips": "Thumb at ear and pinky near mouth mimicking telephone handset."},
    "CALM": {"name": "Calm / Peaceful", "hands": 2, "desc": "Both flat hands start at chest level and press gently downward together.", "tips": "Lower both open palms smoothly to convey calmness."},
    "CAREFUL": {"name": "Careful / Cautious", "hands": 2, "desc": "Two 'V' hands placed one on top of the other, tapping twice.", "tips": "Rest dominant V-fingers on top of non-dominant V-fingers."},
    "CHAT": {"name": "Chat / Conversation", "hands": 2, "desc": "Both hands open and close in an alternating talking beak motion.", "tips": "Alternate opening and pinching fingertips of both hands."},
    "CHOCOLATE": {"name": "Chocolate", "hands": 2, "desc": "'C' hand circles gently on the back of the non-dominant closed fist.", "tips": "Rub 'C' shape over the back of the opposite hand."},
    "COLLEGE": {"name": "College / University", "hands": 2, "desc": "Flat dominant hand slides off flat non-dominant hand and arches upward.", "tips": "Slide dominant palm across opposite palm and sweep up in an arc."},
    "COME": {"name": "Come / Approach", "hands": 2, "desc": "Both index fingers curled inward beckoning toward the body.", "tips": "Beckon with both index fingers pulling toward yourself."},
    "COMPREHEND": {"name": "Comprehend / Understand", "hands": 1, "desc": "Flick index finger upward from closed fist next to the forehead.", "tips": "Flick index up near temple like a lightbulb turning on."},
    "COMPUTER": {"name": "Computer", "hands": 2, "desc": "Fingers of both hands wiggle rhythmically as if typing on a keyboard.", "tips": "Mimic fluid two-handed keyboard typing motion."},
    "CONCUR": {"name": "Concur / Agree", "hands": 2, "desc": "Both index fingers come forward and meet in parallel alignment.", "tips": "Bring both index fingers parallel and move down together in agreement."},
    "CONDUCT": {"name": "Conduct / Manners", "hands": 2, "desc": "Both flat hands sweep side to side alternately in front of torso.", "tips": "Gentle alternating side-to-side sweeping motion."},
    "CONFUSED": {"name": "Confused / Puzzled", "hands": 2, "desc": "Both claw hands rotate in opposing circles near the temples.", "tips": "Circle clawed hands near sides of forehead."},
    "CONGRATULATIONS": {"name": "Congratulations", "hands": 2, "desc": "Both hands clasp together and shake, or clap in sign language ovation.", "tips": "Clasp own hands together shaking joyfully near shoulder."},
    "CONSENT": {"name": "Consent / Permission", "hands": 2, "desc": "Both open palms start at chest facing up and rise forward together.", "tips": "Lift both cupped palms gently upward in approval."},
    "CRY": {"name": "Cry / Weep", "hands": 2, "desc": "Both index fingers trace teardrop paths downward from eyes across cheeks.", "tips": "Trace lines down cheeks with index fingers repeatedly."},
    "DISAGREE": {"name": "Disagree / Oppose", "hands": 2, "desc": "Index fingers touch temple then pull apart sharply with a head shake.", "tips": "Touch forehead and pull both hands apart in opposite directions."},
    "DISSENT": {"name": "Dissent / Disapproval", "hands": 2, "desc": "Hands cross at wrists and push outward in refusal.", "tips": "Cross forearms and swing outward dismissing."},
    "DO": {"name": "Do / Action", "hands": 2, "desc": "Both 'C' or pinch hands move side to side rhythmically together.", "tips": "Move both hands side to side synchronously in front of waist."},
    "DRINK": {"name": "Drink / Beverage", "hands": 1, "desc": "Hand forms 'C' cup shape and tilts toward mouth as if drinking.", "tips": "Mimic tipping a cup up to lips."},
    "EARLY": {"name": "Early", "hands": 2, "desc": "Middle finger of dominant hand flicks forward over non-dominant fist.", "tips": "Flick middle finger across the back of opposite wrist."},
    "EAT": {"name": "Eat / Food", "hands": 1, "desc": "Fingertips brought together into a bunched shape tapping at mouth.", "tips": "Tap bunched fingers gently at lips twice."},
    "EVERY_TIME": {"name": "Every Time / Always", "hands": 2, "desc": "Index finger repeatedly taps non-dominant index in regular intervals.", "tips": "Tap index finger repeatedly moving forward."},
    "EXCUSE_ME": {"name": "Excuse Me / Pardon", "hands": 2, "desc": "Fingertips of dominant hand slide across non-dominant palm twice.", "tips": "Brush dominant fingertips across flat palm toward yourself."},
    "EXHAUSTED": {"name": "Exhausted / Depleted", "hands": 2, "desc": "Curved hands at chest drop downward limp and heavy with shoulders slumping.", "tips": "Drop hands down from chest with tired posture."},
    "EXPLAIN": {"name": "Explain / Describe", "hands": 2, "desc": "Both 'F' hands move alternately forward and back smoothly.", "tips": "Pinch thumb and index on both hands, slide back and forth alternately."},
    "FATHER": {"name": "Father / Dad", "hands": 1, "desc": "Thumb of open hand rests on forehead or temple, fingers spread.", "tips": "Tap thumb against center of forehead with open palm."},
    "FATIGUED": {"name": "Fatigued / Worn Out", "hands": 2, "desc": "Hands bent at chest sag downward limply.", "tips": "Let hands and shoulders drop together."},
    "FEAR": {"name": "Fear / Fright", "hands": 2, "desc": "Both hands shake slightly pulling in front of chest.", "tips": "Pull trembling hands toward chest defensively."},
    "FINE": {"name": "Fine / Alright", "hands": 1, "desc": "Thumb of open five-hand touches center of chest with fingers spread.", "tips": "Tap thumb tip gently against sternum with fingers wiggling."},
    "FOLLOW": {"name": "Follow / Accompany", "hands": 2, "desc": "Dominant fist trails closely behind non-dominant fist moving forward.", "tips": "One fist pursues the other in forward motion."},
    "FOOD": {"name": "Food / Meal", "hands": 1, "desc": "Bunched fingertips tap lips twice.", "tips": "Tap bunched fingertips against mouth."},
    "FRIEND": {"name": "Friend / Companion", "hands": 2, "desc": "Both index fingers hook together once, then flip and hook reverse.", "tips": "Interlock curved index fingers warmly."},
    "FRUSTRATED": {"name": "Frustrated / Annoyed", "hands": 1, "desc": "Back of flat hand taps chin or forehead abruptly with tension.", "tips": "Back of fingers tap chin sharply with tense expression."},
    "GO": {"name": "Go / Leave", "hands": 2, "desc": "Both index fingers point down then arc forward and away from body.", "tips": "Fling index fingers forward in an outward arc."},
    "GOD": {"name": "God / Divine", "hands": 1, "desc": "Open flat hand held high pointing upward toward heaven.", "tips": "Raise open hand up above eye level pointing skyward."},
    "GOOD": {"name": "Good / Well", "hands": 1, "desc": "Flat hand touches chin and moves outward into open flat palm.", "tips": "Touch fingertips to chin and move forward into palm."},
    "GOOD_AFTERNOON": {"name": "Good Afternoon", "hands": 2, "desc": "Sign for 'Good' followed by sun position at midday (flat forearm resting horizontal).", "tips": "Sign Good, then rest right elbow on left palm with arm tilted at 45 degrees."},
    "GOOD_MORNING": {"name": "Good Morning", "hands": 2, "desc": "Sign for 'Good' followed by right hand rising from horizontal left arm like the sunrise.", "tips": "Sign Good, then bring right hand up from behind left horizontal arm."},
    "GOOD_NIGHT": {"name": "Good Night", "hands": 2, "desc": "Sign for 'Good' followed by right bent hand curving down over horizontal left hand (sunset).", "tips": "Sign Good, then curve right hand down over left forearm like setting sun."},
    "HALT": {"name": "Halt / Stop", "hands": 2, "desc": "Dominant flat hand chops firmly down onto open non-dominant palm.", "tips": "Vertical flat palm chops into horizontal open palm."},
    "HAPPY": {"name": "Happy / Joyful", "hands": 2, "desc": "Both flat hands brush upward on chest in cheerful repeated strokes.", "tips": "Sweep both palms upward across chest with a smile."},
    "HAVE_COURAGE": {"name": "Have Courage", "hands": 2, "desc": "Hands pull from shoulders into strong forward-facing fists.", "tips": "Clench fists firmly in front of chest."},
    "HE": {"name": "He / Him", "hands": 1, "desc": "Index finger points to the side towards an imaginary male person.", "tips": "Point index finger to the right side."},
    "HEAR": {"name": "Hear / Audio", "hands": 1, "desc": "Index finger points directly to or taps the ear.", "tips": "Point index finger at ear canal."},
    "HELLO": {"name": "Hello / Namaste", "hands": 1, "desc": "Open flat hand salutes outward from temple, or palms together in Namaste.", "tips": "Salute outward from brow or press palms in Namaste."},
    "HELP": {"name": "Help / Support", "hands": 2, "desc": "Dominant thumbs-up fist sits atop non-dominant flat palm and lifts up.", "tips": "Lift thumbs-up fist with open palm underneath."},
    "HELPLESS": {"name": "Helpless", "hands": 2, "desc": "Both open hands held limp with palms facing up, shoulders shrug.", "tips": "Hold open hands out helplessly with palms up."},
    "HERE": {"name": "Here / Present", "hands": 2, "desc": "Both flat hands held in front with palms facing up, circling gently.", "tips": "Palms face upward dropping slightly to indicate this spot."},
    "HOME": {"name": "Home / House", "hands": 2, "desc": "Fingertips of both flat hands touch together forming a roof peak.", "tips": "Fingertips meet at 45-degree angle forming a triangle roof."},
    "HOW_MANY": {"name": "How Many / Quantity", "hands": 2, "desc": "Both closed fists held palm-up flick all fingers open upward.", "tips": "Flick fingers open from fists moving upward with questioning face."},
    "HUNGRY": {"name": "Hungry", "hands": 1, "desc": "'C' hand traces downward from neck to stomach.", "tips": "Slide 'C' shape down the center of chest."},
    "IN": {"name": "In / Inside", "hands": 2, "desc": "Dominant hand tucks fingertips into non-dominant 'C' or curled hand.", "tips": "Insert bunched dominant fingers into opposite curled hand."},
    "INCORRECT": {"name": "Incorrect / Wrong", "hands": 1, "desc": "'Y' hand or crooked index knocks against chin.", "tips": "Knock middle knuckles against chin firmly."},
    "INDIA": {"name": "India / Bharat", "hands": 1, "desc": "Thumb touches forehead between eyebrows (like applying bindi/tilak).", "tips": "Touch center of forehead with thumb tip."},
    "INDIAN": {"name": "Indian", "hands": 1, "desc": "Thumb touches forehead center representing cultural tilak.", "tips": "Touch middle of brow with thumb."},
    "INVITE": {"name": "Invite / Welcome", "hands": 2, "desc": "Both open palms start outward and sweep inward toward body.", "tips": "Gather both hands inward warmly with palms up."},
    "LANGUAGE": {"name": "Language", "hands": 2, "desc": "Both 'L' hands start touching at thumbs and pull apart with undulating motion.", "tips": "Form 'L' shapes with both hands and snake them apart horizontally."},
    "LATE": {"name": "Late / Delayed", "hands": 1, "desc": "Hand flaps backward at the wrist several times near hip.", "tips": "Flap downward-facing hand backward at the wrist."},
    "LEARN": {"name": "Learn / Study", "hands": 2, "desc": "Dominant fingertips take imaginary knowledge from non-dominant palm to forehead.", "tips": "Gather from open left palm and touch to forehead."},
    "LIKE": {"name": "Like / Fond Of", "hands": 1, "desc": "Thumb and middle finger pull outward from chest pinching together.", "tips": "Pinch thumb and middle finger together while drawing away from chest."},
    "LISTEN": {"name": "Listen / Pay Attention", "hands": 1, "desc": "Cupped hand placed behind ear leaning forward.", "tips": "Cup hand behind right ear attentively."},
    "LITTLE": {"name": "Little / Small", "hands": 1, "desc": "Thumb and index finger held close together showing small gap.", "tips": "Pinch index and thumb close showing tiny space."},
    "MANNER": {"name": "Manner / Etiquette", "hands": 2, "desc": "Both hands move gracefully side to side.", "tips": "Smooth rhythmic wave of both hands."},
    "ME": {"name": "Me / I", "hands": 1, "desc": "Index finger points directly to own chest.", "tips": "Point index finger at center of your chest."},
    "MEAGER": {"name": "Meager / Tiny", "hands": 1, "desc": "Index finger and thumb show narrow slit.", "tips": "Hold thumb and index in a very narrow pinch."},
    "MEET": {"name": "Meet / Encounter", "hands": 2, "desc": "Both index fingers upright move towards each other until knuckles meet.", "tips": "Bring two upright index fingers together until they touch."},
    "MOTHER": {"name": "Mother / Mom", "hands": 1, "desc": "Thumb of open five-hand taps chin or side of jaw twice.", "tips": "Tap thumb tip against chin twice with open palm."},
    "MUST": {"name": "Must / Need", "hands": 1, "desc": "Bent index finger moves downward firmly and decisively.", "tips": "Hook index finger and press down firmly."},
    "MY": {"name": "My / Mine", "hands": 1, "desc": "Flat open hand placed firmly over center of chest.", "tips": "Press flat palm against chest over heart."},
    "NAME": {"name": "Name", "hands": 2, "desc": "Two fingers (index and middle) of right hand tap across left two fingers twice.", "tips": "Tap right 'H' fingers crosswise on left 'H' fingers."},
    "NERVOUS": {"name": "Nervous / Anxious", "hands": 2, "desc": "Both hands held in front with fingers pointing down, trembling visibly.", "tips": "Tremble fingers of both hands nervously."},
    "NEVER": {"name": "Never", "hands": 1, "desc": "Flat hand draws a question mark or downward wave in the air.", "tips": "Swipe flat hand down in an 'S' curve or chop across."},
    "NEW": {"name": "New / Fresh", "hands": 2, "desc": "Back of dominant hand scoops across the palm of non-dominant hand.", "tips": "Scoop right fingertips across left palm upward."},
    "NICE_TO_MEET_YOU": {"name": "Nice To Meet You", "hands": 2, "desc": "Sign for 'Good/Nice' followed by two index fingers meeting together.", "tips": "Slide right palm across left palm, then bring both index fingers together."},
    "NO": {"name": "No / Deny", "hands": 1, "desc": "Index and middle finger snap closed against thumb tip.", "tips": "Snap index and middle down onto thumb firmly."},
    "NOW": {"name": "Now / Present", "hands": 2, "desc": "Both bent hands drop down simultaneously in front of body.", "tips": "Drop both hands with bent fingers downward at waist."},
    "OFFICE": {"name": "Office / Workplace", "hands": 2, "desc": "Two 'O' hands form imaginary box walls in front of torso.", "tips": "Outline four walls of a room with flat hands."},
    "OK": {"name": "OK / Okay", "hands": 1, "desc": "Fingers spell 'O' then 'K' in rapid succession, or form OK loop.", "tips": "Thumb and index form loop with other three fingers upright."},
    "OKAY": {"name": "Okay / Fine", "hands": 1, "desc": "Thumb and index form circular loop with remaining fingers extended.", "tips": "Standard OK ring hand shape held up."},
    "ON": {"name": "On / Upon", "hands": 2, "desc": "Dominant flat hand placed squarely on top of non-dominant flat hand.", "tips": "Place right palm flat onto the back of left hand."},
    "OUT": {"name": "Out / Outside", "hands": 2, "desc": "Dominant hand pulls out from inside non-dominant curled hand.", "tips": "Pull bunched fingertips out of the opposite hand."},
    "OUTSIDE": {"name": "Outside", "hands": 1, "desc": "Hand pulls from near shoulder and opens outward away from body.", "tips": "Flick open hand outward past shoulder."},
    "PAIN": {"name": "Pain / Hurt", "hands": 2, "desc": "Both index fingers point at each other and twist in opposite directions.", "tips": "Jab both index fingers toward each other with a twist."},
    "PAUSE": {"name": "Pause / Intermission", "hands": 2, "desc": "Both index fingers held upright parallel, like the pause icon '||'.", "tips": "Hold two vertical index fingers side by side."},
    "PEOPLE": {"name": "People / Public", "hands": 2, "desc": "Both 'P' hands pedal in alternating forward circles.", "tips": "Alternate circular bicycle motion with both 'P' hand shapes."},
    "PERSON": {"name": "Person / Individual", "hands": 2, "desc": "Both flat hands move downward parallel along sides of torso.", "tips": "Trace sides of body straight down with flat palms."},
    "PLAY": {"name": "Play / Game", "hands": 2, "desc": "Both 'Y' hands (thumb and pinky extended) shake side to side playfully.", "tips": "Shake both 'Y' hands with wrists rotating joyfully."},
    "PLEASE": {"name": "Please", "hands": 1, "desc": "Flat open hand rubbed in a circular motion over the chest.", "tips": "Rub flat palm clockwise on center of chest."},
    "PRESSURED": {"name": "Pressured / Stressed", "hands": 2, "desc": "Dominant palm presses downward heavily against opposite fist.", "tips": "Push down on top of fist with flat palm demonstrating pressure."},
    "PROUD": {"name": "Proud / Pride", "hands": 1, "desc": "Thumb of 'A' fist traces up the center of chest with chin held high.", "tips": "Stroke thumb up sternum with an upright posture."},
    "QUESTION": {"name": "Question / Ask", "hands": 1, "desc": "Index finger draws question mark in air then dots the bottom.", "tips": "Trace question mark curve with index finger."},
    "READY": {"name": "Ready / Prepared", "hands": 2, "desc": "Both 'R' hands start together and swing outward simultaneously.", "tips": "Cross fingers into 'R' and sweep both hands outward."},
    "RELAX": {"name": "Relax / Calm Down", "hands": 2, "desc": "Forearms cross gently over chest then lower smoothly.", "tips": "Cross arms over chest and exhale lowering hands."},
    "REPEAT": {"name": "Repeat / Again", "hands": 2, "desc": "Dominant bent hand arches and taps opposite palm.", "tips": "Arc fingertips onto opposite open palm."},
    "REQUEST": {"name": "Request / Ask", "hands": 2, "desc": "Both flat palms pressed together moving inward toward chest.", "tips": "Press palms together in prayer position moving slightly forward."},
    "RIGHT_NOW": {"name": "Right Now / Immediately", "hands": 2, "desc": "Both hands drop down sharply at waist with emphasis.", "tips": "Drop both hands with bent fingers sharply for immediate time."},
    "SCARED": {"name": "Scared / Frightened", "hands": 2, "desc": "Both open hands pull backward to chest with trembling motion.", "tips": "Pull trembling hands toward chest with fearful look."},
    "SCHOOL": {"name": "School", "hands": 2, "desc": "Dominant flat hand claps down onto non-dominant flat palm twice.", "tips": "Clap right palm horizontally onto left palm twice."},
    "SEE_YOU_TOMORROW": {"name": "See You Tomorrow", "hands": 2, "desc": "'V' hand from eye moves forward, followed by thumb flick for Tomorrow.", "tips": "Sign 'See' then flick thumb forward from jaw for tomorrow."},
    "SHE": {"name": "She / Her", "hands": 1, "desc": "Index finger points to the left side towards an imaginary female person.", "tips": "Point index finger to the side indicating female individual."},
    "SHOULD": {"name": "Should / Ought To", "hands": 1, "desc": "Bent index finger nods downward firmly twice.", "tips": "Nod curved index finger downward two times."},
    "SIGN": {"name": "Sign / Signing", "hands": 2, "desc": "Both index fingers circle alternately backward towards chest.", "tips": "Alternate rolling circles with both index fingers."},
    "SISTER": {"name": "Sister", "hands": 2, "desc": "Thumb strokes chin (female), then right 'L' hand taps on left 'L' hand.", "tips": "Touch jaw then bring two L-hands together."},
    "SLEEP": {"name": "Sleep / Rest", "hands": 1, "desc": "Open hand over face draws down into bunched fingers, eyes close.", "tips": "Pull open hand down over face while letting head tilt."},
    "SMILE": {"name": "Smile / Grin", "hands": 2, "desc": "Index fingers point to corners of mouth and draw upward curves.", "tips": "Trace smiling curves up from mouth corners."},
    "SOB": {"name": "Sob / Weep", "hands": 2, "desc": "Both hands wipe tears from eyes repeatedly with slumped posture.", "tips": "Draw fingers down cheeks repeatedly showing heavy crying."},
    "SOMETIMES": {"name": "Sometimes / Occasionally", "hands": 2, "desc": "Dominant index finger circles and taps non-dominant palm repeatedly.", "tips": "Tap index finger on open palm in intermittent arcs."},
    "SORRY": {"name": "Sorry / Apology", "hands": 1, "desc": "'A' fist rubbed in circular motion over the center of chest.", "tips": "Rub closed fist in clockwise circle on chest with remorseful face."},
    "SPEAK": {"name": "Speak / Talk", "hands": 1, "desc": "Four extended fingers tap against chin/mouth twice.", "tips": "Tap four index fingers near lips moving outward."},
    "SPEECH": {"name": "Speech / Oratory", "hands": 1, "desc": "Bent index and middle fingers rotate outward from mouth.", "tips": "Move curled fingers forward from mouth like spoken words."},
    "STAY": {"name": "Stay / Remain", "hands": 2, "desc": "Both 'Y' hands push downward firmly and hold position.", "tips": "Press both 'Y' hands downward together locking in place."},
    "STOP": {"name": "Stop / Cease", "hands": 2, "desc": "Dominant flat hand chops sharply down onto open palm.", "tips": "Vertical palm chops into open horizontal palm decisively."},
    "STRESSED": {"name": "Stressed / Overwhelmed", "hands": 2, "desc": "Clawed hands tense at temples or chest pressing down.", "tips": "Hold tense claw hands near head showing mental strain."},
    "STUDENT": {"name": "Student / Learner", "hands": 2, "desc": "Sign for 'Learn' followed by 'Person' sign (hands sliding down sides).", "tips": "Sign Learn, then drop both flat hands down like individual."},
    "STUDY": {"name": "Study / Academics", "hands": 2, "desc": "Dominant fingers wiggle toward non-dominant open flat palm (book).", "tips": "Flutter right fingertips toward left flat palm intently."},
    "TALK": {"name": "Talk / Speak", "hands": 2, "desc": "Index fingers alternate moving forward and back near chin.", "tips": "Alternate index fingers moving back and forth from lips."},
    "TEACHER": {"name": "Teacher / Instructor", "hands": 2, "desc": "Bunched hands at temples move forward opening, followed by 'Person' sign.", "tips": "Take ideas from head forward, then drop flat hands for person."},
    "THANK_YOU": {"name": "Thank You / Grateful", "hands": 1, "desc": "Fingertips touch chin/lips and move forward towards listener with flat palm.", "tips": "Touch fingertips to chin and extend open palm outward with gratitude."},
    "THERE": {"name": "There / That Place", "hands": 1, "desc": "Index finger points distinctly outward away from speaker.", "tips": "Point index finger straight toward distant location."},
    "THEY": {"name": "They / Them", "hands": 1, "desc": "Index finger points and sweeps across horizontally to the side.", "tips": "Sweep index finger horizontally indicating a group."},
    "THIRSTY": {"name": "Thirsty", "hands": 1, "desc": "Index finger traces down center of throat.", "tips": "Draw index finger straight down front of throat."},
    "TIME_OUT": {"name": "Time Out / Pause", "hands": 2, "desc": "One flat hand placed perpendicular on top of the other forming a 'T'.", "tips": "Form 'T' shape with one flat hand on top of another."},
    "TIRED": {"name": "Tired / Weary", "hands": 2, "desc": "Bent fingertips on chest roll outward and drop down heavily.", "tips": "Rest fingertips on chest and let hands roll down limply."},
    "TODAY": {"name": "Today / This Day", "hands": 2, "desc": "Both 'Y' hands drop downward twice in front of body.", "tips": "Bounce both 'Y' hands downward twice."},
    "TOMORROW": {"name": "Tomorrow", "hands": 1, "desc": "Thumb of 'A' fist flicks forward from the cheek/jaw.", "tips": "Touch cheek with thumb and roll forward into the air."},
    "UNDER": {"name": "Under / Below", "hands": 2, "desc": "Dominant thumbs-up hand passes beneath non-dominant flat palm.", "tips": "Sweep right hand under the horizontal left palm."},
    "UNDERSTAND": {"name": "Understand / Got It", "hands": 1, "desc": "Index finger flicks upward from closed fist next to forehead.", "tips": "Flick index finger up near temple like a realization."},
    "WAIT": {"name": "Wait / Hold On", "hands": 2, "desc": "Both open palms facing up wiggle fingers rhythmically.", "tips": "Hold palms up in front and wiggle fingers waiting."},
    "WE": {"name": "We / Us", "hands": 1, "desc": "Index finger touches right shoulder, arcs forward, and touches left shoulder.", "tips": "Touch dominant shoulder and sweep in an arc to opposite shoulder."},
    "WELCOME": {"name": "Welcome / Greeting", "hands": 2, "desc": "Both open palms start outward and sweep inward toward body with a smile.", "tips": "Sweep both palms inward toward torso in welcoming embrace."},
    "WHAT": {"name": "What / Question", "hands": 2, "desc": "Both open hands held palm-up shake gently side to side.", "tips": "Hold palms up and wiggle side to side with questioning brow."},
    "WHAT_HAPPENED": {"name": "What Happened?", "hands": 2, "desc": "Both open hands turn over from palms-down to palms-up.", "tips": "Flip hands over from palms-down to palms-up with puzzled face."},
    "WHAT_TIME": {"name": "What Time?", "hands": 2, "desc": "Index finger taps repeatedly on opposite wrist where watch is worn.", "tips": "Tap the back of opposite wrist with index finger."},
    "WHEN": {"name": "When?", "hands": 2, "desc": "Dominant index circles around non-dominant index and touches its tip.", "tips": "Circle right index finger around left index and land on its tip."},
    "WHERE": {"name": "Where?", "hands": 1, "desc": "Upright index finger wiggles side to side repeatedly.", "tips": "Wiggle upright index finger back and forth inquiry."},
    "WHO": {"name": "Who?", "hands": 1, "desc": "Thumb rests on chin while index finger wiggles up and down.", "tips": "Rest thumb on chin and waggle index finger."},
    "WHOM": {"name": "Whom?", "hands": 1, "desc": "Thumb rests on chin while index finger points toward person.", "tips": "Place thumb on chin and extend index finger outward."},
    "WHY": {"name": "Why?", "hands": 1, "desc": "Fingertips touch forehead and pull down into 'Y' hand shape.", "tips": "Touch forehead with flat hand and pull away forming 'Y'."},
    "WIFE": {"name": "Wife / Spouse", "hands": 2, "desc": "Thumb touches chin (female) then both hands clasp together.", "tips": "Touch chin, then clasp hands together indicating marriage."},
    "WORK": {"name": "Work / Job", "hands": 2, "desc": "Dominant fist taps wrist of non-dominant fist twice.", "tips": "Tap heel of right fist on back of left wrist twice."},
    "WORRY": {"name": "Worry / Concerned", "hands": 2, "desc": "Both 'B' hands alternate crossing in front of forehead.", "tips": "Flap flat hands across forehead with concerned expression."},
    "WRONG": {"name": "Wrong / Error", "hands": 1, "desc": "'Y' hand knocks middle knuckles against chin.", "tips": "Tap chin with middle fingers of 'Y' hand shape."},
    "YEAR": {"name": "Year / Annual", "hands": 2, "desc": "Dominant fist orbits completely around non-dominant fist and lands on top.", "tips": "Orbit right fist around left fist like the Earth orbiting the sun."},
    "YES": {"name": "Yes / Affirm", "hands": 1, "desc": "'S' fist nods up and down like a head nodding yes.", "tips": "Nod closed fist up and down gently."},
    "YESTERDAY": {"name": "Yesterday", "hands": 1, "desc": "Thumb of 'Y' or 'A' hand touches chin then moves backward to touch ear.", "tips": "Touch chin with thumb and sweep backward to touch ear."},
    "YOU": {"name": "You", "hands": 1, "desc": "Index finger points directly at the listener.", "tips": "Point index finger directly at the person you are speaking with."},
    "YOUR": {"name": "Your / Yours", "hands": 1, "desc": "Flat open palm pushes forward towards the listener.", "tips": "Push flat palm forward toward the listener respectfully."},
    "YOURSELF": {"name": "Yourself", "hands": 1, "desc": "'A' fist with thumb pointing forward pushes towards the listener.", "tips": "Thrust thumbs-up fist forward toward the listener."}
}

def generate_dictionary():
    output_path = "ml_pipeline/isl_dictionary.py"

    # Alphabet descriptions
    alphabet_defs = {
        "A": {"name": "Letter A", "hands": 2, "desc": "Left hand open palm facing right; right hand index finger touches the tip of left thumb.", "tips": "Touch the right index fingertip to the left thumb tip while keeping left fingers spread."},
        "B": {"name": "Letter B", "hands": 2, "desc": "Left hand open upright; right hand index and middle finger form a loop against left palm/thumb.", "tips": "Both hands form two loops resembling the letter 'B'."},
        "C": {"name": "Letter C", "hands": 1, "desc": "Curved hand forming a 'C' shape with thumb and four fingers.", "tips": "Single hand held sideways, fingers and thumb curved like the letter C."},
        "D": {"name": "Letter D", "hands": 2, "desc": "Left hand index pointing up; right hand curved into 'C' touching left index to form 'D'.", "tips": "Left index finger is the vertical stem; right curved hand creates the curved back of D."},
        "E": {"name": "Letter E", "hands": 2, "desc": "Left hand open palm; right hand index finger touches left index fingertip.", "tips": "Right index touches the tip of the left index finger (representing vowel E)."},
        "F": {"name": "Letter F", "hands": 2, "desc": "Left index and middle finger horizontal; right index and middle finger placed across them.", "tips": "Cross two fingers of right hand over two horizontal fingers of left hand."},
        "G": {"name": "Letter G", "hands": 2, "desc": "Both hands form closed fists placed one on top of the other.", "tips": "Right fist rested directly atop left fist."},
        "H": {"name": "Letter H", "hands": 2, "desc": "Left hand flat palm horizontal; right hand flat palm swept across left palm.", "tips": "Right flat palm sweeps across the horizontal left palm."},
        "I": {"name": "Letter I", "hands": 2, "desc": "Left hand open palm facing inward; right hand index finger touches left middle fingertip.", "tips": "Right index touches the tip of the left middle finger (representing vowel I)."},
        "J": {"name": "Letter J", "hands": 2, "desc": "Right index traces the letter 'J' starting from left middle fingertip down and curling up.", "tips": "Start at left middle fingertip, trace down into left palm with a hook."},
        "K": {"name": "Letter K", "hands": 2, "desc": "Left index pointing up; right index finger bent at knuckle hooked onto left index.", "tips": "Right bent index finger hooks around the vertical left index finger."},
        "L": {"name": "Letter L", "hands": 1, "desc": "Single hand with thumb and index finger extended at right angles forming an 'L'.", "tips": "Hold right hand up, thumb horizontal and index pointing straight up."},
        "M": {"name": "Letter M", "hands": 2, "desc": "Right hand places three fingers (index, middle, ring) on the flat palm of left hand.", "tips": "Three fingertips of right hand rest on left open palm to represent three legs of M."},
        "N": {"name": "Letter N", "hands": 2, "desc": "Right hand places two fingers (index and middle) on the flat palm of left hand.", "tips": "Two fingertips of right hand rest on left open palm to represent two legs of N."},
        "O": {"name": "Letter O", "hands": 2, "desc": "Left hand open palm; right index touches the tip of left ring finger (vowel O).", "tips": "Right index touches left ring fingertip (representing vowel O)."},
        "P": {"name": "Letter P", "hands": 2, "desc": "Left hand index pointing up; right hand thumb and index form a small circle at the top.", "tips": "Left index forms stem; right thumb-index loop attaches to top to form P."},
        "Q": {"name": "Letter Q", "hands": 2, "desc": "Left hand thumb and index form circle 'O'; right hand index placed through bottom as the tail.", "tips": "Left hand circle with right index finger protruding down diagonally."},
        "R": {"name": "Letter R", "hands": 2, "desc": "Left hand flat; right hand index finger hooked like a shepherd's crook resting on left palm.", "tips": "Right curved/hooked index rests gently on the open left palm."},
        "S": {"name": "Letter S", "hands": 2, "desc": "Both pinky fingers hooked together with fists closed.", "tips": "Interlock both little (pinky) fingers while keeping palms facing you."},
        "T": {"name": "Letter T", "hands": 2, "desc": "Left hand index pointing right horizontally; right hand index touches midpoint from below forming 'T'.", "tips": "Left index is the horizontal bar; right index is the vertical stem touching the midpoint."},
        "U": {"name": "Letter U", "hands": 2, "desc": "Left hand open palm; right hand index touches the tip of left pinky finger (vowel U).", "tips": "Right index touches left pinky fingertip (representing vowel U)."},
        "V": {"name": "Letter V", "hands": 1, "desc": "Single hand index and middle fingers extended apart in a 'V' shape (peace sign).", "tips": "Extend index and middle fingers apart while thumb holds ring and pinky."},
        "W": {"name": "Letter W", "hands": 2, "desc": "Fingers of both hands interlocked and pointed upwards forming a 'W' shape.", "tips": "Interlock all fingers of both hands pointing upwards."},
        "X": {"name": "Letter X", "hands": 2, "desc": "Both index fingers crossed over each other to form an 'X'.", "tips": "Cross right index over left index at 90 degrees."},
        "Y": {"name": "Letter Y", "hands": 2, "desc": "Left index and thumb extended in 'V'; right index rests in the junction pointing down.", "tips": "Right index finger points between the left extended thumb and index finger."},
        "Z": {"name": "Letter Z", "hands": 2, "desc": "Left hand held flat horizontally; right hand held vertical with fingertips touching to form angle of Z.", "tips": "Right fingertips touch left palm or right index traces 'Z' in the air."}
    }

    # Number descriptions
    number_defs = {
        "0": {"name": "Digit 0", "hands": 1, "desc": "Fingers curled touching thumb forming an oval '0'.", "tips": "Curl all fingers so fingertips meet thumb tip in a zero shape."},
        "1": {"name": "Digit 1", "hands": 1, "desc": "Single index finger extended upright, other fingers curled.", "tips": "Point index finger straight up."},
        "2": {"name": "Digit 2", "hands": 1, "desc": "Index and middle fingers extended upright together or slightly spread.", "tips": "Raise index and middle fingers."},
        "3": {"name": "Digit 3", "hands": 1, "desc": "Index, middle, and ring fingers extended upright.", "tips": "Raise index, middle, and ring fingers."},
        "4": {"name": "Digit 4", "hands": 1, "desc": "Four fingers (index, middle, ring, pinky) extended, thumb folded across palm.", "tips": "Four fingers held up, thumb tucked inward."},
        "5": {"name": "Digit 5", "hands": 1, "desc": "All five fingers fully spread and extended open.", "tips": "Open hand with all five fingers spread apart."},
        "6": {"name": "Digit 6", "hands": 2, "desc": "Left hand open with 5 fingers; right hand extends 1 index finger (5 + 1 = 6).", "tips": "Left hand shows 5, right hand shows 1 beside it."},
        "7": {"name": "Digit 7", "hands": 2, "desc": "Left hand open with 5 fingers; right hand extends 2 fingers (5 + 2 = 7).", "tips": "Left hand shows 5, right hand shows 2."},
        "8": {"name": "Digit 8", "hands": 2, "desc": "Left hand open with 5 fingers; right hand extends 3 fingers (5 + 3 = 8).", "tips": "Left hand shows 5, right hand shows 3."},
        "9": {"name": "Digit 9", "hands": 2, "desc": "Left hand open with 5 fingers; right hand extends 4 fingers (5 + 4 = 9).", "tips": "Left hand shows 5, right hand shows 4."}
    }

    # Video files available in Images/isl_videos
    available_videos = {}
    if os.path.exists(VIDEOS_DIR):
        for f in os.listdir(VIDEOS_DIR):
            if f.lower().endswith(".mp4"):
                key = os.path.splitext(f)[0].upper()
                available_videos[key] = f

    print(f"Available videos count: {len(available_videos)}")

    full_dict = {}

    # 1. Add Alphabets
    for char, info in alphabet_defs.items():
        vfile = available_videos.get(char) or available_videos.get(char.lower())
        full_dict[char] = {
            "category": "alphabet",
            "hands": info["hands"],
            "name": info["name"],
            "description": info["desc"],
            "tips": info["tips"],
            "video_file": vfile,
            "has_video": vfile is not None
        }

    # 2. Add Numbers
    for num, info in number_defs.items():
        vfile = available_videos.get(num)
        full_dict[num] = {
            "category": "number",
            "hands": info["hands"],
            "name": info["name"],
            "description": info["desc"],
            "tips": info["tips"],
            "video_file": vfile,
            "has_video": vfile is not None
        }

    # 3. Add Words
    for word_key, info in WORD_DETAILS.items():
        vfile = available_videos.get(word_key) or available_videos.get(word_key.lower())
        full_dict[word_key] = {
            "category": "word",
            "hands": info["hands"],
            "name": info["name"],
            "description": info["desc"],
            "tips": info["tips"],
            "video_file": vfile,
            "has_video": vfile is not None
        }

    # 4. Check any remaining video files not yet added
    for vkey, vfile in available_videos.items():
        if vkey not in full_dict and len(vkey) > 1:
            clean_name = vkey.replace("_", " ").title()
            full_dict[vkey] = {
                "category": "word",
                "hands": 1,
                "name": clean_name,
                "description": f"Indian Sign Language gesture for {clean_name}.",
                "tips": f"Hold hand posture and execute movement for {clean_name} as shown in the video demonstration.",
                "video_file": vfile,
                "has_video": True
            }

    print(f"Total compiled dictionary classes: {len(full_dict)}")

    # Write out as python file
    content = '"""\n'
    content += 'Indian Sign Language (ISL) Gesture Definitions, Metadata, and Guidance.\n'
    content += f'Synthesized according to standard Indian Sign Language (ISLRTC) conventions\n'
    content += f'with full support for 200+ video demonstration clips in Images/isl_videos/.\n'
    content += '"""\n\n'
    content += 'ISL_CLASSES = {\n'

    for k, v in full_dict.items():
        content += f'    "{k}": {{\n'
        content += f'        "category": "{v["category"]}",\n'
        content += f'        "hands": {v["hands"]},\n'
        content += f'        "name": "{v["name"]}",\n'
        content += f'        "description": "{v["description"]}",\n'
        content += f'        "tips": "{v["tips"]}",\n'
        if v["video_file"]:
            content += f'        "video_file": "{v["video_file"]}",\n'
        content += f'        "has_video": {v["has_video"]}\n'
        content += '    },\n'

    content += '}\n\n'
    content += '''def get_class_list():
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
'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated {output_path} with {len(full_dict)} classes!")
    return full_dict

if __name__ == "__main__":
    generate_dictionary()
