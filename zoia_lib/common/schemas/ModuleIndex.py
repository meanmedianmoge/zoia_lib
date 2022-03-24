# format:
# {
#   module type: {
#     name, # default module name
#     category, # module category
#     description, # module description
#     default blocks, # number of blocks that appear by default
#     min blocks, # min number of blocks a module can use
#     max blocks, # max number of blocks a module can use
#     params, # number of adjustable CV jacks
#     cpu # average amount of CPU (this doesn't factor in matrix DSP)
#     blocks, # list of all blocks the module can use
#     options, # module options, list of each
#   }
# }

import json

module_index = {
    0: {
        "name": "SV Filter",
        "category": "Audio",
        "description": """
            The State Variable Filter will resonate and cutoff around a set frequency.
        """,
        "default_blocks": 4,
        "min_blocks": 3,
        "max_blocks": 6,
        "params": 2,
        "cpu": 3,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "frequency": {"isDefault": True, "isParam": True, "position": 1},
            "resonance": {"isDefault": True, "isParam": True, "position": 2},
            "lowpass_output": {"isDefault": True, "isParam": False, "position": 3},
            "hipass_output": {"isDefault": False, "isParam": False, "position": 4},
            "bandpass_output": {"isDefault": False, "isParam": False, "position": 5},
        },
        "options": {
            "lowpass_output": ["on", "off"],
            "hipass_output": ["off", "on"],
            "bandpass_output": ["off", "on"],
            "freq_change": ["smooth", "instant"],
        },
    },
    1: {
        "name": "Audio Input",
        "category": "Interface",
        "description": """
            Connect audio from the outside world into the grid.
            This could be a guitar, bass, synth module, computer Audio, etc
        """,
        "default_blocks": 2,
        "min_blocks": 1,
        "max_blocks": 2,
        "params": 0,
        "cpu": 0.4,
        "blocks": {
            "output_L": {"isDefault": True, "isParam": False, "position": 0},
            "output_R": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {"channels": ["stereo", "left", "right"]},
    },
    2: {
        "name": "Audio Output",
        "category": "Interface",
        "description": """
            Connect audio from your ZOIA into the outside world.
            Connect to your amplifier, a DI box, your audio interface, etc.
            An optional gain control lets you tweak the output level.
        """,
        "default_blocks": 2,
        "min_blocks": 1,
        "max_blocks": 3,
        "params": 1,
        "cpu": 1.7,
        "blocks": {
            "input_L": {"isDefault": True, "isParam": False, "position": 0},
            "input_R": {"isDefault": True, "isParam": False, "position": 1},
            "gain": {"isDefault": False, "isParam": True, "position": 2},
        },
        "options": {
            "gain_control": ["off", "on"],
            "channels": ["stereo", "left", "right"],
        },
    },
    3: {
        "name": "Aliaser",
        "category": "Audio",
        "description": """
            Aliaser produces samples of incoming audio and compares them against each other to find imperfections.
            These imperfections become the outgoing audio.
            As sample count grows, so too does the thickness of the outgoing sound.
            This effect is a signal hog so be sure to boost your connection strengths incoming and outgoing.
            Try connecting a LFO or envelope follower to the alias amount.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "cpu": 0.7,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "#_of_samples": {"isDefault": True, "isParam": True, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {},
    },
    4: {
        "name": "Sequencer",
        "category": "CV",
        "description": """
            The sequencer allows you to create a number of "steps" (1-32) that can be cycled through,
            and each step can be used to send a CV value out of that tracks output.
            The sequencer can have up to 8 tracks, each with their own unique output.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 42,
        "params": 34,
        "cpu": 2,
        "blocks": {
            "step_1": {"isDefault": True, "isParam": True, "position": 0},
            "step_2": {"isDefault": False, "isParam": True, "position": 1},
            "step_3": {"isDefault": False, "isParam": True, "position": 2},
            "step_4": {"isDefault": False, "isParam": True, "position": 3},
            "step_5": {"isDefault": False, "isParam": True, "position": 4},
            "step_6": {"isDefault": False, "isParam": True, "position": 5},
            "step_7": {"isDefault": False, "isParam": True, "position": 6},
            "step_8": {"isDefault": False, "isParam": True, "position": 7},
            "step_9": {"isDefault": False, "isParam": True, "position": 8},
            "step_10": {"isDefault": False, "isParam": True, "position": 9},
            "step_11": {"isDefault": False, "isParam": True, "position": 10},
            "step_12": {"isDefault": False, "isParam": True, "position": 11},
            "step_13": {"isDefault": False, "isParam": True, "position": 12},
            "step_14": {"isDefault": False, "isParam": True, "position": 13},
            "step_15": {"isDefault": False, "isParam": True, "position": 14},
            "step_16": {"isDefault": False, "isParam": True, "position": 15},
            "step_17": {"isDefault": False, "isParam": True, "position": 16},
            "step_18": {"isDefault": False, "isParam": True, "position": 17},
            "step_19": {"isDefault": False, "isParam": True, "position": 18},
            "step_20": {"isDefault": False, "isParam": True, "position": 19},
            "step_21": {"isDefault": False, "isParam": True, "position": 20},
            "step_22": {"isDefault": False, "isParam": True, "position": 21},
            "step_23": {"isDefault": False, "isParam": True, "position": 22},
            "step_24": {"isDefault": False, "isParam": True, "position": 23},
            "step_25": {"isDefault": False, "isParam": True, "position": 24},
            "step_26": {"isDefault": False, "isParam": True, "position": 25},
            "step_27": {"isDefault": False, "isParam": True, "position": 26},
            "step_28": {"isDefault": False, "isParam": True, "position": 27},
            "step_29": {"isDefault": False, "isParam": True, "position": 28},
            "step_30": {"isDefault": False, "isParam": True, "position": 29},
            "step_31": {"isDefault": False, "isParam": True, "position": 30},
            "step_32": {"isDefault": False, "isParam": True, "position": 31},
            "gate_in": {"isDefault": True, "isParam": True, "position": 32},
            "queue_start": {"isDefault": False, "isParam": True, "position": 33},
            "out_track_1": {"isDefault": True, "isParam": False, "position": 34},
            "out_track_2": {"isDefault": False, "isParam": False, "position": 35},
            "out_track_3": {"isDefault": False, "isParam": False, "position": 36},
            "out_track_4": {"isDefault": False, "isParam": False, "position": 37},
            "out_track_5": {"isDefault": False, "isParam": False, "position": 38},
            "out_track_6": {"isDefault": False, "isParam": False, "position": 39},
            "out_track_7": {"isDefault": False, "isParam": False, "position": 40},
            "out_track_8": {"isDefault": False, "isParam": False, "position": 41},
        },
        "options": {
            "number_of_steps": list(range(1, 33)),
            "num_of_tracks": list(range(1, 9)),
            "restart_jack": ["off", "on"],
            "behavior": ["loop", "once"],
        },
    },
    5: {
        "name": "LFO",
        "category": "CV",
        "description": """
            The Low Frequency Oscillator is one of the workhorse modules of the ZOIA.
            This will generate CV in the waveform and range of your choosing.
            Connect it to a sequencer to cycle through steps, to an audio effect to
            swing it's parameters around, or to any outboard piece of gear through a
            MIDI or CV interface module.
            The connection strength you enter at the output will determine the maximum
            sweep of the LFO.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 5,
        "params": 4,
        "cpu": 0.3,
        "blocks": {
            "cv_control": {"isDefault": True, "isParam": True, "position": 0},
            "tap_control": {"isDefault": False, "isParam": True, "position": 1},
            "swing_amount": {"isDefault": False, "isParam": True, "position": 2},
            "phase_input": {"isDefault": False, "isParam": True, "position": 4},
            "phase_reset": {"isDefault": False, "isParam": True, "position": 5},
            "output": {"isDefault": True, "isParam": False, "position": 3},
        },
        "options": {
            "waveform": ["square", "sine", "triangle", "sawtooth", "ramp", "random"],
            "swing_control": ["off", "on"],
            "output": ["0 to 1", "-1 to 1"],
            "input": ["cv", "tap", "linear_cv"],
            "phase_input": ["off", "on"],
            "phase_reset": ["off", "on"],
        },
    },
    6: {
        "name": "ADSR",
        "category": "CV",
        "description": """
            The Attack Decay Sustain Release module is what gives a note generated
            from an oscillator a natural sounding envelope when played from a keyboard.
            Connect your oscillator or other audio source to the input of a VCA,
            and connect the CV output of the ADSR to the CV input on the VCA.
            Connect the keyboard or MIDI note gate out to the CV input of the ADSR
            and you've got yourself a simple synthesizer!
            Tweak the values to taste, or connect them to other CV inputs for experimentation.
            Use the optional retrigger input to restart the envelope around a note
            that is played before the ADSR is released.
        """,
        "default_blocks": 6,
        "min_blocks": 4,
        "max_blocks": 10,
        "params": 9,
        "cpu": 0.07,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "retrigger": {"isDefault": False, "isParam": True, "position": 1},
            "delay": {"isDefault": False, "isParam": True, "position": 2},
            "attack": {"isDefault": True, "isParam": True, "position": 3},
            "hold_attack_decay": {"isDefault": False, "isParam": True, "position": 4},
            "decay": {"isDefault": True, "isParam": True, "position": 5},
            "sustain": {"isDefault": True, "isParam": True, "position": 6},
            "hold_sustain_release": {"isDefault": False, "isParam": True, "position": 7},
            "release": {"isDefault": True, "isParam": True, "position": 8},
            "cv_output": {"isDefault": True, "isParam": False, "position": 9},
        },
        "options": {
            "retrigger_input": ["off", "on"],
            "initial_delay": ["off", "on"],
            "hold_attack_decay": ["off", "on"],
            "str": ["on", "off"],
            "immediate_release": ["on", "off"],
            "hold_sustain_release": ["off", "on"],
            "time_scale": ["exponent", "linear"],
        },
    },
    7: {
        "name": "VCA",
        "category": "Audio",
        "description": """
            The Voltage Controlled Amplifier module will interpret incoming CV at the
            level control and boost or cut the volume.
            Connect an ADSR to create a natural sounding envelope for an oscillator passing through.
            Connect an LFO to create a tremolo effect.
            Or connect an expression pedal module or MIDI input for an external volume control.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 5,
        "params": 1,
        "cpu": 0.7,
        "blocks": {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_2": {"isDefault": False, "isParam": False, "position": 1},
            "level_control": {"isDefault": True, "isParam": True, "position": 2},
            "audio_out_1": {"isDefault": True, "isParam": False, "position": 3},
            "audio_out_2": {"isDefault": False, "isParam": False, "position": 4},
        },
        "options": {"channels": ["1in->1out", "stereo"]},
    },
    8: {
        "name": "Audio Multiply",
        "category": "Audio",
        "description": """
            Takes one audio input and mathematically multiplies it with the other.
            This produces a ring mod/vocoder-like effect.
            This module likes hot signals to be sure to bump the connection strengths.
            Remember that silence at any one of the inputs will result in silence at the output!
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 0,
        "cpu": 0.4,
        "blocks": {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_2": {"isDefault": True, "isParam": False, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {},
    },
    9: {
        "name": "Bit Crusher",
        "category": "Audio",
        "description": """
            Bit Crusher produces distortion by reducing audio bandwidth by a set number of bits.
            Distortion becomes audible around 20 bits reduced.
            This effect can get noisy so try it with a gate.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "cpu": 1,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "crushed_bits": {"isDefault": True, "isParam": True, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {"fractions": ["off", "on"]},
    },
    10: {
        "name": "Sample and Hold",
        "category": "CV",
        "description": """
            Sample and Hold will take the CV value at the input and hold it in place
            at the output until triggered to look again at the input and update the output.
            Connect a LFO to the trigger to convert smooth changes in CV into stepped changes in CV.
            The speed of the LFO will determine the perceived resolution of the CV output.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "cpu": 0.1,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "trigger": {"isDefault": True, "isParam": True, "position": 1},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {"track & hold": ["off", "on"]},
    },
    11: {
        "name": "OD and Distortion",
        "category": "Effect",
        "description": """
            The OD & Distortion module provides classic overdrive and distortion tones.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 4,
        "params": 2,
        "cpu": 17,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "input_gain": {"isDefault": True, "isParam": True, "position": 1},
            "output_gain": {"isDefault": True, "isParam": True, "position": 3},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {"model": ["plexi", "germ", "classic", "pushed", "edgy"]},
    },
    12: {
        "name": "Env Follower",
        "category": "Analysis",
        "description": """
            Envelope Follower will interpret an incoming audio signal as a CV signal
            based on its signal strength.
            Use this to trigger filter sweeps, audio effects parameters, LFO rates, etc.
            The connection strength can act as a sensitivity control.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 4,
        "params": 2,
        "cpu": 5,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "rise_time": {"isDefault": False, "isParam": True, "position": 1},
            "fall_time": {"isDefault": False, "isParam": True, "position": 2},
            "cv_output": {"isDefault": True, "isParam": False, "position": 3},
        },
        "options": {"rise_fall_time": ["off", "on"], "output_scale": ["log", "linear"]},
    },
    13: {
        "name": "Delay Line",
        "category": "Audio",
        "description": """
            The Delay Line is a simple module that takes audio at the input and
            delays it by a set amount of time.
            There is no dry signal, there are no repeats.
            You can create repeats by connecting the output back to the input,
            using the connection strength to adjust number of repeats.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 4,
        "params": 3,
        "cpu": 3,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "delay_time": {"isDefault": True, "isParam": True, "position": 1},
            "modulation_in": {"isDefault": False, "isParam": True, "position": 2},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3},
            "audio_out": {"isDefault": True, "isParam": False, "position": 4},
        },
        "options": {
            "max_time": ["1s", "2s", "4s", "8s", "16s", "100ms"],
            "tap_tempo_in": ["no", "yes"],
            "interpolation": ["on", "off"],
            "CV Input": ["exponent", "linear"],
        },
    },
    14: {
        "name": "Oscillator",
        "category": "Audio",
        "description": """
            Generates an audio signal in the waveform of your choice.
            Connect a MIDI device, keyboard module, sequencer, pitch detector,
            LFO, or any CV source to select the frequency or note the oscillator will play.
            You can modulate the frequency or pulse width with the optional parameters.
            Negative CV inputs (from -1 to 0) will generate sub-bass frequencies
            between 0.027Hz and 27.49Hz. Be careful!
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 4,
        "params": 2,
        "cpu": 10,
        "blocks": {
            "frequency": {"isDefault": True, "isParam": True, "position": 0},
            "fm_input": {"isDefault": False, "isParam": False, "position": 1},
            "duty_cycle": {"isDefault": False, "isParam": True, "position": 2},
            "audio_out": {"isDefault": True, "isParam": False, "position": 3},
        },
        "options": {
            "waveform": ["sine", "square", "triangle", "sawtooth"],
            "fm_in": ["off", "on"],
            "duty_cycle": ["off", "on"],
            "upsampling": ["none", "2x"],
        },
    },
    15: {
        "name": "Pushbutton",
        "category": "Interface",
        "description": """
            Turns a grid button into a button you can push to send a CV signal.
            Tap in a tempo, open up a VCA, trigger a sequencer, or anything else.
            The grid is your oyster!
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.02,
        "blocks": {"cv_output": {"isDefault": True, "isParam": False, "position": 1}},
        "options": {
            "action": ["momentary", "latching"],
            "normally": ["zero", "one"]
        },
    },
    16: {
        "name": "Keyboard",
        "category": "Interface",
        "description": """
            Turns grid buttons into a keyboard you can connect to an oscillator and play.
            No external MIDI controller necessary!
            Tune each keyboard button using the knob to have it play your desired note.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 43,
        "params": 40,
        "cpu": 0.1,
        "blocks": {
            "note_1": {"isDefault": True, "isParam": True, "position": 0},
            "note_2": {"isDefault": False, "isParam": True, "position": 1},
            "note_3": {"isDefault": False, "isParam": True, "position": 2},
            "note_4": {"isDefault": False, "isParam": True, "position": 3},
            "note_5": {"isDefault": False, "isParam": True, "position": 4},
            "note_6": {"isDefault": False, "isParam": True, "position": 5},
            "note_7": {"isDefault": False, "isParam": True, "position": 6},
            "note_8": {"isDefault": False, "isParam": True, "position": 7},
            "note_9": {"isDefault": False, "isParam": True, "position": 8},
            "note_10": {"isDefault": False, "isParam": True, "position": 9},
            "note_11": {"isDefault": False, "isParam": True, "position": 10},
            "note_12": {"isDefault": False, "isParam": True, "position": 11},
            "note_13": {"isDefault": False, "isParam": True, "position": 12},
            "note_14": {"isDefault": False, "isParam": True, "position": 13},
            "note_15": {"isDefault": False, "isParam": True, "position": 14},
            "note_16": {"isDefault": False, "isParam": True, "position": 15},
            "note_17": {"isDefault": False, "isParam": True, "position": 16},
            "note_18": {"isDefault": False, "isParam": True, "position": 17},
            "note_19": {"isDefault": False, "isParam": True, "position": 18},
            "note_20": {"isDefault": False, "isParam": True, "position": 19},
            "note_21": {"isDefault": False, "isParam": True, "position": 20},
            "note_22": {"isDefault": False, "isParam": True, "position": 21},
            "note_23": {"isDefault": False, "isParam": True, "position": 22},
            "note_24": {"isDefault": False, "isParam": True, "position": 23},
            "note_25": {"isDefault": False, "isParam": True, "position": 24},
            "note_26": {"isDefault": False, "isParam": True, "position": 28},
            "note_27": {"isDefault": False, "isParam": True, "position": 29},
            "note_28": {"isDefault": False, "isParam": True, "position": 30},
            "note_29": {"isDefault": False, "isParam": True, "position": 31},
            "note_30": {"isDefault": False, "isParam": True, "position": 32},
            "note_31": {"isDefault": False, "isParam": True, "position": 33},
            "note_32": {"isDefault": False, "isParam": True, "position": 34},
            "note_33": {"isDefault": False, "isParam": True, "position": 35},
            "note_34": {"isDefault": False, "isParam": True, "position": 36},
            "note_35": {"isDefault": False, "isParam": True, "position": 37},
            "note_36": {"isDefault": False, "isParam": True, "position": 38},
            "note_37": {"isDefault": False, "isParam": True, "position": 39},
            "note_38": {"isDefault": False, "isParam": True, "position": 40},
            "note_39": {"isDefault": False, "isParam": True, "position": 41},
            "note_40": {"isDefault": False, "isParam": True, "position": 42},
            "note_out": {"isDefault": True, "isParam": False, "position": 25},
            "gate_out": {"isDefault": True, "isParam": False, "position": 26},
            "trigger_out": {"isDefault": True, "isParam": False, "position": 27},
        },
        "options": {"#_of_notes": list(range(1, 41))},
    },
    17: {
        "name": "CV Invert",
        "category": "CV",
        "description": """
            Inverts the incoming CV.
            For example, a CV input of 1 will output as -1.
            An input of 0.2 will output as -0.2. 	
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.02,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {},
    },
    18: {
        "name": "Steps",
        "category": "CV",
        "description": """
            Steps will interpret incoming changes in upward CV as a tempo, split the wave
            cycle into a set number of steps, and then send the CV present at the input
            during each step to the output.
            You can use this to convert a nice smooth LFO and reduce its resolution into steps.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "cpu": 0.7,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "quant_steps": {"isDefault": True, "isParam": True, "position": 1},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {},
    },
    19: {
        "name": "Slew Limiter",
        "category": "CV",
        "description": """
            Slew Limiter is similar in behaviour to CV Filter except that the rate of
            change in changes of CV happen linearly instead of logarithmically.
            This is the classic portamento, and can be used anywhere CV changes occur
            to give them a different feel.
            Try using an unlinked Slew Limiter with a stomp switch module to give more
            expression pedal-like behaviour to your stomp switch.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 4,
        "params": 2,
        "cpu": 0.2,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "slew_rate": {"isDefault": True, "isParam": True, "position": 1},
            "rising_lag": {"isDefault": False, "isParam": True, "position": 2},
            "falling_lag": {"isDefault": False, "isParam": True, "position": 3},
            "cv_output": {"isDefault": True, "isParam": False, "position": 4},
        },
        "options": {
            "control": ["linked", "separate"],
        },
    },
    20: {
        "name": "Midi Notes In",
        "category": "Interface",
        "description": """
            Connect your MIDI keyboard controller to the ZOIA.
            Connect the note out to an oscillator to have it play your note,
            and connect the gate out to an ADSR (connected to a VCA) for a natural envelope. 
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 32,
        "params": 0,
        "cpu": 0.3,
        "blocks": {
            "note_out_1": {"isDefault": True, "isParam": False, "position": 0},
            "gate_out_1": {"isDefault": True, "isParam": False, "position": 1},
            "velocity_out_1": {"isDefault": False, "isParam": False, "position": 2},
            "trigger_out_1": {"isDefault": False, "isParam": False, "position": 3},
            "note_out_2": {"isDefault": False, "isParam": False, "position": 4},
            "gate_out_2": {"isDefault": False, "isParam": False, "position": 5},
            "velocity_out_2": {"isDefault": False, "isParam": False, "position": 6},
            "trigger_out_2": {"isDefault": False, "isParam": False, "position": 7},
            "note_out_3": {"isDefault": False, "isParam": False, "position": 8},
            "gate_out_3": {"isDefault": False, "isParam": False, "position": 9},
            "velocity_out_3": {"isDefault": False, "isParam": False, "position": 10},
            "trigger_out_3": {"isDefault": False, "isParam": False, "position": 11},
            "note_out_4": {"isDefault": False, "isParam": False, "position": 12},
            "gate_out_4": {"isDefault": False, "isParam": False, "position": 13},
            "velocity_out_4": {"isDefault": False, "isParam": False, "position": 14},
            "trigger_out_4": {"isDefault": False, "isParam": False, "position": 15},
            "note_out_5": {"isDefault": False, "isParam": False, "position": 16},
            "gate_out_5": {"isDefault": False, "isParam": False, "position": 17},
            "velocity_out_5": {"isDefault": False, "isParam": False, "position": 18},
            "trigger_out_5": {"isDefault": False, "isParam": False, "position": 19},
            "note_out_6": {"isDefault": False, "isParam": False, "position": 20},
            "gate_out_6": {"isDefault": False, "isParam": False, "position": 21},
            "velocity_out_6": {"isDefault": False, "isParam": False, "position": 22},
            "trigger_out_6": {"isDefault": False, "isParam": False, "position": 23},
            "note_out_7": {"isDefault": False, "isParam": False, "position": 24},
            "gate_out_7": {"isDefault": False, "isParam": False, "position": 25},
            "velocity_out_7": {"isDefault": False, "isParam": False, "position": 26},
            "trigger_out_7": {"isDefault": False, "isParam": False, "position": 27},
            "note_out_8": {"isDefault": False, "isParam": False, "position": 28},
            "gate_out_8": {"isDefault": False, "isParam": False, "position": 29},
            "velocity_out_8": {"isDefault": False, "isParam": False, "position": 30},
            "trigger_out_8": {"isDefault": False, "isParam": False, "position": 31},
        },
        "options": {
            "midi_channel": list(range(1, 17)),
            "#_of_outputs": list(range(1, 9)),
            "priority": ["newest", "oldest", "highest", "lowest", "RoundRobin"],
            "greedy": ["no", "yes"],
            "velocity_output": ["off", "on"],
            "low_note": list(range(0, 128)),
            "high_note": list(range(0, 128))[::-1],
            "trigger_pulse": ["off", "on"],
        },
    },
    21: {
        "name": "Midi CC In",
        "category": "Interface",
        "description": """
            Connect encoder knobs and sliders on a MIDI interface.
            Take note of the outgoing CC number of each control and enter it into the controller option.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {"cc_out": {"isDefault": True, "isParam": False, "position": 0}},
        "options": {
            "midi_channel": list(range(1, 17)),
            "controller": list(range(0, 128)),
            "output_range": ["0 to 1", "-1 to 1"],
        },
    },
    22: {
        "name": "Multiplier",
        "category": "CV",
        "description": """
            Multiply will take the CV signal present at each input and multiply
            them together at the output.
            In this way you can use one CV source to amplify, tame, or modulate another.
            Remember that a value of 0 at any input will result in 0 at the output.
            It's math!
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 9,
        "params": 2,
        "cpu": 0.2,
        "blocks": {
            "cv_input_1": {"isDefault": True, "isParam": True, "position": 0},
            "cv_input_2": {"isDefault": True, "isParam": True, "position": 1},
            "cv_input_3": {"isDefault": False, "isParam": True, "position": 2},
            "cv_input_4": {"isDefault": False, "isParam": True, "position": 3},
            "cv_input_5": {"isDefault": False, "isParam": True, "position": 4},
            "cv_input_6": {"isDefault": False, "isParam": True, "position": 5},
            "cv_input_7": {"isDefault": False, "isParam": True, "position": 6},
            "cv_input_8": {"isDefault": False, "isParam": True, "position": 7},
            "cv_output": {"isDefault": True, "isParam": False, "position": 8},
        },
        "options": {"num_inputs": list(range(2, 9))},
    },
    23: {
        "name": "Compressor",
        "category": "Effect",
        "description": """
            Compression is a vastly useful audio tool that controls your signal level
            according to changes in input level.
            You can create natural reductions in gain to help things mix better, help
            tame or enhance transients in synth or instrument signals, etc.
            The optional stereo side will trigger the module's functions in unison on both
            channels, creating true stereo compression.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 9,
        "params": 4,
        "cpu": 3,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "threshold": {"isDefault": True, "isParam": True, "position": 2},
            "attack": {"isDefault": False, "isParam": True, "position": 3},
            "release": {"isDefault": False, "isParam": True, "position": 4},
            "ratio": {"isDefault": False, "isParam": True, "position": 5},
            "sidechain_in": {"isDefault": False, "isParam": False, "position": 8},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7},
        },
        "options": {
            "attack_ctrl": ["off", "on"],
            "release_ctrl": ["off", "on"],
            "ratio_ctrl": ["off", "on"],
            "channels": ["1in->1out", "stereo"],
            "sidechain": ["internal", "external"],
        },
    },
    24: {
        "name": "Multi Filter",
        "category": "Audio",
        "description": """
            A general purpose filter with gain, frequency, and Q controls.
            Configurable as a high pass, low pass, band pass, bell, hi shelf, or low shelf.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 5,
        "params": 3,
        "cpu": 0.8,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "gain": {"isDefault": False, "isParam": True, "position": 1},
            "frequency": {"isDefault": True, "isParam": True, "position": 2},
            "q": {"isDefault": True, "isParam": True, "position": 3},
            "audio_out": {"isDefault": True, "isParam": False, "position": 4},
        },
        "options": {
            "filter_shape": [
                "lowpass",
                "highpass",
                "bandpass",
                "bell",
                "hi_shelf",
                "low_shelf",
            ],
        },
    },
    25: {
        "name": "Plate Reverb",
        "category": "Effect",
        "description": """
            Bask in the ebb and flow of steel molecules as they vibrate with the warm vintage
            vibe of so many classic recordings.
        """,
        "default_blocks": 8,
        "min_blocks": 8,
        "max_blocks": 8,
        "params": 4,
        "cpu": 22,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": True, "isParam": False, "position": 1},
            "decay_time": {"isDefault": True, "isParam": True, "position": 3},
            "low_eq": {"isDefault": True, "isParam": True, "position": 6},
            "high_eq": {"isDefault": True, "isParam": True, "position": 7},
            "mix": {"isDefault": True, "isParam": True, "position": 2},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 4},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 5},
        },
        "options": {},
    },
    26: {
        "name": "Buffer Delay",
        "category": "Audio",
        "description": """
            Delays internal audio signal by N buffer(s).
            This module is inaudible, but useful anywhere you need to line up
            internal parallel audio connections precisely.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 0,
        "cpu": 0.2,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "audio_out": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {"buffer_length": list(range(0, 17))},
    },
    27: {
        "name": "All Pass Filter",
        "category": "Audio",
        "description": """
            All Pass Filter passes through all frequencies at equal gain,
            but changes phase relationship between them.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "cpu": 5,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "filter_gain": {"isDefault": True, "isParam": True, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {"#_of_poles": list(range(1, 9))},
    },
    28: {
        "name": "Quantizer",
        "category": "CV",
        "description": """
            Quantizer will interpret incoming CV and send its nearest equivalent note as a CV output.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 4,
        "params": 3,
        "cpu": 1,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "key": {"isDefault": False, "isParam": True, "position": 2},
            "scale": {"isDefault": False, "isParam": True, "position": 3},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {
            "key_scale_jacks": ["no", "yes"],
            "scales": ["basic", "extended"],
        },
    },
    29: {
        "name": "Phaser",
        "category": "Effect",
        "description": """
            Set to stun, Phaser shifts the phase over a set quantity of stages and
            sweeps the frequency of these poles at a set rate.
            An optional stereo channel rounds out the list of features. 
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "cpu": 15,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "rate": {"isDefault": True, "isParam": True, "position": 3},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 7},
            "control_in": {"isDefault": False, "isParam": True, "position": 8},
            "resonance": {"isDefault": True, "isParam": True, "position": 4},
            "width": {"isDefault": True, "isParam": True, "position": 9},
            "mix": {"isDefault": True, "isParam": True, "position": 2},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 5},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 6},
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "2in->2out"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "number_of_stages": [4, 2, 1, 3, 6, 8],
        },
    },
    30: {
        "name": "Looper",
        "category": "Audio",
        "description": """
            The Looper module allows you to record, overdub, and play back incoming audio,
            forwards or backwards, at the speed of your choice (pitch shifted).
            Get loopy!
        """,
        "default_blocks": 5,
        "min_blocks": 5,
        "max_blocks": 10,
        "params": 6,
        "cpu": 3,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "record": {"isDefault": True, "isParam": True, "position": 1},
            "restart_playback": {"isDefault": True, "isParam": True, "position": 2},
            "stop_play": {"isDefault": False, "isParam": True, "position": 9},
            "speed_pitch": {"isDefault": True, "isParam": True, "position": 3},
            "start_position": {"isDefault": False, "isParam": True, "position": 4},
            "loop_length": {"isDefault": False, "isParam": True, "position": 5},
            "reverse_playback": {"isDefault": False, "isParam": True, "position": 7},
            "reset": {"isDefault": False, "isParam": True, "position": 8},
            "audio_out": {"isDefault": True, "isParam": False, "position": 6},
        },
        "options": {
            "max_rec_time": ["1s", "2s", "4s", "8s", "16s", "32s"],
            "length_edit": ["off", "on"],
            "playback": ["once", "loop"],
            "length": ["fixed", "pre_speed"],
            "hear_while_rec": ["no", "yes"],
            "play_reverse": ["no", "yes"],
            "overdub": ["no", "yes"],
            "stop_play_button": ["no", "yes"],
        },
    },
    31: {
        "name": "In Switch",
        "category": "CV",
        "description": """
            In Switch takes a selected quantity of CV inputs and allows you
            to switch between them to a single CV output.
            You can use this to select between LFOs to a CV source, external CV modules,
            or use in conjunction with the CV out switch to choose between ADSRs
            or other CV module chains
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 18,
        "params": 17,
        "cpu": 0.2,
        "blocks": {
            "cv_input_1": {"isDefault": True, "isParam": True, "position": 0},
            "cv_input_2": {"isDefault": False, "isParam": True, "position": 1},
            "cv_input_3": {"isDefault": False, "isParam": True, "position": 2},
            "cv_input_4": {"isDefault": False, "isParam": True, "position": 3},
            "cv_input_5": {"isDefault": False, "isParam": True, "position": 4},
            "cv_input_6": {"isDefault": False, "isParam": True, "position": 5},
            "cv_input_7": {"isDefault": False, "isParam": True, "position": 6},
            "cv_input_8": {"isDefault": False, "isParam": True, "position": 7},
            "cv_input_9": {"isDefault": False, "isParam": True, "position": 8},
            "cv_input_10": {"isDefault": False, "isParam": True, "position": 9},
            "cv_input_11": {"isDefault": False, "isParam": True, "position": 10},
            "cv_input_12": {"isDefault": False, "isParam": True, "position": 11},
            "cv_input_13": {"isDefault": False, "isParam": True, "position": 12},
            "cv_input_14": {"isDefault": False, "isParam": True, "position": 13},
            "cv_input_15": {"isDefault": False, "isParam": True, "position": 14},
            "cv_input_16": {"isDefault": False, "isParam": True, "position": 15},
            "in_select": {"isDefault": True, "isParam": True, "position": 16},
            "cv_output": {"isDefault": True, "isParam": False, "position": 17},
        },
        "options": {"num_inputs": list(range(1, 17))},
    },
    32: {
        "name": "Out Switch",
        "category": "CV",
        "description": """
            Out Switch takes a CV input and routes it between a set quantity of CV outputs.
            You can use it to select which sequencers, ADSRs, or tap tempos to send triggers to, etc
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 18,
        "params": 2,
        "cpu": 0.2,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "out_select": {"isDefault": True, "isParam": True, "position": 1},
            "cv_output_1": {"isDefault": True, "isParam": False, "position": 2},
            "cv_output_2": {"isDefault": False, "isParam": False, "position": 3},
            "cv_output_3": {"isDefault": False, "isParam": False, "position": 4},
            "cv_output_4": {"isDefault": False, "isParam": False, "position": 5},
            "cv_output_5": {"isDefault": False, "isParam": False, "position": 6},
            "cv_output_6": {"isDefault": False, "isParam": False, "position": 7},
            "cv_output_7": {"isDefault": False, "isParam": False, "position": 8},
            "cv_output_8": {"isDefault": False, "isParam": False, "position": 9},
            "cv_output_9": {"isDefault": False, "isParam": False, "position": 10},
            "cv_output_10": {"isDefault": False, "isParam": False, "position": 11},
            "cv_output_11": {"isDefault": False, "isParam": False, "position": 12},
            "cv_output_12": {"isDefault": False, "isParam": False, "position": 13},
            "cv_output_13": {"isDefault": False, "isParam": False, "position": 14},
            "cv_output_14": {"isDefault": False, "isParam": False, "position": 15},
            "cv_output_15": {"isDefault": False, "isParam": False, "position": 16},
            "cv_output_16": {"isDefault": False, "isParam": False, "position": 17},
        },
        "options": {"num_outputs": list(range(1, 17))},
    },
    33: {
        "name": "Audio In Switch",
        "category": "Audio",
        "description": """
            Audio In Switch takes a selected quantity of audio inputs and allows you
            to switch between them to a single output.
            You can use this to select between instruments at your input jacks,
            use it in conjunction with the Audio Out Switch to select between
            effects chains, or use it anywhere you'd like to be able to select
            between incoming audio sources using CV.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 18,
        "params": 1,
        "cpu": 0.8,
        "blocks": {
            "audio_input_1": {"isDefault": True, "isParam": False, "position": 0},
            "audio_input_2": {"isDefault": False, "isParam": False, "position": 1},
            "audio_input_3": {"isDefault": False, "isParam": False, "position": 2},
            "audio_input_4": {"isDefault": False, "isParam": False, "position": 3},
            "audio_input_5": {"isDefault": False, "isParam": False, "position": 4},
            "audio_input_6": {"isDefault": False, "isParam": False, "position": 5},
            "audio_input_7": {"isDefault": False, "isParam": False, "position": 6},
            "audio_input_8": {"isDefault": False, "isParam": False, "position": 7},
            "audio_input_9": {"isDefault": False, "isParam": False, "position": 10},
            "audio_input_10": {"isDefault": False, "isParam": False, "position": 11},
            "audio_input_11": {"isDefault": False, "isParam": False, "position": 12},
            "audio_input_12": {"isDefault": False, "isParam": False, "position": 13},
            "audio_input_13": {"isDefault": False, "isParam": False, "position": 14},
            "audio_input_14": {"isDefault": False, "isParam": False, "position": 15},
            "audio_input_15": {"isDefault": False, "isParam": False, "position": 14},
            "audio_input_16": {"isDefault": False, "isParam": False, "position": 15},
            "in_select": {"isDefault": True, "isParam": True, "position": 16},
            "audio_output": {"isDefault": True, "isParam": False, "position": 17},
        },
        "options": {"num_inputs": list(range(1, 17)), "fades": ["on", "off"]},
    },
    34: {
        "name": "Audio Out Switch",
        "category": "Audio",
        "description": """
            Audio Out Switch takes an audio input and routes it between a set
            quantity of audio outputs.
            You can use it at your output jacks to select between amplifiers
            or mixer channels, use it in conjunction with the Audio In Switch to
            select between effects chains, or use it anywhere you'd like to be able
            to select an outgoing audio path using CV.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 18,
        "params": 1,
        "cpu": 0.7,
        "blocks": {
            "audio_input": {"isDefault": True, "isParam": False, "position": 0},
            "in_select": {"isDefault": True, "isParam": True, "position": 1},
            "audio_output_1": {"isDefault": True, "isParam": False, "position": 2},
            "audio_output_2": {"isDefault": False, "isParam": False, "position": 3},
            "audio_output_3": {"isDefault": True, "isParam": False, "position": 4},
            "audio_output_4": {"isDefault": False, "isParam": False, "position": 5},
            "audio_output_5": {"isDefault": True, "isParam": False, "position": 6},
            "audio_output_6": {"isDefault": False, "isParam": False, "position": 7},
            "audio_output_7": {"isDefault": True, "isParam": False, "position": 8},
            "audio_output_8": {"isDefault": False, "isParam": False, "position": 9},
            "audio_output_9": {"isDefault": True, "isParam": False, "position": 10},
            "audio_output_10": {"isDefault": False, "isParam": False, "position": 11},
            "audio_output_11": {"isDefault": True, "isParam": False, "position": 12},
            "audio_output_12": {"isDefault": False, "isParam": False, "position": 13},
            "audio_output_13": {"isDefault": True, "isParam": False, "position": 14},
            "audio_output_14": {"isDefault": False, "isParam": False, "position": 15},
            "audio_output_15": {"isDefault": True, "isParam": False, "position": 16},
            "audio_output_16": {"isDefault": False, "isParam": False, "position": 17},
        },
        "options": {"num_outputs": list(range(1, 17)), "fades": ["on", "off"]},
    },
    35: {
        "name": "Midi Pressure",
        "category": "Interface",
        "description": """
            Many MIDI keyboards have an aftertouch feature that can be triggered
            by pressing down on a note after it's fully depressed.
            You can use after touch to trigger a little extra pizazz in your sound.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.03,
        "blocks": {
            "channel_pressure": {"isDefault": True, "isParam": False, "position": 0}
        },
        "options": {"midi_channel": list(range(1, 17))},
    },
    36: {
        "name": "Onset Detector",
        "category": "Analysis",
        "description": """
            Onset Detector looks for incoming audio signal and generates a CV trigger at the peaks.
            Use a regular audio source to advance a sequencer, tap a tempo, etc
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 3,
        "params": 1,
        "cpu": 0.7,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "sensitivity": {"isDefault": False, "isParam": True, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {"sensitivity": ["off", "on"]},
    },
    37: {
        "name": "Rhythm",
        "category": "CV",
        "description": """
            Rhythm will take an incoming CV signal, interpret it as a series of triggers,
            record those triggers and play them back at the output.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 5,
        "params": 3,
        "cpu": 0.5,
        "blocks": {
            "rec_start_stop": {"isDefault": True, "isParam": True, "position": 0},
            "rhythm_in": {"isDefault": True, "isParam": True, "position": 1},
            "play": {"isDefault": True, "isParam": True, "position": 2},
            "done_out": {"isDefault": False, "isParam": False, "position": 3},
            "rhythm_out": {"isDefault": True, "isParam": False, "position": 4},
        },
        "options": {
            "done_ctrl": ["off", "on"],
        },
    },
    38: {
        "name": "Noise",
        "category": "Audio",
        "description": """
            Generates white noise from a single button.
            Use the strength of your connection as a level control.
            Helpful in connection with VCAs and ADSRs in creating drum sounds, etc.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.4,
        "blocks": {"audio_out": {"isDefault": True, "isParam": False, "position": 0}},
        "options": {},
    },
    39: {
        "name": "Random",
        "category": "CV",
        "description": """
            Random will generate numbers continuously or when triggered with the option trigger in.
            Connect an LFO to the trigger in to get regularly updated random numbers.
            Try it with a CV in switch to toggle some randomness into  your life.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.1,
        "blocks": {
            "trigger_in": {"isDefault": False, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {"output": ["0 to 1", "-1 to 1"], "new_val_on_trig": ["off", "on"]},
    },
    40: {
        "name": "Gate",
        "category": "Effect",
        "description": """
            A standard in studio audio tools, gate can also be used as the key ingredient
            in gated fuzz tones.
            Use it to filter out noise from an audio source, or to cut the end off
            of a reverb's decay, thus creating the classic gated reverb sound.
            Make sure to experiment with the sidechain input!
        """,
        "default_blocks": 5,
        "min_blocks": 3,
        "max_blocks": 8,
        "params": 3,
        "cpu": 3,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "threshold": {"isDefault": True, "isParam": True, "position": 2},
            "attack": {"isDefault": False, "isParam": True, "position": 3},
            "release": {"isDefault": False, "isParam": True, "position": 4},
            "sidechain_in": {"isDefault": False, "isParam": False, "position": 7},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 5},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 6},
        },
        "options": {
            "attack_ctrl": ["off", "on"],
            "release_ctrl": ["off", "on"],
            "channels": ["1in->1out", "stereo"],
            "sidechain": ["internal", "external"],
        },
    },
    41: {
        "name": "Tremolo",
        "category": "Effect",
        "description": """
            Up and down, side to side.
            Tremolo helps your smile get wide.
            Set speed and depth and tap in a tempo if you like.
            If you'd like a tremolo effect with more control, try creating one using
            the VCA or Audio Panner along with LFOs and various other CV tools to get radical!
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 6,
        "params": 2,
        "cpu": 2,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "rate": {"isDefault": True, "isParam": True, "position": 2},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3},
            "direct": {"isDefault": False, "isParam": True, "position": 4},
            "depth": {"isDefault": True, "isParam": True, "position": 5},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7},
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "2in->2out"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "waveform": ["fender-ish", "vox-ish", "triangle", "sine", "square"],
        },
    },
    42: {
        "name": "Tone Control",
        "category": "Effect",
        "description": """
            Tone Control is a 3 or 4 band tone control.
            Use this in conjunction with Distortion, Delay w/Mod, Reverb, or even
            a clean sound to fundamentally change its character.
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 10,
        "params": 6,
        "cpu": 5,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "low_shelf": {"isDefault": True, "isParam": True, "position": 2},
            "mid_gain_1": {"isDefault": True, "isParam": True, "position": 3},
            "mid_freq_1": {"isDefault": True, "isParam": True, "position": 4},
            "mid_gain_2": {"isDefault": False, "isParam": True, "position": 5},
            "mid_freq_2": {"isDefault": False, "isParam": True, "position": 6},
            "high_shelf": {"isDefault": True, "isParam": True, "position": 7},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 9},
        },
        "options": {
            "channels": ["1in->1out", "stereo"],
            "num_mid_bands": [1, 2],
        },
    },
    43: {
        "name": "Delay w Mod",
        "category": "Effect",
        "description": """
            Delay is one of the classic delay effects.
            Delay w/Mod differs from the Delay Line module found in Audio Out in
            that it runs a dry signal alongside the wet, has a feedback section,
            and a modulation section.
            Set the delay time either by tap or rotary/CV input.
            Optional stereo outputs round out the list of features.
            You can change the character of the delay effect with the "type"
            option, and/or by setting your mix to wet only, adding tone control
            and other effects to the output, and connecting your audio source
            directly to your output (bypassing the delay module) to act as the dry signal.
        """,
        "default_blocks": 7,
        "min_blocks": 7,
        "max_blocks": 9,
        "params": 5,
        "cpu": 18,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "delay_time": {"isDefault": True, "isParam": True, "position": 2},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 5},
            "feedback": {"isDefault": True, "isParam": True, "position": 3},
            "mod_rate": {"isDefault": True, "isParam": True, "position": 4},
            "mod_depth": {"isDefault": True, "isParam": True, "position": 6},
            "mix": {"isDefault": True, "isParam": True, "position": 7},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 9},
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "2in->2out"],
            "control": ["rate", "tap_tempo"],
            "type": ["clean", "tape", "old_tape", "bbd"],
            "tap_ratio": [
                "1:1",
                "2:3",
                "1:2",
                "1:3",
                "3:8",
                "1:4",
                "3:16",
                "1:8",
                "1:16",
                "1:32",
            ],
        },
    },
    44: {
        "name": "Stompswitch",
        "category": "Interface",
        "description": """
            Use this module to connect a stomp switch to other modules.
            This can be any of ZOIA's 3 stomp switches or an external one.
            If using an external, remember to set it up in the Config Menu.
            Once placed, the Scroll and Bypass stomp switches must be "switched to"
            by holding them both on together for 2 seconds, this will allow them to
            function in the modules instead of as ZOIA's main user interface.
            Hold again for 2 seconds to switch back.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {"cv_output": {"isDefault": True, "isParam": False, "position": 0}},
        "options": {
            "stompswitch": ["left", "middle", "right", "ext"],
            "action": ["momentary", "latching"],
            "normally": ["zero", "one"],
        },
    },
    45: {
        "name": "Value",
        "category": "CV",
        "description": """
            Value allows you to connect to multiple modules and adjust their
            parameters simultaneously from one CV adjustment at the input.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.15,
        "blocks": {
            "value": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {"output": ["0 to 1", "-1 to 1"]},
    },
    46: {
        "name": "CV Delay",
        "category": "CV",
        "description": """
            CV Delay will take incoming CV and delay it in time by a set amount.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "cpu": 1.5,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "delay_time": {"isDefault": True, "isParam": True, "position": 1},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {"cv_input": ["exponent", "linear"]},
    },
    47: {
        "name": "CV Loop",
        "category": "CV",
        "description": """
            CV Loop functions similar to an audio looper except records patterns
            of CV signal instead of audio.
            You can record and play back snippets of LFOs, sequences, changes in CV
            or MIDI control etc.
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 7,
        "cpu": 0.1,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "record": {"isDefault": True, "isParam": True, "position": 1},
            "play": {"isDefault": True, "isParam": True, "position": 2},
            "playback_speed": {"isDefault": True, "isParam": True, "position": 3},
            "start_position": {"isDefault": False, "isParam": True, "position": 4},
            "stop_position": {"isDefault": False, "isParam": True, "position": 5},
            "restart_loop": {"isDefault": True, "isParam": True, "position": 6},
            "cv_output": {"isDefault": True, "isParam": False, "position": 7},
        },
        "options": {
            "max_rec_time": list(range(1, 17)),
            "length_edit": ["off", "on"]
        },
    },
    48: {
        "name": "CV Filter",
        "category": "CV",
        "description": """
            CV Filter dictates the length of time a CV output will take to
            respond to a change in CV input, determined by the time constant.
            The CV change occurs logarithmically for a nice smooth transition.
            Use this module in series with a MIDI/keyboard note to add portamento
            to your synth voice.
            You can also use this module to vary the shape of an LFO waveform or connect
            to a stomp switch to produce a long slow change in an audio effect.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 4,
        "params": 2,
        "cpu": 0.1,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "time_constant": {"isDefault": True, "isParam": True, "position": 1},
            "rise_constant": {"isDefault": False, "isParam": True, "position": 3},
            "fall_constant": {"isDefault": False, "isParam": True, "position": 4},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {"control": ["linked", "separate"]},
    },
    49: {
        "name": "Clock Divider",
        "category": "CV",
        "description": """
            Clock Divider module will detect tempo of incoming CV upward changes,
            divide it by a user determined ratio, and output CV triggers at the resulting tempo.
            This can be a handy way of getting a tap tempo from a slightly irregular waveform.
        """,
        "default_blocks": 5,
        "min_blocks": 4,
        "max_blocks": 5,
        "params": 4,
        "cpu": 0.4,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "reset_in": {"isDefault": True, "isParam": True, "position": 1},
            "modifier": {"isDefault": False, "isParam": True, "position": 2},
            "dividend": {"isDefault": True, "isParam": True, "position": 4},
            "divisor": {"isDefault": True, "isParam": True, "position": 5},
            "cv_output": {"isDefault": True, "isParam": False, "position": 3},
        },
        "options": {"input": ["tap", "cv_control"]},
    },
    50: {
        "name": "Comparator",
        "category": "CV",
        "description": """
            Comparator is a logic module that will switch CV on if positive input
            is equal to or greater than negative input, and off if positive input is
            less than negative input.
            Off can be defined as 0 or -1 by the output range.
            This can be useful if you'd like to have something happen, but only above
            a certain threshold.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "cpu": 0.04,
        "blocks": {
            "cv_positive_input": {"isDefault": True, "isParam": True, "position": 0},
            "cv_negative_input": {"isDefault": True, "isParam": True, "position": 1},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {"output": ["0 to 1", "-1 to 1"]},
    },
    51: {
        "name": "CV Rectify",
        "category": "CV",
        "description": """
            CV Rectify will interpret incoming CV from -1 to 1 and "flip" the negative
            values into positive values equidistant from 0.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.02,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {},
    },
    52: {
        "name": "Trigger",
        "category": "CV",
        "description": """
            Creates a very short CV pulse (value of 1) on detection of upward CV input.
            This is useful in creating a tap tempos from regular or irregular CV waveforms,
            triggering sequencers or ADSRs at specific times, etc.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.1,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {},
    },
    53: {
        "name": "Stereo Spread",
        "category": "Audio",
        "description": """
            Stereo Spread will take one or two channels and enhance their stereo field.
            This is generally used right before an audio output module but, as always,
            feel free to experiment!
        """,
        "default_blocks": 5,
        "min_blocks": 4,
        "max_blocks": 5,
        "params": 1,
        "cpu": 2,
        "blocks": {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_2": {"isDefault": False, "isParam": False, "position": 1},
            "side_gain": {"isDefault": False, "isParam": True, "position": 2},
            "delay_time": {"isDefault": True, "isParam": True, "position": 3},
            "audio_out_1": {"isDefault": True, "isParam": False, "position": 4},
            "audio_out_2": {"isDefault": True, "isParam": False, "position": 5},
        },
        "options": {"method": ["mid_side", "haas"]},
    },
    54: {
        "name": "Cport Exp CV In",
        "category": "Interface",
        "description": """
            Connect your expression pedal or a control voltage signal from an external source.
            Remember to set CPort to either exp or cv in the Config Menu.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {"cv_output": {"isDefault": True, "isParam": False, "position": 0}},
        "options": {"output_range": ["0 to 1", "-1 to 1"]},
    },
    55: {
        "name": "Cport CV Out",
        "category": "Interface",
        "description": """
            This module interprets internal CV and sends it down the ring of a 1/4"
            TRS connector in the control port as a standard CV signal of 0-5 volts.
            Remember to set CPort to cv in the Config Menu.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.2,
        "blocks": {"cv_input": {"isDefault": True, "isParam": True, "position": 0}},
        "options": {"input_range": ["0 to 1", "-1 to 1"]},
    },
    56: {
        "name": "UI Button",
        "category": "Interface",
        "description": """
            UI Button can function in a couple different ways.
            It can show you a specific colour at a specific brightness based on the
            setting of or CV sent to the input.
            It can also act as a pushbutton with output enabled.
            To use as a visualizing pixel, connect CV and send the following values:
            EXTENDED RANGE:
            Red: 0 - 0.049 (max bright 0.0375),
            Orange: 0.05 - 0.099 (max bright 0.0875),
            Mango: 0.10 - 0.149 (max bright 0.1375),
            Yellow: 0.15 - 0.199 (max bright 0.1875),
            Lime: 0.20 - 0.249 (max bright 0.2375),
            Green: 0.25 - 0.299 (max bright 0.2875),
            Surf: 0.30 - 0.349 (max bright 0.3375),
            Aqua: 0.35 - 0.399 (max bright 0.3875),
            Sky: 0.40 - 0.449 (max bright 0.4375),
            Blue: 0.45 - 0.499 (max bright 0.4875), 
            Purple: 0.50 - 0.549 (max bright 0.5375), 
            Magenta: 0.55 - 0.599 (max bright 0.5875), 
            Pink: 0.60 - 0.649 (max bright 0.6375), 
            Peach: 0.65 - 0.699 (max bright 0.6875), 
            White: 0.70 - 0.749 (max bright 0.7375).
            BASIC RANGE:
            Blue = 0 to 0.099 (0.74 max brightness), 
            Green = 0.1 to 0.199 (0.174 max brightness), 
            Red = 0.2 to 0.299 (0.274 max brightness), 
            Yellow = 0.3 to 0.399 (0.374 max brightness), 
            Cyan = 0.4 to 0.499 (0.474 max brightness), 
            Magenta = 0.5 to 0.599 (0.574 max brightness), 
            White = 0.6 to 0.699 (0.6 to 0.674 brightness).
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.04,
        "blocks": {
            "in": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": False, "isParam": False, "position": 1},
        },
        "options": {
            "cv_output": ["disabled", "enabled"],
            "range": ["basic", "extended"],
        },
    },
    57: {
        "name": "Audio Panner",
        "category": "Audio",
        "description": """
            Audio Panner takes either one or two input channels and pans them between two outputs.
            Connect an LFO for a stereo tremolo effect.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 5,
        "params": 3,
        "cpu": 1,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "pan": {"isDefault": True, "isParam": True, "position": 2},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 3},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 4},
        },
        "options": {
            "channels": ["1in->2out", "2in->2out"],
            "pan_type": ["equal_pwr", "-4.5dB", "linear"],
        },
    },
    58: {
        "name": "Pitch Detector",
        "category": "Analysis",
        "description": """
            Pitch Detector interprets the pitch of a connected audio signal as a CV note output,
            which can be sent to an oscillator or quantizer.
            You can affect the tracking by changing the connection strength between
            the audio source and the audio input, and transpose which note the oscillator
            will generate using the connection strength to the oscillator.
            Click knob to toggle display between frequency in Hz and note.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 0,
        "cpu": 2.5,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {},
    },
    59: {
        "name": "Pitch Shifter",
        "category": "Audio",
        "description": """
            Pitch Shifter transposes the pitch of incoming audio.
            Click the knob on the pitch shift parameter to cycle views of
            CV value, semitones, or cents.
            Connect an LFO to produce a vibrato effect, or connect whatever you'd like!
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "cpu": 15.5,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "pitch_shift": {"isDefault": True, "isParam": True, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {},
    },
    60: {
        "name": "Midi Note Out",
        "category": "Interface",
        "description": """
            Send MIDI notes out to external MIDI enabled gear through ZOIA's MIDI outputs.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 3,
        "params": 3,
        "cpu": 0.1,
        "blocks": {
            "note_in": {"isDefault": True, "isParam": True, "position": 0},
            "gate_in": {"isDefault": True, "isParam": True, "position": 1},
            "velocity_in": {"isDefault": False, "isParam": True, "position": 2},
        },
        "options": {
            "midi_channel": list(range(1, 17)),
            "velocity_output": ["off", "on"],
        },
    },
    61: {
        "name": "Midi CC Out",
        "category": "Interface",
        "description": """
            Send Control Change messages to external MIDI enabled gear through ZOIA's MIDI outputs.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "cpu": 0.2,
        "blocks": {"cc": {"isDefault": True, "isParam": True, "position": 0}},
        "options": {
            "midi_channel": list(range(1, 17)),
            "controller": list(range(0, 128)),
        },
    },
    62: {
        "name": "Midi PC Out",
        "category": "Interface",
        "description": """
            Send Program Change messages to external MIDI enabled gear.
            Select the Program Change value and send a CV signal to trigger
            in to send message through ZOIA's MIDI outputs.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 2,
        "cpu": 0.1,
        "blocks": {
            "pc": {"isDefault": True, "isParam": True, "position": 0},
            "trigger_in": {"isDefault": True, "isParam": True, "position": 1},
        },
        "options": {"midi_channel": list(range(1, 17))},
    },
    63: {
        "name": "Bit Modulator",
        "category": "Audio",
        "description": """
            Bit Modulator takes one audio input and compares it against the other,
            creating an unholy glitchy combination of both sounds at the output.
            Choose between 3 different logic flavours with the "type" option.
            When taking audio from an external source, it's recommended to put a gate before the input.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 0,
        "cpu": 1.2,
        "blocks": {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_2": {"isDefault": True, "isParam": False, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        },
        "options": {"type": ["xor", "and", "or"]},
    },
    64: {
        "name": "Audio Balance",
        "category": "Audio",
        "description": """
            Audio Balance mixes an output from 2 inputs.
            You can run this module either mono or stereo.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 7,
        "params": 1,
        "cpu": 1.7,
        "blocks": {
            "audio_in_1_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_1_R": {"isDefault": False, "isParam": False, "position": 4},
            "audio_in_2_L": {"isDefault": True, "isParam": False, "position": 1},
            "audio_in_2_R": {"isDefault": False, "isParam": False, "position": 5},
            "mix": {"isDefault": True, "isParam": True, "position": 2},
            "audio_output_L": {"isDefault": True, "isParam": False, "position": 3},
            "audio_output_R": {"isDefault": False, "isParam": False, "position": 6},
        },
        "options": {"stereo": ["mono", "stereo"]},
    },
    65: {
        "name": "Inverter",
        "category": "Audio",
        "description": """
            The Inverter module takes incoming audio signal and inverts the
            sound wave 180 degrees out of phase.
            This module is inaudible unless you have a phase related problem
            you are trying to solve, in which case it can be very audible.
            Be sure to put a 1 Buffer Delay module into your "dry" side to
            line up the Inverter in time for proper phase cancellation.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 0,
        "cpu": 0.3,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "audio_out": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {},
    },
    66: {
        "name": "Fuzz",
        "category": "Effect",
        "description": """
            The Fuzz module provides gnarly fuzz tones for your sonic enjoyment.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 4,
        "params": 2,
        "cpu": 16,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "input_gain": {"isDefault": True, "isParam": True, "position": 1},
            "output_gain": {"isDefault": True, "isParam": True, "position": 2},
            "audio_out": {"isDefault": True, "isParam": False, "position": 3},
        },
        "options": {"model": ["efuzzy", "burly", "scoopy", "ugly"]},
    },
    67: {
        "name": "Ghostverb",
        "category": "Effect",
        "description": """
            A spooky, ghostly reverb sound akin to the Ghost mode found in the Empress Reverb.
            Scare the crap out of all your friends!
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "cpu": 45,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "decay_feedback": {"isDefault": True, "isParam": True, "position": 2},
            "rate": {"isDefault": True, "isParam": True, "position": 3},
            "resonance": {"isDefault": True, "isParam": True, "position": 4},
            "mix": {"isDefault": True, "isParam": True, "position": 5},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7},
        },
        "options": {"channels": ["1in->1out", "1in->2out", "stereo"]},
    },
    68: {
        "name": "Cabinet Sim",
        "category": "Effect",
        "description": """
            A versatile guitar cabinet simulator.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 4,
        "params": 0,
        "cpu": 10,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 2},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 3},
        },
        "options": {
            "channels": ["mono", "stereo"],
            "type": [
                "4x12_full",
                "2x12_dark",
                "2x12_modern",
                "1x12",
                "1x8_lofi",
                "1x12_vintage",
                "4x12_hifi",
            ],
        },
    },
    69: {
        "name": "Flanger",
        "category": "Effect",
        "description": """
            ZOIA's Flanger module is borrowed right from the Empress Nebulus.
            This quite versatile flanger encompasses lots of comb filtering territory,
            but don't hesitate to build flange tones yourself using LFOs and delay lines!
        """,
        "default_blocks": 7,
        "min_blocks": 7,
        "max_blocks": 9,
        "params": 5,
        "cpu": 11,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "rate": {"isDefault": True, "isParam": True, "position": 2},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3},
            "direct": {"isDefault": False, "isParam": True, "position": 4},
            "regen": {"isDefault": True, "isParam": True, "position": 5},
            "width": {"isDefault": True, "isParam": True, "position": 6},
            "tone_tilt_eq": {"isDefault": True, "isParam": True, "position": 7},
            "mix": {"isDefault": True, "isParam": True, "position": 8},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 9},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 10},
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "type": ["1960s", "1970s", "thru_0"],
        },
    },
    70: {
        "name": "Chorus",
        "category": "Effect",
        "description": """
            The classic chorus effect.
            A nice sounding, fairly standard chorus.
            Get wackier sounds from it by using CV direct, or build
            your own from LFOs and delay lines!
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "cpu": 13,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "rate": {"isDefault": True, "isParam": True, "position": 2},
            "tap_tempo_in": {"isDefaut": False, "isParam": True, "position": 3},
            "direct": {"isDefault": False, "isParam": True, "position": 4},
            "width": {"isDefault": True, "isParam": True, "position": 5},
            "tone_tilt_eq": {"isDefault": True, "isParam": True, "position": 6},
            "mix": {"isDefault": True, "isParam": True, "position": 7},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 9},
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "type": ["classic"],
        },
    },
    71: {
        "name": "Vibrato",
        "category": "Effect",
        "description": """
            Vibrato is your typical pitch bending, wet only sound you'd find on
            such classic units as the Empress Nebulus, just to name one.
            Get bendy!
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 6,
        "params": 2,
        "cpu": 5,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "rate": {"isDefault": True, "isParam": True, "position": 2},
            "tap_tempo_in": {"isDefaut": False, "isParam": True, "position": 3},
            "direct": {"isDefault": False, "isParam": True, "position": 4},
            "width": {"isDefault": True, "isParam": True, "position": 5},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7},
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "waveform": ["sine", "triangle", "swung_sine", "swung"],
        },
    },
    72: {
        "name": "Env Filter",
        "category": "Effect",
        "description": """
            Get your quack on!
            This fully featured envelope filter has everything you
            need to tune in that perfect envelope filter and get funky.
            Great on guitar, bass, or anything else!
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "cpu": 7,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "sensitivity": {"isDefault": True, "isParam": True, "position": 2},
            "min_freq": {"isDefault": True, "isParam": True, "position": 3},
            "max_freq": {"isDefault": True, "isParam": True, "position": 4},
            "filter_q": {"isDefault": True, "isParam": True, "position": 5},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7},
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "filter_type": ["bpf", "hpf", "lpf"],
            "direction": ["up", "down"],
        },
    },
    73: {
        "name": "Ring Modulator",
        "category": "Effect",
        "description": """
            A gnarly ring modulation effect.
            A robot's nightmare, a tweaker's delight!
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 6,
        "params": 3,
        "cpu": 14,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "frequency": {"isDefault": True, "isParam": True, "position": 1},
            "ext_in": {"isDefault": False, "isParam": False, "position": 2},
            "duty_cycle": {"isDefault": False, "isParam": True, "position": 3},
            "mix": {"isDefault": True, "isParam": True, "position": 4},
            "audio_out": {"isDefault": True, "isParam": False, "position": 5},
        },
        "options": {
            "waveform": ["sine", "square", "triangle", "sawtooth"],
            "ext_audio_in": ["off", "on"],
            "duty_cycle": ["off", "on"],
            "upsampling": ["none", "2x"],
        },
    },
    74: {
        "name": "Hall Reverb",
        "category": "Effect",
        "description": """
            It's like you're there, looking up at the pulpit, with the warm sun
            casting in beams of coloured light from the stained glass windows.
            You're in reverb heaven, now.
        """,
        "default_blocks": 8,
        "min_blocks": 8,
        "max_blocks": 8,
        "params": 4,
        "cpu": 22,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": True, "isParam": False, "position": 1},
            "decay_time": {"isDefault": True, "isParam": True, "position": 2},
            "low_eq": {"isDefault": True, "isParam": True, "position": 6},
            "lpf_freq": {"isDefault": True, "isParam": True, "position": 7},
            "mix": {"isDefault": True, "isParam": True, "position": 3},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 4},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 5},
        },
        "options": {},
    },
    75: {
        "name": "Ping Pong Delay",
        "category": "Effect",
        "description": """
            Ping Pong Delay is almost identical to the Delay w/ Mod except for one key aspect:
            the delay repeats ping pong from left to right across stereo outputs.
            When stereo inputs are selected, one input will ping while the other pongs,
            followed by a pong while the other pings into the opposite and then correct outputs.
        """,
        "default_blocks": 7,
        "min_blocks": 7,
        "max_blocks": 9,
        "params": 5,
        "cpu": 18,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "delay_time": {"isDefault": True, "isParam": True, "position": 2},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3},
            "feedback": {"isDefault": True, "isParam": True, "position": 4},
            "mod_rate": {"isDefault": True, "isParam": True, "position": 5},
            "mod_depth": {"isDefault": True, "isParam": True, "position": 6},
            "mix": {"isDefault": True, "isParam": True, "position": 7},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 9},
        },
        "options": {
            "channels": ["1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "type": ["clean", "tape", "old_tape", "bbd"],
            "tap_ratio": [
                "1:1",
                "2:3",
                "1:2",
                "1:3",
                "3:8",
                "1:4",
                "3:16",
                "1:8",
                "1:16",
                "1:32",
            ],
        },
    },
    76: {
        "name": "Audio Mixer",
        "category": "Audio",
        "description": """
            Audio Mixer functions like a stripped down mixing console,
            where gain is your channel fader and you can place an optional pan control.
            Mix up to 8 channels, in mono or stereo.
        """,
        "default_blocks": 5,
        "min_blocks": 5,
        "max_blocks": 34,
        "params": 16,
        "cpu": 7,
        "blocks": {
            "audio_in_1_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_1_R": {"isDefault": False, "isParam": False, "position": 1},
            "audio_in_2_L": {"isDefault": True, "isParam": False, "position": 2},
            "audio_in_2_R": {"isDefault": False, "isParam": False, "position": 3},
            "audio_in_3_L": {"isDefault": False, "isParam": False, "position": 4},
            "audio_in_3_R": {"isDefault": False, "isParam": False, "position": 5},
            "audio_in_4_L": {"isDefault": False, "isParam": False, "position": 6},
            "audio_in_4_R": {"isDefault": False, "isParam": False, "position": 7},
            "audio_in_5_L": {"isDefault": False, "isParam": False, "position": 8},
            "audio_in_5_R": {"isDefault": False, "isParam": False, "position": 9},
            "audio_in_6_L": {"isDefault": False, "isParam": False, "position": 10},
            "audio_in_6_R": {"isDefault": False, "isParam": False, "position": 11},
            "audio_in_7_L": {"isDefault": False, "isParam": False, "position": 12},
            "audio_in_7_R": {"isDefault": False, "isParam": False, "position": 13},
            "audio_in_8_L": {"isDefault": False, "isParam": False, "position": 14},
            "audio_in_8_R": {"isDefault": False, "isParam": False, "position": 15},
            "gain_1": {"isDefault": True, "isParam": True, "position": 16},
            "gain_2": {"isDefault": True, "isParam": True, "position": 17},
            "gain_3": {"isDefault": False, "isParam": True, "position": 18},
            "gain_4": {"isDefault": False, "isParam": True, "position": 19},
            "gain_5": {"isDefault": False, "isParam": True, "position": 20},
            "gain_6": {"isDefault": False, "isParam": True, "position": 21},
            "gain_7": {"isDefault": False, "isParam": True, "position": 22},
            "gain_8": {"isDefault": False, "isParam": True, "position": 23},
            "pan_1": {"isDefault": False, "isParam": True, "position": 24},
            "pan_2": {"isDefault": False, "isParam": True, "position": 25},
            "pan_3": {"isDefault": False, "isParam": True, "position": 26},
            "pan_4": {"isDefault": False, "isParam": True, "position": 27},
            "pan_5": {"isDefault": False, "isParam": True, "position": 28},
            "pan_6": {"isDefault": False, "isParam": True, "position": 29},
            "pan_7": {"isDefault": False, "isParam": True, "position": 30},
            "pan_8": {"isDefault": False, "isParam": True, "position": 31},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 32},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 33},
        },
        "options": {
            "channels": list(range(2, 9)),
            "stereo": ["mono", "stereo"],
            "panning": ["off", "on"],
        },
    },
    77: {
        "name": "CV Flip Flop",
        "category": "CV",
        "description": """
            This is essentially a latching CV switch with an output of 0 or 1.
            When the input sees an upward CV change, the flip flop is triggered to
            change it's output state from 0 to 1 at the next upward change in CV,
            which must occur after a downward change in CV.
            So, the flip flop changes from 0 to 1 at every other upward change in CV.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.2,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        },
        "options": {},
    },
    78: {
        "name": "Diffuser",
        "category": "Audio",
        "description": """
            Diffuser spreads your signal across the galaxy like so many shimmering little stars.
            On it's own it sounds like a modulated slapback delay with no dry signal,
            but it can be used to construct many a tonal/atonal masterpiece.
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 6,
        "params": 4,
        "cpu": 2,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "gain": {"isDefault": True, "isParam": True, "position": 1},
            "size": {"isDefault": True, "isParam": True, "position": 2},
            "mod_width": {"isDefault": True, "isParam": True, "position": 3},
            "mod_rate": {"isDefault": True, "isParam": True, "position": 4},
            "audio_out": {"isDefault": True, "isParam": False, "position": 5},
        },
        "options": {},
    },
    79: {
        "name": "Reverb Lite",
        "category": "Effect",
        "description": """
            A straightforward CPU friendly reverb sound to add some smoosh to heavier workload patches.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 6,
        "params": 2,
        "cpu": 10,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "decay_time": {"isDefault": True, "isParam": True, "position": 2},
            "mix": {"isDefault": True, "isParam": True, "position": 3},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 4},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 5},
        },
        "options": {"channels": ["1in->1out", "1in->2out", "stereo"]},
    },
    80: {
        "name": "Room Reverb",
        "category": "Effect",
        "description": """
            Well, you're cooped up in your little room.
            But that's okay, because you've got some tasty room reverb to swim around in.
            Don't worry, somebody will come get you out someday.
        """,
        "default_blocks": 8,
        "min_blocks": 8,
        "max_blocks": 8,
        "params": 4,
        "cpu": 22,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": True, "isParam": False, "position": 1},
            "decay_time": {"isDefault": True, "isParam": True, "position": 2},
            "low_eq": {"isDefault": True, "isParam": True, "position": 3},
            "lpf_freq": {"isDefault": True, "isParam": True, "position": 4},
            "mix": {"isDefault": True, "isParam": True, "position": 5},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 7},
        },
        "options": {},
    },
    81: {
        "name": "Pixel",
        "category": "Interface",
        "description": """
            Puts a coloured block on the grid.
            The brightness can be controlled by a cv signal or an audio signal.
            Pixel is a simple, elegant way to create a more visually
            interactive user interface for your patch.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "cpu": 0.01,
        "blocks": {
            "cv_in": {"isDefault": True, "isParam": True, "position": 0},
            "audio_in": {"isDefault": False, "isParam": False, "position": 1},
        },
        "options": {"control": ["cv", "audio"]},
    },
    82: {
        "name": "Midi Clock In",
        "category": "Interface",
        "description": """
            Connect MIDI clock to sync your patches to the outside world.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 4,
        "params": 0,
        "cpu": 0.1,
        "blocks": {
            "quarter_out": {"isDefault": True, "isParam": False, "position": 0},
            "clock_out": {"isDefault": False, "isParam": False, "position": 1},
            "reset_out": {"isDefault": False, "isParam": False, "position": 2},
            "run_out": {"isDefault": False, "isParam": False, "position": 3},
        },
        "options": {
            "clock_out": ["disabled", "enabled"],
            "run_out": ["disabled", "enabled"],
            "divider": ["disabled", "enabled"],
            "beat_modifier": [
                "1",
                "2",
                "3",
                "4",
                "6",
                "12",
                "1/12",
                "1/6",
                "1/4",
                "1/3",
                "1/2",
            ],
        },
    },
    83: {
        "name": "Granular",
        "category": "Audio",
        "description": """
            Granular breaks up incoming audio into tiny little grains and
            spits them back out in the quantity and shape of your choosing.
            Go from modest textures to completely unrecognizable oscillations.
            Granular can also be used as a granular delay by creating a feedback
            path from the output back to the input...
        """,
        "default_blocks": 8,
        "min_blocks": 8,
        "max_blocks": 10,
        "params": 6,
        "cpu": 8,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "grain_size": {"isDefault": True, "isParam": True, "position": 2},
            "grain_position": {"isDefault": True, "isParam": True, "position": 3},
            "density": {"isDefault": True, "isParam": True, "position": 4},
            "texture": {"isDefault": True, "isParam": True, "position": 5},
            "speed_pitch": {"isDefault": True, "isParam": True, "position": 6},
            "freeze": {"isDefault": True, "isParam": True, "position": 7},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 9},
        },
        "options": {
            "num_grains": list(range(1, 9)),
            "channels": ["mono", "stereo"],
            "pos_control": ["cv", "tap_tempo"],
            "size_control": ["cv", "tap_tempo"],
        },
    },
    84: {
        "name": "Midi Clock Out",
        "category": "Interface",
        "description": """
            Generate MIDI clock to sync outside devices to your ZOIA.
            Clock sends directly to ZOIA's MIDI output.
        """,
        "default_blocks": 3,
        "min_blocks": 1,
        "max_blocks": 5,
        "params": 5,
        "cpu": 0.3,
        "blocks": {
            "tap_cv_control": {"isDefault": True, "isParam": True, "position": 0},
            "sent": {"isDefault": True, "isParam": True, "position": 1},
            "reset": {"isDefault": True, "isParam": True, "position": 2},
            "send_position": {"isDefault": False, "isParam": True, "position": 3},
            "song_position": {"isDefault": False, "isParam": True, "position": 4},
        },
        "options": {
            "input": ["tap", "cv_control"],
            "run_in": ["enabled", "disabled"],
            "reset_in": ["enabled", "disabled"],
            "position": ["disabled", "enabled"],
        },
    },
    85: {
        "name": "Tap to CV",
        "category": "CV",
        "description": """
            Outputs a CV value proportional to the tap tempo input.	
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 4,
        "params": 2,
        "cpu": 0.12,
        "blocks": {
            "tap_input": {"isDefault": True, "isParam": False, "position": 0},
            "min_time": {"isDefault": False, "isParam": True, "position": 1},
            "max_time": {"isDefault": False, "isParam": True, "position": 2},
            "output": {"isDefault": True, "isParam": False, "position": 3},
        },
        "options": {"range": ["off", "on"], "output": ["linear", "exponential"]},
    },
    86: {
        "name": "Midi Pitch Bend In",
        "category": "Interface",
        "description": """
            Collects MIDI data from pitch bend wheel on keyboards,
            can be applied to oscillator frequency in parallel with MIDI note data,
            or used in other ways.	
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {"pitch_bend": {"isDefault": True, "isParam": False, "position": 0}},
        "options": {"midi_channel": list(range(1, 17))},
    },
    87: {
        "name": "Euro CV Out 4",
        "category": "Interface",
        "description": """
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "cpu": 0.1,
        "blocks": {"cv_in": {"isDefault": True, "isParam": True, "position": 0}},
        "options": {
            "out_range": ["0 to 10V", "0 to 5V", "-5 to 5V"],
            "in_range": ["0 to 1", "-1 to 1"],
            "transpose": ["A", "C"],
        },
    },
    88: {
        "name": "Euro CV In 1",
        "category": "Interface",
        "description": """
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {"cv_out": {"isDefault": True, "isParam": False, "position": 0}},
        "options": {
            "out_range": ["0 to 1", "-1 to 1"],
            "in_range": ["0 to 10V", "0 to 5V", "-5 to 5V"],
            "clock_filter": ["none", "2,8", "1,4", "5,5"],
            "transpose": ["A", "C"],
        },
    },
    89: {
        "name": "Euro CV In 2",
        "category": "Interface",
        "description": """
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {"cv_out": {"isDefault": True, "isParam": False, "position": 0}},
        "options": {
            "out_range": ["0 to 1", "-1 to 1"],
            "in_range": ["0 to 10V", "0 to 5V", "-5 to 5V"],
            "clock_filter": ["none", "2,8", "1,4", "5,5"],
            "transpose": ["A", "C"],
        },
    },
    90: {
        "name": "Euro CV In 3",
        "category": "Interface",
        "description": """
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {"cv_out": {"isDefault": True, "isParam": False, "position": 0}},
        "options": {
            "out_range": ["0 to 1", "-1 to 1"],
            "in_range": ["0 to 10V", "0 to 5V", "-5 to 5V"],
            "clock_filter": ["none", "2,8", "1,4", "5,5"],
            "transpose": ["A", "C"],
        },
    },
    91: {
        "name": "Euro CV In 4",
        "category": "Interface",
        "description": """
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {"cv_out": {"isDefault": True, "isParam": False, "position": 0}},
        "options": {
            "out_range": ["0 to 1", "-1 to 1"],
            "in_range": ["0 to 10V", "0 to 5V", "-5 to 5V"],
            "clock_filter": ["none", "2,8", "1,4", "5,5"],
            "transpose": ["A", "C"],
        },
    },
    92: {
        "name": "Euro Headphone Amp",
        "category": "Interface",
        "description": """
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "cpu": 0.4,
        "blocks": {
            "level": {"isDefault": True, "isParam": True, "position": 0},
        },
        "options": {},
    },
    93: {
        "name": "Euro Audio Input 1",
        "category": "Interface",
        "description": """
            Connect audio from the outside world into the grid.
            This could be a guitar, bass, synth module, computer Audio, etc
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.4,
        "blocks": {
            "output": {"isDefault": True, "isParam": False, "position": 0},
        },
        "options": {"input_pad": ["6dB", "12dB", "no_pad"]},
    },
    94: {
        "name": "Euro Audio Input 2",
        "category": "Interface",
        "description": """
            Connect audio from the outside world into the grid.
            This could be a guitar, bass, synth module, computer Audio, etc
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.4,
        "blocks": {
            "output": {"isDefault": True, "isParam": False, "position": 0},
        },
        "options": {"input_pad": ["6dB", "12dB", "no_pad"]},
    },
    95: {
        "name": "Euro Audio Output 1",
        "category": "Interface",
        "description": """
            Connect audio from your ZOIA into the outside world.
            Connect to your amplifier, a DI box, your audio interface, etc.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.4,
        "blocks": {
            "input": {"isDefault": True, "isParam": False, "position": 0},
        },
        "options": {},
    },
    96: {
        "name": "Euro Audio Output 2",
        "category": "Interface",
        "description": """
            Connect audio from your ZOIA into the outside world.
            Connect to your amplifier, a DI box, your audio interface, etc.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.4,
        "blocks": {
            "input": {"isDefault": True, "isParam": False, "position": 0},
        },
        "options": {},
    },
    97: {
        "name": "Euro Pushbutton 1",
        "category": "Interface",
        "description": """
            Turns a grid button into a button you can push to send a CV signal.
            Tap in a tempo, open up a VCA, trigger a sequencer, or anything else.
            The grid is your oyster!
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.02,
        "blocks": {"cv_output": {"isDefault": True, "isParam": False, "position": 1}},
        "options": {"action": ["momentary", "latching"], "normally": ["zero", "one"]},
    },
    98: {
        "name": "Euro Pushbutton 2",
        "category": "Interface",
        "description": """
            Turns a grid button into a button you can push to send a CV signal.
            Tap in a tempo, open up a VCA, trigger a sequencer, or anything else.
            The grid is your oyster!
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.02,
        "blocks": {"cv_output": {"isDefault": True, "isParam": False, "position": 1}},
        "options": {"action": ["momentary", "latching"], "normally": ["zero", "one"]},
    },
    99: {
        "name": "Euro CV Out 1",
        "category": "Interface",
        "description": """
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "cpu": 0.1,
        "blocks": {"cv_in": {"isDefault": True, "isParam": True, "position": 0}},
        "options": {
            "out_range": ["0 to 10V", "0 to 5V", "-5 to 5V"],
            "in_range": ["0 to 1", "-1 to 1"],
            "transpose": ["A", "C"],
        },
    },
    100: {
        "name": "Euro CV Out 2",
        "category": "Interface",
        "description": """
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "cpu": 0.1,
        "blocks": {"cv_in": {"isDefault": True, "isParam": True, "position": 0}},
        "options": {
            "out_range": ["0 to 10V", "0 to 5V", "-5 to 5V"],
            "in_range": ["0 to 1", "-1 to 1"],
            "transpose": ["A", "C"],
        },
    },
    101: {
        "name": "Euro CV Out 3",
        "category": "Interface",
        "description": """
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "cpu": 0.1,
        "blocks": {"cv_in": {"isDefault": True, "isParam": True, "position": 0}},
        "options": {
            "out_range": ["0 to 10V", "0 to 5V", "-5 to 5V"],
            "in_range": ["0 to 1", "-1 to 1"],
            "transpose": ["A", "C"],
        },
    },
    102: {
        "name": "Sampler",
        "category": "Audio",
        "description": """
        """,
        "default_blocks": 7,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "cpu": 0.9,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "record": {"isDefault": True, "isParam": True, "position": 1},
            "sample_playback": {"isDefault": True, "isParam": False, "position": 2},
            "playback_speed": {"isDefault": True, "isParam": True, "position": 3},
            "start": {"isDefault": True, "isParam": True, "position": 4},
            "length": {"isDefault": True, "isParam": True, "position": 5},
            "cv_output": {"isDefault": False, "isParam": False, "position": 6},
            "audio_out": {"isDefault": True, "isParam": False, "position": 7},
        },
        "options": {
            "record": ["enabled", "disabled"],
            "playback": ["trigger", "gate", "loop"],
            "cv_output": ["off", "on"],
        },
    },
    103: {
        "name": "Device Control",
        "category": "Interface",
        "description": """
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "cpu": 0.1,
        "blocks": {
            "bypass": {"isDefault": True, "isParam": True, "position": 0},
            "aux": {"isDefault": False, "isParam": True, "position": 1},
            "performance": {"isDefault": False, "isParam": True, "position": 2},
        },
        "options": {
            "control": ["bypass", "stomp aux", "perform"],
        },
    },
    104: {
        "name": "CV Mixer",
        "category": "CV",
        "description": """
            An 8 channel CV Mixer and Attenuverter.
        """,
        "default_blocks": 5,
        "min_blocks": 5,
        "max_blocks": 17,
        "params": 16,
        "cpu": 0.7,
        "blocks": {
            "cv_in_1": {"isDefault": True, "isParam": True, "position": 0},
            "cv_in_2": {"isDefault": True, "isParam": True, "position": 1},
            "cv_in_3": {"isDefault": False, "isParam": True, "position": 2},
            "cv_in_4": {"isDefault": False, "isParam": True, "position": 3},
            "cv_in_5": {"isDefault": False, "isParam": True, "position": 4},
            "cv_in_6": {"isDefault": False, "isParam": True, "position": 5},
            "cv_in_7": {"isDefault": False, "isParam": True, "position": 6},
            "cv_in_8": {"isDefault": False, "isParam": True, "position": 7},
            "atten_1": {"isDefault": True, "isParam": True, "position": 8},
            "atten_2": {"isDefault": True, "isParam": True, "position": 9},
            "atten_3": {"isDefault": False, "isParam": True, "position": 10},
            "atten_4": {"isDefault": False, "isParam": True, "position": 11},
            "atten_5": {"isDefault": False, "isParam": True, "position": 12},
            "atten_6": {"isDefault": False, "isParam": True, "position": 13},
            "atten_7": {"isDefault": False, "isParam": True, "position": 14},
            "atten_8": {"isDefault": False, "isParam": True, "position": 15},
            "cv_output": {"isDefault": True, "isParam": False, "position": 16},
        },
        "options": {
            "num_channels": list(range(1, 9)),
            "levels": ["summing", "average"],
        },
    },
}

for k, v in list(module_index.items()):
    module_index[str(k)] = module_index.pop(k)

with open("zoia_lib/common/schemas/ModuleIndex.json", "w") as f:
    json.dump(module_index, f)

# import json2table
# with open("documentation/resources/mod.html", "w") as f:
#     f.write(json2table.convert(
#         module_index,
#         build_direction="LEFT_TO_RIGHT",
#         table_attributes={"style": "Width:100%"}
#         )
#     )
