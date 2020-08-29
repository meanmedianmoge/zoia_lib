# -*- coding: utf-8 -*-
"""
Created: 9:58 AM on 7/25/20
Author: Mike Moger
Usage:
"""

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

properties = {
    0: {
        'name': 'sv_filter',
        'category': 'audio',
        'max_blocks': 6,
        'params': 2,
        'cpu': 3,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'frequency': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'resonance': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'lowpass_output': {
                'isDefault': True,
                'isParam': False,
                'position': 3
            },
            'hipass_output': {
                'isDefault': False,
                'isParam': False,
                'position': 4
            },
            'bandpass_output': {
                'isDefault': False,
                'isParam': False,
                'position': 5
            }
        },
        'options': {
            'lowpass_output': ['on', 'off'],
            'hipass_output': ['off', 'on'],
            'bandpass_output': ['off', 'on']
        }
    },
    1: {
        'name': 'audio_input',
        'category': 'interface',
        'max_blocks': 2,
        'params': 0,
        'cpu': 0.4,
        'blocks': {
            'input_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'input_R': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            }
        },
        'options': {
            'channels': ['stereo', 'left', 'right']
        }
    },
    2: {
        'name': 'audio_output',
        'category': 'interface',
        'max_blocks': 3,
        'params': 1,
        'cpu': 1.7,
        'blocks': {
            'input_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'input_R': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            },
            'gain': {
                'isDefault': False,
                'isParam': True,
                'position': 2
            }
        },
        'options': {
            'gain_control': ['off', 'on'],
            'channels': ['stereo', 'left', 'right']
        }
    },
    3: {
        'name': 'aliaser',
        'category': 'audio',
        'max_blocks': 3,
        'params': 1,
        'cpu': 0.7,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            '#_of_samples': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            None
        }
    },
    4: {
        'name': 'sequencer',
        'category': 'cv',
        'max_blocks': 42,
        'params': 34,
        'cpu': 2,
        'blocks': {
            'step_#': {
                'isDefault': True,
                'isParam': True,
                'position': [0-31]
            },
            'gate_in': {
                'isDefault': True,
                'isParam': True,
                'position': 32
            },
            'queue_start': {
                'isDefault': False,
                'isParam': True,
                'position': 33
            },
            # type is determined by clicking the encoder per track
            'out_type': {
                'isDefault': True,
                'isParam': False,
                'position': [34-41],
                'type': ['cv', 'gate', 'ratchet']
            }
        },
        'options': {
            'number_of_steps': [1-32],
            'num_of_tracks': [1-8],
            'restart_jack': ['off', 'on'],
            'behavior': ['loop', 'once']
        }
    },
    5: {
        'name': 'lfo',
        'category': 'cv',
        'max_blocks': 5,
        'params': 4,
        'cpu': 0.3,
        'blocks': {
            'frequency_trigger_in': {
                'isDefault': True,
                'isParam': True,
                'position': 0,
                'type': ['frequency', 'trigger_in']
            },
            'swing_amount': {
                'isDefault': False,
                'isParam': True,
                'position': 1
            },
            'phase_input': {
                'isDefault': False,
                'isParam': False,
                'position': 2
            },
            'phase_reset': {
                'isDefault': False,
                'isParam': True,
                'position': 3
            },
            'output': {
                'isDefault': True,
                'isParam': False,
                'position': 4
            }
        },
        'options': {
            'waveform': ['square', 'sine', 'triangle',
                         'sawtooth', 'ramp', 'random'],
            'swing_control': ['off', 'on'],
            'output': ['0 to 1', '-1 to 1'],
            'input': ['cv', 'trigger'],
            'phase_input': ['off', 'on'],
            'phase_reset': ['off', 'on']
        }
    },
    6: {
        'name': 'adsr',
        'category': 'cv',
        'max_blocks': 10,
        'params': 9,
        'cpu': 0.07,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'retrigger': {
                'isDefault': False,
                'isParam': True,
                'position': 1
            },
            'delay': {
                'isDefault': False,
                'isParam': True,
                'position': 2
            },
            'attack': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'hold_attack_decay': {
                'isDefault': False,
                'isParam': True,
                'position': 4
            },
            'decay': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'sustain': {
                'isDefault': True,
                'isParam': True,
                'position': 6
            },
            'hold_sustain_release': {
                'isDefault': False,
                'isParam': True,
                'position': 7
            },
            'release': {
                'isDefault': True,
                'isParam': True,
                'position': 8
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 9
            }
        },
        'options': {
            'retrigger_input': ['off', 'on'],
            'initial_delay': ['off', 'on'],
            'hold_attack_decay': ['off', 'on'],
            'str': ['on', 'off'],
            'immediate_release': ['on', 'off'],
            'hold_sustain_release': ['off', 'on']
        }
    },
    7: {
        'name': 'vca',
        'category': 'audio',
        'max_blocks': 5,
        'params': 1,
        'cpu': 0.7,
        'blocks': {
            'audio_in_1': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_2': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'level_control': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'audio_out_1': {
                'isDefault': True,
                'isParam': False,
                'position': 3
            },
            'audio_out_2': {
                'isDefault': False,
                'isParam': False,
                'position': 4
            }
        },
        'options': {
            'channels': ['1in->1out', 'stereo']
        }
    },
    8: {
        'name': 'audio_multiply',
        'category': 'audio',
        'max_blocks': 3,
        'params': 0,
        'cpu': 0.4,
        'blocks': {
            'audio_in_1': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_2': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            None
        }
    },
    9: {
        'name': 'bit_crusher',
        'category': 'audio',
        'max_blocks': 3,
        'params': 1,
        'cpu': 1,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'crushed_bits': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            'fractions': ['off', 'on']
        }
    },
    10: {
        'name': 'sample_and_hold',
        'category': 'cv',
        'max_blocks': 3,
        'params': 2,
        'cpu': 0.1,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'trigger': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            None
        }
    },
    11: {
        'name': 'od_and_distortion',
        'category': 'effect',
        'max_blocks': 4,
        'params': 2,
        'cpu': 17,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'input_gain': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'output_gain': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 3
            }
        },
        'options': {
            'model': ['plexi', 'germ', 'classic', 'pushed']
        }
    },
    12: {
        'name': 'env_follower',
        'category': 'analysis',
        'max_blocks': 4,
        'params': 2,
        'cpu': 5,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'rise_time': {
                'isDefault': False,
                'isParam': True,
                'position': 1
            },
            'fall_time': {
                'isDefault': False,
                'isParam': True,
                'position': 2
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 3
            }
        },
        'options': {
            'rise_fall_time': ['off', 'on'],
            'output_scale': ['log', 'linear']
        }
    },
    13: {
        'name': 'delay_line',
        'category': 'audio',
        'max_blocks': 4,
        'params': 2,
        'cpu': 3,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'delay_time': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'modulation_in': {
                'isDefault': False,
                'isParam': True,
                'position': 1
            },
            'tap_tempo_in': {
                'isDefault': False,
                'isParam': True,
                'position': 2
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': [2-3]
            }
        },
        'options': {
            'max_time': ['1s', '2s', '4s', '8s', '16s', '100ms'],
            'tap_tempo_in': ['no', 'yes']
        }
    },
    14: {
        'name': 'oscillator',
        'category': 'audio',
        'max_blocks': 4,
        'params': 2,
        'cpu': 10,
        'blocks': {
            'frequency': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'fm_input': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'duty_cycle': {
                'isDefault': False,
                'isParam': True,
                'position': 2
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 3
            }
        },
        'options': {
            'waveform': ['sine', 'square', 'triangle', 'sawtooth'],
            'fm_in': ['off', 'on'],
            'duty_cycle': ['off', 'on'],
            'upsampling': ['none', '2x']
        }
    },
    15: {
        'name': 'pushbutton',
        'category': 'interface',
        'max_blocks': 1,
        'params': 0,
        'cpu': 0.02,
        'blocks': {
            'switch': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            }
        },
        'options': {
            'action': ['momentary', 'latching'],
            'normally': ['zero', 'one']
        }
    },
    16: {
        'name': 'keyboard',
        'category': 'interface',
        'max_blocks': 26,
        'params': 23,
        'cpu': 0.1,
        'blocks': {
            'note_#': {
                'isDefault': True,
                'isParam': True,
                'position': [0-22]
            },
            'note_out': {
                'isDefault': True,
                'isParam': False,
                'position': 23
            },
            'gate_out': {
                'isDefault': True,
                'isParam': False,
                'position': 24
            },
            'trigger_out': {
                'isDefault': True,
                'isParam': False,
                'position': 25
            }
        },
        'options': {
            '#_of_notes': [1-23]
        }
    },
    17: {
        'name': 'cv_filter',
        'category': 'cv',
        'max_blocks': 3,
        'params': 2,
        'cpu': 0.02,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'time_constant': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            None
        }
    },
    18: {
        'name': 'steps',
        'category': 'cv',
        'max_blocks': 3,
        'params': 2,
        'cpu': 0.7,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'quant_steps': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            None
        }
    },
    19: {
        'name': 'slew_limiter',
        'category': 'cv',
        'max_blocks': 4,
        'params': 2,
        'cpu': 0.2,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'slew_rate': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'rising_lag': {
                'isDefault': False,
                'isParam': True,
                'position': 1
            },
            'falling_lag': {
                'isDefault': False,
                'isParam': True,
                'position': 2
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': [2-3]
            }
        },
        'options': {
            'control': ['linked', 'separate'],
        }
    },
    20: {
        'name': 'midi_notes_in',
        'category': 'interface',
        'max_blocks': 32,
        'params': 0,
        'cpu': 0.3,
        'blocks': {
            'note_out': {
                'isDefault': True,
                'isParam': False,
                'position': [0, 4, 8, 12, 16, 20, 24, 28]
            },
            'gate_out': {
                'isDefault': True,
                'isParam': False,
                'position': [1, 5, 9, 13, 17, 21, 25, 29]
            },
            'velocity_out': {
                'isDefault': False,
                'isParam': False,
                'position': [2, 6, 10, 14, 18, 22, 26, 30]
            },
            'trigger_out': {
                'isDefault': False,
                'isParam': False,
                'position': [3, 7, 11, 15, 19, 23, 27, 31]
            }
        },
        'options': {
            'midi_channel': [1-16],
            '#_of_outputs': [1-8],
            'priority': ['newest', 'oldest', 'highest', 'lowest', 'round_robin'],
            'greedy': ['no', 'yes'],
            'velocity_output': ['off', 'on'],
            'low_note': [0-127],
            'high_note': [127-0],
            'trigger_pulse': ['off', 'on']
        }
    },
    21: {
        'name': 'midi_cc_in',
        'category': 'interface',
        'max_blocks': 1,
        'params': 0,
        'cpu': 0.1,
        'blocks': {
            'cc_value': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            }
        },
        'options': {
            'midi_channel': [1-16],
            'controller': [0-127],
            'output_range': ['0 to 1', '-1 to 1']
        }
    },
    22: {
        'name': 'multiplier',
        'category': 'cv',
        'max_blocks': 4,
        'params': 2,
        'cpu': 0.2,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': [0-8]
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 9
            }
        },
        'options': {
            'num_inputs': [2-8]
        }
    },
    23: {
        'name': 'compressor',
        'category': 'effect',
        'max_blocks': 9,
        'params': 4,
        'cpu': 3,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'threshold': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'attack': {
                'isDefault': False,
                'isParam': True,
                'position': 3
            },
            'release': {
                'isDefault': False,
                'isParam': True,
                'position': 4
            },
            'ratio': {
                'isDefault': False,
                'isParam': True,
                'position': 5
            },
            'sidechain_in': {
                'isDefault': False,
                'isParam': False,
                'position': 6
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 7
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 8
            }
        },
        'options': {
            'attack_ctrl': ['off', 'on'],
            'release_ctrl': ['off', 'on'],
            'ratio_ctrl': ['off', 'on'],
            'channels': ['1in->1out', 'stereo'],
            'sidechain': ['internal', 'external']
        }
    },
    24: {
        'name': 'multi-filter',
        'category': 'audio',
        'max_blocks': 5,
        'params': 3,
        'cpu': 0.8,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'gain': {
                'isDefault': False,
                'isParam': True,
                'position': 1
            },
            'frequency': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'q': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False
            }
        },
        'options': {
            'filter_shape': ['lowpass', 'highpass', 'bandpass',
                             'bell', 'hi_shelf', 'low_shelf'],
        }
    },
    25: {
        'name': 'plate_reverb',
        'category': 'effect',
        'max_blocks': 8,
        'params': 4,
        'cpu': 22,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            },
            'decay_time': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'low_eq': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'high_eq': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 6
            },
            'audio_out_R': {
                'isDefault': True,
                'isParam': False,
                'position': 7
            }
        },
        'options': {
            None
        }
    },
    26: {
        'name': 'buffer_delay',
        'category': 'audio',
        'max_blocks': 2,
        'params': 0,
        'cpu': 0.2,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            }
        },
        'options': {
            'buffer_length': [0-16]
        }
    },
    27: {
        'name': 'all_pass_filter',
        'category': 'audio',
        'max_blocks': 3,
        'params': 1,
        'cpu': 5,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'filter_gain': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            '#_of_poles': [1-8]
        }
    },
    28: {
        'name': 'quantizer',
        'category': 'cv',
        'max_blocks': 4,
        'params': 3,
        'cpu': 1,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'key': {
                'isDefault': False,
                'isParam': True,
                'position': 1
            },
            'scale': {
                'isDefault': False,
                'isParam': True,
                'position': 2
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 3
            }
        },
        'options': {
            'key_scale_jacks': ['no', 'yes']
        }
    },
    29: {
        'name': 'phaser',
        'category': 'effect',
        'max_blocks': 8,
        'params': 4,
        'cpu': 15,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'control_in': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'resonance': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'width': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 6
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 7
            }
        },
        'options': {
            'channels': ['1in->1out', '1in->2out', '2in->2out'],
            'control': ['rate', 'tap_tempo', 'cv_direct'],
            'number_of_stages': [4, 2, 1, 3, 6, 8]
        }
    },
    30: {
        'name': 'looper',
        'category': 'audio',
        'max_blocks': 9,
        'params': 6,
        'cpu': 3,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'record': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'restart_playback': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            },
            'stop_play': {
                'isDefault': False,
                'isParam': True,
                'position': 3
            },
            'speed_pitch': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'start_position': {
                'isDefault': False,
                'isParam': True,
                'position': 5
            },
            'loop_length': {
                'isDefault': False,
                'isParam': False,
                'position': 6
            },
            'reverse_playback': {
                'isDefault': False,
                'isParam': True,
                'position': 7
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 8
            }
        },
        'options': {
            'max_rec_time': ['1s', '2s', '4s', '8s', '16s', '32s'],
            'length_edit': ['off', 'on'],
            'playback': ['once', 'loop'],
            'length': ['fixed', 'pre_speed'],
            'hear_while_rec': ['no', 'yes'],
            'play_reverse': ['no', 'yes'],
            'overdub': ['no', 'yes'],
            'stop_play_button': ['no', 'yes']
        }
    },
    31: {
        'name': 'in_switch',
        'category': 'cv',
        'max_blocks': 18,
        'params': 17,
        'cpu': 0.2,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': [0-15]
            },
            'in_select': {
                'isDefault': True,
                'isParam': True,
                'position': 16
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 17
            }
        },
        'options': {
            'num_inputs': [2-16]
        }
    },
    32: {
        'name': 'out_switch',
        'category': 'cv',
        'max_blocks': 18,
        'params': 2,
        'cpu': 0.2,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'out_select': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': [2-17]
            }
        },
        'options': {
            'num_outputs': [2-16]
        }
    },
    33: {
        'name': 'audio_in_switch',
        'category': 'audio',
        'max_blocks': 18,
        'params': 1,
        'cpu': 0.8,
        'blocks': {
            'audio_input': {
                'isDefault': True,
                'isParam': False,
                'position': [0-15]
            },
            'in_select': {
                'isDefault': True,
                'isParam': True,
                'position': 16
            },
            'audio_output': {
                'isDefault': True,
                'isParam': False,
                'position': 17
            }
        },
        'options': {
            'num_inputs': [2-16]
        }
    },
    34: {
        'name': 'audio_out_switch',
        'category': 'audio',
        'max_blocks': 18,
        'params': 1,
        'cpu': 0.7,
        'blocks': {
            'audio_input': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'in_select': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'audio_output': {
                'isDefault': True,
                'isParam': False,
                'position': [2-17]
            }
        },
        'options': {
            'num_outputs': [2-16]
        }
    },
    35: {
        'name': 'midi_pressure',
        'category': 'interface',
        'max_blocks': 1,
        'params': 0,
        'cpu': 0.03,
        'blocks': {
            'channel_pressure': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            }
        },
        'options': {
            'midi_channel': [1-16]
        }
    },
    36: {
        'name': 'onset_detector',
        'category': 'analysis',
        'max_blocks': 3,
        'params': 1,
        'cpu': 0.7,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'sensitivity': {
                'isDefault': False,
                'isParam': True,
                'position': 1
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            'sensitivity': ['off', 'on']
        }
    },
    37: {
        'name': 'rhythm',
        'category': 'cv',
        'max_blocks': 5,
        'params': 3,
        'cpu': 0.5,
        'blocks': {
            'rec_start_stop': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'rhythm_in': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'play': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'play_done': {
                'isDefault': False,
                'isParam': False,
                'position': 3
            },
            'rhythm_out': {
                'isDefault': True,
                'isParam': False,
                'position': 5
            }
        },
        'options': {
            'done_ctrl': ['off', 'on'],
        }
    },
    38: {
        'name': 'noise',
        'category': 'audio',
        'max_blocks': 1,
        'params': 0,
        'cpu': 0.4,
        'blocks': {
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            }
        },
        'options': {
            None
        }
    },
    39: {
        'name': 'random',
        'category': 'cv',
        'max_blocks': 2,
        'params': 1,
        'cpu': 0.1,
        'blocks': {
            'trigger_in': {
                'isDefault': False,
                'isParam': True,
                'position': 0
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            }
        },
        'options': {
            'output': ['0 to 1', '-1 to 1'],
            'new_val_on_trig': ['off', 'on']
        }
    },
    40: {
        'name': 'gate',
        'category': 'effect',
        'max_blocks': 8,
        'params': 3,
        'cpu': 3,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'threshold': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'attack': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'release': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'sidechain_in': {
                'isDefault': False,
                'isParam': False,
                'position': 5
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 6
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 7
            }
        },
        'options': {
            'attack_ctrl': ['off', 'on'],
            'release_ctrl': ['off', 'on'],
            'channels': ['1in->1out', '1in->2out', '2in->2out'],
            'sidechain': ['internal', 'external']
        }
    },
    41: {
        'name': 'tremolo',
        'category': 'effect',
        'max_blocks': 6,
        'params': 2,
        'cpu': 2,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'control_in': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'depth': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 4
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 5
            }
        },
        'options': {
            'channels': ['1in->1out', '1in->2out', '2in->2out'],
            'control': ['rate', 'tap_tempo', 'cv_direct'],
            'waveform': ['fender-ish', 'vox-ish', 'triangle', 'sine', 'square']
        }
    },
    42: {
        'name': 'tone_control',
        'category': 'effect',
        'max_blocks': 10,
        'params': 6,
        'cpu': 5,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'low_shelf': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'mid_gain_1': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'mid_freq_1': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'mid_gain_2': {
                'isDefault': False,
                'isParam': True,
                'position': 5
            },
            'mid_freq_2': {
                'isDefault': False,
                'isParam': True,
                'position': 6
            },
            'high_shelf': {
                'isDefault': True,
                'isParam': True,
                'position': 7
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 8
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 9
            }
        },
        'options': {
            'channels': ['1in->1out', '1in->2out', '2in->2out'],
            'num_mid_bands': [1, 2]
        }
    },
    43: {
        'name': 'delay_w_mod',
        'category': 'effect',
        'max_blocks': 9,
        'params': 5,
        'cpu': 18,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'delay_time': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'feedback': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'mod_rate': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'mod_depth': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 6
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 7
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 8
            }
        },
        'options': {
            'channels': ['1in->1out', '1in->2out', '2in->2out'],
            'control': ['rate', 'tap_tempo'],
            'type': ['clean', 'tape', 'old_tape', 'bbd'],
            'tap_ratio': ['1:1', '2:3', '1:2', '1:3', '3:8', '1:4',
                          '3:16', '1:8', '1:16', '1:32']
        }
    },
    44: {
        'name': 'stompswitch',
        'category': 'interface',
        'max_blocks': 1,
        'params': 0,
        'cpu': 0.1,
        'blocks': {
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            }
        },
        'options': {
            'stompswitch': ['left', 'middle', 'right', 'ext'],
            'action': ['momentary', 'latching'],
            'normally': ['zero', 'one']
        }
    },
    45: {
        'name': 'value',
        'category': 'cv',
        'max_blocks': 2,
        'params': 1,
        'cpu': 0.15,
        'blocks': {
            'value': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            }
        },
        'options': {
            'output': ['0 to 1', '-1 to 1']
        }
    },
    46: {
        'name': 'cv_delay',
        'category': 'cv',
        'max_blocks': 3,
        'params': 2,
        'cpu': 1.5,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'delay_time': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            None
        }
    },
    47: {
        'name': 'cv_loop',
        'category': 'cv',
        'max_blocks': 8,
        'params': 7,
        'cpu': 0.1,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'record': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'play': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'playback_speed': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'start_position': {
                'isDefault': False,
                'isParam': True,
                'position': 4
            },
            'stop_position': {
                'isDefault': False,
                'isParam': True,
                'position': 5
            },
            'restart_loop': {
                'isDefault': True,
                'isParam': True,
                'position': 6
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 7
            }
        },
        'options': {
            'max_rec_time': [1-16],
            'length_edit': ['off', 'on']
        }
    },
    48: {
        'name': 'cv_filter',
        'category': 'cv',
        'max_blocks': 3,
        'params': 2,
        'cpu': 0.1,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'time_constant': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            None
        }
    },
    49: {
        'name': 'clock_divider',
        'category': 'cv',
        'max_blocks': 4,
        'params': 3,
        'cpu': 0.4,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'reset_switch': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'clock_ratio': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 3
            }
        },
        'options': {
            None
        }
    },
    50: {
        'name': 'comparator',
        'category': 'cv',
        'max_blocks': 3,
        'params': 2,
        'cpu': 0.04,
        'blocks': {
            'cv_positive_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'cv_negative_input': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            'output': ['0 to 1', '-1 to 1']
        }
    },
    51: {
        'name': 'cv_rectify',
        'category': 'cv',
        'max_blocks': 2,
        'params': 1,
        'cpu': 0.02,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            }
        },
        'options': {
            None
        }
    },
    52: {
        'name': 'trigger',
        'category': 'cv',
        'max_blocks': 2,
        'params': 1,
        'cpu': 0.1,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            }
        },
        'options': {
            None
        }
    },
    53: {
        'name': 'stereo_spread',
        'category': 'audio',
        'max_blocks': 5,
        'params': 1,
        'cpu': 2,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            },
            'delay_time': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'side_gain': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': [2-3]
            },
            'audio_out_R': {
                'isDefault': True,
                'isParam': False,
                'position': [3-4]
            }
        },
        'options': {
            'method': ['mid_side', 'haas']
        }
    },
    54: {
        'name': 'cport_exp_cv_in',
        'category': 'interface',
        'max_blocks': 1,
        'params': 0,
        'cpu': 0.1,
        'blocks': {
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            }
        },
        'options': {
            'output_range': ['0 to 1', '-1 to 1']
        }
    },
    55: {
        'name': 'cport_cv_out',
        'category': 'interface',
        'max_blocks': 1,
        'params': 0,
        'cpu': 0.2,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            }
        },
        'options': {
            'input_range': ['0 to 1', '-1 to 1']
        }
    },
    56: {
        'name': 'ui_button',
        'category': 'interface',
        'max_blocks': 2,
        'params': 1,
        'cpu': 0.04,
        'blocks': {
            'in': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'cv_output': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            }
        },
        'options': {
            None
        }
    },
    57: {
        'name': 'audio_panner',
        'category': 'audio',
        'max_blocks': 5,
        'params': 3,
        'cpu': 1,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'pan': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 3
            },
            'audio_out_R': {
                'isDefault': True,
                'isParam': False,
                'position': 4
            }
        },
        'options': {
            'channels': ['1in->2out', '2in->2out'],
            'pan_type': ['equal_pwr', '-4.5dB', 'linear']
        }
    },
    58: {
        'name': 'pitch_detector',
        'category': 'analysis',
        'max_blocks': 2,
        'params': 0,
        'cpu': 2.5,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            }
        },
        'options': {
            None
        }
    },
    59: {
        'name': 'pitch_shifter',
        'category': 'audio',
        'max_blocks': 3,
        'params': 1,
        'cpu': 15.5,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'pitch_shift': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            None
        }
    },
    60: {
        'name': 'midi_note_out',
        'category': 'interface',
        'max_blocks': 3,
        'params': 3,
        'cpu': 0.1,
        'blocks': {
            'note_in': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'gate_in': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'velocity_out': {
                'isDefault': False,
                'isParam': True,
                'position': 2
            }
        },
        'options': {
            'midi_channel': [1-16],
            'velocity_output': ['off', 'on']
        }
    },
    61: {
        'name': 'midi_cc_out',
        'category': 'interface',
        'max_blocks': 1,
        'params': 1,
        'cpu': 0.2,
        'blocks': {
            'cc_out': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            }
        },
        'options': {
            'midi_channel': [1-16],
            'controller': [0-127]
        }
    },
    62: {
        'name': 'midi_pc_out',
        'category': 'interface',
        'max_blocks': 2,
        'params': 2,
        'cpu': 0.1,
        'blocks': {
            'pc_out': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'trigger_in': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            }
        },
        'options': {
            'midi_channel': [1-16]
        }
    },
    63: {
        'name': 'bit_modulator',
        'category': 'audio',
        'max_blocks': 3,
        'params': 0,
        'cpu': 1.2,
        'blocks': {
            'audio_in_1': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_2': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            }
        },
        'options': {
            'type': ['xor', 'and', 'or']
        }
    },
    64: {
        'name': 'audio_balance',
        'category': 'audio',
        'max_blocks': 6,
        'params': 1,
        'cpu': 1.7,
        'blocks': {
            'audio_in_1_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_1_R': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            },
            'audio_in_2_L': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            },
            'audio_in_2_R': {
                'isDefault': True,
                'isParam': False,
                'position': 3
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': [2, 4]
            },
            'audio_output_L': {
                'isDefault': True,
                'isParam': False,
                'position': [3, 5]
            },
            'audio_output_R': {
                'isDefault': True,
                'isParam': False,
                'position': 6
            }
        },
        'options': {
            'stereo': ['mono', 'stereo']
        }
    },
    65: {
        'name': 'inverter',
        'category': 'audio',
        'max_blocks': 2,
        'params': 0,
        'cpu': 0.3,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            }
        },
        'options': {
            None
        }
    },
    66: {
        'name': 'fuzz',
        'category': 'effect',
        'max_blocks': 4,
        'params': 2,
        'cpu': 16,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'input_gain': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'output_gain': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 3
            }
        },
        'options': {
            'model': ['efuzzy', 'burly', 'scoopy', 'ugly']
        }
    },
    67: {
        'name': 'ghostverb',
        'category': 'effect',
        'max_blocks': 8,
        'params': 4,
        'cpu': 45,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'decay_feedback': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'rate': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'resonance': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 6
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 7
            }
        },
        'options': {
            'channels': ['1in->1out', '1in->2out', 'stereo']
        }
    },
    68: {
        'name': 'cabinet_sim',
        'category': 'effect',
        'max_blocks': 4,
        'params': 0,
        'cpu': 10,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 2
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 3
            }
        },
        'options': {
            'channels': ['mono', 'stereo'],
            'type': ['4x12_full', '2x12_dark', '2x12_modern', '1x12',
                     '1x8_lofi', '1x12_vintage', '4x12_hifi']
        }
    },
    69: {
        'name': 'flanger',
        'category': 'effect',
        'max_blocks': 9,
        'params': 5,
        'cpu': 11,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'control_in': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'regen': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'width': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'tone_tilt_eq': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 6
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 7
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 8
            }
        },
        'options': {
            'channels': ['1in->1out', '1in->2out', 'stereo'],
            'control': ['rate', 'tap_tempo', 'cv_direct'],
            'type': ['1960s', '1970s', 'thru_0']
        }
    },
    70: {
        'name': 'chorus',
        'category': 'effect',
        'max_blocks': 8,
        'params': 4,
        'cpu': 13,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'control_in': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'width': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'tone_tilt_eq': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 6
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 7
            }
        },
        'options': {
            'channels': ['1in->1out', '1in->2out', 'stereo'],
            'control': ['rate', 'tap_tempo', 'cv_direct'],
            'type': ['classic']
        }
    },
    71: {
        'name': 'vibrato',
        'category': 'effect',
        'max_blocks': 6,
        'params': 2,
        'cpu': 5,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'control_in': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'width': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 4
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 5
            }
        },
        'options': {
            'channels': ['1in->1out', '1in->2out', 'stereo'],
            'control': ['rate', 'tap_tempo', 'cv_direct'],
            'waveform': ['sine', 'triangle', 'swung_sine', 'swung']
        }
    },
    72: {
        'name': 'env_filter',
        'category': 'effect',
        'max_blocks': 8,
        'params': 4,
        'cpu': 7,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'sensitivity': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'min_freq': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'max_freq': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'filter_q': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 6
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 7
            }
        },
        'options': {
            'channels': ['1in->1out', '1in->2out', 'stereo'],
            'control': ['rate', 'tap_tempo', 'cv_direct'],
            'direction': ['up', 'down']
        }
    },
    73: {
        'name': 'ring_modulator',
        'category': 'effect',
        'max_blocks': 5,
        'params': 3,
        'cpu': 14,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'frequency': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'ext_in': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'duty_cycle': {
                'isDefault': False,
                'isParam': True,
                'position': 2
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 4
            }
        },
        'options': {
            'waveform': ['since', 'square', 'triangle', 'sawtooth'],
            'ext_audio_in': ['off', 'on'],
            'duty_cycle': ['off', 'on'],
            'upsampling': ['none', '2x']
        }
    },
    74: {
        'name': 'hall_reverb',
        'category': 'effect',
        'max_blocks': 8,
        'params': 4,
        'cpu': 22,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            },
            'decay_time': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'low_eq': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'lpf_freq': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 6
            },
            'audio_out_R': {
                'isDefault': True,
                'isParam': False,
                'position': 7
            }
        },
        'options': {
            None
        }
    },
    75: {
        'name': 'ping_pong_delay',
        'category': 'effect',
        'max_blocks': 9,
        'params': 5,
        'cpu': 18,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'delay_time': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'feedback': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'mod_rate': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'mod_depth': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 6
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 7
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 8
            }
        },
        'options': {
            'channels': ['1in->1out', 'stereo'],
            'control': ['rate', 'tap_tempo', 'cv_direct'],
            'type': ['clean', 'tape', 'old_tape', 'bbd'],
            'tap_ratio': ['1:1', '2:3', '1:2', '1:3', '3:8', '1:4',
                          '3:16', '1:8', '1:16', '1:32']
        }
    },
    76: {
        'name': 'audio_mixer',
        'category': 'audio',
        'max_blocks': 34,
        'params': 16,
        'cpu': [3-20],
        'blocks': {
            'audio_in_1_L': {
                'isDefault': True,
                'isParam': False,
                'position': [0, 4, 8, 12, 16, 20, 24]
            },
            'audio_in_1_R': {
                'isDefault': False,
                'isParam': False,
                'position': [1, 5, 9, 13, 17, 21, 25]
            },
            'audio_in_2_L': {
                'isDefault': True,
                'isParam': False,
                'position': [2, 6, 10, 14, 18, 22, 26]
            },
            'audio_in_2_R': {
                'isDefault': False,
                'isParam': False,
                'position': [3, 7, 11, 15, 19, 23, 27]
            },
            'gain_1': {
                'isDefault': True,
                'isParam': True,
                'position': 28
            },
            'gain_2': {
                'isDefault': True,
                'isParam': True,
                'position': 29
            },
            'pan_1': {
                'isDefault': False,
                'isParam': True,
                'position': 30
            },
            'pan_2': {
                'isDefault': False,
                'isParam': True,
                'position': 31
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 32
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 33
            }
        },
        'options': {
            'channels': [2-8],
            'stereo': ['mono', 'stereo'],
            'panning': ['off', 'on']
        }
    },
    77: {
        'name': 'cv_flip_flop',
        'category': 'cv',
        'max_blocks': 2,
        'params': 1,
        'cpu': 0.2,
        'blocks': {
            'cv_input': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            },
            'cv_output': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            }
        },
        'options': {
            None
        }
    },
    78: {
        'name': 'diffuser',
        'category': 'audio',
        'max_blocks': 6,
        'params': 4,
        'cpu': 2,
        'blocks': {
            'audio_in': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'gain': {
                'isDefault': True,
                'isParam': True,
                'position': 1
            },
            'size': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'mod_width': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'mod_rate': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'audio_out': {
                'isDefault': True,
                'isParam': False,
                'position': 5
            }
        },
        'options': {
            None
        }
    },
    79: {
        'name': 'reverb_lite',
        'category': 'effect',
        'max_blocks': 6,
        'params': 2,
        'cpu': 10,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'decay_time': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 4
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 5
            }
        },
        'options': {
            'channels': ['1in->1out', '1in->2out', 'stereo']
        }
    },
    80: {
        'name': 'room_reverb',
        'category': 'effect',
        'max_blocks': 8,
        'params': 4,
        'cpu': 22,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': True,
                'isParam': False,
                'position': 1
            },
            'decay_time': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'low_eq': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'lpf_freq': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'mix': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 6
            },
            'audio_out_R': {
                'isDefault': True,
                'isParam': False,
                'position': 7
            }
        },
        'options': {
            None
        }
    },
    81: {
        'name': 'pixel',
        'category': 'interface',
        'max_blocks': 1,
        'params': 1,
        'cpu': 0.01,
        'blocks': {
            'cv_audio_in': {
                'isDefault': True,
                'isParam': True,
                'position': 0
            }
        },
        'options': {
            'control': ['cv', 'audio']
        }
    },
    82: {
        'name': 'midi_clock_in',
        'category': 'interface',
        'max_blocks': 4,
        'params': 0,
        'cpu': 0.1,
        'blocks': {
            'cc_value': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'clock_out': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'run_out': {
                'isDefault': False,
                'isParam': False,
                'position': 2
            },
            'divider': {
                'isDefault': False,
                'isParam': False,
                'position': 3
            }
        },
        'options': {
            'clock_out': ['disabled', 'enabled'],
            'run_out': ['disabled', 'enabled'],
            'divider': ['disabled', 'enabled'],
            'channel': [1-11]
        }
    },
    83: {
        'name': 'granular',
        'category': 'audio',
        'max_blocks': 10,
        'params': 6,
        'cpu': 8,
        'blocks': {
            'audio_in_L': {
                'isDefault': True,
                'isParam': False,
                'position': 0
            },
            'audio_in_R': {
                'isDefault': False,
                'isParam': False,
                'position': 1
            },
            'grain_size': {
                'isDefault': True,
                'isParam': True,
                'position': 2
            },
            'grain_position': {
                'isDefault': True,
                'isParam': True,
                'position': 3
            },
            'density': {
                'isDefault': True,
                'isParam': True,
                'position': 4
            },
            'texture': {
                'isDefault': True,
                'isParam': True,
                'position': 5
            },
            'speed_pitch': {
                'isDefault': True,
                'isParam': True,
                'position': 6
            },
            'freeze': {
                'isDefault': True,
                'isParam': True,
                'position': 7
            },
            'audio_out_L': {
                'isDefault': True,
                'isParam': False,
                'position': 8
            },
            'audio_out_R': {
                'isDefault': False,
                'isParam': False,
                'position': 9
            }
        },
        'options': {
            'num_grains': [1-8],
            'channels': ['mono', 'stereo'],
            'pos_control': ['cv', 'tap_tempo'],
            'size_control': ['cv', 'tap_tempo']
        }
    },
    84: [
        'midi_clock_out',
        'interface',
        5,
        5,
        [2, 2, 2, 2],
        ['tap', 'enabled', 'enabled', 'disabled'],
        0.3
    ],
    85: [
        'tap_to_cv',
        'cv',
        4,
        2,
        [2, 2],
        ['40hz', 'linear'],
        0.1
    ]
}
