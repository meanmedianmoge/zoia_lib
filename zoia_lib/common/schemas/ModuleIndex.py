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
            The State Variable Filter will resonate and cutoff around a set
            frequency.
        """,
        "default_blocks": 4,
        "min_blocks": 3,
        "max_blocks": 6,
        "params": 2,
        "param_defaults": {
            "frequency": 0,
            "resonance": 0,
        },
        "cpu": 1,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "frequency": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "resonance": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "lowpass_output": {"isDefault": True, "isParam": False, "position": 3, "type": "audio_out"},
            "hipass_output": {"isDefault": False, "isParam": False, "position": 4, "type": "audio_out"},
            "bandpass_output": {"isDefault": False, "isParam": False, "position": 5, "type": "audio_out"},
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
            Connect audio from the outside world into the grid. This could be a
            guitar, bass, synth module, computer audio, etc.
        """,
        "default_blocks": 2,
        "min_blocks": 1,
        "max_blocks": 2,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.3,
        "blocks": {
            "output_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_out"},
            "output_R": {"isDefault": True, "isParam": False, "position": 1, "type": "audio_out"},
        },
        "options": {"channels": ["stereo", "left", "right"]},
    },
    2: {
        "name": "Audio Output",
        "category": "Interface",
        "description": """
            Connect audio from your ZOIA into the outside world. Connect to your
            amplifier, a DI box, your audio interface, etc. An optional gain control
            lets you tweak the output level.
        """,
        "default_blocks": 2,
        "min_blocks": 1,
        "max_blocks": 3,
        "params": 1,
        "param_defaults": {
            "gain": 0.83,
        },
        "cpu": 1,
        "blocks": {
            "input_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "input_R": {"isDefault": True, "isParam": False, "position": 1, "type": "audio_in"},
            "gain": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
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
            Aliaser produces samples of incoming audio and compares them against
            each other to find imperfections. These imperfections become the
            outgoing audio. As sample count grows, so too does the thickness of the
            outgoing sound. This effect is a signal hog so be sure to boost your
            connection strengths incoming and outgoing. Try connecting a LFO or
            envelope follower to the alias amount.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "param_defaults": {
            "#_of_samples": 0.5,
        },
        "cpu": 0.6,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "#_of_samples": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_out"},
        },
        "options": {},
    },
    4: {
        "name": "Sequencer",
        "category": "CV",
        "description": """
            The sequencer allows you to create a number of "steps" (1-32) that can
            be cycled through, and each step can be used to send a CV value out of
            that tracks output. The sequencer can have up to 8 tracks, each with
            their own unique output so it's possible to create complex melodies or
            rhythmic patterns. Try connecting an LFO to the sequencer's gate input
            to start the sequencer cycle. Then connect the sequencer output to an
            oscillator, a cv track to the oscillator's frequency input, and set each
            step to a different note. Now your ZOIA is playing itself!
            note: the first track on the sequencer can have each step controlled
            directly by other CV sources as well.
        """,
        "default_blocks": 6,
        "min_blocks": 3,
        "max_blocks": 44,
        "params": 36,
        "param_defaults": {
            "step_1": 0,
            "step_2": 0,
            "step_3": 0,
            "step_4": 0,
            "step_5": 0,
            "step_6": 0,
            "step_7": 0,
            "step_8": 0,
            "step_9": 0,
            "step_10": 0,
            "step_11": 0,
            "step_12": 0,
            "step_13": 0,
            "step_14": 0,
            "step_15": 0,
            "step_16": 0,
            "step_17": 0,
            "step_18": 0,
            "step_19": 0,
            "step_20": 0,
            "step_21": 0,
            "step_22": 0,
            "step_23": 0,
            "step_24": 0,
            "step_25": 0,
            "step_26": 0,
            "step_27": 0,
            "step_28": 0,
            "step_29": 0,
            "step_30": 0,
            "step_31": 0,
            "step_32": 0,
            "gate_in": 0,
            "queue_start": 0,
            "key_input_note": 0,
            "key_input_gate": 0,
        },
        "cpu": 2,
        "blocks": {
            "step_1": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "step_2": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "step_3": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "step_4": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "step_5": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "step_6": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "step_7": {"isDefault": False, "isParam": True, "position": 6, "type": "cv_in"},
            "step_8": {"isDefault": False, "isParam": True, "position": 7, "type": "cv_in"},
            "step_9": {"isDefault": False, "isParam": True, "position": 8, "type": "cv_in"},
            "step_10": {"isDefault": False, "isParam": True, "position": 9, "type": "cv_in"},
            "step_11": {"isDefault": False, "isParam": True, "position": 10, "type": "cv_in"},
            "step_12": {"isDefault": False, "isParam": True, "position": 11, "type": "cv_in"},
            "step_13": {"isDefault": False, "isParam": True, "position": 12, "type": "cv_in"},
            "step_14": {"isDefault": False, "isParam": True, "position": 13, "type": "cv_in"},
            "step_15": {"isDefault": False, "isParam": True, "position": 14, "type": "cv_in"},
            "step_16": {"isDefault": False, "isParam": True, "position": 15, "type": "cv_in"},
            "step_17": {"isDefault": False, "isParam": True, "position": 16, "type": "cv_in"},
            "step_18": {"isDefault": False, "isParam": True, "position": 17, "type": "cv_in"},
            "step_19": {"isDefault": False, "isParam": True, "position": 18, "type": "cv_in"},
            "step_20": {"isDefault": False, "isParam": True, "position": 19, "type": "cv_in"},
            "step_21": {"isDefault": False, "isParam": True, "position": 20, "type": "cv_in"},
            "step_22": {"isDefault": False, "isParam": True, "position": 21, "type": "cv_in"},
            "step_23": {"isDefault": False, "isParam": True, "position": 22, "type": "cv_in"},
            "step_24": {"isDefault": False, "isParam": True, "position": 23, "type": "cv_in"},
            "step_25": {"isDefault": False, "isParam": True, "position": 24, "type": "cv_in"},
            "step_26": {"isDefault": False, "isParam": True, "position": 25, "type": "cv_in"},
            "step_27": {"isDefault": False, "isParam": True, "position": 26, "type": "cv_in"},
            "step_28": {"isDefault": False, "isParam": True, "position": 27, "type": "cv_in"},
            "step_29": {"isDefault": False, "isParam": True, "position": 28, "type": "cv_in"},
            "step_30": {"isDefault": False, "isParam": True, "position": 29, "type": "cv_in"},
            "step_31": {"isDefault": False, "isParam": True, "position": 30, "type": "cv_in"},
            "step_32": {"isDefault": False, "isParam": True, "position": 31, "type": "cv_in"},
            "gate_in": {"isDefault": True, "isParam": True, "position": 32, "type": "cv_in"},
            "queue_start": {"isDefault": False, "isParam": True, "position": 33, "type": "cv_in"},
            "key_input_note": {"isDefault": False, "isParam": True, "position": 34, "type": "cv_in"},
            "key_input_gate": {"isDefault": False, "isParam": True, "position": 35, "type": "cv_in"},
            "out_track_1": {"isDefault": True, "isParam": False, "position": 36, "type": "cv_out"},
            "out_track_2": {"isDefault": False, "isParam": False, "position": 37, "type": "cv_out"},
            "out_track_3": {"isDefault": False, "isParam": False, "position": 38, "type": "cv_out"},
            "out_track_4": {"isDefault": False, "isParam": False, "position": 39, "type": "cv_out"},
            "out_track_5": {"isDefault": False, "isParam": False, "position": 40, "type": "cv_out"},
            "out_track_6": {"isDefault": False, "isParam": False, "position": 41, "type": "cv_out"},
            "out_track_7": {"isDefault": False, "isParam": False, "position": 42, "type": "cv_out"},
            "out_track_8": {"isDefault": False, "isParam": False, "position": 43, "type": "cv_out"},
        },
        "options": {
            "number_of_steps": list(range(1, 33)),
            "num_of_tracks": list(range(1, 9)),
            "restart_jack": ["off", "on"],
            "behavior": ["loop", "one_shot", "cv_step"],
            "key_input": ["off", "selected", "increment", "active"],
            "number_of_pages": list(range(1, 9)),
        },
    },
    5: {
        "name": "LFO",
        "category": "CV",
        "description": """
            The Low Frequency Oscillator is one of the workhorse modules of the
            ZOIA. This will generate CV in the waveform and range of your choosing.
            Connect it to a sequencer to cycle through steps, to an audio effect to
            swing it's parameters around, or to any outboard piece of gear through a
            MIDI or CV interface module. The connection strength you enter at the
            output will determine the maximum sweep of the LFO.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 5,
        "params": 4,
        "param_defaults": {
            "cv_control": 0.2,
            "tap_control": 0,
            "swing_amount": 0.5,
            "phase_input": 0.5,
            "phase_reset": 0,
        },
        "cpu": 0.3,
        "blocks": {
            "cv_control": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "tap_control": {"isDefault": False, "isParam": True, "position": 1, "type": "cv_in"},
            "swing_amount": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "phase_input": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "phase_reset": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "output": {"isDefault": True, "isParam": False, "position": 3, "type": "cv_out"},
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
            from an oscillator a natural sounding envelope when played from a
            keyboard. Connect your oscillator or other audio source to the input of
            a VCA, and connect the CV output of the ADSR to the CV input on the VCA.
            Connect the keyboard or MIDI note gate out to the CV input of the ADSR
            and you've got yourself a simple synthesizer! Tweak the values to taste,
            or connect them to other CV inputs for experimentation. Use the optional
            retrigger input to restart the envelope around a note that is played
            before the ADSR is released.
        """,
        "default_blocks": 6,
        "min_blocks": 4,
        "max_blocks": 10,
        "params": 9,
        "param_defaults": {
            "cv_input": 0,
            "retrigger": 0,
            "delay": 0,
            "attack": 0.4,
            "hold_attack_decay": 0.4,
            "decay": 0.4,
            "sustain": 0.5,
            "hold_sustain_release": 0.4,
            "release": 0.5,
        },
        "cpu": 0.07,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "retrigger": {"isDefault": False, "isParam": True, "position": 1, "type": "cv_in"},
            "delay": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "attack": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "hold_attack_decay": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "decay": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "sustain": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "hold_sustain_release": {"isDefault": False, "isParam": True, "position": 7, "type": "cv_in"},
            "release": {"isDefault": True, "isParam": True, "position": 8, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 9, "type": "cv_out"},
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
            The Voltage Controlled Amplifier module will interpret incoming CV at
            the level control and boost or cut the volume. Connect an ADSR to create
            a natural sounding envelope for an oscillator passing through. Connect
            an LFO to create a tremolo effect. Or connect an expression pedal module
            or MIDI input for an external volume control.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 5,
        "params": 1,
        "param_defaults": {
            "level_control": 0,
        },
        "cpu": 0.3,
        "blocks": {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_2": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "level_control": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "audio_out_1": {"isDefault": True, "isParam": False, "position": 3, "type": "audio_out"},
            "audio_out_2": {"isDefault": False, "isParam": False, "position": 4, "type": "audio_out"},
        },
        "options": {"channels": ["1in->1out", "stereo"]},
    },
    8: {
        "name": "Audio Multiply",
        "category": "Audio",
        "description": """
            Takes one audio input and mathematically multiplies it with the other.
            This produces a ring mod/vocoder-like effect, or can be used as an
            alternative to a pitch-shifter to produce analog-like octave fuzz sounds
            when used with a fuzz or distortion. This module likes hot signals so be
            sure to bump the connection strengths. Remember that silence at any one
            of the inputs will result in silence at the output!
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.2,
        "blocks": {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_2": {"isDefault": True, "isParam": False, "position": 1, "type": "audio_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_out"},
        },
        "options": {},
    },
    9: {
        "name": "Bit Crusher",
        "category": "Audio",
        "description": """
            Bit Crusher produces distortion by reducing audio bandwidth by a set
            number of bits. Distortion becomes audible around 20 bits reduced. This
            effect can get noisy so try it with a gate.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "param_defaults": {
            "crushed_bits": 0,
        },
        "cpu": 0.3,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "crushed_bits": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_out"},
        },
        "options": {"fractions": ["off", "on"]},
    },
    10: {
        "name": "Sample and Hold",
        "category": "CV",
        "description": """
            Sample and Hold will take the CV value at the input and hold it in place
            at the output until triggered to look again at the input and update the
            output. Connect a LFO to the trigger to convert smooth changes in CV
            into stepped changes in CV. The speed of the LFO will determine the
            perceived resolution of the CV output.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "param_defaults": {
            "cv_input": 0,
            "trigger": 0,
        },
        "cpu": 0.1,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "trigger": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2, "type": "cv_out"},
        },
        "options": {"track & hold": ["off", "on"]},
    },
    11: {
        "name": "OD & Distortion",
        "category": "Effect",
        "description": """
            The OD & Distortion module provides classic overdrive and distortion
            tones.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 4,
        "params": 2,
        "param_defaults": {
            "input_gain": 0.25,
            "output_gain": 0.75,
        },
        "cpu": 14.2,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "input_gain": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "output_gain": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_out"},
        },
        "options": {"model": ["plexi", "germ", "classic", "pushed", "edgy"]},
    },
    12: {
        "name": "Env Follower",
        "category": "Analysis",
        "description": """
            Envelope Follower will interpret an incoming audio signal as a CV signal
            based on its signal strength. Use this to trigger filter sweeps, audio
            effects parameters, LFO rates, etc. The connection strength can act as a
            sensitivity control.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 4,
        "params": 2,
        "param_defaults": {
            "rise_time": 0.21,
            "fall_time": 0.42,
        },
        "cpu": 2.5,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "rise_time": {"isDefault": False, "isParam": True, "position": 1, "type": "cv_in"},
            "fall_time": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 3, "type": "cv_out"},
        },
        "options": {"rise_fall_time": ["off", "on"], "output_scale": ["log", "linear"]},
    },
    13: {
        "name": "Delay Line",
        "category": "Audio",
        "description": """
            The Delay Line is a simple module that takes audio at the input and
            delays it by a set amount of time. There is no dry signal, there are no
            repeats. You can create repeats by connecting the output back to the
            input, using the connection strength to adjust number of repeats.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 4,
        "params": 3,
        "param_defaults": {
            "delay_time": 0,
            "modulation_in": 0,
            "tap_tempo_in": 0,
        },
        "cpu": 2,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "delay_time": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "modulation_in": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 4, "type": "audio_out"},
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
            Generates an audio signal in the waveform of your choice. Connect a MIDI
            device, keyboard module, sequencer, pitch detector, LFO, or any CV
            source to select the frequency or note the oscillator will play.  You
            can modulate the frequency or pulse width with the optional parameters.
            Negative CV inputs (from -1 to 0) will generate sub-bass frequencies
            between 0.027Hz and 27.49Hz. Be careful!
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 4,
        "params": 2,
        "param_defaults": {
            "frequency": 0,
            "duty_cycle": 0.5,
        },
        "cpu": 6,
        "blocks": {
            "frequency": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "fm_input": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "duty_cycle": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 3, "type": "audio_out"},
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
            Turns a grid button into a button you can push to send a CV signal. Tap
            in a tempo, open up a VCA, trigger a sequencer, or anything else. The
            grid is your oyster!
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.02,
        "blocks": {"cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"}},
        "options": {
            "action": ["momentary", "latching"],
            "normally": ["zero", "one"]
        },
    },
    16: {
        "name": "Keyboard",
        "category": "Interface",
        "description": """
            Turns grid buttons into a keyboard you can connect to an oscillator and
            play. No external MIDI controller necessary! Tune each keyboard button
            using the knob to have it play your desired note.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 43,
        "params": 40,
        "param_defaults": {
            "note_1": 0,
            "note_2": 0,
            "note_3": 0,
            "note_4": 0,
            "note_5": 0,
            "note_6": 0,
            "note_7": 0,
            "note_8": 0,
            "note_9": 0,
            "note_10": 0,
            "note_11": 0,
            "note_12": 0,
            "note_13": 0,
            "note_14": 0,
            "note_15": 0,
            "note_16": 0,
            "note_17": 0,
            "note_18": 0,
            "note_19": 0,
            "note_20": 0,
            "note_21": 0,
            "note_22": 0,
            "note_23": 0,
            "note_24": 0,
            "note_25": 0,
            "note_26": 0,
            "note_27": 0,
            "note_28": 0,
            "note_29": 0,
            "note_30": 0,
            "note_31": 0,
            "note_32": 0,
            "note_33": 0,
            "note_34": 0,
            "note_35": 0,
            "note_36": 0,
            "note_37": 0,
            "note_38": 0,
            "note_39": 0,
            "note_40": 0,
        },
        "cpu": 0.1,
        "blocks": {
            "note_1": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "note_2": {"isDefault": False, "isParam": True, "position": 1, "type": "cv_in"},
            "note_3": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "note_4": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "note_5": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "note_6": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "note_7": {"isDefault": False, "isParam": True, "position": 6, "type": "cv_in"},
            "note_8": {"isDefault": False, "isParam": True, "position": 7, "type": "cv_in"},
            "note_9": {"isDefault": False, "isParam": True, "position": 8, "type": "cv_in"},
            "note_10": {"isDefault": False, "isParam": True, "position": 9, "type": "cv_in"},
            "note_11": {"isDefault": False, "isParam": True, "position": 10, "type": "cv_in"},
            "note_12": {"isDefault": False, "isParam": True, "position": 11, "type": "cv_in"},
            "note_13": {"isDefault": False, "isParam": True, "position": 12, "type": "cv_in"},
            "note_14": {"isDefault": False, "isParam": True, "position": 13, "type": "cv_in"},
            "note_15": {"isDefault": False, "isParam": True, "position": 14, "type": "cv_in"},
            "note_16": {"isDefault": False, "isParam": True, "position": 15, "type": "cv_in"},
            "note_17": {"isDefault": False, "isParam": True, "position": 16, "type": "cv_in"},
            "note_18": {"isDefault": False, "isParam": True, "position": 17, "type": "cv_in"},
            "note_19": {"isDefault": False, "isParam": True, "position": 18, "type": "cv_in"},
            "note_20": {"isDefault": False, "isParam": True, "position": 19, "type": "cv_in"},
            "note_21": {"isDefault": False, "isParam": True, "position": 20, "type": "cv_in"},
            "note_22": {"isDefault": False, "isParam": True, "position": 21, "type": "cv_in"},
            "note_23": {"isDefault": False, "isParam": True, "position": 22, "type": "cv_in"},
            "note_24": {"isDefault": False, "isParam": True, "position": 23, "type": "cv_in"},
            "note_25": {"isDefault": False, "isParam": True, "position": 24, "type": "cv_in"},
            "note_26": {"isDefault": False, "isParam": True, "position": 28, "type": "cv_in"},
            "note_27": {"isDefault": False, "isParam": True, "position": 29, "type": "cv_in"},
            "note_28": {"isDefault": False, "isParam": True, "position": 30, "type": "cv_in"},
            "note_29": {"isDefault": False, "isParam": True, "position": 31, "type": "cv_in"},
            "note_30": {"isDefault": False, "isParam": True, "position": 32, "type": "cv_in"},
            "note_31": {"isDefault": False, "isParam": True, "position": 33, "type": "cv_in"},
            "note_32": {"isDefault": False, "isParam": True, "position": 34, "type": "cv_in"},
            "note_33": {"isDefault": False, "isParam": True, "position": 35, "type": "cv_in"},
            "note_34": {"isDefault": False, "isParam": True, "position": 36, "type": "cv_in"},
            "note_35": {"isDefault": False, "isParam": True, "position": 37, "type": "cv_in"},
            "note_36": {"isDefault": False, "isParam": True, "position": 38, "type": "cv_in"},
            "note_37": {"isDefault": False, "isParam": True, "position": 39, "type": "cv_in"},
            "note_38": {"isDefault": False, "isParam": True, "position": 40, "type": "cv_in"},
            "note_39": {"isDefault": False, "isParam": True, "position": 41, "type": "cv_in"},
            "note_40": {"isDefault": False, "isParam": True, "position": 42, "type": "cv_in"},
            "note_out": {"isDefault": True, "isParam": False, "position": 25, "type": "cv_out"},
            "gate_out": {"isDefault": True, "isParam": False, "position": 26, "type": "cv_out"},
            "trigger_out": {"isDefault": True, "isParam": False, "position": 27, "type": "cv_out"},
        },
        "options": {"#_of_notes": list(range(1, 41))},
    },
    17: {
        "name": "CV Invert",
        "category": "CV",
        "description": """
            Inverts the incoming CV. For example, a CV input of 1 will output as -1.
            An input of 0.2 will output as -0.2.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "param_defaults": {
            "cv_input": 0,
        },
        "cpu": 0.02,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"},
        },
        "options": {},
    },
    18: {
        "name": "Steps",
        "category": "CV",
        "description": """
            Steps will interpret incoming changes in upward CV as a tempo, split the
            wave cycle into a set number of steps, and then send the CV present at
            the input during each step to the output. You can use this to convert a
            nice smooth LFO and reduce its resolution into steps.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "param_defaults": {
            "cv_input": 0,
            "quant_steps": 0,
        },
        "cpu": 0.7,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "quant_steps": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2, "type": "cv_out"},
        },
        "options": {},
    },
    19: {
        "name": "Slew Limiter",
        "category": "CV",
        "description": """
            Slew Limiter is similar in behaviour to CV Filter except that the rate
            of change in changes of CV happen linearly instead of logarithmically.
            This is the classic portamento, and can be used anywhere CV changes
            occur to give them a different feel. Try using an unlinked Slew Limiter
            with a stomp switch module to give more expression pedal-like behaviour
            to your stomp switch.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 4,
        "params": 2,
        "param_defaults": {
            "cv_input": 0,
            "slew_rate": 0.71,
            "rising_lag": 0.71,
            "falling_lag": 0.71,
        },
        "cpu": 0.2,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "slew_rate": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "rising_lag": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "falling_lag": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 4, "type": "cv_out"},
        },
        "options": {
            "control": ["linked", "separate"],
        },
    },
    20: {
        "name": "Midi Notes In",
        "category": "Interface",
        "description": """
            Connect your MIDI keyboard controller to the ZOIA. Connect the note out
            to an oscillator to have it play your note, and connect the gate out to
            an ADSR (connected to a VCA) for a natural envelope.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 32,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {
            "note_out_1": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"},
            "gate_out_1": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"},
            "velocity_out_1": {"isDefault": False, "isParam": False, "position": 2, "type": "cv_out"},
            "trigger_out_1": {"isDefault": False, "isParam": False, "position": 3, "type": "cv_out"},
            "note_out_2": {"isDefault": False, "isParam": False, "position": 4, "type": "cv_out"},
            "gate_out_2": {"isDefault": False, "isParam": False, "position": 5, "type": "cv_out"},
            "velocity_out_2": {"isDefault": False, "isParam": False, "position": 6, "type": "cv_out"},
            "trigger_out_2": {"isDefault": False, "isParam": False, "position": 7, "type": "cv_out"},
            "note_out_3": {"isDefault": False, "isParam": False, "position": 8, "type": "cv_out"},
            "gate_out_3": {"isDefault": False, "isParam": False, "position": 9, "type": "cv_out"},
            "velocity_out_3": {"isDefault": False, "isParam": False, "position": 10, "type": "cv_out"},
            "trigger_out_3": {"isDefault": False, "isParam": False, "position": 11, "type": "cv_out"},
            "note_out_4": {"isDefault": False, "isParam": False, "position": 12, "type": "cv_out"},
            "gate_out_4": {"isDefault": False, "isParam": False, "position": 13, "type": "cv_out"},
            "velocity_out_4": {"isDefault": False, "isParam": False, "position": 14, "type": "cv_out"},
            "trigger_out_4": {"isDefault": False, "isParam": False, "position": 15, "type": "cv_out"},
            "note_out_5": {"isDefault": False, "isParam": False, "position": 16, "type": "cv_out"},
            "gate_out_5": {"isDefault": False, "isParam": False, "position": 17, "type": "cv_out"},
            "velocity_out_5": {"isDefault": False, "isParam": False, "position": 18, "type": "cv_out"},
            "trigger_out_5": {"isDefault": False, "isParam": False, "position": 19, "type": "cv_out"},
            "note_out_6": {"isDefault": False, "isParam": False, "position": 20, "type": "cv_out"},
            "gate_out_6": {"isDefault": False, "isParam": False, "position": 21, "type": "cv_out"},
            "velocity_out_6": {"isDefault": False, "isParam": False, "position": 22, "type": "cv_out"},
            "trigger_out_6": {"isDefault": False, "isParam": False, "position": 23, "type": "cv_out"},
            "note_out_7": {"isDefault": False, "isParam": False, "position": 24, "type": "cv_out"},
            "gate_out_7": {"isDefault": False, "isParam": False, "position": 25, "type": "cv_out"},
            "velocity_out_7": {"isDefault": False, "isParam": False, "position": 26, "type": "cv_out"},
            "trigger_out_7": {"isDefault": False, "isParam": False, "position": 27, "type": "cv_out"},
            "note_out_8": {"isDefault": False, "isParam": False, "position": 28, "type": "cv_out"},
            "gate_out_8": {"isDefault": False, "isParam": False, "position": 29, "type": "cv_out"},
            "velocity_out_8": {"isDefault": False, "isParam": False, "position": 30, "type": "cv_out"},
            "trigger_out_8": {"isDefault": False, "isParam": False, "position": 31, "type": "cv_out"},
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
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cc_out": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"}},
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
            Multiply will take the CV signal present at each input and multiply them
            together at the output. In this way you can use one CV source to
            amplify, tame, or modulate another. Remember that a value of 0 at any
            input will result in 0 at the output. It's math!
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 9,
        "params": 2,
        "param_defaults": {
            "cv_input_1": 0,
            "cv_input_2": 0,
            "cv_input_3": 0,
            "cv_input_4": 0,
            "cv_input_5": 0,
            "cv_input_6": 0,
            "cv_input_7": 0,
            "cv_input_8": 0,
        },
        "cpu": 0.2,
        "blocks": {
            "cv_input_1": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_input_2": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "cv_input_3": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "cv_input_4": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "cv_input_5": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "cv_input_6": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "cv_input_7": {"isDefault": False, "isParam": True, "position": 6, "type": "cv_in"},
            "cv_input_8": {"isDefault": False, "isParam": True, "position": 7, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 8, "type": "cv_out"},
        },
        "options": {"num_inputs": list(range(2, 9))},
    },
    23: {
        "name": "Compressor",
        "category": "Effect",
        "description": """
            Compression is a vastly useful audio tool that controls your signal
            level according to changes in input level. You can create natural
            reductions in gain to help things mix better, help tame or enhance
            transients in synth or instrument signals, etc. The optional stereo side
            will trigger the module's functions in unison on both channels, creating
            true stereo compression.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 9,
        "params": 4,
        "param_defaults": {
            "threshold": 0.5,
            "attack": 0.5,
            "release": 0.5,
            "ratio": 0.2,
        },
        "cpu": 2.4,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "threshold": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "attack": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "release": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "ratio": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "sidechain_in": {"isDefault": False, "isParam": False, "position": 8, "type": "audio_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7, "type": "audio_out"},
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
        "param_defaults": {
            "gain": 0.5,
            "frequency": 0.5,
            "q": 0.28,
        },
        "cpu": 0.8,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "gain": {"isDefault": False, "isParam": True, "position": 1, "type": "cv_in"},
            "frequency": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "q": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 4, "type": "audio_out"},
        },
        "options": {
            "filter_shape": [
                "lowpass",
                "hi_shelf",
                "bell",
                "highpass",
                "low_shelf",
                "bandpass",
            ],
        },
    },
    25: {
        "name": "Plate Reverb",
        "category": "Effect",
        "description": """
            Bask in the ebb and flow of steel molecules as they vibrate with the
            warm vintage vibe of so many classic recordings.
        """,
        "default_blocks": 8,
        "min_blocks": 8,
        "max_blocks": 8,
        "params": 4,
        "param_defaults": {
            "decay_time": 0.5,
            "low_eq": 0.5,
            "high_eq": 0.5,
            "mix": 0.5,
        },
        "cpu": 16.7,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": True, "isParam": False, "position": 1, "type": "audio_in"},
            "decay_time": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "low_eq": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "high_eq": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 4, "type": "audio_out"},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 5, "type": "audio_out"},
        },
        "options": {},
    },
    26: {
        "name": "Buffer Delay",
        "category": "Audio",
        "description": """
            Delays internal audio signal by number of buffers set by buffers option.
            This module is inaudible, but useful anywhere you need to line up
            internal parallel audio connections precisely.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.2,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 1, "type": "audio_out"},
        },
        "options": {"buffer_length": list(range(0, 17))},
    },
    27: {
        "name": "All Pass Filter",
        "category": "Audio",
        "description": """
            All Pass Filter passes through all frequencies at equal gain, but
            changes phase relationship between them.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "param_defaults": {
            "filter_gain": 0,
        },
        "cpu": 3,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "filter_gain": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_out"},
        },
        "options": {"#_of_poles": list(range(1, 9))},
    },
    28: {
        "name": "Quantizer",
        "category": "CV",
        "description": """
            Quantizer will interpret incoming CV and send its nearest equivalent
            note as a CV output.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 4,
        "params": 3,
        "param_defaults": {
            "cv_input": 0,
            "key": 0,
            "scale": 0,
        },
        "cpu": 1,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "key": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "scale": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"},
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
            sweeps the frequency of these poles at a set rate. An optional stereo
            channel rounds out the list of features.
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "param_defaults": {
            "rate": 0.1,
            "tap_tempo_in": 0,
            "control_in": 0,
            "resonance": 0,
            "width": 0.7,
            "mix": 0.5,
        },
        "cpu": 7.5,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "rate": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 7, "type": "cv_in"},
            "control_in": {"isDefault": False, "isParam": True, "position": 8, "type": "cv_in"},
            "resonance": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "width": {"isDefault": True, "isParam": True, "position": 9, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 5, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 6, "type": "audio_out"},
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
            The Looper module allows you to record, overdub, and play back incoming
            audio, forwards or backwards, at the speed of your choice (pitch
            shifted). Get loopy!
        """,
        "default_blocks": 5,
        "min_blocks": 5,
        "max_blocks": 10,
        "params": 6,
        "param_defaults": {
            "record": 0,
            "restart_playback": 0,
            "stop_play": 0,
            "speed_pitch": 0.5,
            "start_position": 0,
            "loop_length": 1,
            "reverse_playback": 0,
            "reset": 0,
        },
        "cpu": 0.3,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "record": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "restart_playback": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "stop_play": {"isDefault": False, "isParam": True, "position": 9, "type": "cv_in"},
            "speed_pitch": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "start_position": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "loop_length": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "reverse_playback": {"isDefault": False, "isParam": True, "position": 7, "type": "cv_in"},
            "reset": {"isDefault": False, "isParam": True, "position": 8, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 6, "type": "audio_out"},
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
            In Switch takes a selected quantity of CV inputs and allows you to
            switch between them to a single CV output. You can use this to select
            between LFOs to a CV source, external CV modules, or use in conjunction
            with the CV out switch to choose between ADSRs or other CV module chains
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 18,
        "params": 17,
        "param_defaults": {
            "cv_input_1": 0,
            "cv_input_2": 0,
            "cv_input_3": 0,
            "cv_input_4": 0,
            "cv_input_5": 0,
            "cv_input_6": 0,
            "cv_input_7": 0,
            "cv_input_8": 0,
            "cv_input_9": 0,
            "cv_input_10": 0,
            "cv_input_11": 0,
            "cv_input_12": 0,
            "cv_input_13": 0,
            "cv_input_14": 0,
            "cv_input_15": 0,
            "cv_input_16": 0,
            "in_select": 0,
        },
        "cpu": 0.2,
        "blocks": {
            "cv_input_1": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_input_2": {"isDefault": False, "isParam": True, "position": 1, "type": "cv_in"},
            "cv_input_3": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "cv_input_4": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "cv_input_5": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "cv_input_6": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "cv_input_7": {"isDefault": False, "isParam": True, "position": 6, "type": "cv_in"},
            "cv_input_8": {"isDefault": False, "isParam": True, "position": 7, "type": "cv_in"},
            "cv_input_9": {"isDefault": False, "isParam": True, "position": 8, "type": "cv_in"},
            "cv_input_10": {"isDefault": False, "isParam": True, "position": 9, "type": "cv_in"},
            "cv_input_11": {"isDefault": False, "isParam": True, "position": 10, "type": "cv_in"},
            "cv_input_12": {"isDefault": False, "isParam": True, "position": 11, "type": "cv_in"},
            "cv_input_13": {"isDefault": False, "isParam": True, "position": 12, "type": "cv_in"},
            "cv_input_14": {"isDefault": False, "isParam": True, "position": 13, "type": "cv_in"},
            "cv_input_15": {"isDefault": False, "isParam": True, "position": 14, "type": "cv_in"},
            "cv_input_16": {"isDefault": False, "isParam": True, "position": 15, "type": "cv_in"},
            "in_select": {"isDefault": True, "isParam": True, "position": 16, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 17, "type": "cv_out"},
        },
        "options": {"num_inputs": list(range(1, 17))},
    },
    32: {
        "name": "Out Switch",
        "category": "CV",
        "description": """
            Out Switch takes a CV input and routes it between a set quantity of CV
            outputs. You can use it to select which sequencers, ADSRs, or tap tempos
            to send triggers to, etc.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 18,
        "params": 2,
        "param_defaults": {
            "cv_input": 0,
            "out_select": 0,
        },
        "cpu": 0.2,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "out_select": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "cv_output_1": {"isDefault": True, "isParam": False, "position": 2, "type": "cv_out"},
            "cv_output_2": {"isDefault": False, "isParam": False, "position": 3, "type": "cv_out"},
            "cv_output_3": {"isDefault": False, "isParam": False, "position": 4, "type": "cv_out"},
            "cv_output_4": {"isDefault": False, "isParam": False, "position": 5, "type": "cv_out"},
            "cv_output_5": {"isDefault": False, "isParam": False, "position": 6, "type": "cv_out"},
            "cv_output_6": {"isDefault": False, "isParam": False, "position": 7, "type": "cv_out"},
            "cv_output_7": {"isDefault": False, "isParam": False, "position": 8, "type": "cv_out"},
            "cv_output_8": {"isDefault": False, "isParam": False, "position": 9, "type": "cv_out"},
            "cv_output_9": {"isDefault": False, "isParam": False, "position": 10, "type": "cv_out"},
            "cv_output_10": {"isDefault": False, "isParam": False, "position": 11, "type": "cv_out"},
            "cv_output_11": {"isDefault": False, "isParam": False, "position": 12, "type": "cv_out"},
            "cv_output_12": {"isDefault": False, "isParam": False, "position": 13, "type": "cv_out"},
            "cv_output_13": {"isDefault": False, "isParam": False, "position": 14, "type": "cv_out"},
            "cv_output_14": {"isDefault": False, "isParam": False, "position": 15, "type": "cv_out"},
            "cv_output_15": {"isDefault": False, "isParam": False, "position": 16, "type": "cv_out"},
            "cv_output_16": {"isDefault": False, "isParam": False, "position": 17, "type": "cv_out"},
        },
        "options": {"num_outputs": list(range(1, 17))},
    },
    33: {
        "name": "Audio In Switch",
        "category": "Audio",
        "description": """
            Audio In Switch takes a selected quantity of audio inputs and allows you
            to switch between them to a single output. You can use this to select
            between instruments at your input jacks, use it in conjunction with the
            Audio Out Switch to select between effects chains, or use it anywhere
            you'd like to be able to select between incoming audio sources using CV.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 18,
        "params": 1,
        "param_defaults": {
            "in_select": 0,
        },
        "cpu": 0.8,
        "blocks": {
            "audio_input_1": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_input_2": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "audio_input_3": {"isDefault": False, "isParam": False, "position": 2, "type": "audio_in"},
            "audio_input_4": {"isDefault": False, "isParam": False, "position": 3, "type": "audio_in"},
            "audio_input_5": {"isDefault": False, "isParam": False, "position": 4, "type": "audio_in"},
            "audio_input_6": {"isDefault": False, "isParam": False, "position": 5, "type": "audio_in"},
            "audio_input_7": {"isDefault": False, "isParam": False, "position": 6, "type": "audio_in"},
            "audio_input_8": {"isDefault": False, "isParam": False, "position": 7, "type": "audio_in"},
            "audio_input_9": {"isDefault": False, "isParam": False, "position": 10, "type": "audio_in"},
            "audio_input_10": {"isDefault": False, "isParam": False, "position": 11, "type": "audio_in"},
            "audio_input_11": {"isDefault": False, "isParam": False, "position": 12, "type": "audio_in"},
            "audio_input_12": {"isDefault": False, "isParam": False, "position": 13, "type": "audio_in"},
            "audio_input_13": {"isDefault": False, "isParam": False, "position": 14, "type": "audio_in"},
            "audio_input_14": {"isDefault": False, "isParam": False, "position": 15, "type": "audio_in"},
            "audio_input_15": {"isDefault": False, "isParam": False, "position": 14, "type": "audio_in"},
            "audio_input_16": {"isDefault": False, "isParam": False, "position": 15, "type": "audio_in"},
            "in_select": {"isDefault": True, "isParam": True, "position": 16, "type": "cv_in"},
            "audio_output": {"isDefault": True, "isParam": False, "position": 17, "type": "audio_out"},
        },
        "options": {"num_inputs": list(range(1, 17)), "fades": ["on", "off"]},
    },
    34: {
        "name": "Audio Out Switch",
        "category": "Audio",
        "description": """
            Audio Out Switch takes an audio input and routes it between a set
            quantity of audio outputs. You can use it at your output jacks to select
            between amplifiers or mixer channels, use it in conjunction with the
            Audio In Switch to select between effects chains, or use it anywhere
            you'd like to be able to select an outgoing audio path using CV.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 18,
        "params": 1,
        "param_defaults": {
            "in_select": 0,
        },
        "cpu": 0.7,
        "blocks": {
            "audio_input": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "in_select": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "audio_output_1": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_out"},
            "audio_output_2": {"isDefault": False, "isParam": False, "position": 3, "type": "audio_out"},
            "audio_output_3": {"isDefault": True, "isParam": False, "position": 4, "type": "audio_out"},
            "audio_output_4": {"isDefault": False, "isParam": False, "position": 5, "type": "audio_out"},
            "audio_output_5": {"isDefault": True, "isParam": False, "position": 6, "type": "audio_out"},
            "audio_output_6": {"isDefault": False, "isParam": False, "position": 7, "type": "audio_out"},
            "audio_output_7": {"isDefault": True, "isParam": False, "position": 8, "type": "audio_out"},
            "audio_output_8": {"isDefault": False, "isParam": False, "position": 9, "type": "audio_out"},
            "audio_output_9": {"isDefault": True, "isParam": False, "position": 10, "type": "audio_out"},
            "audio_output_10": {"isDefault": False, "isParam": False, "position": 11, "type": "audio_out"},
            "audio_output_11": {"isDefault": True, "isParam": False, "position": 12, "type": "audio_out"},
            "audio_output_12": {"isDefault": False, "isParam": False, "position": 13, "type": "audio_out"},
            "audio_output_13": {"isDefault": True, "isParam": False, "position": 14, "type": "audio_out"},
            "audio_output_14": {"isDefault": False, "isParam": False, "position": 15, "type": "audio_out"},
            "audio_output_15": {"isDefault": True, "isParam": False, "position": 16, "type": "audio_out"},
            "audio_output_16": {"isDefault": False, "isParam": False, "position": 17, "type": "audio_out"},
        },
        "options": {"num_outputs": list(range(1, 17)), "fades": ["on", "off"]},
    },
    35: {
        "name": "Midi Pressure",
        "category": "Interface",
        "description": """
            Many MIDI keyboards have an aftertouch feature that can be triggered by
            pressing down on a note after it's fully depressed. You can use after
            touch to trigger a little extra pizazz in your sound.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.03,
        "blocks": {
            "channel_pressure": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"},
        },
        "options": {"midi_channel": list(range(1, 17))},
    },
    36: {
        "name": "Onset Detector",
        "category": "Analysis",
        "description": """
            Onset Detector looks for incoming audio signal and generates a CV
            trigger at the peaks. Use a regular audio source to advance a sequencer,
            tap a tempo, etc
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 3,
        "params": 1,
        "param_defaults": {
            "sensitivity": 0.5,
        },
        "cpu": 12.3,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "sensitivity": {"isDefault": False, "isParam": True, "position": 1, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_out"},
        },
        "options": {"sensitivity": ["off", "on"]},
    },
    37: {
        "name": "Rhythm",
        "category": "CV",
        "description": """
            Rhythm will take an incoming CV signal, interpret it as a series of
            triggers, record those triggers and play them back at the output.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 5,
        "params": 3,
        "param_defaults": {
            "rec_start_stop": 0,
            "rhythm_in": 0,
            "play": 0,
        },
        "cpu": 0.5,
        "blocks": {
            "rec_start_stop": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "rhythm_in": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "play": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "done_out": {"isDefault": False, "isParam": False, "position": 3, "type": "cv_out"},
            "rhythm_out": {"isDefault": True, "isParam": False, "position": 4, "type": "cv_out"},
        },
        "options": {
            "done_ctrl": ["off", "on"],
        },
    },
    38: {
        "name": "Noise",
        "category": "Audio",
        "description": """
            Generates white noise from a single button. Use the strength of your
            connection as a level control. Helpful in connection with VCAs and ADSRs
            in creating drum sounds, etc.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.4,
        "blocks": {"audio_out": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_out"}},
        "options": {},
    },
    39: {
        "name": "Random",
        "category": "CV",
        "description": """
            Random will generate numbers continuously or when triggered with the
            option trigger in. Connect an LFO to the trigger in to get regularly
            updated random numbers. Try it with a CV in switch to toggle some
            randomness into  your life.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 2,
        "params": 1,
        "param_defaults": {
            "trigger_in": 0,
        },
        "cpu": 0.1,
        "blocks": {
            "trigger_in": {"isDefault": False, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"},
        },
        "options": {"output": ["0 to 1", "-1 to 1"], "new_val_on_trig": ["off", "on"]},
    },
    40: {
        "name": "Gate",
        "category": "Effect",
        "description": """
            A standard in studio audio tools, gate can also be used as the key
            ingredient in gated fuzz tones. Use it to filter out noise from an audio
            source, or to cut the end off of a reverb's decay, thus creating the
            classic gated reverb sound. Make sure to experiment with the sidechain
            input!
        """,
        "default_blocks": 5,
        "min_blocks": 3,
        "max_blocks": 8,
        "params": 3,
        "param_defaults": {
            "threshold": 0,
            "attack": 0.5,
            "release": 0.5,
        },
        "cpu": 2.8,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "threshold": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "attack": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "release": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "sidechain_in": {"isDefault": False, "isParam": False, "position": 7, "type": "audio_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 5, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 6, "type": "audio_out"},
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
            Up and down, side to side. Tremolo helps your smile get wide. Set speed
            and depth and tap in a tempo if you like. If you'd like a tremolo effect
            with more control, try creating one using the VCA or Audio Panner along
            with LFOs and various other CV tools to get radical!
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 6,
        "params": 2,
        "param_defaults": {
            "rate": 0.5,
            "tap_tempo_in": 0,
            "direct": 0,
            "depth": 0.59,
        },
        "cpu": 1.5,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "rate": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "direct": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "depth": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7, "type": "audio_out"},
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
            Tone Control is a 3 or 4 band tone control. Use this in conjunction with
            Distortion, Delay w/Mod, Reverb, or even a clean sound to fundamentally
            change its character.
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 10,
        "params": 6,
        "param_defaults": {
            "low_shelf": 0.5,
            "mid_gain_1": 0.5,
            "mid_freq_1": 0.5,
            "mid_gain_2": 0.5,
            "mid_freq_2": 0.5,
            "high_shelf": 0.5,
        },
        "cpu": 2.2,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "low_shelf": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "mid_gain_1": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "mid_freq_1": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "mid_gain_2": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "mid_freq_2": {"isDefault": False, "isParam": True, "position": 6, "type": "cv_in"},
            "high_shelf": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 9, "type": "audio_out"},
        },
        "options": {
            "channels": ["1in->1out", "stereo"],
            "num_mid_bands": [1, 2],
        },
    },
    43: {
        "name": "Delay w/Mod",
        "category": "Effect",
        "description": """
            Delay is one of the classic delay effects. Delay w/Mod differs from the
            Delay Line module found in Audio Out in that it runs a dry signal
            alongside the wet, has a feedback section, and a modulation section. Set
            the delay time either by tap or rotary/CV input. Optional stereo outputs
            round out the list of features. You can change the character of the
            delay effect with the "type" option, and/or by setting your mix to wet
            only, adding tone control and other effects to the output, and
            connecting your audio source directly to your output (bypassing the
            delay module) to act as the dry signal.
        """,
        "default_blocks": 7,
        "min_blocks": 7,
        "max_blocks": 9,
        "params": 5,
        "param_defaults": {
            "delay_time": 0.5,
            "tap_tempo_in": 0,
            "feedback": 0.4,
            "mod_rate": 0.3,
            "mod_depth": 0.2,
            "mix": 0.2,
        },
        "cpu": 11,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "delay_time": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "feedback": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "mod_rate": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "mod_depth": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 9, "type": "audio_out"},
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
            Use this module to connect a stomp switch to other modules. This can be
            any of ZOIA's 3 stomp switches or an external one. If using an external,
            remember to set it up in the Config Menu. Once placed, the Scroll and
            Bypass stomp switches must be "switched to" by holding them both on
            together for 2 seconds, this will allow them to function in the modules
            instead of as ZOIA's main user interface. Hold again for 2 seconds to
            switch back.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cv_output": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"}},
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
        "param_defaults": {
            "value": 0,
        },
        "cpu": 0.15,
        "blocks": {
            "value": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"},
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
        "param_defaults": {
            "cv_input": 0,
            "delay_time": 0,
        },
        "cpu": 1.5,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "delay_time": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2, "type": "cv_out"},
        },
        "options": {"cv_input": ["exponent", "linear"]},
    },
    47: {
        "name": "CV Loop",
        "category": "CV",
        "description": """
            CV Loop functions similar to an audio looper except records patterns of
            CV signal instead of audio. You can record and play back snippets of
            LFOs, sequences, changes in CV or MIDI control etc.
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 7,
        "param_defaults": {
            "cv_input": 0,
            "record": 0,
            "play": 0,
            "playback_speed": 0.5,
            "start_position": 0,
            "stop_position": 1,
            "restart_loop": 0,
        },
        "cpu": 0.1,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "record": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "play": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "playback_speed": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "start_position": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "stop_position": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "restart_loop": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 7, "type": "cv_out"},
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
            CV Filter dictates the length of time a CV output will take to respond
            to a change in CV input, determined by the time constant. The CV change
            occurs logarithmically for a nice smooth transition. Use this module in
            series with a MIDI/keyboard note to add portamento to your synth voice.
            You can also use this module to vary the shape of an LFO waveform or
            connect to a stomp switch to produce a long slow change in an audio
            effect.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 4,
        "params": 2,
        "param_defaults": {
            "cv_input": 0,
            "time_constant": 0,
            "rise_constant": 0,
            "fall_constant": 0,
        },
        "cpu": 0.1,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "time_constant": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "rise_constant": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "fall_constant": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2, "type": "cv_out"},
        },
        "options": {"control": ["linked", "separate"]},
    },
    49: {
        "name": "Clock Divider",
        "category": "CV",
        "description": """
            Clock Divider module will detect tempo of incoming CV upward changes,
            divide it by a user determined ratio, and output CV triggers at the
            resulting tempo. This can be a handy way of getting a tap tempo from a
            slightly irregular waveform.
        """,
        "default_blocks": 5,
        "min_blocks": 4,
        "max_blocks": 5,
        "params": 4,
        "param_defaults": {
            "cv_input": 0,
            "reset_in": 0,
            "modifier": 0,
            "dividend": 0,
            "divisor": 0,
        },
        "cpu": 0.14,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "reset_in": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "modifier": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "dividend": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "divisor": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 3, "type": "cv_out"},
        },
        "options": {"input": ["tap", "cv_control"]},
    },
    50: {
        "name": "Comparator",
        "category": "CV",
        "description": """
            Comparator is a logic module that will switch CV on if positive input is
            equal to or greater than negative input, and off if positive input is
            less than negative input. Off can be defined as 0 or -1 by the output
            range. This can be useful if you'd like to have something happen, but
            only above a certain threshold.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "param_defaults": {
            "cv_positive_input": 0,
            "cv_negative_input": 0,
        },
        "cpu": 0.04,
        "blocks": {
            "cv_positive_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_negative_input": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2, "type": "cv_out"},
        },
        "options": {"output": ["0 to 1", "-1 to 1"]},
    },
    51: {
        "name": "CV Rectify",
        "category": "CV",
        "description": """
            CV Rectify will interpret incoming CV from -1 to 1 and "flip" the
            negative values into positive values equidistant from 0.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "param_defaults": {
            "cv_input": 0,
        },
        "cpu": 0.07,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"},
        },
        "options": {},
    },
    52: {
        "name": "Trigger",
        "category": "CV",
        "description": """
            Creates a very short CV pulse (value of 1) on detection of upward CV
            input. This is useful in creating a tap tempos from regular or irregular
            CV waveforms, triggering sequencers or ADSRs at specific times, etc.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "param_defaults": {
            "cv_input": 0,
        },
        "cpu": 0.1,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"},
        },
        "options": {},
    },
    53: {
        "name": "Stereo Spread",
        "category": "Audio",
        "description": """
            Stereo Spread will take one or two channels and enhance their stereo
            field. This is generally used right before an audio output module but,
            as always, feel free to experiment!
        """,
        "default_blocks": 5,
        "min_blocks": 4,
        "max_blocks": 5,
        "params": 1,
        "param_defaults": {
            "side_gain": 0.83,
            "delay_time": 0.5,
        },
        "cpu": 1.5,
        "blocks": {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_2": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "side_gain": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "delay_time": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "audio_out_1": {"isDefault": True, "isParam": False, "position": 4, "type": "audio_out"},
            "audio_out_2": {"isDefault": True, "isParam": False, "position": 5, "type": "audio_out"},
        },
        "options": {"method": ["mid_side", "haas"]},
    },
    54: {
        "name": "Cport Exp/CV In",
        "category": "Interface",
        "description": """
            Connect your expression pedal or a control voltage signal from an external source.
            Remember to set CPort to either exp or cv in the Config Menu.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cv_output": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"}},
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
        "param_defaults": {
        },
        "cpu": 0.2,
        "blocks": {"cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"}},
        "options": {"input_range": ["0 to 1", "-1 to 1"]},
    },
    56: {
        "name": "UI Button",
        "category": "Interface",
        "description": """
            UI Button can function in a couple different ways. It can show you a
            specific colour at a specific brightness based on the setting of or CV
            sent to the input. It can also act as a pushbutton with output enabled.
            To use as a visualizing pixel, connect CV and send the following values:
            EXTENDED RANGE: Red: 0 - 0.049 (max bright 0.0375), Orange: 0.05 - 0.099
            (max bright 0.0875), Mango: 0.10 - 0.149 (max bright 0.1375), Yellow:
            0.15 - 0.199 (max bright 0.1875), Lime: 0.20 - 0.249 (max bright
            0.2375), Green: 0.25 - 0.299 (max bright 0.2875), Surf: 0.30 - 0.349
            (max bright 0.3375), Aqua: 0.35 - 0.399 (max bright 0.3875), Sky: 0.40 -
            0.449 (max bright 0.4375), Blue: 0.45 - 0.499 (max bright 0.4875),
            Purple: 0.50 - 0.549 (max bright 0.5375), Magenta: 0.55 - 0.599 (max
            bright 0.5875), Pink: 0.60 - 0.649 (max bright 0.6375), Peach: 0.65 -
            0.699 (max bright 0.6875) , White: 0.70 - 0.749 (max bright 0.7375).
            BASIC RANGE: Blue = 0 to 0.099 (0.74 max brightness), Green = 0.1 to
            0.199 (0.174 max brightness), Red = 0.2 to 0.299 (0.274 max brightness),
            Yellow = 0.3 to 0.399 (0.374 max brightness), Cyan = 0.4 to 0.499 (0.474
            max brightness), Magenta = 0.5 to 0.599 (0.574 max brightness), White =
            0.6 to 0.699 (0.6 to 0.674 brightness).
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 2,
        "params": 1,
        "param_defaults": {
            "in": 0,
        },
        "cpu": 0.04,
        "blocks": {
            "in": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_output": {"isDefault": False, "isParam": False, "position": 1, "type": "cv_out"},
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
            Audio Panner takes either one or two input channels and pans them
            between two outputs. Connect an LFO for a stereo tremolo effect.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 5,
        "params": 3,
        "param_defaults": {
            "pan": 0.5,
        },
        "cpu": 1,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "pan": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 3, "type": "audio_out"},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 4, "type": "audio_out"},
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
            Pitch Detector interprets the pitch of a connected audio signal as a CV
            note output, which can be sent to an oscillator or quantizer. You can
            affect the tracking by changing the connection strength between the
            audio source and the audio input, and transpose which note the
            oscillator will generate using the connection strength to the
            oscillator. Click knob to toggle display between frequency in Hz and
            note.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 2.3,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"},
        },
        "options": {},
    },
    59: {
        "name": "Pitch Shifter",
        "category": "Audio",
        "description": """
            Pitch Shifter transposes the pitch of incoming audio. Click the knob on
            the pitch shift parameter to cycle views of CV value, semitones, or
            cents. Connect an LFO to produce a vibrato effect, or connect whatever
            you'd like!
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "param_defaults": {
            "pitch_shift": 0.5,
        },
        "cpu": 15.1,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "pitch_shift": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_out"},
        },
        "options": {},
    },
    60: {
        "name": "Midi Note Out",
        "category": "Interface",
        "description": """
            Send MIDI notes out to external MIDI enabled gear through ZOIA's MIDI
            outputs.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 3,
        "params": 3,
        "param_defaults": {
            "note_in": 0,
            "gate_in": 0,
            "velocity_in": 0,
        },
        "cpu": 0.1,
        "blocks": {
            "note_in": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "gate_in": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "velocity_in": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
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
        "param_defaults": {
        },
        "cpu": 0.2,
        "blocks": {"cc": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"}},
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
        "param_defaults": {
            "pc": 0,
            "trigger_in": 0,
        },
        "cpu": 0.1,
        "blocks": {
            "pc": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "trigger_in": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
        },
        "options": {"midi_channel": list(range(1, 17))},
    },
    63: {
        "name": "Bit Modulator",
        "category": "Audio",
        "description": """
            Bit Modulator takes one audio input and compares it against the other,
            creating an unholy glitchy combination of both sounds at the output.
            Choose between 3 different logic flavours with the "type" option. When
            taking audio from an external source, it's recommended to put a gate
            before the input.
        """,
        "default_blocks": 3,
        "min_blocks": 3,
        "max_blocks": 3,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.8,
        "blocks": {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_2": {"isDefault": True, "isParam": False, "position": 1, "type": "audio_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_out"},
        },
        "options": {"type": ["xor", "and", "or"]},
    },
    64: {
        "name": "Audio Balance",
        "category": "Audio",
        "description": """
            Audio Balance mixes an output from 2 inputs. You can run this module
            either mono or stereo.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 7,
        "params": 1,
        "param_defaults": {
            "mix": 0.5,
        },
        "cpu": 0.8,
        "blocks": {
            "audio_in_1_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_1_R": {"isDefault": False, "isParam": False, "position": 4, "type": "audio_in"},
            "audio_in_2_L": {"isDefault": True, "isParam": False, "position": 1, "type": "audio_in"},
            "audio_in_2_R": {"isDefault": False, "isParam": False, "position": 5, "type": "audio_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "audio_output_L": {"isDefault": True, "isParam": False, "position": 3, "type": "audio_out"},
            "audio_output_R": {"isDefault": False, "isParam": False, "position": 6, "type": "audio_out"},
        },
        "options": {"stereo": ["mono", "stereo"]},
    },
    65: {
        "name": "Inverter",
        "category": "Audio",
        "description": """
            The Inverter module takes incoming audio signal and inverts the sound
            wave 180 degrees out of phase. This module is inaudible unless you have
            a phase related problem you are trying to solve, in which case it can be
            very audible. Be sure to put a 1 Buffer Delay module into your "dry"
            side to line up the Inverter in time for proper phase cancellation.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.2,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 1, "type": "audio_out"},
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
        "param_defaults": {
            "input_gain": 0.5,
            "output_gain": 0.75,
        },
        "cpu": 14.1,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "input_gain": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "output_gain": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 3, "type": "audio_out"},
        },
        "options": {"model": ["efuzzy", "burly", "scoopy", "ugly"]},
    },
    67: {
        "name": "Ghostverb",
        "category": "Effect",
        "description": """
            A spooky, ghostly reverb sound akin to the Ghost mode found in the
            Empress Reverb. Scare the crap out of all your friends!
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "param_defaults": {
            "decay_feedback": 0.5,
            "rate": 0.5,
            "resonance": 0.5,
            "mix": 0.5,
        },
        "cpu": 24.5,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "decay_feedback": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "rate": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "resonance": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7, "type": "audio_out"},
        },
        "options": {"channels": ["1in->1out", "1in->2out", "stereo"]},
    },
    68: {
        "name": "Cabinet Sim",
        "category": "Effect",
        "description": """
            A versatile guitar cabinet simulator
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 4,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 7,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 3, "type": "audio_out"},
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
            ZOIA's Flanger module is borrowed right from the Empress Nebulus. This
            quite versatile flanger encompasses lots of comb filtering territory,
            but don't hesitate to build flange tones yourself using LFOs and delay
            lines!
        """,
        "default_blocks": 7,
        "min_blocks": 7,
        "max_blocks": 9,
        "params": 5,
        "param_defaults": {
            "rate": 0.1,
            "tap_tempo_in": 0,
            "direct": 0,
            "regen": 0.6,
            "width": 0.5,
            "tone_tilt_eq": 0.5,
            "mix": 0.5,
        },
        "cpu": 7.35,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "rate": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "direct": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "regen": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "width": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "tone_tilt_eq": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 8, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 9, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 10, "type": "audio_out"},
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
            The classic chorus effect. A nice sounding, fairly standard chorus. Get
            wackier sounds from it by using CV direct, or build your own from LFOs
            and delay lines!
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "param_defaults": {
            "rate": 0.1,
            "direct": 0,
            "width": 0.5,
            "tone_tilt_eq": 0.5,
            "mix": 0.5,
        },
        "cpu": 8,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "rate": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "tap_tempo_in": {"isDefaut": False, "isParam": True, "position": 3, "type": "cv_in"},
            "direct": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "width": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "tone_tilt_eq": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 9, "type": "audio_out"},
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
            Vibrato is your typical pitch bending, wet only sound you'd find on such
            classic units as the Empress Nebulus, just to name one. Get bendy!
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 6,
        "params": 2,
        "param_defaults": {
            "rate": 0.5,
            "direct": 0,
            "width": 0.5,
        },
        "cpu": 4.1,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "rate": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "tap_tempo_in": {"isDefaut": False, "isParam": True, "position": 3, "type": "cv_in"},
            "direct": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "width": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7, "type": "audio_out"},
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
            Get your quack on! This fully featured envelope filter has everything
            you need to tune in that perfect envelope filter and get funky. Great on
            guitar, bass, or anything else!
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "param_defaults": {
            "sensitivity": 0.5,
            "min_freq": 0.2,
            "max_freq": 0.75,
            "filter_q": 0.33,
        },
        "cpu": 3.35,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "sensitivity": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "min_freq": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "max_freq": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "filter_q": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7, "type": "audio_out"},
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
            A gnarly ring modulation effect. A robot's nightmare, a tweaker's
            delight!
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 6,
        "params": 3,
        "param_defaults": {
            "frequency": 0,
            "duty_cycle": 0.5,
            "mix": 0.5,
        },
        "cpu": 5.3,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "frequency": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "ext_in": {"isDefault": False, "isParam": False, "position": 2, "type": "audio_in"},
            "duty_cycle": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 5, "type": "audio_out"},
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
        "param_defaults": {
            "decay_time": 0.5,
            "mix": 0.5,
            "low_eq": 0.5,
            "lpf_freq": 0.5,
        },
        "cpu": 17,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": True, "isParam": False, "position": 1, "type": "audio_in"},
            "decay_time": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "low_eq": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "lpf_freq": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 4, "type": "audio_out"},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 5, "type": "audio_out"},
        },
        "options": {},
    },
    75: {
        "name": "Ping Pong Delay",
        "category": "Effect",
        "description": """
            Ping Pong Delay is almost identical to the Delay w/ Mod except for one
            key aspect: the delay repeats ping pong from left to right across stereo
            outputs. When stereo inputs are selected, one input will ping while the
            other pongs, followed by a pong while the other pings into the opposite
            and then correct outputs.
        """,
        "default_blocks": 7,
        "min_blocks": 7,
        "max_blocks": 9,
        "params": 5,
        "param_defaults": {
            "delay_time": 0.5,
            "tap_tempo_in": 0,
            "feedback": 0.35,
            "mod_rate": 0.25,
            "mod_depth": 0.2,
            "mix": 0.2,
        },
        "cpu": 13.4,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "delay_time": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "feedback": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "mod_rate": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "mod_depth": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8, "type": "audio_out"},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 9, "type": "audio_out"},
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
            Audio Mixer functions like a stripped down mixing console, where gain is
            your channel fader and you can place an optional pan control. Mix up to
            8 channels, in mono or stereo.
        """,
        "default_blocks": 5,
        "min_blocks": 5,
        "max_blocks": 34,
        "params": 16,
        "param_defaults": {
            "gain_1": 0.83,
            "gain_2": 0.83,
            "gain_3": 0.83,
            "gain_4": 0.83,
            "gain_5": 0.83,
            "gain_6": 0.83,
            "gain_7": 0.83,
            "gain_8": 0.83,
            "pan_1": 0.5,
            "pan_2": 0.5,
            "pan_3": 0.5,
            "pan_4": 0.5,
            "pan_5": 0.5,
            "pan_6": 0.5,
            "pan_7": 0.5,
            "pan_8": 0.5,
        },
        "cpu": 11.5,
        "blocks": {
            "audio_in_1_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_1_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "audio_in_2_L": {"isDefault": True, "isParam": False, "position": 2, "type": "audio_in"},
            "audio_in_2_R": {"isDefault": False, "isParam": False, "position": 3, "type": "audio_in"},
            "audio_in_3_L": {"isDefault": False, "isParam": False, "position": 4, "type": "audio_in"},
            "audio_in_3_R": {"isDefault": False, "isParam": False, "position": 5, "type": "audio_in"},
            "audio_in_4_L": {"isDefault": False, "isParam": False, "position": 6, "type": "audio_in"},
            "audio_in_4_R": {"isDefault": False, "isParam": False, "position": 7, "type": "audio_in"},
            "audio_in_5_L": {"isDefault": False, "isParam": False, "position": 8, "type": "audio_in"},
            "audio_in_5_R": {"isDefault": False, "isParam": False, "position": 9, "type": "audio_in"},
            "audio_in_6_L": {"isDefault": False, "isParam": False, "position": 10, "type": "audio_in"},
            "audio_in_6_R": {"isDefault": False, "isParam": False, "position": 11, "type": "audio_in"},
            "audio_in_7_L": {"isDefault": False, "isParam": False, "position": 12, "type": "audio_in"},
            "audio_in_7_R": {"isDefault": False, "isParam": False, "position": 13, "type": "audio_in"},
            "audio_in_8_L": {"isDefault": False, "isParam": False, "position": 14, "type": "audio_in"},
            "audio_in_8_R": {"isDefault": False, "isParam": False, "position": 15, "type": "audio_in"},
            "gain_1": {"isDefault": True, "isParam": True, "position": 16, "type": "cv_in"},
            "gain_2": {"isDefault": True, "isParam": True, "position": 17, "type": "cv_in"},
            "gain_3": {"isDefault": False, "isParam": True, "position": 18, "type": "cv_in"},
            "gain_4": {"isDefault": False, "isParam": True, "position": 19, "type": "cv_in"},
            "gain_5": {"isDefault": False, "isParam": True, "position": 20, "type": "cv_in"},
            "gain_6": {"isDefault": False, "isParam": True, "position": 21, "type": "cv_in"},
            "gain_7": {"isDefault": False, "isParam": True, "position": 22, "type": "cv_in"},
            "gain_8": {"isDefault": False, "isParam": True, "position": 23, "type": "cv_in"},
            "pan_1": {"isDefault": False, "isParam": True, "position": 24, "type": "cv_in"},
            "pan_2": {"isDefault": False, "isParam": True, "position": 25, "type": "cv_in"},
            "pan_3": {"isDefault": False, "isParam": True, "position": 26, "type": "cv_in"},
            "pan_4": {"isDefault": False, "isParam": True, "position": 27, "type": "cv_in"},
            "pan_5": {"isDefault": False, "isParam": True, "position": 28, "type": "cv_in"},
            "pan_6": {"isDefault": False, "isParam": True, "position": 29, "type": "cv_in"},
            "pan_7": {"isDefault": False, "isParam": True, "position": 30, "type": "cv_in"},
            "pan_8": {"isDefault": False, "isParam": True, "position": 31, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 32, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 33, "type": "audio_out"},
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
            This is essentially a latching CV switch with an output of 0 or 1. When
            the input sees an upward CV change, the flip flop is triggered to change
            it's output state from 0 to 1 at the next upward change in CV, which
            must occur after a downward change in CV. So, the flip flop changes from
            0 to 1 at every other upward change in CV.
        """,
        "default_blocks": 2,
        "min_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "param_defaults": {
            "cv_input": 0,
        },
        "cpu": 0.2,
        "blocks": {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"},
        },
        "options": {},
    },
    78: {
        "name": "Diffuser",
        "category": "Audio",
        "description": """
            Diffuser spreads your signal across the galaxy like so many shimmering
            little stars. On it's own it sounds like a modulated slapback delay with
            no dry signal, but it can be used to construct many a tonal/atonal
            masterpiece.
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 6,
        "params": 4,
        "param_defaults": {
            "gain": 0,
            "size": 0.5,
            "mod_width": 0,
            "mod_rate": 0,
        },
        "cpu": 1.7,
        "blocks": {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "gain": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "size": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "mod_width": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "mod_rate": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "audio_out": {"isDefault": True, "isParam": False, "position": 5, "type": "audio_out"},
        },
        "options": {},
    },
    79: {
        "name": "Reverb Lite",
        "category": "Effect",
        "description": """
            A straightforward CPU friendly reverb sound to add some smoosh to
            heavier workload patches.
        """,
        "default_blocks": 4,
        "min_blocks": 4,
        "max_blocks": 6,
        "params": 2,
        "param_defaults": {
            "decay_time": 0.5,
            "mix": 0.5,
        },
        "cpu": 6.5,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "decay_time": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 4, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 5, "type": "audio_out"},
        },
        "options": {"channels": ["1in->1out", "1in->2out", "stereo"]},
    },
    80: {
        "name": "Room Reverb",
        "category": "Effect",
        "description": """
            Well, you're cooped up in your little room. But that's okay, because
            you've got some tasty room reverb to swim around in. Don't worry,
            somebody will come get you out someday.
        """,
        "default_blocks": 8,
        "min_blocks": 8,
        "max_blocks": 8,
        "params": 4,
        "param_defaults": {
            "decay_time": 0.16,
            "low_eq": 0.5,
            "lpf_freq": 0.5,
            "mix": 0.5,
        },
        "cpu": 17,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": True, "isParam": False, "position": 1, "type": "audio_in"},
            "decay_time": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "low_eq": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "lpf_freq": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6, "type": "audio_out"},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 7, "type": "audio_out"},
        },
        "options": {},
    },
    81: {
        "name": "Pixel",
        "category": "Interface",
        "description": """
            Puts a coloured block on the grid. The brightness can be controlled by a
            cv signal or an audio signal. Pixel is a simple, elegant way to create a
            more visually interactive user interface for your patch.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "param_defaults": {
            "cv_in": 0,
        },
        "cpu": 0.01,
        "blocks": {
            "cv_in": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "audio_in": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
        },
        "options": {"control": ["cv", "audio"]},
    },
    82: {
        "name": "Midi Clock In",
        "category": "Interface",
        "description": """
            Connect incoming MIDI clock to sync your patches to the outside world.
            Connects directly to ZOIA's MIDI input.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 4,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {
            "quarter_out": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"},
            "clock_out": {"isDefault": False, "isParam": False, "position": 1, "type": "cv_out"},
            "reset_out": {"isDefault": False, "isParam": False, "position": 2, "type": "cv_out"},
            "run_out": {"isDefault": False, "isParam": False, "position": 3, "type": "cv_out"},
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
            Granular breaks up incoming audio into tiny little grains and spits them
            back out in the quantity and shape of your choosing. Go from modest
            textures to completely unrecognizable oscillations. Granular can also be
            used as a granular delay by creating a feedback path from the output
            back to the input...
        """,
        "default_blocks": 8,
        "min_blocks": 8,
        "max_blocks": 10,
        "params": 6,
        "param_defaults": {
            "grain_size": 0.5,
            "grain_position": 0.1,
            "density": 1,
            "texture": 0.5,
            "speed_pitch": 0.5,
            "freeze": 0,
        },
        "cpu": 17,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "grain_size": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "grain_position": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "density": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "texture": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "speed_pitch": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "freeze": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 9, "type": "audio_out"},
        },
        "options": {
            "num_grains": list(range(1, 9)),
            "channels": ["mono", "stereo"],
            "pos_control": ["cv", "tap_tempo"],
            "size_control": ["cv", "tap_tempo"],
            "max_grain_size": ["1s", "4s", "16s"],
        },
    },
    84: {
        "name": "Midi Clock Out",
        "category": "Interface",
        "description": """
            Generate MIDI clock to sync outside devices to your ZOIA. Clock sends
            directly to ZOIA's MIDI output.
        """,
        "default_blocks": 3,
        "min_blocks": 1,
        "max_blocks": 5,
        "params": 5,
        "param_defaults": {
            "tap_cv_control": 0,
            "sent": 0,
            "reset": 0,
            "send_position": 0,
            "song_position": 0,
        },
        "cpu": 0.3,
        "blocks": {
            "tap_cv_control": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "sent": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "reset": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "send_position": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "song_position": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
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
        "param_defaults": {
            "min_time": 0,
            "max_time": 1,
        },
        "cpu": 0.12,
        "blocks": {
            "tap_input": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_in"},
            "min_time": {"isDefault": False, "isParam": True, "position": 1, "type": "cv_in"},
            "max_time": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "output": {"isDefault": True, "isParam": False, "position": 3, "type": "cv_out"},
        },
        "options": {"range": ["off", "on"], "output": ["linear", "exponential"]},
    },
    86: {
        "name": "Midi Pitch Bend",
        "category": "Interface",
        "description": """
            Collects MIDI data from pitch bend wheel on keyboards, can be applied to
            oscillator frequency in parallel with MIDI note data, or used in other
            ways.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"pitch_bend": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"}},
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
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cv_in": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"}},
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
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cv_out": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"}},
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
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cv_out": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"}},
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
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cv_out": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"}},
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
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cv_out": {"isDefault": True, "isParam": False, "position": 0, "type": "cv_out"}},
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
        "param_defaults": {
            "level": 0.83,
        },
        "cpu": 0.4,
        "blocks": {
            "level": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
        },
        "options": {},
    },
    93: {
        "name": "Euro Audio Input 1",
        "category": "Interface",
        "description": """
            Connect audio from the outside world into the grid.
            This could be a guitar, bass, synth module, computer audio, etc.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.4,
        "blocks": {
            "output": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_out"},
        },
        "options": {"input_pad": ["6dB", "12dB", "no_pad"]},
    },
    94: {
        "name": "Euro Audio Input 2",
        "category": "Interface",
        "description": """
            Connect audio from the outside world into the grid.
            This could be a guitar, bass, synth module, computer audio, etc.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "param_defaults": {
        },
        "cpu": 0.4,
        "blocks": {
            "output": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_out"},
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
        "param_defaults": {
        },
        "cpu": 0.4,
        "blocks": {
            "input": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
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
        "param_defaults": {
        },
        "cpu": 0.4,
        "blocks": {
            "input": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
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
        "param_defaults": {
        },
        "cpu": 0.02,
        "blocks": {"cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"}},
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
        "param_defaults": {
        },
        "cpu": 0.02,
        "blocks": {"cv_output": {"isDefault": True, "isParam": False, "position": 1, "type": "cv_out"}},
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
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cv_in": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"}},
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
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cv_in": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"}},
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
        "param_defaults": {
        },
        "cpu": 0.1,
        "blocks": {"cv_in": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"}},
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
            Lets you play and record WAV files from an SD card.
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 12,
        "params": 6,
        "param_defaults": {
            "record": 0,
            "sample_playback": 0,
            "speed_pitch": 0.5,
            "direction": 0,
            "start": 0,
            "length": 1,
        },
        "cpu": 0.9,
        "blocks": {
            "audio_in_L": {"isDefault": False, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "record": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "sample_playback": {"isDefault": True, "isParam": True, "position": 3, "type": "cv_in"},
            "speed_pitch": {"isDefault": True, "isParam": True, "position": 4, "type": "cv_in"},
            "direction": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "start": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "length": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "position_cv_out": {"isDefault": False, "isParam": False, "position": 8, "type": "cv_out"},
            "loop_end_cv_out": {"isDefault": False, "isParam": False, "position": 9, "type": "cv_out"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 10, "type": "audio_out"},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 11, "type": "audio_out"},
        },
        "options": {
            "record": ["disabled", "new sample", "overdub", "punch-in"],
            "playback": ["trigger", "gate", "loop"],
            "reverse_button": ["off", "on"],
            "cv_outputs": ["off", "on"],
        },
    },
    103: {
        "name": "Device Control",
        "category": "Interface",
        "description": """
            Control the bypass state, performance mode, or stomp aux mode using CV.
            A rising or falling CV value will toggle the selected control.
        """,
        "default_blocks": 1,
        "min_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "param_defaults": {
            "bypass": 0,
            "aux": 0,
            "performance": 0,
        },
        "cpu": 0.1,
        "blocks": {
            "bypass": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "aux": {"isDefault": False, "isParam": True, "position": 1, "type": "cv_in"},
            "performance": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
        },
        "options": {
            "control": ["bypass", "stomp aux", "perform"],
        },
    },
    104: {
        "name": "CV Mixer",
        "category": "CV",
        "description": """
            It's like the audio mixer but for CV
            signals, with a few extra features! The atten parameter for each channel
            controls the amount and polarity of the signal that is passed through to the
            output: 1.0 passes the full signal, 0.5 fully attenuates it, and 0.0 fully
            inverts it. The 'mode' option lets you select how these signals are summed
            at the output. Summing mode simply adds up all of the signals, clipping
            anything outside the +1/-1 CV range. Average mode divides each signal by
            the number of inputs before summing them at the output. This ensures that
            the output doesn't get clipped. Try mixing multiple LFOs to create a wild
            new waveform, or blend a few sequencers to create a unique melody!
        """,
        "default_blocks": 5,
        "min_blocks": 5,
        "max_blocks": 17,
        "params": 16,
        "param_defaults": {
            "cv_in_1": 0,
            "cv_in_2": 0,
            "cv_in_3": 0,
            "cv_in_4": 0,
            "cv_in_5": 0,
            "cv_in_6": 0,
            "cv_in_7": 0,
            "cv_in_8": 0,
            "atten_1": 0.5,
            "atten_2": 0.5,
            "atten_3": 0.5,
            "atten_4": 0.5,
            "atten_5": 0.5,
            "atten_6": 0.5,
            "atten_7": 0.5,
            "atten_8": 0.5,
        },
        "cpu": 0.3,
        "blocks": {
            "cv_in_1": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "cv_in_2": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "cv_in_3": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "cv_in_4": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "cv_in_5": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "cv_in_6": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "cv_in_7": {"isDefault": False, "isParam": True, "position": 6, "type": "cv_in"},
            "cv_in_8": {"isDefault": False, "isParam": True, "position": 7, "type": "cv_in"},
            "atten_1": {"isDefault": True, "isParam": True, "position": 8, "type": "cv_in"},
            "atten_2": {"isDefault": True, "isParam": True, "position": 9, "type": "cv_in"},
            "atten_3": {"isDefault": False, "isParam": True, "position": 10, "type": "cv_in"},
            "atten_4": {"isDefault": False, "isParam": True, "position": 11, "type": "cv_in"},
            "atten_5": {"isDefault": False, "isParam": True, "position": 12, "type": "cv_in"},
            "atten_6": {"isDefault": False, "isParam": True, "position": 13, "type": "cv_in"},
            "atten_7": {"isDefault": False, "isParam": True, "position": 14, "type": "cv_in"},
            "atten_8": {"isDefault": False, "isParam": True, "position": 15, "type": "cv_in"},
            "cv_output": {"isDefault": True, "isParam": False, "position": 16, "type": "cv_out"},
        },
        "options": {
            "num_channels": list(range(1, 9)),
            "levels": ["summing", "average"],
        },
    },
    105: {
        "name": "Logic Gate",
        "category": "CV",
        "description": """
            Perform logical operations with CV inputs.
            Operations include AND, OR, NOT, NOR, NAND, XOR, XNOR.
        """,
        "default_blocks": 3,
        "min_blocks": 2,
        "max_blocks": 40,
        "params": 39,
        "param_defaults": {
            "in_1": 0,
            "in_2": 0,
            "in_3": 0,
            "in_4": 0,
            "in_5": 0,
            "in_6": 0,
            "in_7": 0,
            "in_8": 0,
            "in_9": 0,
            "in_10": 0,
            "in_11": 0,
            "in_12": 0,
            "in_13": 0,
            "in_14": 0,
            "in_15": 0,
            "in_16": 0,
            "in_17": 0,
            "in_18": 0,
            "in_19": 0,
            "in_20": 0,
            "in_21": 0,
            "in_22": 0,
            "in_23": 0,
            "in_24": 0,
            "in_25": 0,
            "in_26": 0,
            "in_27": 0,
            "in_28": 0,
            "in_29": 0,
            "in_30": 0,
            "in_31": 0,
            "in_32": 0,
            "in_33": 0,
            "in_34": 0,
            "in_35": 0,
            "in_36": 0,
            "in_37": 0,
            "in_38": 0,
            "threshold": 0,
        },
        "cpu": 0.1,
        "blocks": {
            "in_1": {"isDefault": True, "isParam": True, "position": 0, "type": "cv_in"},
            "in_2": {"isDefault": True, "isParam": True, "position": 1, "type": "cv_in"},
            "in_3": {"isDefault": False, "isParam": True, "position": 2, "type": "cv_in"},
            "in_4": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "in_5": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "in_6": {"isDefault": False, "isParam": True, "position": 5, "type": "cv_in"},
            "in_7": {"isDefault": False, "isParam": True, "position": 6, "type": "cv_in"},
            "in_8": {"isDefault": False, "isParam": True, "position": 7, "type": "cv_in"},
            "in_9": {"isDefault": False, "isParam": True, "position": 8, "type": "cv_in"},
            "in_10": {"isDefault": False, "isParam": True, "position": 9, "type": "cv_in"},
            "in_11": {"isDefault": False, "isParam": True, "position": 10, "type": "cv_in"},
            "in_12": {"isDefault": False, "isParam": True, "position": 11, "type": "cv_in"},
            "in_13": {"isDefault": False, "isParam": True, "position": 12, "type": "cv_in"},
            "in_14": {"isDefault": False, "isParam": True, "position": 13, "type": "cv_in"},
            "in_15": {"isDefault": False, "isParam": True, "position": 14, "type": "cv_in"},
            "in_16": {"isDefault": False, "isParam": True, "position": 15, "type": "cv_in"},
            "in_17": {"isDefault": False, "isParam": True, "position": 16, "type": "cv_in"},
            "in_18": {"isDefault": False, "isParam": True, "position": 17, "type": "cv_in"},
            "in_19": {"isDefault": False, "isParam": True, "position": 18, "type": "cv_in"},
            "in_20": {"isDefault": False, "isParam": True, "position": 19, "type": "cv_in"},
            "in_21": {"isDefault": False, "isParam": True, "position": 20, "type": "cv_in"},
            "in_22": {"isDefault": False, "isParam": True, "position": 21, "type": "cv_in"},
            "in_23": {"isDefault": False, "isParam": True, "position": 22, "type": "cv_in"},
            "in_24": {"isDefault": False, "isParam": True, "position": 23, "type": "cv_in"},
            "in_25": {"isDefault": False, "isParam": True, "position": 24, "type": "cv_in"},
            "in_26": {"isDefault": False, "isParam": True, "position": 25, "type": "cv_in"},
            "in_27": {"isDefault": False, "isParam": True, "position": 26, "type": "cv_in"},
            "in_28": {"isDefault": False, "isParam": True, "position": 27, "type": "cv_in"},
            "in_29": {"isDefault": False, "isParam": True, "position": 28, "type": "cv_in"},
            "in_30": {"isDefault": False, "isParam": True, "position": 29, "type": "cv_in"},
            "in_31": {"isDefault": False, "isParam": True, "position": 30, "type": "cv_in"},
            "in_32": {"isDefault": False, "isParam": True, "position": 31, "type": "cv_in"},
            "in_33": {"isDefault": False, "isParam": True, "position": 32, "type": "cv_in"},
            "in_34": {"isDefault": False, "isParam": True, "position": 33, "type": "cv_in"},
            "in_35": {"isDefault": False, "isParam": True, "position": 34, "type": "cv_in"},
            "in_36": {"isDefault": False, "isParam": True, "position": 35, "type": "cv_in"},
            "in_37": {"isDefault": False, "isParam": True, "position": 36, "type": "cv_in"},
            "in_38": {"isDefault": False, "isParam": True, "position": 37, "type": "cv_in"},
            "threshold": {"isDefault": False, "isParam": True, "position": 38, "type": "cv_in"},
            "cv_out": {"isDefault": True, "isParam": False, "position": 39, "type": "cv_out"},
        },
        "options": {
            "operation": ["AND", "OR", "NOR", "NAND", "XOR", "XNOR", "NOT"],
            "num_of_inputs": list(range(2, 39)),
            "threshold": ["off", "on"]
        },
    },
    106: {
        "name": "Reverse Delay",
        "category": "Effect",
        "description": """
            This effect reverses your repeats while giving you control over their pitch.
            Choose from unity pitch, fine detuning (a few cents up or down),
            or intervals such as a 4th, 5th, or octave above or below unity.
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 9,
        "params": 5,
        "param_defaults": {
            "delay_time": 0.5,
            "tap_tempo_in": 0,
            "tap_ratio": 0,
            "feedback": 0.35,
            "pitch": 0.5,
            "mix": 0.2,
        },
        "cpu": 0.1,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "delay_time": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "tap_ratio": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "feedback": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "pitch": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 9, "type": "audio_out"},
        },
        "options": {
            "channels": ["mono", "stereo"],
            "control": ["rate", "tap_tempo"],
        }
    },
    107: {
        "name": "Univibe",
        "category": "Effect",
        "description": """
            A multi-dimensional effect that combines vibrato and phase shifting to create lush,
            swooshing sounds.
        """,
        "default_blocks": 6,
        "min_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "param_defaults": {
            "rate": 0.5,
            "tap_tempo_in": 0,
            "direct": 0,
            "depth": 0.5,
            "resonance": 0.33,
            "mix": 0.5,
        },
        "cpu": 0.1,
        "blocks": {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0, "type": "audio_in"},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1, "type": "audio_in"},
            "rate": {"isDefault": True, "isParam": True, "position": 2, "type": "cv_in"},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3, "type": "cv_in"},
            "direct": {"isDefault": False, "isParam": True, "position": 4, "type": "cv_in"},
            "depth": {"isDefault": True, "isParam": True, "position": 5, "type": "cv_in"},
            "resonance": {"isDefault": True, "isParam": True, "position": 6, "type": "cv_in"},
            "mix": {"isDefault": True, "isParam": True, "position": 7, "type": "cv_in"},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 8, "type": "audio_out"},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 9, "type": "audio_out"},
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
        }
    },
}

for k, v in list(module_index.items()):
    module_index[str(k)] = module_index.pop(k)

with open("zoia_lib/common/schemas/ModuleIndex.json", "w") as f:
    json.dump(module_index, f)

# import json2table
# with open("documentation/resources/mod.html", "w") as f:
#     filtered_module_index = {}
#     display_fields = [
#         "name",
#         "category",
#         "description",
#         "cpu",
#         "param_defaults",
#         "options",
#     ]
#     for module_id, module_data in module_index.items():
#         filtered_module_index[module_id] = {
#             field: module_data.get(field) for field in display_fields
#         }
#     f.write(json2table.convert(
#         filtered_module_index,
#         build_direction="LEFT_TO_RIGHT",
#         table_attributes={"style": "Width:100%"}
#         )
#     )
