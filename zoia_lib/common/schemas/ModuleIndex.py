# format:
# {
#   module type: {
#     name, # default module name
#     category, # module category
#     max blocks, # total blocks a module can use
#     params, # number of adjustable CV jacks
#     cpu # average amount of CPU (this doesn't factor in matrix DSP, just purely the module itself)
#     blocks, # default and optional blocks the module uses on the grid
#     options, # module options, list of each
#   }
# }

import json
module_index = {
    0: {
        "name": "SV Filter",
        "category": "audio",
        "default_blocks": 4,
        "max_blocks": 6,
        "params": 2,
        "cpu": 3,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "frequency": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "resonance": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "lowpass_output": {
                "isDefault": True,
                "isParam": False,
                "position": 3
            },
            "hipass_output": {
                "isDefault": False,
                "isParam": False,
                "position": 4
            },
            "bandpass_output": {
                "isDefault": False,
                "isParam": False,
                "position": 5
            }
        },
        "options": {
            "lowpass_output": ["on", "off"],
            "hipass_output": ["off", "on"],
            "bandpass_output": ["off", "on"]
        }
    },
    1: {
        "name": "Audio Input",
        "category": "interface",
        "default_blocks": 2,
        "max_blocks": 2,
        "params": 0,
        "cpu": 0.4,
        "blocks": {
            "input_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "input_R": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            }
        },
        "options": {
            "channels": ["stereo", "left", "right"]
        }
    },
    2: {
        "name": "Audio Output",
        "category": "interface",
        "default_blocks": 2,
        "max_blocks": 3,
        "params": 1,
        "cpu": 1.7,
        "blocks": {
            "input_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "input_R": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            },
            "gain": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            }
        },
        "options": {
            "gain_control": ["off", "on"],
            "channels": ["stereo", "left", "right"]
        }
    },
    3: {
        "name": "Aliaser",
        "category": "audio",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "cpu": 0.7,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "#_of_samples": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {}
    },
    4: {
        "name": "Sequencer",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 42,
        "params": 34,
        "cpu": 2,
        "blocks": {
            "step_1": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "step_n": {
                "isDefault": False,
                "isParam": True,
                "position": list(range(1, 32))
            },
            "gate_in": {
                "isDefault": True,
                "isParam": True,
                "position": 32
            },
            "queue_start": {
                "isDefault": False,
                "isParam": True,
                "position": 33
            },
            "out_track_1": {
                "isDefault": True,
                "isParam": False,
                "position": 34,
            },
            "out_track_n": {
                "isDefault": False,
                "isParam": False,
                "position": list(range(35, 42))
            }
        },
        "options": {
            "number_of_steps": list(range(1, 33)),
            "num_of_tracks": list(range(1, 9)),
            "restart_jack": ["off", "on"],
            "behavior": ["loop", "once"]
        }
    },
    5: {
        "name": "LFO",
        "category": "cv",
        "default_blocks": 2,
        "max_blocks": 5,
        "params": 4,
        "cpu": 0.3,
        "blocks": {
            "frequency": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "swing_amount": {
                "isDefault": False,
                "isParam": True,
                "position": 1
            },
            "phase_input": {
                "isDefault": False,
                "isParam": False,
                "position": 2
            },
            "phase_reset": {
                "isDefault": False,
                "isParam": True,
                "position": 3
            },
            "output": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            }
        },
        "options": {
            "waveform": ["square", "sine", "triangle",
                         "sawtooth", "ramp", "random"],
            "swing_control": ["off", "on"],
            "output": ["0 to 1", "-1 to 1"],
            "input": ["cv", "tap", "linear_cv"],
            "phase_input": ["off", "on"],
            "phase_reset": ["off", "on"]
        }
    },
    6: {
        "name": "ADSR",
        "category": "cv",
        "default_blocks": 6,
        "max_blocks": 10,
        "params": 9,
        "cpu": 0.07,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "retrigger": {
                "isDefault": False,
                "isParam": True,
                "position": 1
            },
            "delay": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            },
            "attack": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "hold_attack_decay": {
                "isDefault": False,
                "isParam": True,
                "position": 4
            },
            "decay": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "sustain": {
                "isDefault": True,
                "isParam": True,
                "position": 6
            },
            "hold_sustain_release": {
                "isDefault": False,
                "isParam": True,
                "position": 7
            },
            "release": {
                "isDefault": True,
                "isParam": True,
                "position": 8
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 9
            }
        },
        "options": {
            "retrigger_input": ["off", "on"],
            "initial_delay": ["off", "on"],
            "hold_attack_decay": ["off", "on"],
            "str": ["on", "off"],
            "immediate_release": ["on", "off"],
            "hold_sustain_release": ["off", "on"],
            "time_scale": ["exponent", "linear"]
        }
    },
    7: {
        "name": "VCA",
        "category": "audio",
        "default_blocks": 3,
        "max_blocks": 5,
        "params": 1,
        "cpu": 0.7,
        "blocks": {
            "audio_in_1": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_2": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "level_control": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "audio_out_1": {
                "isDefault": True,
                "isParam": False,
                "position": 3
            },
            "audio_out_2": {
                "isDefault": False,
                "isParam": False,
                "position": 4
            }
        },
        "options": {
            "channels": ["1in->1out", "stereo"]
        }
    },
    8: {
        "name": "Audio Multiply",
        "category": "audio",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 0,
        "cpu": 0.4,
        "blocks": {
            "audio_in_1": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_2": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {}
    },
    9: {
        "name": "Bit Crusher",
        "category": "audio",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "cpu": 1,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "crushed_bits": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {
            "fractions": ["off", "on"]
        }
    },
    10: {
        "name": "Sample & Hold",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "cpu": 0.1,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "trigger": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {}
    },
    11: {
        "name": "OD and Distortion",
        "category": "effect",
        "default_blocks": 4,
        "max_blocks": 4,
        "params": 2,
        "cpu": 17,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "input_gain": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "output_gain": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 3
            }
        },
        "options": {
            "model": ["plexi", "germ", "classic", "pushed"]
        }
    },
    12: {
        "name": "Env Follower",
        "category": "analysis",
        "default_blocks": 2,
        "max_blocks": 4,
        "params": 2,
        "cpu": 5,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "rise_time": {
                "isDefault": False,
                "isParam": True,
                "position": 1
            },
            "fall_time": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 3
            }
        },
        "options": {
            "rise_fall_time": ["off", "on"],
            "output_scale": ["log", "linear"]
        }
    },
    13: {
        "name": "Delay Line",
        "category": "audio",
        "default_blocks": 3,
        "max_blocks": 5,
        "params": 3,
        "cpu": 3,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "delay_time": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "modulation_in": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            },
            "tap_tempo_in": {
                "isDefault": False,
                "isParam": True,
                "position": 3
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            }
        },
        "options": {
            "max_time": ["1s", "2s", "4s", "8s", "16s", "100ms"],
            "tap_tempo_in": ["no", "yes"]
        }
    },
    14: {
        "name": "Oscillator",
        "category": "audio",
        "default_blocks": 2,
        "max_blocks": 4,
        "params": 2,
        "cpu": 10,
        "blocks": {
            "frequency": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "fm_input": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "duty_cycle": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 3
            }
        },
        "options": {
            "waveform": ["sine", "square", "triangle", "sawtooth"],
            "fm_in": ["off", "on"],
            "duty_cycle": ["off", "on"],
            "upsampling": ["none", "2x"]
        }
    },
    15: {
        "name": "Pushbutton",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.02,
        "blocks": {
            "switch": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            }
        },
        "options": {
            "action": ["momentary", "latching"],
            "normally": ["zero", "one"]
        }
    },
    16: {
        "name": "Keyboard",
        "category": "interface",
        "default_blocks": 4,
        "max_blocks": 43,
        "params": 49,
        "cpu": 0.1,
        "blocks": {
            "note_1": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "note_n": {
                "isDefault": False,
                "isParam": True,
                "position": list(range(1, 40))
            },
            "note_out": {
                "isDefault": True,
                "isParam": False,
                "position": 41
            },
            "gate_out": {
                "isDefault": True,
                "isParam": False,
                "position": 42
            },
            "trigger_out": {
                "isDefault": True,
                "isParam": False,
                "position": 43
            }
        },
        "options": {
            "#_of_notes": list(range(1, 41))
        }
    },
    17: {
        "name": "CV Filter",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "cpu": 0.02,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "time_constant": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {}
    },
    18: {
        "name": "Steps",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "cpu": 0.7,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "quant_steps": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {}
    },
    19: {
        "name": "Slew Limiter",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 4,
        "params": 2,
        "cpu": 0.2,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "slew_rate": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "rising_lag": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            },
            "falling_lag": {
                "isDefault": False,
                "isParam": True,
                "position": 3
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            }
        },
        "options": {
            "control": ["linked", "separate"],
        }
    },
    20: {
        "name": "Midi Notes In",
        "category": "interface",
        "default_blocks": 2,
        "max_blocks": 32,
        "params": 0,
        "cpu": 0.3,
        "blocks": {
            "note_out_1": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "gate_out_1": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            },
            "velocity_out_1": {
                "isDefault": False,
                "isParam": False,
                "position": 2
            },
            "trigger_out_1": {
                "isDefault": False,
                "isParam": False,
                "position": 3
            },
            "note_out_n": {
                "isDefault": False,
                "isParam": False,
                "position": [4, 8, 12, 16, 20, 24, 28]
            },
            "gate_out_n": {
                "isDefault": False,
                "isParam": False,
                "position": [5, 9, 13, 17, 21, 25, 29]
            },
            "velocity_out_n": {
                "isDefault": False,
                "isParam": False,
                "position": [6, 10, 14, 18, 22, 26, 30]
            },
            "trigger_out_n": {
                "isDefault": False,
                "isParam": False,
                "position": [7, 11, 15, 19, 23, 27, 31]
            },
        },
        "options": {
            "midi_channel": list(range(1, 17)),
            "#_of_outputs": list(range(1, 9)),
            "priority": ["newest", "oldest", "highest", "lowest", "RoundRobin"],
            "greedy": ["no", "yes"],
            "velocity_output": ["off", "on"],
            "low_note": list(range(0, 128)),
            "high_note": list(range(0, 128))[::-1],
            "trigger_pulse": ["off", "on"]
        }
    },
    21: {
        "name": "Midi CC In",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {
            "cc_value": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            }
        },
        "options": {
            "midi_channel": list(range(1, 17)),
            "controller": list(range(0, 128)),
            "output_range": ["0 to 1", "-1 to 1"]
        }
    },
    22: {
        "name": "Multiplier",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 10,
        "params": 2,
        "cpu": 0.2,
        "blocks": {
            "cv_input_1": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "cv_input_2": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "cv_input_n": {
                "isDefault": False,
                "isParam": True,
                "position": list(range(2, 9))
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 9
            }
        },
        "options": {
            "num_inputs": list(range(2, 9))
        }
    },
    23: {
        "name": "Compressor",
        "category": "effect",
        "default_blocks": 3,
        "max_blocks": 9,
        "params": 4,
        "cpu": 3,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "threshold": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "attack": {
                "isDefault": False,
                "isParam": True,
                "position": 3
            },
            "release": {
                "isDefault": False,
                "isParam": True,
                "position": 4
            },
            "ratio": {
                "isDefault": False,
                "isParam": True,
                "position": 5
            },
            "sidechain_in": {
                "isDefault": False,
                "isParam": False,
                "position": 6
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 7
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 8
            }
        },
        "options": {
            "attack_ctrl": ["off", "on"],
            "release_ctrl": ["off", "on"],
            "ratio_ctrl": ["off", "on"],
            "channels": ["1in->1out", "stereo"],
            "sidechain": ["internal", "external"]
        }
    },
    24: {
        "name": "Multi Filter",
        "category": "audio",
        "default_blocks": 4,
        "max_blocks": 5,
        "params": 3,
        "cpu": 0.8,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "gain": {
                "isDefault": False,
                "isParam": True,
                "position": 1
            },
            "frequency": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "q": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            }
        },
        "options": {
            "filter_shape": ["lowpass", "highpass", "bandpass",
                             "bell", "hi_shelf", "low_shelf"],
        }
    },
    25: {
        "name": "Plate Reverb",
        "category": "effect",
        "default_blocks": 8,
        "max_blocks": 8,
        "params": 4,
        "cpu": 22,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            },
            "decay_time": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "low_eq": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "high_eq": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 6
            },
            "audio_out_R": {
                "isDefault": True,
                "isParam": False,
                "position": 7
            }
        },
        "options": {}
    },
    26: {
        "name": "Buffer Delay",
        "category": "audio",
        "default_blocks": 2,
        "max_blocks": 2,
        "params": 0,
        "cpu": 0.2,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            }
        },
        "options": {
            "buffer_length": list(range(0, 17))
        }
    },
    27: {
        "name": "All Pass Filter",
        "category": "audio",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "cpu": 5,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "filter_gain": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {
            "#_of_poles": list(range(1, 9))
        }
    },
    28: {
        "name": "Quantizer",
        "category": "cv",
        "default_blocks": 2,
        "max_blocks": 4,
        "params": 3,
        "cpu": 1,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "key": {
                "isDefault": False,
                "isParam": True,
                "position": 1
            },
            "scale": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 3
            }
        },
        "options": {
            "key_scale_jacks": ["no", "yes"]
        }
    },
    29: {
        "name": "Phaser",
        "category": "effect",
        "default_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "cpu": 15,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "control_in": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "resonance": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "width": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 6
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 7
            }
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "2in->2out"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "number_of_stages": [4, 2, 1, 3, 6, 8]
        }
    },
    30: {
        "name": "Looper",
        "category": "audio",
        "default_blocks": 5,
        "max_blocks": 9,
        "params": 6,
        "cpu": 3,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "record": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "restart_playback": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            },
            "stop_play": {
                "isDefault": False,
                "isParam": True,
                "position": 3
            },
            "speed_pitch": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "start_position": {
                "isDefault": False,
                "isParam": True,
                "position": 5
            },
            "loop_length": {
                "isDefault": False,
                "isParam": False,
                "position": 6
            },
            "reverse_playback": {
                "isDefault": False,
                "isParam": True,
                "position": 7
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 8
            }
        },
        "options": {
            "max_rec_time": ["1s", "2s", "4s", "8s", "16s", "32s"],
            "length_edit": ["off", "on"],
            "playback": ["once", "loop"],
            "length": ["fixed", "pre_speed"],
            "hear_while_rec": ["no", "yes"],
            "play_reverse": ["no", "yes"],
            "overdub": ["no", "yes"],
            "stop_play_button": ["no", "yes"]
        }
    },
    31: {
        "name": "In Switch",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 18,
        "params": 17,
        "cpu": 0.2,
        "blocks": {
            "cv_input_1": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "cv_input_n": {
                "isDefault": False,
                "isParam": True,
                "position": list(range(1, 16))
            },
            "in_select": {
                "isDefault": True,
                "isParam": True,
                "position": 16
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 17
            }
        },
        "options": {
            "num_inputs": list(range(1, 17))
        }
    },
    32: {
        "name": "Out Switch",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 18,
        "params": 2,
        "cpu": 0.2,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "out_select": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "cv_output_1": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            },
            "cv_output_n": {
                "isDefault": False,
                "isParam": False,
                "position": list(range(3, 18))
            }
        },
        "options": {
            "num_outputs": list(range(1, 17))
        }
    },
    33: {
        "name": "Audio In Switch",
        "category": "audio",
        "default_blocks": 3,
        "max_blocks": 18,
        "params": 1,
        "cpu": 0.8,
        "blocks": {
            "audio_input_1": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_input_n": {
                "isDefault": False,
                "isParam": False,
                "position": list(range(1, 16))
            },
            "in_select": {
                "isDefault": True,
                "isParam": True,
                "position": 16
            },
            "audio_output": {
                "isDefault": True,
                "isParam": False,
                "position": 17
            }
        },
        "options": {
            "num_inputs": list(range(1, 17)),
            "fades": ["on", "off"]
        }
    },
    34: {
        "name": "Audio Out Switch",
        "category": "audio",
        "default_blocks": 3,
        "max_blocks": 18,
        "params": 1,
        "cpu": 0.7,
        "blocks": {
            "audio_input": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "in_select": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "audio_output_1": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            },
            "audio_output_n": {
                "isDefault": True,
                "isParam": False,
                "position": list(range(3, 18))
            }
        },
        "options": {
            "num_outputs": list(range(1, 17)),
            "fades": ["on", "off"]
        }
    },
    35: {
        "name": "Midi Pressure",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.03,
        "blocks": {
            "channel_pressure": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            }
        },
        "options": {
            "midi_channel": list(range(1, 17))
        }
    },
    36: {
        "name": "Onset Detector",
        "category": "analysis",
        "default_blocks": 2,
        "max_blocks": 3,
        "params": 1,
        "cpu": 0.7,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "sensitivity": {
                "isDefault": False,
                "isParam": True,
                "position": 1
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {
            "sensitivity": ["off", "on"]
        }
    },
    37: {
        "name": "Rhythm",
        "category": "cv",
        "default_blocks": 4,
        "max_blocks": 5,
        "params": 3,
        "cpu": 0.5,
        "blocks": {
            "rec_start_stop": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "rhythm_in": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "play": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "play_done": {
                "isDefault": False,
                "isParam": False,
                "position": 3
            },
            "rhythm_out": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            }
        },
        "options": {
            "done_ctrl": ["off", "on"],
        }
    },
    38: {
        "name": "Noise",
        "category": "audio",
        "default_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.4,
        "blocks": {
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            }
        },
        "options": {}
    },
    39: {
        "name": "Random",
        "category": "cv",
        "default_blocks": 1,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.1,
        "blocks": {
            "trigger_in": {
                "isDefault": False,
                "isParam": True,
                "position": 0
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            }
        },
        "options": {
            "output": ["0 to 1", "-1 to 1"],
            "new_val_on_trig": ["off", "on"]
        }
    },
    40: {
        "name": "Gate",
        "category": "effect",
        "default_blocks": 5,
        "max_blocks": 8,
        "params": 3,
        "cpu": 3,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "threshold": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "attack": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "release": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "sidechain_in": {
                "isDefault": False,
                "isParam": False,
                "position": 5
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 6
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 7
            }
        },
        "options": {
            "attack_ctrl": ["off", "on"],
            "release_ctrl": ["off", "on"],
            "channels": ["1in->1out", "1in->2out", "2in->2out"],
            "sidechain": ["internal", "external"]
        }
    },
    41: {
        "name": "Tremolo",
        "category": "effect",
        "default_blocks": 4,
        "max_blocks": 6,
        "params": 2,
        "cpu": 2,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "control_in": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "depth": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 5
            }
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "2in->2out"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "waveform": ["fender-ish", "vox-ish", "triangle", "sine", "square"]
        }
    },
    42: {
        "name": "Tone Control",
        "category": "effect",
        "default_blocks": 6,
        "max_blocks": 10,
        "params": 6,
        "cpu": 5,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "low_shelf": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "mid_gain_1": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "mid_freq_1": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "mid_gain_2": {
                "isDefault": False,
                "isParam": True,
                "position": 5
            },
            "mid_freq_2": {
                "isDefault": False,
                "isParam": True,
                "position": 6
            },
            "high_shelf": {
                "isDefault": True,
                "isParam": True,
                "position": 7
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 8
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 9
            }
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "2in->2out"],
            "num_mid_bands": [1, 2]
        }
    },
    43: {
        "name": "Delay w Mod",
        "category": "effect",
        "default_blocks": 7,
        "max_blocks": 9,
        "params": 5,
        "cpu": 18,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "delay_time": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "feedback": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "mod_rate": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "mod_depth": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 6
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 7
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 8
            }
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "2in->2out"],
            "control": ["rate", "tap_tempo"],
            "type": ["clean", "tape", "old_tape", "bbd"],
            "tap_ratio": ["1:1", "2:3", "1:2", "1:3", "3:8", "1:4",
                          "3:16", "1:8", "1:16", "1:32"]
        }
    },
    44: {
        "name": "Stompswitch",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            }
        },
        "options": {
            "stompswitch": ["left", "middle", "right", "ext"],
            "action": ["momentary", "latching"],
            "normally": ["zero", "one"]
        }
    },
    45: {
        "name": "Value",
        "category": "cv",
        "default_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.15,
        "blocks": {
            "value": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            }
        },
        "options": {
            "output": ["0 to 1", "-1 to 1"]
        }
    },
    46: {
        "name": "CV Delay",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "cpu": 1.5,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "delay_time": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {}
    },
    47: {
        "name": "CV Loop",
        "category": "cv",
        "default_blocks": 6,
        "max_blocks": 8,
        "params": 7,
        "cpu": 0.1,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "record": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "play": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "playback_speed": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "start_position": {
                "isDefault": False,
                "isParam": True,
                "position": 4
            },
            "stop_position": {
                "isDefault": False,
                "isParam": True,
                "position": 5
            },
            "restart_loop": {
                "isDefault": True,
                "isParam": True,
                "position": 6
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 7
            }
        },
        "options": {
            "max_rec_time": list(range(1, 17)),
            "length_edit": ["off", "on"]
        }
    },
    48: {
        "name": "CV Filter",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "cpu": 0.1,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "time_constant": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {}
    },
    49: {
        "name": "Clock Divider",
        "category": "cv",
        "default_blocks": 5,
        "max_blocks": 5,
        "params": 4,
        "cpu": 0.4,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "reset_switch": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "dividend": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "divisor": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            }
        },
        "options": {
            "input": ["tap", "cv_control"]
        }
    },
    50: {
        "name": "Comparator",
        "category": "cv",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 2,
        "cpu": 0.04,
        "blocks": {
            "cv_positive_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "cv_negative_input": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {
            "output": ["0 to 1", "-1 to 1"]
        }
    },
    51: {
        "name": "CV Rectify",
        "category": "cv",
        "default_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.02,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            }
        },
        "options": {}
    },
    52: {
        "name": "Trigger",
        "category": "cv",
        "default_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.1,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            }
        },
        "options": {}
    },
    53: {
        "name": "Stereo Spread",
        "category": "audio",
        "default_blocks": 4,
        "max_blocks": 5,
        "params": 1,
        "cpu": 2,
        "blocks": {
            "audio_in_1": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_2": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "delay_time": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "side_gain": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            },
            "audio_out_1": {
                "isDefault": True,
                "isParam": False,
                "position": 3
            },
            "audio_out_2": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            }
        },
        "options": {
            "method": ["mid_side", "haas"]
        }
    },
    54: {
        "name": "Cport Exp CV In",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            }
        },
        "options": {
            "output_range": ["0 to 1", "-1 to 1"]
        }
    },
    55: {
        "name": "Cport CV Out",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.2,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            }
        },
        "options": {
            "input_range": ["0 to 1", "-1 to 1"]
        }
    },
    56: {
        "name": "UI Button",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.04,
        "blocks": {
            "in": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "cv_output": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            }
        },
        "options": {}
    },
    57: {
        "name": "Audio Panner",
        "category": "audio",
        "default_blocks": 4,
        "max_blocks": 5,
        "params": 3,
        "cpu": 1,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "pan": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 3
            },
            "audio_out_R": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            }
        },
        "options": {
            "channels": ["1in->2out", "2in->2out"],
            "pan_type": ["equal_pwr", "-4.5dB", "linear"]
        }
    },
    58: {
        "name": "Pitch Detector",
        "category": "analysis",
        "default_blocks": 2,
        "max_blocks": 2,
        "params": 0,
        "cpu": 2.5,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            }
        },
        "options": {

        }
    },
    59: {
        "name": "Pitch Shifter",
        "category": "audio",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 1,
        "cpu": 15.5,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "pitch_shift": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {}
    },
    60: {
        "name": "Midi Note Out",
        "category": "interface",
        "default_blocks": 2,
        "max_blocks": 3,
        "params": 3,
        "cpu": 0.1,
        "blocks": {
            "note_in": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "gate_in": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "velocity_out": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            }
        },
        "options": {
            "midi_channel": list(range(1, 17)),
            "velocity_output": ["off", "on"]
        }
    },
    61: {
        "name": "Midi CC Out",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "cpu": 0.2,
        "blocks": {
            "cc_out": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            }
        },
        "options": {
            "midi_channel": list(range(1, 17)),
            "controller": list(range(0, 128))
        }
    },
    62: {
        "name": "midi_pc_out",
        "category": "interface",
        "default_blocks": 2,
        "max_blocks": 2,
        "params": 2,
        "cpu": 0.1,
        "blocks": {
            "pc_out": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "trigger_in": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            }
        },
        "options": {
            "midi_channel": list(range(1, 17))
        }
    },
    63: {
        "name": "Bit Modulator",
        "category": "audio",
        "default_blocks": 3,
        "max_blocks": 3,
        "params": 0,
        "cpu": 1.2,
        "blocks": {
            "audio_in_1": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_2": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            }
        },
        "options": {
            "type": ["xor", "and", "or"]
        }
    },
    64: {
        "name": "Audio Balance",
        "category": "audio",
        "default_blocks": 4,
        "max_blocks": 7,
        "params": 1,
        "cpu": 1.7,
        "blocks": {
            "audio_in_1_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_1_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "audio_in_2_L": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            },
            "audio_in_2_R": {
                "isDefault": False,
                "isParam": False,
                "position": 3
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "audio_output_L": {
                "isDefault": True,
                "isParam": False,
                "position": 5
            },
            "audio_output_R": {
                "isDefault": False,
                "isParam": False,
                "position": 6
            }
        },
        "options": {
            "stereo": ["mono", "stereo"]
        }
    },
    65: {
        "name": "Inverter",
        "category": "audio",
        "default_blocks": 2,
        "max_blocks": 2,
        "params": 0,
        "cpu": 0.3,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            }
        },
        "options": {}
    },
    66: {
        "name": "Fuzz",
        "category": "effect",
        "default_blocks": 4,
        "max_blocks": 4,
        "params": 2,
        "cpu": 16,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "input_gain": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "output_gain": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 3
            }
        },
        "options": {
            "model": ["efuzzy", "burly", "scoopy", "ugly"]
        }
    },
    67: {
        "name": "Ghostverb",
        "category": "effect",
        "default_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "cpu": 45,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "decay_feedback": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "rate": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "resonance": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 6
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 7
            }
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"]
        }
    },
    68: {
        "name": "Cabinet Sim",
        "category": "effect",
        "default_blocks": 2,
        "max_blocks": 4,
        "params": 0,
        "cpu": 10,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 3
            }
        },
        "options": {
            "channels": ["mono", "stereo"],
            "type": ["4x12_full", "2x12_dark", "2x12_modern", "1x12",
                     "1x8_lofi", "1x12_vintage", "4x12_hifi"]
        }
    },
    69: {
        "name": "Flanger",
        "category": "effect",
        "default_blocks": 7,
        "max_blocks": 9,
        "params": 5,
        "cpu": 11,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "control_in": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "regen": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "width": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "tone_tilt_eq": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 6
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 7
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 8
            }
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "type": ["1960s", "1970s", "thru_0"]
        }
    },
    70: {
        "name": "Chorus",
        "category": "effect",
        "default_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "cpu": 13,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "control_in": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "width": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "tone_tilt_eq": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 6
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 7
            }
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "type": ["classic"]
        }
    },
    71: {
        "name": "Vibrato",
        "category": "effect",
        "default_blocks": 4,
        "max_blocks": 6,
        "params": 2,
        "cpu": 5,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "control_in": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "width": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 5
            }
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "waveform": ["sine", "triangle", "swung_sine", "swung"]
        }
    },
    72: {
        "name": "Env Filter",
        "category": "effect",
        "default_blocks": 6,
        "max_blocks": 8,
        "params": 4,
        "cpu": 7,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "sensitivity": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "min_freq": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "max_freq": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "filter_q": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 6
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 7
            }
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "direction": ["up", "down"]
        }
    },
    73: {
        "name": "Ring Modulator",
        "category": "effect",
        "default_blocks": 4,
        "max_blocks": 6,
        "params": 3,
        "cpu": 14,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "frequency": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "ext_in": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "duty_cycle": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            }
        },
        "options": {
            "waveform": ["since", "square", "triangle", "sawtooth"],
            "ext_audio_in": ["off", "on"],
            "duty_cycle": ["off", "on"],
            "upsampling": ["none", "2x"]
        }
    },
    74: {
        "name": "Hall Reverb",
        "category": "effect",
        "default_blocks": 8,
        "max_blocks": 8,
        "params": 4,
        "cpu": 22,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            },
            "decay_time": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "low_eq": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "lpf_freq": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 6
            },
            "audio_out_R": {
                "isDefault": True,
                "isParam": False,
                "position": 7
            }
        },
        "options": {}
    },
    75: {
        "name": "Ping Pong Delay",
        "category": "effect",
        "default_blocks": 7,
        "max_blocks": 9,
        "params": 5,
        "cpu": 18,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "delay_time": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "feedback": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "mod_rate": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "mod_depth": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 6
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 7
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 8
            }
        },
        "options": {
            "channels": ["1in->1out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "type": ["clean", "tape", "old_tape", "bbd"],
            "tap_ratio": ["1:1", "2:3", "1:2", "1:3", "3:8", "1:4",
                          "3:16", "1:8", "1:16", "1:32"]
        }
    },
    76: {
        "name": "Audio Mixer",
        "category": "audio",
        "default_blocks": 5,
        "max_blocks": 34,
        "params": 16,
        "cpu": 7,
        "blocks": {
            "audio_in_1_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_2_L": {
                "isDefault": True,
                "isParam": False,
                "position": 2
            },
            "audio_in_n_L": {
                "isDefault": False,
                "isParam": False,
                "position": [4, 6, 10, 14, 18, 22, 26]
            },
            "audio_in_n_R": {
                "isDefault": False,
                "isParam": False,
                "position": [1, 3, 5, 7, 11, 15, 19, 23, 27]
            },
            "gain_n": {
                "isDefault": True,
                "isParam": True,
                "position": list(range(28, 30))
            },
            "pan_n": {
                "isDefault": False,
                "isParam": True,
                "position": list(range(30, 31))
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 32
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 33
            }
        },
        "options": {
            "channels": list(range(2, 9)),
            "stereo": ["mono", "stereo"],
            "panning": ["off", "on"]
        }
    },
    77: {
        "name": "CV Flip Flop",
        "category": "cv",
        "default_blocks": 2,
        "max_blocks": 2,
        "params": 1,
        "cpu": 0.2,
        "blocks": {
            "cv_input": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            },
            "cv_output": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            }
        },
        "options": {}
    },
    78: {
        "name": "Diffuser",
        "category": "audio",
        "default_blocks": 6,
        "max_blocks": 6,
        "params": 4,
        "cpu": 2,
        "blocks": {
            "audio_in": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "gain": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "size": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "mod_width": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "mod_rate": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "audio_out": {
                "isDefault": True,
                "isParam": False,
                "position": 5
            }
        },
        "options": {}
    },
    79: {
        "name": "Reverb Lite",
        "category": "effect",
        "default_blocks": 4,
        "max_blocks": 6,
        "params": 2,
        "cpu": 10,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "decay_time": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 4
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 5
            }
        },
        "options": {
            "channels": ["1in->1out", "1in->2out", "stereo"]
        }
    },
    80: {
        "name": "Room Reverb",
        "category": "effect",
        "default_blocks": 8,
        "max_blocks": 8,
        "params": 4,
        "cpu": 22,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": True,
                "isParam": False,
                "position": 1
            },
            "decay_time": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "low_eq": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "lpf_freq": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "mix": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 6
            },
            "audio_out_R": {
                "isDefault": True,
                "isParam": False,
                "position": 7
            }
        },
        "options": {}
    },
    81: {
        "name": "Pixel",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 1,
        "params": 1,
        "cpu": 0.01,
        "blocks": {
            "cv_audio_in": {
                "isDefault": True,
                "isParam": True,
                "position": 0
            }
        },
        "options": {
            "control": ["cv", "audio"]
        }
    },
    82: {
        "name": "Midi Clock In",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 4,
        "params": 0,
        "cpu": 0.1,
        "blocks": {
            "cc_value": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "clock_out": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "run_out": {
                "isDefault": False,
                "isParam": False,
                "position": 2
            },
            "divider": {
                "isDefault": False,
                "isParam": False,
                "position": 3
            }
        },
        "options": {
            "clock_out": ["disabled", "enabled"],
            "run_out": ["disabled", "enabled"],
            "divider": ["disabled", "enabled"],
            "beat_modifier": ["1", "2", "3", "4", "6", "12",
                              "1/12", "1/6", "1/4", "1/3", "1/2"]
        }
    },
    83: {
        "name": "Granular",
        "category": "audio",
        "default_blocks": 8,
        "max_blocks": 10,
        "params": 6,
        "cpu": 8,
        "blocks": {
            "audio_in_L": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "audio_in_R": {
                "isDefault": False,
                "isParam": False,
                "position": 1
            },
            "grain_size": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "grain_position": {
                "isDefault": True,
                "isParam": True,
                "position": 3
            },
            "density": {
                "isDefault": True,
                "isParam": True,
                "position": 4
            },
            "texture": {
                "isDefault": True,
                "isParam": True,
                "position": 5
            },
            "speed_pitch": {
                "isDefault": True,
                "isParam": True,
                "position": 6
            },
            "freeze": {
                "isDefault": True,
                "isParam": True,
                "position": 7
            },
            "audio_out_L": {
                "isDefault": True,
                "isParam": False,
                "position": 8
            },
            "audio_out_R": {
                "isDefault": False,
                "isParam": False,
                "position": 9
            }
        },
        "options": {
            "num_grains": list(range(1, 9)),
            "channels": ["mono", "stereo"],
            "pos_control": ["cv", "tap_tempo"],
            "size_control": ["cv", "tap_tempo"]
        }
    },
    84: {
        "name": "Midi Clock Out",
        "category": "interface",
        "default_blocks": 3,
        "max_blocks": 5,
        "params": 5,
        "cpu": 0.3,
        "blocks": {
            "tap_control": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "cv_control": {
                "isDefault": False,
                "isParam": True,
                "position": 0
            },
            "sent:": {
                "isDefault": True,
                "isParam": True,
                "position": 1
            },
            "reset": {
                "isDefault": True,
                "isParam": True,
                "position": 2
            },
            "send_position": {
                "isDefault": False,
                "isParam": True,
                "position": 3
            },
            "song_position": {
                "isDefault": False,
                "isParam": True,
                "position": 4
            }
        },
        "options": {
            "input": ["tap", "cv_control"],
            "run_in": ["enabled", "disabled"],
            "reset_in": ["enabled", "disabled"],
            "position": ["disabled", "enabled"]
        }
    },
    85: {
        "name": "Tap to CV",
        "category": "cv",
        "default_blocks": 2,
        "max_blocks": 4,
        "params": 2,
        "cpu": 0.1,
        "blocks": {
            "tap_input": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            },
            "min_time": {
                "isDefault": False,
                "isParam": True,
                "position": 1
            },
            "max_time": {
                "isDefault": False,
                "isParam": True,
                "position": 2
            },
            "output": {
                "isDefault": True,
                "isParam": False,
                "position": 3
            }
        },
        "options": {
            "range": ["40hz", "time"],
            "output": ["linear", "exponential"]
        }
    },
    86: {
        "name": "Midi Pitch Bend In",
        "category": "interface",
        "default_blocks": 1,
        "max_blocks": 1,
        "params": 0,
        "cpu": 0.1,
        "blocks": {
            "pitch_bend": {
                "isDefault": True,
                "isParam": False,
                "position": 0
            }
        },
        "options": {
            "midi_channel": list(range(1, 17))
        }
    }
}

for k, v in list(module_index.items()):
    module_index[str(k)] = module_index.pop(k)

with open("zoia_lib/common/schemas/ModuleIndex.json", "w") as f:
    json.dump(module_index, f)

# for i in module_index:
#     pos = []
#     for j, k in module_index[i]['blocks'].items():
#         if k['isDefault']:
#             data = k['position']
#             if isinstance(data, list):
#                 for l in data:
#                     pos.append(l)
#             else:
#                 pos.append(data)
#     module_index[i]["default_blocks"] = len(pos)
#
#     pos = []
#     for j, k in module_index[i]['blocks'].items():
#         data = k['position']
#         if isinstance(data, list):
#             for l in data:
#                 pos.append(l)
#         else:
#             pos.append(data)
#     module_index[i]["max_blocks"] = max(pos)+1
