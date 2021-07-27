from zoia_lib.backend.zoia_module import ZoiaModule


class SVFilter(ZoiaModule):
    def __init__(self, version):
        self.module_id = 0
        self.name = "SV Filter"
        self.version = version
        self.category = "Audio"
        self.description = """
            The State Variable Filter will resonate and cutoff around a set frequency.
            """
        self.default_blocks = 4
        self.min_blocks = 3
        self.max_blocks = 6
        self.params = 2
        self.cpu = 3
        self.version_properties = {
            "0": {
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
                }
            }
        }
        self.blocks = self.version_properties[str(version)]["blocks"]
        self.options = self.version_properties[str(version)]["options"]
        self.saveable_data = {}
        super().__init__()

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0], d[1], d[2]]
        for i, j in zip(opt, range(3, 6)):
            if i[1] == "on":
                blocks.append(d[j])

        return blocks


class AudioInput(ZoiaModule):
    def __init__(self, version):
        self.module_id = 1
        self.name = "Audio Input"
        self.version = version
        self.category = "Interface"
        self.description = """
            Connect audio from the outside world into the grid.
            This could be a guitar, bass, synth module, computer Audio, etc
            """
        self.default_blocks = 2
        self.min_blocks = 1
        self.max_blocks = 2
        self.params = 0
        self.cpu = 0.4
        self.blocks = {
            "output_L": {"isDefault": True, "isParam": False, "position": 0},
            "output_R": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {"channels": ["stereo", "left", "right"]}
        self.saveable_data = {}
        super.__init__()

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        if opt[0][1] == "left":
            blocks = [d[0]]
        elif opt[0][1] == "right":
            blocks = [d[1]]
        else:
            blocks = [d[0], d[1]]

        return blocks


class AudioOutput(ZoiaModule):
    def __init__(self, version):
        self.module_id = 2
        self.name = "Audio Output"
        self.version = version
        self.category = "Interface"
        self.description = """
            Connect audio from your ZOIA into the outside world.
            Connect to your amplifier, a DI box, your audio interface, etc.
            An optional gain control lets you tweak the output level.
            """
        self.default_blocks = 2
        self.min_blocks = 1
        self.max_blocks = 3
        self.params = 1
        self.cpu = 1.7
        self.blocks = {
            "input_L": {"isDefault": True, "isParam": False, "position": 0},
            "input_R": {"isDefault": True, "isParam": False, "position": 1},
            "gain": {"isDefault": False, "isParam": True, "position": 2},
        }
        self.options = {
            "gain_control": ["off", "on"],
            "channels": ["stereo", "left", "right"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        if opt[1][1] == "left":
            blocks = [d[0]]
        elif opt[1][1] == "right":
            blocks = [d[1]]
        else:
            blocks = [d[0], d[1]]
        if opt[0][1] == "on":
            blocks.append(d[2])

        return blocks


class Aliaser(ZoiaModule):
    def __init__(self, version):
        self.module_id = 3
        self.name = "Aliaser"
        self.version = version
        self.category = "Audio"
        self.description = """
            Aliaser produces samples of incoming audio and compares them against each other to find imperfections.
            These imperfections become the outgoing audio.
            As sample count grows, so too does the thickness of the outgoing sound.
            This effect is a signal hog so be sure to boost your connection strengths incoming and outgoing.
            Try connecting a LFO or envelope follower to the alias amount.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 3
        self.params = 1
        self.cpu = 0.7
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "#_of_samples": {"isDefault": True, "isParam": True, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Sequencer(ZoiaModule):
    def __init__(self, version):
        self.module_id = 4
        self.name = "Sequencer"
        self.version = version
        self.category = "CV"
        self.description = """
            The sequencer allows you to create a number of \steps\ (1-32) that can be cycled through,
            and each step can be used to send a CV value out of that tracks output.
            The sequencer can have up to 8 tracks, each with their own unique output.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 42
        self.params = 34
        self.cpu = 2
        self.blocks = {
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
        }
        self.options = {
            "number_of_steps": list(range(1, 33)),
            "num_of_tracks": list(range(1, 9)),
            "restart_jack": ["off", "on"],
            "behavior": ["loop", "once"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = []
        for i in range(1, int(opt[0][1]) + 1):
            blocks.append(d[i - 1])
        blocks.append(d[32])
        if opt[2][1] == "on":
            blocks.append(d[33])
        for i in range(1, int(opt[1][1]) + 1):
            blocks.append(d[i + 33])

        return blocks


class LFO(ZoiaModule):
    def __init__(self, version):
        self.module_id = 5
        self.name = "LFO"
        self.version = version
        self.category = "CV"
        self.description = """
            The Low Frequency Oscillator is one of the workhorse modules of the ZOIA.
            This will generate CV in the waveform and range of your choosing.
            Connect it to a sequencer to cycle through steps, to an audio effect to
            swing it's parameters around, or to any outboard piece of gear through a
            MIDI or CV interface module.
            The connection strength you enter at the output will determine the maximum
            sweep of the LFO.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 5
        self.params = 4
        self.cpu = 0.3
        self.blocks = {
            "cv_control": {"isDefault": True, "isParam": True, "position": 0},
            "tap_control": {"isDefault": False, "isParam": True, "position": 1},
            "swing_amount": {"isDefault": False, "isParam": True, "position": 2},
            "phase_input": {"isDefault": False, "isParam": True, "position": 4},
            "phase_reset": {"isDefault": False, "isParam": True, "position": 5},
            "output": {"isDefault": True, "isParam": False, "position": 3},
        }
        self.options = {
            "waveform": ["square", "sine", "triangle", "sawtooth", "ramp", "random"],
            "swing_control": ["off", "on"],
            "output": ["0 to 1", "-1 to 1"],
            "input": ["cv", "tap", "linear_cv"],
            "phase_input": ["off", "on"],
            "phase_reset": ["off", "on"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = []
        if opt[3][1] != "tap":
            blocks.append(d[0])
        else:
            blocks.append(d[1])
        if opt[1][1] == "on":
            blocks.append(d[2])
        if opt[4][1] == "on":
            blocks.append(d[3])
        if opt[5][1] == "on":
            blocks.append(d[4])
        blocks.append(d[5])

        return blocks


class ADSR(ZoiaModule):
    def __init__(self, version):
        self.module_id = 6
        self.name = "ADSR"
        self.version = version
        self.category = "CV"
        self.description = """
            The Attack Decay Sustain Release module is what gives a note generated
            from an oscillator a natural sounding envelope when played from a keyboard.
            Connect your oscillator or other audio source to the input of a VCA,
            and connect the CV output of the ADSR to the CV input on the VCA.
            Connect the keyboard or MIDI note gate out to the CV input of the ADSR
            and you've got yourself a simple synthesizer!
            Tweak the values to taste, or connect them to other CV inputs for experimentation.
            Use the optional retrigger input to restart the envelope around a note
            that is played before the ADSR is released.
            """
        self.default_blocks = 6
        self.min_blocks = 4
        self.max_blocks = 10
        self.params = 9
        self.cpu = 0.07
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "retrigger": {"isDefault": False, "isParam": True, "position": 1},
            "delay": {"isDefault": False, "isParam": True, "position": 2},
            "attack": {"isDefault": True, "isParam": True, "position": 3},
            "hold_attack_decay": {"isDefault": False, "isParam": True, "position": 4},
            "decay": {"isDefault": True, "isParam": True, "position": 5},
            "sustain": {"isDefault": True, "isParam": True, "position": 6},
            "hold_sustain_release": {
                "isDefault": False,
                "isParam": True,
                "position": 7,
            },
            "release": {"isDefault": True, "isParam": True, "position": 8},
            "cv_output": {"isDefault": True, "isParam": False, "position": 9},
        }
        self.options = {
            "retrigger_input": ["off", "on"],
            "initial_delay": ["off", "on"],
            "hold_attack_decay": ["off", "on"],
            "str": ["on", "off"],
            "immediate_release": ["on", "off"],
            "hold_sustain_release": ["off", "on"],
            "time_scale": ["exponent", "linear"],
        }
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "on":
            blocks.append(d[1])
        if opt[1][1] == "on":
            blocks.append(d[2])
        blocks.append(d[3])
        if opt[2][1] == "on":
            blocks.append(d[4])
        blocks.append(d[5])
        if opt[3][1] == "on":
            blocks.append(d[6])
        if opt[5][1] == "on":
            blocks.append(d[7])
        if opt[3][1] == "on":
            blocks.append(d[8])
        blocks.append(d[9])

        return blocks


class VCA(ZoiaModule):
    def __init__(self, version):
        self.module_id = 7
        self.name = "VCA"
        self.version = version
        self.category = "Audio"
        self.description = """
            The Voltage Controlled Amplifier module will interpret incoming CV at the
            level control and boost or cut the volume.
            Connect an ADSR to create a natural sounding envelope for an oscillator passing through.
            Connect an LFO to create a tremolo effect.
            Or connect an expression pedal module or MIDI input for an external volume control.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 5
        self.params = 1
        self.cpu = 0.7
        self.blocks = {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_2": {"isDefault": False, "isParam": False, "position": 1},
            "level_control": {"isDefault": True, "isParam": True, "position": 2},
            "audio_out_1": {"isDefault": True, "isParam": False, "position": 3},
            "audio_out_2": {"isDefault": False, "isParam": False, "position": 4},
        }
        self.options = {"channels": ["1in->1out", "stereo"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "stereo":
            blocks.append(d[1])
        blocks.append(d[2])
        blocks.append(d[3])
        if opt[0][1] == "stereo":
            blocks.append(d[4])

        return blocks


class AudioMultiply(ZoiaModule):
    def __init__(self, version):
        self.module_id = 8
        self.name = "Audio Multiply"
        self.version = version
        self.category = "Audio"
        self.description = """
            Takes one audio input and mathematically multiplies it with the other.
            This produces a ring mod/vocoder-like effect.
            This module likes hot signals to be sure to bump the connection strengths.
            Remember that silence at any one of the inputs will result in silence at the output!
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 3
        self.params = 0
        self.cpu = 0.4
        self.blocks = {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_2": {"isDefault": True, "isParam": False, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class BitCrusher(ZoiaModule):
    def __init__(self, version):
        self.module_id = 9
        self.name = "Bit Crusher"
        self.version = version
        self.category = "Audio"
        self.description = """
            Bit Crusher produces distortion by reducing audio bandwidth by a set number of bits.
            Distortion becomes audible around 20 bits reduced.
            This effect can get noisy so try it with a gate.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 3
        self.params = 1
        self.cpu = 1
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "crushed_bits": {"isDefault": True, "isParam": True, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {"fractions": ["off", "on"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class SampleandHold(ZoiaModule):
    def __init__(self, version):
        self.module_id = 10
        self.name = "Sample and Hold"
        self.version = version
        self.category = "CV"
        self.description = """
            Sample and Hold will take the CV value at the input and hold it in place
            at the output until triggered to look again at the input and update the output.
            Connect a LFO to the trigger to convert smooth changes in CV into stepped changes in CV.
            The speed of the LFO will determine the perceived resolution of the CV output.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 3
        self.params = 2
        self.cpu = 0.1
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "trigger": {"isDefault": True, "isParam": True, "position": 1},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {"track & hold": ["off", "on"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class ODandDistortion(ZoiaModule):
    def __init__(self, version):
        self.module_id = 11
        self.name = "OD and Distortion"
        self.version = version
        self.category = "Effect"
        self.description = """
            The OD & Distortion module provides classic overdrive and distortion tones.
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 4
        self.params = 2
        self.cpu = 17
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "input_gain": {"isDefault": True, "isParam": True, "position": 1},
            "output_gain": {"isDefault": True, "isParam": True, "position": 3},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {"model": ["plexi", "germ", "classic", "pushed", "edgy"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class EnvFollower(ZoiaModule):
    def __init__(self, version):
        self.module_id = 12
        self.name = "Env Follower"
        self.version = version
        self.category = "Analysis"
        self.description = """
            Envelope Follower will interpret an incoming audio signal as a CV signal
            based on its signal strength.
            Use this to trigger filter sweeps, audio effects parameters, LFO rates, etc.
            The connection strength can act as a sensitivity control.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 4
        self.params = 2
        self.cpu = 5
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "rise_time": {"isDefault": False, "isParam": True, "position": 1},
            "fall_time": {"isDefault": False, "isParam": True, "position": 2},
            "cv_output": {"isDefault": True, "isParam": False, "position": 3},
        }
        self.options = {
            "rise_fall_time": ["off", "on"],
            "output_scale": ["log", "linear"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "on":
            blocks.append(d[1])
            blocks.append(d[2])
        blocks.append(d[3])

        return blocks


class DelayLine(ZoiaModule):
    def __init__(self, version):
        self.module_id = 13
        self.name = "Delay Line"
        self.version = version
        self.category = "Audio"
        self.description = """
            The Delay Line is a simple module that takes audio at the input and
            delays it by a set amount of time.
            There is no dry signal, there are no repeats.
            You can create repeats by connecting the output back to the input,
            using the connection strength to adjust number of repeats.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 4
        self.params = 3
        self.cpu = 3
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "delay_time": {"isDefault": True, "isParam": True, "position": 1},
            "modulation_in": {"isDefault": False, "isParam": True, "position": 2},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3},
            "audio_out": {"isDefault": True, "isParam": False, "position": 4},
        }
        self.options = {
            "max_time": ["1s", "2s", "4s", "8s", "16s", "100ms"],
            "tap_tempo_in": ["no", "yes"],
            "interpolation": ["on", "off"],
            "CV Input": ["exponent", "linear"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[1][1] == "yes":
            blocks.append(d[2])
            blocks.append(d[3])
        else:
            blocks.append(d[1])
        blocks.append(d[4])

        return blocks


class Oscillator(ZoiaModule):
    def __init__(self, version):
        self.module_id = 14
        self.name = "Oscillator"
        self.version = version
        self.category = "Audio"
        self.description = """
            Generates an audio signal in the waveform of your choice.
            Connect a MIDI device, keyboard module, sequencer, pitch detector,
            LFO, or any CV source to select the frequency or note the oscillator will play.
            You can modulate the frequency or pulse width with the optional parameters.
            Negative CV inputs (from -1 to 0) will generate sub-bass frequencies
            between 0.027Hz and 27.49Hz. Be careful!
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 4
        self.params = 2
        self.cpu = 10
        self.blocks = {
            "frequency": {"isDefault": True, "isParam": True, "position": 0},
            "fm_input": {"isDefault": False, "isParam": False, "position": 1},
            "duty_cycle": {"isDefault": False, "isParam": True, "position": 2},
            "audio_out": {"isDefault": True, "isParam": False, "position": 3},
        }
        self.options = {
            "waveform": ["sine", "square", "triangle", "sawtooth"],
            "fm_in": ["off", "on"],
            "duty_cycle": ["off", "on"],
            "upsampling": ["none", "2x"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[1][1] == "on":
            blocks.append(d[1])
        if opt[2][1] == "on":
            blocks.append(d[2])
        blocks.append(d[3])

        return blocks


class Pushbutton(ZoiaModule):
    def __init__(self, version):
        self.module_id = 15
        self.name = "Pushbutton"
        self.version = version
        self.category = "Interface"
        self.description = """
            Turns a grid button into a button you can push to send a CV signal.
            Tap in a tempo, open up a VCA, trigger a sequencer, or anything else.
            The grid is your oyster!
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 1
        self.params = 0
        self.cpu = 0.02
        self.blocks = {
            "cv_output": {"isDefault": True, "isParam": False, "position": 1}
        }
        self.options = {
            "action": ["momentary", "latching"],
            "normally": ["zero", "one"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Keyboard(ZoiaModule):
    def __init__(self, version):
        self.module_id = 16
        self.name = "Keyboard"
        self.version = version
        self.category = "Interface"
        self.description = """
            Turns grid buttons into a keyboard you can connect to an oscillator and play.
            No external MIDI controller necessary!
            Tune each keyboard button using the knob to have it play your desired note.
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 43
        self.params = 40
        self.cpu = 0.1
        self.blocks = {
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
        }
        self.options = {"#_of_notes": list(range(1, 41))}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = []
        for i in range(1, opt[0][1] + 1):
            blocks.append(d[i - 1])
        blocks.append(d[40])
        blocks.append(d[41])
        blocks.append(d[42])

        return blocks


class CVInvert(ZoiaModule):
    def __init__(self, version):
        self.module_id = 17
        self.name = "CV Invert"
        self.version = version
        self.category = "CV"
        self.description = """
            Inverts the incoming CV.
            For example, a CV input of 1 will output as -1.
            An input of 0.2 will output as -0.2.                """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 2
        self.params = 1
        self.cpu = 0.02
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Steps(ZoiaModule):
    def __init__(self, version):
        self.module_id = 18
        self.name = "Steps"
        self.version = version
        self.category = "CV"
        self.description = """
            Steps will interpret incoming changes in upward CV as a tempo, split the wave
            cycle into a set number of steps, and then send the CV present at the input
            during each step to the output.
            You can use this to convert a nice smooth LFO and reduce its resolution into steps.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 3
        self.params = 2
        self.cpu = 0.7
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "quant_steps": {"isDefault": True, "isParam": True, "position": 1},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class SlewLimiter(ZoiaModule):
    def __init__(self, version):
        self.module_id = 19
        self.name = "Slew Limiter"
        self.version = version
        self.category = "CV"
        self.description = """
            Slew Limiter is similar in behaviour to CV Filter except that the rate of
            change in changes of CV happen linearly instead of logarithmically.
            This is the classic portamento, and can be used anywhere CV changes occur
            to give them a different feel.
            Try using an unlinked Slew Limiter with a stomp switch module to give more
            expression pedal-like behaviour to your stomp switch.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 4
        self.params = 2
        self.cpu = 0.2
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "slew_rate": {"isDefault": True, "isParam": True, "position": 1},
            "rising_lag": {"isDefault": False, "isParam": True, "position": 2},
            "falling_lag": {"isDefault": False, "isParam": True, "position": 3},
            "cv_output": {"isDefault": True, "isParam": False, "position": 4},
        }
        self.options = {"control": ["linked", "separate"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "linked":
            blocks.append(d[1])
        else:
            blocks.append(d[2])
            blocks.append(d[3])
        blocks.append(d[4])

        return blocks


class MidiNotesIn(ZoiaModule):
    def __init__(self, version):
        self.module_id = 20
        self.name = "Midi Notes In"
        self.version = version
        self.category = "Interface"
        self.description = """
            Connect your MIDI keyboard controller to the ZOIA.
            Connect the note out to an oscillator to have it play your note,
            and connect the gate out to an ADSR (connected to a VCA) for a natural envelope. 
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 32
        self.params = 0
        self.cpu = 0.3
        self.blocks = {
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
        }
        self.options = {
            "midi_channel": list(range(1, 17)),
            "#_of_outputs": list(range(1, 9)),
            "priority": ["newest", "oldest", "highest", "lowest", "RoundRobin"],
            "greedy": ["no", "yes"],
            "velocity_output": ["off", "on"],
            "low_note": list(range(0, 128)),
            "high_note": list(range(0, 128))[::-1],
            "trigger_pulse": ["off", "on"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = []
        for i in range(1, opt[1][1] + 1):
            blocks.append(d[4 * (i - 1)])
            blocks.append(d[4 * (i - 1) + 1])
            if opt[4][1] == "on":
                blocks.append(d[4 * (i - 1) + 2])
            if opt[7][1] == "on":
                blocks.append(d[4 * (i - 1) + 3])

        return blocks


class MidiCCIn(ZoiaModule):
    def __init__(self, version):
        self.module_id = 21
        self.name = "Midi CC In"
        self.version = version
        self.category = "Interface"
        self.description = """
            Connect encoder knobs and sliders on a MIDI interface.
            Take note of the outgoing CC number of each control and enter it into the controller option.
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 1
        self.params = 0
        self.cpu = 0.1
        self.blocks = {"cc_out": {"isDefault": True, "isParam": False, "position": 0}}
        self.options = {
            "midi_channel": list(range(1, 17)),
            "controller": list(range(0, 128)),
            "output_range": ["0 to 1", "-1 to 1"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Multiplier(ZoiaModule):
    def __init__(self, version):
        self.module_id = 22
        self.name = "Multiplier"
        self.version = version
        self.category = "CV"
        self.description = """
            Multiply will take the CV signal present at each input and multiply
            them together at the output.
            In this way you can use one CV source to amplify, tame, or modulate another.
            Remember that a value of 0 at any input will result in 0 at the output.
            It's math!
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 9
        self.params = 2
        self.cpu = 0.2
        self.blocks = {
            "cv_input_1": {"isDefault": True, "isParam": True, "position": 0},
            "cv_input_2": {"isDefault": True, "isParam": True, "position": 1},
            "cv_input_3": {"isDefault": False, "isParam": True, "position": 2},
            "cv_input_4": {"isDefault": False, "isParam": True, "position": 3},
            "cv_input_5": {"isDefault": False, "isParam": True, "position": 4},
            "cv_input_6": {"isDefault": False, "isParam": True, "position": 5},
            "cv_input_7": {"isDefault": False, "isParam": True, "position": 6},
            "cv_input_8": {"isDefault": False, "isParam": True, "position": 7},
            "cv_output": {"isDefault": True, "isParam": False, "position": 8},
        }
        self.options = {"num_inputs": list(range(2, 9))}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        for i in range(2, opt[0][1] + 1):
            blocks.append(d[i - 1])
        blocks.append(d[8])

        return blocks


class Compressor(ZoiaModule):
    def __init__(self, version):
        self.module_id = 23
        self.name = "Compressor"
        self.version = version
        self.category = "Effect"
        self.description = """
            Compression is a vastly useful audio tool that controls your signal level
            according to changes in input level.
            You can create natural reductions in gain to help things mix better, help
            tame or enhance transients in synth or instrument signals, etc.
            The optional stereo side will trigger the module's functions in unison on both
            channels, creating True stereo compression.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 9
        self.params = 4
        self.cpu = 3
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "threshold": {"isDefault": True, "isParam": True, "position": 2},
            "attack": {"isDefault": False, "isParam": True, "position": 3},
            "release": {"isDefault": False, "isParam": True, "position": 4},
            "ratio": {"isDefault": False, "isParam": True, "position": 5},
            "sidechain_in": {"isDefault": False, "isParam": False, "position": 8},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7},
        }
        self.options = {
            "attack_ctrl": ["off", "on"],
            "release_ctrl": ["off", "on"],
            "ratio_ctrl": ["off", "on"],
            "channels": ["1in->1out", "stereo"],
            "sidechain": ["internal", "external"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[3][1] == "stereo":
            blocks.append(d[1])
        blocks.append(d[2])
        if opt[0][1] == "on":
            blocks.append(d[3])
        if opt[1][1] == "on":
            blocks.append(d[4])
        if opt[2][1] == "on":
            blocks.append(d[5])
        if opt[4][1] == "external":
            blocks.append(d[6])
        blocks.append(d[7])
        if opt[3][1] == "stereo":
            blocks.append(d[8])

        return blocks


class MultiFilter(ZoiaModule):
    def __init__(self, version):
        self.module_id = 24
        self.name = "Multi Filter"
        self.version = version
        self.category = "Audio"
        self.description = """
            A general purpose filter with gain, frequency, and Q controls.
            Configurable as a high pass, low pass, band pass, bell, hi shelf, or low shelf.
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 5
        self.params = 3
        self.cpu = 0.8
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "gain": {"isDefault": False, "isParam": True, "position": 1},
            "frequency": {"isDefault": True, "isParam": True, "position": 2},
            "q": {"isDefault": True, "isParam": True, "position": 3},
            "audio_out": {"isDefault": True, "isParam": False, "position": 4},
        }
        self.options = {
            "filter_shape": [
                "lowpass",
                "highpass",
                "bandpass",
                "bell",
                "hi_shelf",
                "low_shelf",
            ]
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] in ["bell", "hi_shelf", "low_shelf"]:
            blocks.append(d[1])
        blocks.append(d[2])
        blocks.append(d[3])
        blocks.append(d[4])

        return blocks


class PlateReverb(ZoiaModule):
    def __init__(self, version):
        self.module_id = 25
        self.name = "Plate Reverb"
        self.version = version
        self.category = "Effect"
        self.description = """
            Bask in the ebb and flow of steel molecules as they vibrate with the warm vintage
            vibe of so many classic recordings.
            """
        self.default_blocks = 8
        self.min_blocks = 8
        self.max_blocks = 8
        self.params = 4
        self.cpu = 22
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": True, "isParam": False, "position": 1},
            "decay_time": {"isDefault": True, "isParam": True, "position": 3},
            "low_eq": {"isDefault": True, "isParam": True, "position": 6},
            "high_eq": {"isDefault": True, "isParam": True, "position": 7},
            "mix": {"isDefault": True, "isParam": True, "position": 2},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 4},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 5},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class BufferDelay(ZoiaModule):
    def __init__(self, version):
        self.module_id = 26
        self.name = "Buffer Delay"
        self.version = version
        self.category = "Audio"
        self.description = """
            Delays internal audio signal by N buffer(s).
            This module is inaudible, but useful anywhere you need to line up
            internal parallel audio connections precisely.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 2
        self.params = 0
        self.cpu = 0.2
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "audio_out": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {"buffer_length": list(range(0, 17))}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class AllPassFilter(ZoiaModule):
    def __init__(self, version):
        self.module_id = 27
        self.name = "All Pass Filter"
        self.version = version
        self.category = "Audio"
        self.description = """
            All Pass Filter passes through all frequencies at equal gain,
            but changes phase relationship between them.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 3
        self.params = 1
        self.cpu = 5
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "filter_gain": {"isDefault": True, "isParam": True, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {"#_of_poles": [1, 2, 3, 4, 5, 6, 7, 8]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Quantizer(ZoiaModule):
    def __init__(self, version):
        self.module_id = 28
        self.name = "Quantizer"
        self.version = version
        self.category = "CV"
        self.description = """
            Quantizer will interpret incoming CV and send its nearest equivalent note as a CV output.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 4
        self.params = 3
        self.cpu = 1
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "key": {"isDefault": False, "isParam": True, "position": 2},
            "scale": {"isDefault": False, "isParam": True, "position": 3},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {"key_scale_jacks": ["no", "yes"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "yes":
            blocks.append(d[1])
            blocks.append(d[2])
        blocks.append(d[3])

        return blocks


class Phaser(ZoiaModule):
    def __init__(self, version):
        self.module_id = 29
        self.name = "Phaser"
        self.version = version
        self.category = "Effect"
        self.description = """
            Set to stun, Phaser shifts the phase over a set quantity of stages and
            sweeps the frequency of these poles at a set rate.
            An optional stereo channel rounds out the list of features. 
            """
        self.default_blocks = 6
        self.min_blocks = 6
        self.max_blocks = 8
        self.params = 4
        self.cpu = 15
        self.blocks = {
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
        }
        self.options = {
            "channels": ["1in->1out", "1in->2out", "2in->2out"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "number_of_stages": [4, 2, 1, 3, 6, 8],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "2in->2out":
            blocks.append(d[1])
        if opt[1][1] == "rate":
            blocks.append(d[2])
        elif opt[1][1] == "tap_tempo":
            blocks.append(d[3])
        else:
            blocks.append(d[4])
        blocks.append(d[5])
        blocks.append(d[6])
        blocks.append(d[7])
        blocks.append(d[8])
        if opt[0][1] != "1in->1out":
            blocks.append(d[9])

        return blocks


class Looper(ZoiaModule):
    def __init__(self, version):
        self.module_id = 30
        self.name = "Looper"
        self.version = version
        self.category = "Audio"
        self.description = """
            The Looper module allows you to record, overdub, and play back incoming audio,
            forwards or backwards, at the speed of your choice (pitch shifted).
            Get loopy!
            """
        self.default_blocks = 5
        self.min_blocks = 5
        self.max_blocks = 10
        self.params = 6
        self.cpu = 3
        self.blocks = {
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
        }
        self.options = {
            "max_rec_time": ["1s", "2s", "4s", "8s", "16s", "32s"],
            "length_edit": ["off", "on"],
            "playback": ["once", "loop"],
            "length": ["fixed", "pre_speed"],
            "hear_while_rec": ["no", "yes"],
            "play_reverse": ["no", "yes"],
            "overdub": ["no", "yes"],
            "stop_play_button": ["no", "yes"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0], d[1], d[2]]
        if opt[7][1] == "yes":
            blocks.append(d[3])
        blocks.append(d[4])
        if opt[1][1] == "on":
            blocks.append(d[5])
            blocks.append(d[6])
        if opt[5][1] == "yes":
            blocks.append(d[7])
        if opt[6][1] == "yes":
            blocks.append(d[8])
        blocks.append(d[9])

        return blocks


class InSwitch(ZoiaModule):
    def __init__(self, version):
        self.module_id = 31
        self.name = "In Switch"
        self.version = version
        self.category = "CV"
        self.description = """
            In Switch takes a selected quantity of CV inputs and allows you
            to switch between them to a single CV output.
            You can use this to select between LFOs to a CV source, external CV modules,
            or use in conjunction with the CV out switch to choose between ADSRs
            or other CV module chains
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 18
        self.params = 17
        self.cpu = 0.2
        self.blocks = {
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
        }
        self.options = {"num_inputs": list(range(1, 17))}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = []
        for i in range(1, opt[0][1] + 1):
            blocks.append(d[i - 1])
        blocks.append(d[16])
        blocks.append(d[17])

        return blocks


class OutSwitch(ZoiaModule):
    def __init__(self, version):
        self.module_id = 32
        self.name = "Out Switch"
        self.version = version
        self.category = "CV"
        self.description = """
            Out Switch takes a CV input and routes it between a set quantity of CV outputs.
            You can use it to select which sequencers, ADSRs, or tap tempos to send triggers to, etc
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 18
        self.params = 2
        self.cpu = 0.2
        self.blocks = {
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
        }
        self.options = {"num_outputs": list(range(1, 17))}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0], d[1]]
        for i in range(1, opt[0][1] + 1):
            blocks.append(d[i + 1])

        return blocks


class AudioInSwitch(ZoiaModule):
    def __init__(self, version):
        self.module_id = 33
        self.name = "Audio In Switch"
        self.version = version
        self.category = "Audio"
        self.description = """
            Audio In Switch takes a selected quantity of audio inputs and allows you
            to switch between them to a single output.
            You can use this to select between instruments at your input jacks,
            use it in conjunction with the Audio Out Switch to select between
            effects chains, or use it anywhere you'd like to be able to select
            between incoming audio sources using CV.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 18
        self.params = 1
        self.cpu = 0.8
        self.blocks = {
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
        }
        self.options = {
            "num_inputs": list(range(1, 17)),
            "fades": ["on", "off"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = []
        for i in range(1, opt[0][1] + 1):
            blocks.append(d[i - 1])
        blocks.append(d[16])
        blocks.append(d[17])

        return blocks


class AudioOutSwitch(ZoiaModule):
    def __init__(self, version):
        self.module_id = 34
        self.name = "Audio Out Switch"
        self.version = version
        self.category = "Audio"
        self.description = """
            Audio Out Switch takes an audio input and routes it between a set
            quantity of audio outputs.
            You can use it at your output jacks to select between amplifiers
            or mixer channels, use it in conjunction with the Audio In Switch to
            select between effects chains, or use it anywhere you'd like to be able
            to select an outgoing audio path using CV.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 18
        self.params = 1
        self.cpu = 0.7
        self.blocks = {
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
        }
        self.options = {
            "num_outputs": list(range(1, 17)),
            "fades": ["on", "off"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0], d[1]]
        for i in range(1, opt[0][1] + 1):
            blocks.append(d[i + 1])

        return blocks


class MidiPressure(ZoiaModule):
    def __init__(self, version):
        self.module_id = 35
        self.name = "Midi Pressure"
        self.version = version
        self.category = "Interface"
        self.description = """
            Many MIDI keyboards have an aftertouch feature that can be triggered
            by pressing down on a note after it's fully depressed.
            You can use after touch to trigger a little extra pizazz in your sound.
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 1
        self.params = 0
        self.cpu = 0.03
        self.blocks = {
            "channel_pressure": {"isDefault": True, "isParam": False, "position": 0}
        }
        self.options = {"midi_channel": list(range(1, 17))}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class OnsetDetector(ZoiaModule):
    def __init__(self, version):
        self.module_id = 36
        self.name = "Onset Detector"
        self.version = version
        self.category = "Analysis"
        self.description = """
            Onset Detector looks for incoming audio signal and generates a CV trigger at the peaks.
            Use a regular audio source to advance a sequencer, tap a tempo, etc
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 3
        self.params = 1
        self.cpu = 0.7
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "sensitivity": {"isDefault": False, "isParam": True, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {"sensitivity": ["off", "on"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "on":
            blocks.append(d[1])
        blocks.append(d[2])

        return blocks


class Rhythm(ZoiaModule):
    def __init__(self, version):
        self.module_id = 37
        self.name = "Rhythm"
        self.version = version
        self.category = "CV"
        self.description = """
            Rhythm will take an incoming CV signal, interpret it as a series of triggers,
            record those triggers and play them back at the output.
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 5
        self.params = 3
        self.cpu = 0.5
        self.blocks = {
            "rec_start_stop": {"isDefault": True, "isParam": True, "position": 0},
            "rhythm_in": {"isDefault": True, "isParam": True, "position": 1},
            "play": {"isDefault": True, "isParam": True, "position": 2},
            "done_out": {"isDefault": False, "isParam": False, "position": 3},
            "rhythm_out": {"isDefault": True, "isParam": False, "position": 4},
        }
        self.options = {"done_ctrl": ["off", "on"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0], d[1], d[2]]
        if opt[0][1] == "on":
            blocks.append(d[3])
        blocks.append(d[4])

        return blocks


class Noise(ZoiaModule):
    def __init__(self, version):
        self.module_id = 38
        self.name = "Noise"
        self.version = version
        self.category = "Audio"
        self.description = """
            Generates white noise from a single button.
            Use the strength of your connection as a level control.
            Helpful in connection with VCAs and ADSRs in creating drum sounds, etc.
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 1
        self.params = 0
        self.cpu = 0.4
        self.blocks = {
            "audio_out": {"isDefault": True, "isParam": False, "position": 0}
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Random(ZoiaModule):
    def __init__(self, version):
        self.module_id = 39
        self.name = "Random"
        self.version = version
        self.category = "CV"
        self.description = """
            Random will generate numbers continuously or when triggered with the option trigger in.
            Connect an LFO to the trigger in to get regularly updated random numbers.
            Try it with a CV in switch to toggle some randomness into  your life.
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 2
        self.params = 1
        self.cpu = 0.1
        self.blocks = {
            "trigger_in": {"isDefault": False, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {
            "output": ["0 to 1", "-1 to 1"],
            "new_val_on_trig": ["off", "on"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = []
        if opt[1][1] == "on":
            blocks.append(d[0])
        blocks.append(d[1])

        return blocks


class Gate(ZoiaModule):
    def __init__(self, version):
        self.module_id = 40
        self.name = "Gate"
        self.version = version
        self.category = "Effect"
        self.description = """
            A standard in studio audio tools, gate can also be used as the key ingredient
            in gated fuzz tones.
            Use it to filter out noise from an audio source, or to cut the end off
            of a reverb's decay, thus creating the classic gated reverb sound.
            Make sure to experiment with the sidechain input!
            """
        self.default_blocks = 5
        self.min_blocks = 3
        self.max_blocks = 8
        self.params = 3
        self.cpu = 3
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "threshold": {"isDefault": True, "isParam": True, "position": 2},
            "attack": {"isDefault": False, "isParam": True, "position": 3},
            "release": {"isDefault": False, "isParam": True, "position": 4},
            "sidechain_in": {"isDefault": False, "isParam": False, "position": 7},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 5},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 6},
        }
        self.options = {
            "attack_ctrl": ["off", "on"],
            "release_ctrl": ["off", "on"],
            "channels": ["1in->1out", "stereo"],
            "sidechain": ["internal", "external"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[2][1] == "stereo":
            blocks.append(d[1])
        blocks.append(d[2])
        if opt[0][1] == "on":
            blocks.append(d[3])
        if opt[1][1] == "on":
            blocks.append(d[4])
        if opt[3][1] == "external":
            blocks.append(d[5])
        blocks.append(d[6])
        if opt[2][1] == "stereo":
            blocks.append(d[7])

        return blocks


class Tremolo(ZoiaModule):
    def __init__(self, version):
        self.module_id = 41
        self.name = "Tremolo"
        self.version = version
        self.category = "Effect"
        self.description = """
            Up and down, side to side.
            Tremolo helps your smile get wide.
            Set speed and depth and tap in a tempo if you like.
            If you'd like a tremolo effect with more control, try creating one using
            the VCA or Audio Panner along with LFOs and various other CV tools to get radical!
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 6
        self.params = 2
        self.cpu = 2
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "rate": {"isDefault": True, "isParam": True, "position": 2},
            "tap_tempo_in": {"isDefault": False, "isParam": True, "position": 3},
            "direct": {"isDefault": False, "isParam": True, "position": 4},
            "depth": {"isDefault": True, "isParam": True, "position": 5},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7},
        }
        self.options = {
            "channels": ["1in->1out", "1in->2out", "2in->2out"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "waveform": ["fender-ish", "vox-ish", "triangle", "sine", "square"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "2in->2out":
            blocks.append(d[1])
        if opt[1][1] == "rate":
            blocks.append(d[2])
        elif opt[1][1] == "tap_tempo":
            blocks.append(d[3])
        else:
            blocks.append(d[4])
        blocks.append(d[5])
        blocks.append(d[6])
        if opt[0][1] != "1in-1out":
            blocks.append(d[7])

        return blocks


class ToneControl(ZoiaModule):
    def __init__(self, version):
        self.module_id = 42
        self.name = "Tone Control"
        self.version = version
        self.category = "Effect"
        self.description = """
            Tone Control is a 3 or 4 band tone control.
            Use this in conjunction with Distortion, Delay w/Mod, Reverb, or even
            a clean sound to fundamentally change its character.
            """
        self.default_blocks = 6
        self.min_blocks = 6
        self.max_blocks = 10
        self.params = 6
        self.cpu = 5
        self.blocks = {
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
        }
        self.options = {"channels": ["1in->1out", "stereo"], "num_mid_bands": [1, 2]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "stereo":
            blocks.append(d[1])
        blocks.append(d[2])
        blocks.append(d[3])
        blocks.append(d[4])
        if opt[1][1] == 2:
            blocks.append(d[5])
            blocks.append(d[6])
        blocks.append(d[7])
        blocks.append(d[8])
        if opt[0][1] == "stereo":
            blocks.append(d[9])

        return blocks


class DelaywMod(ZoiaModule):
    def __init__(self, version):
        self.module_id = 43
        self.name = "Delay w Mod"
        self.version = version
        self.category = "Effect"
        self.description = """
            Delay is one of the classic delay effects.
            Delay w/Mod differs from the Delay Line module found in Audio Out in
            that it runs a dry signal alongside the wet, has a feedback section,
            and a modulation section.
            Set the delay time either by tap or rotary/CV input.
            Optional stereo outputs round out the list of features.
            You can change the character of the delay effect with the 	ype\n            option, and/or by setting your mix to wet only, adding tone control
            and other effects to the output, and connecting your audio source
            directly to your output (bypassing the delay module) to act as the dry signal.
            """
        self.default_blocks = 7
        self.min_blocks = 7
        self.max_blocks = 9
        self.params = 5
        self.cpu = 18
        self.blocks = {
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
        }
        self.options = {
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
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "2in->2out":
            blocks.append(d[1])
        if opt[1][1] == "rate":
            blocks.append(d[2])
        else:
            blocks.append(d[3])
        blocks.append(d[4])
        blocks.append(d[5])
        blocks.append(d[6])
        blocks.append(d[7])
        blocks.append(d[8])
        if opt[0][1] != "1in->1out":
            blocks.append(d[9])

        return blocks


class Stompswitch(ZoiaModule):
    def __init__(self, version):
        self.module_id = 44
        self.name = "Stompswitch"
        self.version = version
        self.category = "Interface"
        self.description = """
            Use this module to connect a stomp switch to other modules.
            This can be any of ZOIA's 3 stomp switches or an external one.
            If using an external, remember to set it up in the Config Menu.
            Once placed, the Scroll and Bypass stomp switches must be \switched to\n            by holding them both on together for 2 seconds, this will allow them to
            function in the modules instead of as ZOIA's main user interface.
            Hold again for 2 seconds to switch back.
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 1
        self.params = 0
        self.cpu = 0.1
        self.blocks = {
            "cv_output": {"isDefault": True, "isParam": False, "position": 0}
        }
        self.options = {
            "stompswitch": ["left", "middle", "right", "ext"],
            "action": ["momentary", "latching"],
            "normally": ["zero", "one"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Value(ZoiaModule):
    def __init__(self, version):
        self.module_id = 45
        self.name = "Value"
        self.version = version
        self.category = "CV"
        self.description = """
            Value allows you to connect to multiple modules and adjust their
            parameters simultaneously from one CV adjustment at the input.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 2
        self.params = 1
        self.cpu = 0.15
        self.blocks = {
            "value": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {"output": ["0 to 1", "-1 to 1"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class CVDelay(ZoiaModule):
    def __init__(self, version):
        self.module_id = 46
        self.name = "CV Delay"
        self.version = version
        self.category = "CV"
        self.description = """
            CV Delay will take incoming CV and delay it in time by a set amount.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 3
        self.params = 2
        self.cpu = 1.5
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "delay_time": {"isDefault": True, "isParam": True, "position": 1},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class CVLoop(ZoiaModule):
    def __init__(self, version):
        self.module_id = 47
        self.name = "CV Loop"
        self.version = version
        self.category = "CV"
        self.description = """
            CV Loop functions similar to an audio looper except records patterns
            of CV signal instead of audio.
            You can record and play back snippets of LFOs, sequences, changes in CV
            or MIDI control etc.
            """
        self.default_blocks = 6
        self.min_blocks = 6
        self.max_blocks = 8
        self.params = 7
        self.cpu = 0.1
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "record": {"isDefault": True, "isParam": True, "position": 1},
            "play": {"isDefault": True, "isParam": True, "position": 2},
            "playback_speed": {"isDefault": True, "isParam": True, "position": 3},
            "start_position": {"isDefault": False, "isParam": True, "position": 4},
            "stop_position": {"isDefault": False, "isParam": True, "position": 5},
            "restart_loop": {"isDefault": True, "isParam": True, "position": 6},
            "cv_output": {"isDefault": True, "isParam": False, "position": 7},
        }
        self.options = {
            "max_rec_time": list(range(1, 17)),
            "length_edit": ["off", "on"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0], d[1], d[2], d[3]]
        if opt[1][1] == "on":
            blocks.append(d[4])
            blocks.append(d[5])
        blocks.append(d[6])
        blocks.append(d[7])

        return blocks


class CVFilter(ZoiaModule):
    def __init__(self, version):
        self.module_id = 48
        self.name = "CV Filter"
        self.version = version
        self.category = "CV"
        self.description = """
            CV Filter dictates the length of time a CV output will take to
            respond to a change in CV input, determined by the time constant.
            The CV change occurs logarithmically for a nice smooth transition.
            Use this module in series with a MIDI/keyboard note to add portamento
            to your synth voice.
            You can also use this module to vary the shape of an LFO waveform or connect
            to a stomp switch to produce a long slow change in an audio effect.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 4
        self.params = 2
        self.cpu = 0.1
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "time_constant": {"isDefault": True, "isParam": True, "position": 1},
            "rise_constant": {"isDefault": False, "isParam": True, "position": 3},
            "fall_constant": {"isDefault": False, "isParam": True, "position": 4},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {"control": ["linked", "separate"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "linked":
            blocks.append(d[1])
        else:
            blocks.append(d[2])
            blocks.append(d[3])
        blocks.append(d[4])

        return blocks


class ClockDivider(ZoiaModule):
    def __init__(self, version):
        self.module_id = 49
        self.name = "Clock Divider"
        self.version = version
        self.category = "CV"
        self.description = """
            Clock Divider module will detect tempo of incoming CV upward changes,
            divide it by a user determined ratio, and output CV triggers at the resulting tempo.
            This can be a handy way of getting a tap tempo from a slightly irregular waveform.
            """
        self.default_blocks = 5
        self.min_blocks = 4
        self.max_blocks = 5
        self.params = 4
        self.cpu = 0.4
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "reset_in": {"isDefault": True, "isParam": True, "position": 1},
            "modifier": {"isDefault": False, "isParam": True, "position": 2},
            "dividend": {"isDefault": True, "isParam": True, "position": 4},
            "divisor": {"isDefault": True, "isParam": True, "position": 5},
            "cv_output": {"isDefault": True, "isParam": False, "position": 3},
        }
        self.options = {"input": ["tap", "cv_control"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        if self.version >= 1:
            blocks = [d[0], d[1], d[3], d[4], d[5]]
        else:
            blocks = [d[0], d[1], d[2], d[5]]

        return blocks


class Comparator(ZoiaModule):
    def __init__(self, version):
        self.module_id = 50
        self.name = "Comparator"
        self.version = version
        self.category = "CV"
        self.description = """
            Comparator is a logic module that will switch CV on if positive input
            is equal to or greater than negative input, and off if positive input is
            less than negative input.
            Off can be defined as 0 or -1 by the output range.
            This can be useful if you'd like to have something happen, but only above
            a certain threshold.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 3
        self.params = 2
        self.cpu = 0.04
        self.blocks = {
            "cv_positive_input": {"isDefault": True, "isParam": True, "position": 0},
            "cv_negative_input": {"isDefault": True, "isParam": True, "position": 1},
            "cv_output": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {"output": ["0 to 1", "-1 to 1"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class CVRectify(ZoiaModule):
    def __init__(self, version):
        self.module_id = 51
        self.name = "CV Rectify"
        self.version = version
        self.category = "CV"
        self.description = """
            CV Rectify will interpret incoming CV from -1 to 1 and lip\ the negative
            values into positive values equidistant from 0.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 2
        self.params = 1
        self.cpu = 0.02
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Trigger(ZoiaModule):
    def __init__(self, version):
        self.module_id = 52
        self.name = "Trigger"
        self.version = version
        self.category = "CV"
        self.description = """
            Creates a very short CV pulse (value of 1) on detection of upward CV input.
            This is useful in creating a tap tempos from regular or irregular CV waveforms,
            triggering sequencers or ADSRs at specific times, etc.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 2
        self.params = 1
        self.cpu = 0.1
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class StereoSpread(ZoiaModule):
    def __init__(self, version):
        self.module_id = 53
        self.name = "Stereo Spread"
        self.version = version
        self.category = "Audio"
        self.description = """
            Stereo Spread will take one or two channels and enhance their stereo field.
            This is generally used right before an audio output module but, as always,
            feel free to experiment!
            """
        self.default_blocks = 5
        self.min_blocks = 4
        self.max_blocks = 5
        self.params = 1
        self.cpu = 2
        self.blocks = {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_2": {"isDefault": False, "isParam": False, "position": 1},
            "side_gain": {"isDefault": False, "isParam": True, "position": 2},
            "delay_time": {"isDefault": True, "isParam": True, "position": 3},
            "audio_out_1": {"isDefault": True, "isParam": False, "position": 4},
            "audio_out_2": {"isDefault": True, "isParam": False, "position": 5},
        }
        self.options = {"method": ["mid_side", "haas"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        if opt[0][1] == "haas":
            blocks = [d[0], d[3], d[4], d[5]]
        else:
            blocks = [d[0], d[1], d[2], d[4], d[5]]

        return blocks


class CportExpCVIn(ZoiaModule):
    def __init__(self, version):
        self.module_id = 54
        self.name = "Cport Exp CV In"
        self.version = version
        self.category = "Interface"
        self.description = """
            Connect your expression pedal or a control voltage signal from an external source.
            Remember to set CPort to either exp or cv in the Config Menu.
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 1
        self.params = 0
        self.cpu = 0.1
        self.blocks = {
            "cv_output": {"isDefault": True, "isParam": False, "position": 0}
        }
        self.options = {"output_range": ["0 to 1", "-1 to 1"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class CportCVOut(ZoiaModule):
    def __init__(self, version):
        self.module_id = 55
        self.name = "Cport CV Out"
        self.version = version
        self.category = "Interface"
        self.description = """
            This module interprets internal CV and sends it down the ring of a 1/4\n            TRS connector in the control port as a standard CV signal of 0-5 volts.
            Remember to set CPort to cv in the Config Menu.
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 1
        self.params = 0
        self.cpu = 0.2
        self.blocks = {"cv_input": {"isDefault": True, "isParam": True, "position": 0}}
        self.options = {"input_range": ["0 to 1", "-1 to 1"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class UIButton(ZoiaModule):
    def __init__(self, version):
        self.module_id = 56
        self.name = "UI Button"
        self.version = version
        self.category = "Interface"
        self.description = """
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
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 2
        self.params = 1
        self.cpu = 0.04
        self.blocks = {
            "in": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": False, "isParam": False, "position": 1},
        }
        self.options = {
            "cv_output": ["disabled", "enabled"],
            "range": ["extended", "basic"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "enabled":
            blocks.append(d[1])

        return blocks


class AudioPanner(ZoiaModule):
    def __init__(self, version):
        self.module_id = 57
        self.name = "Audio Panner"
        self.version = version
        self.category = "Audio"
        self.description = """
            Audio Panner takes either one or two input channels and pans them between two outputs.
            Connect an LFO for a stereo tremolo effect.
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 5
        self.params = 3
        self.cpu = 1
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "pan": {"isDefault": True, "isParam": True, "position": 2},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 3},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 4},
        }
        self.options = {
            "channels": ["1in->2out", "2in->2out"],
            "pan_type": ["equal_pwr", "-4.5dB", "linear"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "2in->2out":
            blocks.append(d[1])
        blocks.append(d[2])
        blocks.append(d[3])
        blocks.append(d[4])

        return blocks


class PitchDetector(ZoiaModule):
    def __init__(self, version):
        self.module_id = 58
        self.name = "Pitch Detector"
        self.version = version
        self.category = "Analysis"
        self.description = """
            Pitch Detector interprets the pitch of a connected audio signal as a CV note output,
            which can be sent to an oscillator or quantizer.
            You can affect the tracking by changing the connection strength between
            the audio source and the audio input, and transpose which note the oscillator
            will generate using the connection strength to the oscillator.
            Click knob to toggle display between frequency in Hz and note.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 2
        self.params = 0
        self.cpu = 2.5
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class PitchShifter(ZoiaModule):
    def __init__(self, version):
        self.module_id = 59
        self.name = "Pitch Shifter"
        self.version = version
        self.category = "Audio"
        self.description = """
            Pitch Shifter transposes the pitch of incoming audio.
            Click the knob on the pitch shift parameter to cycle views of
            CV value, semitones, or cents.
            Connect an LFO to produce a vibrato effect, or connect whatever you'd like!
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 3
        self.params = 1
        self.cpu = 15.5
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "pitch_shift": {"isDefault": True, "isParam": True, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class MidiNoteOut(ZoiaModule):
    def __init__(self, version):
        self.module_id = 60
        self.name = "Midi Note Out"
        self.version = version
        self.category = "Interface"
        self.description = """
            Send MIDI notes out to external MIDI enabled gear through ZOIA's MIDI outputs.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 3
        self.params = 3
        self.cpu = 0.1
        self.blocks = {
            "note_in": {"isDefault": True, "isParam": True, "position": 0},
            "gate_in": {"isDefault": True, "isParam": True, "position": 1},
            "velocity_in": {"isDefault": False, "isParam": True, "position": 2},
        }
        self.options = {
            "midi_channel": list(range(1, 17)),
            "velocity_output": ["off", "on"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0], d[1]]
        if opt[1][1] == "on":
            blocks.append(d[2])

        return blocks


class MidiCCOut(ZoiaModule):
    def __init__(self, version):
        self.module_id = 61
        self.name = "Midi CC Out"
        self.version = version
        self.category = "Interface"
        self.description = """
            Send Control Change messages to external MIDI enabled gear through ZOIA's MIDI outputs.
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 1
        self.params = 1
        self.cpu = 0.2
        self.blocks = {"cc": {"isDefault": True, "isParam": True, "position": 0}}
        self.options = {
            "midi_channel": list(range(1, 17)),
            "controller": list(range(0, 128)),
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class MidiPCOut(ZoiaModule):
    def __init__(self, version):
        self.module_id = 62
        self.name = "Midi PC Out"
        self.version = version
        self.category = "Interface"
        self.description = """
            Send Program Change messages to external MIDI enabled gear.
            Select the Program Change value and send a CV signal to trigger
            in to send message through ZOIA's MIDI outputs.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 2
        self.params = 2
        self.cpu = 0.1
        self.blocks = {
            "pc": {"isDefault": True, "isParam": True, "position": 0},
            "trigger_in": {"isDefault": True, "isParam": True, "position": 1},
        }
        self.options = {"midi_channel": list(range(1, 17))}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class BitModulator(ZoiaModule):
    def __init__(self, version):
        self.module_id = 63
        self.name = "Bit Modulator"
        self.version = version
        self.category = "Audio"
        self.description = """
            Bit Modulator takes one audio input and compares it against the other,
            creating an unholy glitchy combination of both sounds at the output.
            Choose between 3 different logic flavours with the 	ype\ option.
            When taking audio from an external source, it's recommended to put a gate before the input.
            """
        self.default_blocks = 3
        self.min_blocks = 3
        self.max_blocks = 3
        self.params = 0
        self.cpu = 1.2
        self.blocks = {
            "audio_in_1": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_2": {"isDefault": True, "isParam": False, "position": 1},
            "audio_out": {"isDefault": True, "isParam": False, "position": 2},
        }
        self.options = {"type": ["xor", "and", "or"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class AudioBalance(ZoiaModule):
    def __init__(self, version):
        self.module_id = 64
        self.name = "Audio Balance"
        self.version = version
        self.category = "Audio"
        self.description = """
            Audio Balance mixes an output from 2 inputs.
            You can run this module either mono or stereo.
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 7
        self.params = 1
        self.cpu = 1.7
        self.blocks = {
            "audio_in_1_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_1_R": {"isDefault": False, "isParam": False, "position": 4},
            "audio_in_2_L": {"isDefault": True, "isParam": False, "position": 1},
            "audio_in_2_R": {"isDefault": False, "isParam": False, "position": 5},
            "mix": {"isDefault": True, "isParam": True, "position": 2},
            "audio_output_L": {"isDefault": True, "isParam": False, "position": 3},
            "audio_output_R": {"isDefault": False, "isParam": False, "position": 6},
        }
        self.options = {"stereo": ["mono", "stereo"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        if opt[0][1] == "mono":
            blocks = [d[0], d[2], d[4], d[5]]
        else:
            blocks = d

        return blocks


class Inverter(ZoiaModule):
    def __init__(self, version):
        self.module_id = 65
        self.name = "Inverter"
        self.version = version
        self.category = "Audio"
        self.description = """
            The Inverter module takes incoming audio signal and inverts the
            sound wave 180 degrees out of phase.
            This module is inaudible unless you have a phase related problem
            you are trying to solve, in which case it can be very audible.
            Be sure to put a 1 Buffer Delay module into your \dry\ side to
            line up the Inverter in time for proper phase cancellation.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 2
        self.params = 0
        self.cpu = 0.3
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "audio_out": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Fuzz(ZoiaModule):
    def __init__(self, version):
        self.module_id = 66
        self.name = "Fuzz"
        self.version = version
        self.category = "Effect"
        self.description = """
            The Fuzz module provides gnarly fuzz tones for your sonic enjoyment.
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 4
        self.params = 2
        self.cpu = 16
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "input_gain": {"isDefault": True, "isParam": True, "position": 1},
            "output_gain": {"isDefault": True, "isParam": True, "position": 2},
            "audio_out": {"isDefault": True, "isParam": False, "position": 3},
        }
        self.options = {"model": ["efuzzy", "burly", "scoopy", "ugly"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Ghostverb(ZoiaModule):
    def __init__(self, version):
        self.module_id = 67
        self.name = "Ghostverb"
        self.version = version
        self.category = "Effect"
        self.description = """
            A spooky, ghostly reverb sound akin to the Ghost mode found in the Empress Reverb.
            Scare the crap out of all your friends!
            """
        self.default_blocks = 6
        self.min_blocks = 6
        self.max_blocks = 8
        self.params = 4
        self.cpu = 45
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "decay_feedback": {"isDefault": True, "isParam": True, "position": 2},
            "rate": {"isDefault": True, "isParam": True, "position": 3},
            "resonance": {"isDefault": True, "isParam": True, "position": 4},
            "mix": {"isDefault": True, "isParam": True, "position": 5},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7},
        }
        self.options = {"channels": ["1in->1out", "1in->2out", "stereo"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "stereo":
            blocks.append(d[1])
        blocks.append(d[2])
        blocks.append(d[3])
        blocks.append(d[4])
        blocks.append(d[5])
        blocks.append(d[6])
        if opt[0][1] != "1in>1out":
            blocks.append(d[7])

        return blocks


class CabinetSim(ZoiaModule):
    def __init__(self, version):
        self.module_id = 68
        self.name = "Cabinet Sim"
        self.version = version
        self.category = "Effect"
        self.description = """
            A versatile guitar cabinet simulator.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 4
        self.params = 0
        self.cpu = 10
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 2},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 3},
        }
        self.options = {
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
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        if opt[0][1] == "mono":
            blocks = [d[0], d[2]]
        else:
            blocks = d

        return blocks


class Flanger(ZoiaModule):
    def __init__(self, version):
        self.module_id = 69
        self.name = "Flanger"
        self.version = version
        self.category = "Effect"
        self.description = """
            ZOIA's Flanger module is borrowed right from the Empress Nebulus.
            This quite versatile flanger encompasses lots of comb filtering territory,
            but don't hesitate to build flange tones yourself using LFOs and delay lines!
            """
        self.default_blocks = 7
        self.min_blocks = 7
        self.max_blocks = 9
        self.params = 5
        self.cpu = 11
        self.blocks = {
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
        }
        self.options = {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "type": ["1960s", "1970s", "thru_0"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "stereo":
            blocks.append(d[1])
        if opt[1][1] == "rate":
            blocks.append(d[2])
        elif opt[1][1] == "tap_tempo":
            blocks.append(d[3])
        else:
            blocks.append(d[4])
        blocks.append(d[5])
        blocks.append(d[6])
        blocks.append(d[7])
        blocks.append(d[8])
        blocks.append(d[9])
        if opt[0][1] != "1in>1out":
            blocks.append(d[10])

        return blocks


class Chorus(ZoiaModule):
    def __init__(self, version):
        self.module_id = 70
        self.name = "Chorus"
        self.version = version
        self.category = "Effect"
        self.description = """
            The classic chorus effect.
            A nice sounding, fairly standard chorus.
            Get wackier sounds from it by using CV direct, or build
            your own from LFOs and delay lines!
            """
        self.default_blocks = 6
        self.min_blocks = 6
        self.max_blocks = 8
        self.params = 4
        self.cpu = 13
        self.blocks = {
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
        }
        self.options = {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "type": ["classic"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "stereo":
            blocks.append(d[1])
        if opt[1][1] == "rate":
            blocks.append(d[2])
        elif opt[1][1] == "tap_tempo":
            blocks.append(d[3])
        else:
            blocks.append(d[4])
        blocks.append(d[5])
        blocks.append(d[6])
        blocks.append(d[7])
        blocks.append(d[8])
        if opt[0][1] != "1in>1out":
            blocks.append(d[9])

        return blocks


class Vibrato(ZoiaModule):
    def __init__(self, version):
        self.module_id = 71
        self.name = "Vibrato"
        self.version = version
        self.category = "Effect"
        self.description = """
            Vibrato is your typical pitch bending, wet only sound you'd find on
            such classic units as the Empress Nebulus, just to name one.
            Get bendy!
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 6
        self.params = 2
        self.cpu = 5
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "rate": {"isDefault": True, "isParam": True, "position": 2},
            "tap_tempo_in": {"isDefaut": False, "isParam": True, "position": 3},
            "direct": {"isDefault": False, "isParam": True, "position": 4},
            "width": {"isDefault": True, "isParam": True, "position": 5},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7},
        }
        self.options = {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "control": ["rate", "tap_tempo", "cv_direct"],
            "waveform": ["sine", "triangle", "swung_sine", "swung"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "stereo":
            blocks.append(d[1])
        if opt[1][1] == "rate":
            blocks.append(d[2])
        elif opt[1][1] == "tap_tempo":
            blocks.append(d[3])
        else:
            blocks.append(d[4])
        blocks.append(d[5])
        blocks.append(d[6])
        if opt[0][1] != "1in>1out":
            blocks.append(d[7])

        return blocks


class EnvFilter(ZoiaModule):
    def __init__(self, version):
        self.module_id = 72
        self.name = "Env Filter"
        self.version = version
        self.category = "Effect"
        self.description = """
            Get your quack on!
            This fully featured envelope filter has everything you
            need to tune in that perfect envelope filter and get funky.
            Great on guitar, bass, or anything else!
            """
        self.default_blocks = 6
        self.min_blocks = 6
        self.max_blocks = 8
        self.params = 4
        self.cpu = 7
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "sensitivity": {"isDefault": True, "isParam": True, "position": 2},
            "min_freq": {"isDefault": True, "isParam": True, "position": 3},
            "max_freq": {"isDefault": True, "isParam": True, "position": 4},
            "filter_q": {"isDefault": True, "isParam": True, "position": 5},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 7},
        }
        self.options = {
            "channels": ["1in->1out", "1in->2out", "stereo"],
            "filter_type": ["bpf", "hpf", "lpf"],
            "direction": ["up", "down"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "stereo":
            blocks.append(d[1])
        blocks.append(d[2])
        blocks.append(d[3])
        blocks.append(d[4])
        blocks.append(d[5])
        blocks.append(d[6])
        if opt[0][1] != "1in>1out":
            blocks.append(d[7])

        return blocks


class RingModulator(ZoiaModule):
    def __init__(self, version):
        self.module_id = 73
        self.name = "Ring Modulator"
        self.version = version
        self.category = "Effect"
        self.description = """
            A gnarly ring modulation effect.
            A robot's nightmare, a tweaker's delight!
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 6
        self.params = 3
        self.cpu = 14
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "frequency": {"isDefault": True, "isParam": True, "position": 1},
            "ext_in": {"isDefault": False, "isParam": False, "position": 2},
            "duty_cycle": {"isDefault": False, "isParam": True, "position": 3},
            "mix": {"isDefault": True, "isParam": True, "position": 4},
            "audio_out": {"isDefault": True, "isParam": False, "position": 5},
        }
        self.options = {
            "waveform": ["sine", "square", "triangle", "sawtooth"],
            "ext_audio_in": ["off", "on"],
            "duty_cycle": ["off", "on"],
            "upsampling": ["none", "2x"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[1][1] == "off":
            blocks.append(d[1])
        else:
            blocks.append(d[2])
        if opt[2][1] == "on":
            blocks.append(d[3])
        blocks.append(d[4])
        blocks.append(d[5])

        return blocks


class HallReverb(ZoiaModule):
    def __init__(self, version):
        self.module_id = 74
        self.name = "Hall Reverb"
        self.version = version
        self.category = "Effect"
        self.description = """
            It's like you're there, looking up at the pulpit, with the warm sun
            casting in beams of coloured light from the stained glass windows.
            You're in reverb heaven, now.
            """
        self.default_blocks = 8
        self.min_blocks = 8
        self.max_blocks = 8
        self.params = 4
        self.cpu = 22
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": True, "isParam": False, "position": 1},
            "decay_time": {"isDefault": True, "isParam": True, "position": 2},
            "low_eq": {"isDefault": True, "isParam": True, "position": 6},
            "lpf_freq": {"isDefault": True, "isParam": True, "position": 7},
            "mix": {"isDefault": True, "isParam": True, "position": 3},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 4},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 5},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class PingPongDelay(ZoiaModule):
    def __init__(self, version):
        self.module_id = 75
        self.name = "Ping Pong Delay"
        self.version = version
        self.category = "Effect"
        self.description = """
            Ping Pong Delay is almost identical to the Delay w/ Mod except for one key aspect:
            the delay repeats ping pong from left to right across stereo outputs.
            When stereo inputs are selected, one input will ping while the other pongs,
            followed by a pong while the other pings into the opposite and then correct outputs.
            """
        self.default_blocks = 7
        self.min_blocks = 7
        self.max_blocks = 9
        self.params = 5
        self.cpu = 18
        self.blocks = {
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
        }
        self.options = {
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
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "stereo":
            blocks.append(d[1])
        if opt[1][1] == "rate":
            blocks.append(d[2])
        else:
            blocks.append(d[3])
        blocks.append(d[4])
        blocks.append(d[5])
        blocks.append(d[6])
        blocks.append(d[7])
        blocks.append(d[8])
        blocks.append(d[9])

        return blocks


class AudioMixer(ZoiaModule):
    def __init__(self, version):
        self.module_id = 76
        self.name = "Audio Mixer"
        self.version = version
        self.category = "Audio"
        self.description = """
            Audio Mixer functions like a stripped down mixing console,
            where gain is your channel fader and you can place an optional pan control.
            Mix up to 8 channels, in mono or stereo.
            """
        self.default_blocks = 5
        self.min_blocks = 5
        self.max_blocks = 34
        self.params = 16
        self.cpu = 7
        self.blocks = {
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
        }
        self.options = {
            "channels": list(range(2, 9)),
            "stereo": ["mono", "stereo"],
            "panning": ["off", "on"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = []
        for i in range(1, opt[0][1] + 1):
            blocks.append(d[2 * (i - 1)])
            if opt[1][1] == "stereo":
                blocks.append(d[2 * (i - 1) + 1])
        for i in range(1, opt[0][1] + 1):
            blocks.append(d[i + 15])
        if opt[2][1] == "on":
            for i in range(1, opt[0][1] + 1):
                blocks.append(d[i + 23])
        blocks.append(d[32])
        if opt[1][1] == "stereo":
            blocks.append(d[33])

        return blocks


class CVFlipFlop(ZoiaModule):
    def __init__(self, version):
        self.module_id = 77
        self.name = "CV Flip Flop"
        self.version = version
        self.category = "CV"
        self.description = """
            This is essentially a latching CV switch with an output of 0 or 1.
            When the input sees an upward CV change, the flip flop is triggered to
            change it's output state from 0 to 1 at the next upward change in CV,
            which must occur after a downward change in CV.
            So, the flip flop changes from 0 to 1 at every other upward change in CV.
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 2
        self.params = 1
        self.cpu = 0.2
        self.blocks = {
            "cv_input": {"isDefault": True, "isParam": True, "position": 0},
            "cv_output": {"isDefault": True, "isParam": False, "position": 1},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Diffuser(ZoiaModule):
    def __init__(self, version):
        self.module_id = 78
        self.name = "Diffuser"
        self.version = version
        self.category = "Audio"
        self.description = """
            Diffuser spreads your signal across the galaxy like so many shimmering little stars.
            On it's own it sounds like a modulated slapback delay with no dry signal,
            but it can be used to construct many a tonal/atonal masterpiece.
            """
        self.default_blocks = 6
        self.min_blocks = 6
        self.max_blocks = 6
        self.params = 4
        self.cpu = 2
        self.blocks = {
            "audio_in": {"isDefault": True, "isParam": False, "position": 0},
            "gain": {"isDefault": True, "isParam": True, "position": 1},
            "size": {"isDefault": True, "isParam": True, "position": 2},
            "mod_width": {"isDefault": True, "isParam": True, "position": 3},
            "mod_rate": {"isDefault": True, "isParam": True, "position": 4},
            "audio_out": {"isDefault": True, "isParam": False, "position": 5},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class ReverbLite(ZoiaModule):
    def __init__(self, version):
        self.module_id = 79
        self.name = "Reverb Lite"
        self.version = version
        self.category = "Effect"
        self.description = """
            A straightforward CPU friendly reverb sound to add some smoosh to heavier workload patches.
            """
        self.default_blocks = 4
        self.min_blocks = 4
        self.max_blocks = 6
        self.params = 2
        self.cpu = 10
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": False, "isParam": False, "position": 1},
            "decay_time": {"isDefault": True, "isParam": True, "position": 2},
            "mix": {"isDefault": True, "isParam": True, "position": 3},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 4},
            "audio_out_R": {"isDefault": False, "isParam": False, "position": 5},
        }
        self.options = {"channels": ["1in->1out", "1in->2out", "stereo"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "stereo":
            blocks.append(d[1])
        blocks.append(d[2])
        blocks.append(d[3])
        blocks.append(d[4])
        if opt[0][1] != "1in->1out":
            blocks.append(d[5])

        return blocks


class RoomReverb(ZoiaModule):
    def __init__(self, version):
        self.module_id = 80
        self.name = "Room Reverb"
        self.version = version
        self.category = "Effect"
        self.description = """
            Well, you're cooped up in your little room.
            But that's okay, because you've got some tasty room reverb to swim around in.
            Don't worry, somebody will come get you out someday.
            """
        self.default_blocks = 8
        self.min_blocks = 8
        self.max_blocks = 8
        self.params = 4
        self.cpu = 22
        self.blocks = {
            "audio_in_L": {"isDefault": True, "isParam": False, "position": 0},
            "audio_in_R": {"isDefault": True, "isParam": False, "position": 1},
            "decay_time": {"isDefault": True, "isParam": True, "position": 2},
            "low_eq": {"isDefault": True, "isParam": True, "position": 3},
            "lpf_freq": {"isDefault": True, "isParam": True, "position": 4},
            "mix": {"isDefault": True, "isParam": True, "position": 5},
            "audio_out_L": {"isDefault": True, "isParam": False, "position": 6},
            "audio_out_R": {"isDefault": True, "isParam": False, "position": 7},
        }
        self.options = {}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class Pixel(ZoiaModule):
    def __init__(self, version):
        self.module_id = 81
        self.name = "Pixel"
        self.version = version
        self.category = "Interface"
        self.description = """
            Puts a coloured block on the grid.
            The brightness can be controlled by a cv signal or an audio signal.
            Pixel is a simple, elegant way to create a more visually
            interactive user interface for your patch.
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 1
        self.params = 1
        self.cpu = 0.01
        self.blocks = {
            "cv_in": {"isDefault": True, "isParam": True, "position": 0},
            "audio_in": {"isDefault": False, "isParam": False, "position": 1},
        }
        self.options = {"control": ["cv", "audio"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        if opt[0][1] == "cv":
            blocks = [d[0]]
        else:
            blocks = [d[1]]

        return blocks


class MidiClockIn(ZoiaModule):
    def __init__(self, version):
        self.module_id = 82
        self.name = "Midi Clock In"
        self.version = version
        self.category = "Interface"
        self.description = """
            Connect MIDI clock to sync your patches to the outside world.
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 4
        self.params = 0
        self.cpu = 0.1
        self.blocks = {
            "quarter_out": {"isDefault": True, "isParam": False, "position": 0},
            "clock_out": {"isDefault": False, "isParam": False, "position": 1},
            "reset_out": {"isDefault": False, "isParam": False, "position": 2},
            "run_out": {"isDefault": False, "isParam": False, "position": 3},
        }
        self.options = {
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
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "enabled":
            blocks.append(d[1])
        if opt[1][1] == "enabled":
            blocks.append(d[2])
        if opt[2][1] == "enabled":
            blocks.append(d[3])

        return blocks


class Granular(ZoiaModule):
    def __init__(self, version):
        self.module_id = 83
        self.name = "Granular"
        self.version = version
        self.category = "Audio"
        self.description = """
            Granular breaks up incoming audio into tiny little grains and
            spits them back out in the quantity and shape of your choosing.
            Go from modest textures to completely unrecognizable oscillations.
            Granular can also be used as a granular delay by creating a feedback
            path from the output back to the input...
            """
        self.default_blocks = 8
        self.min_blocks = 8
        self.max_blocks = 10
        self.params = 6
        self.cpu = 8
        self.blocks = {
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
        }
        self.options = {
            "num_grains": list(range(1, 9)),
            "channels": ["mono", "stereo"],
            "pos_control": ["cv", "tap_tempo"],
            "size_control": ["cv", "tap_tempo"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        if opt[1][0] == "mono":
            blocks = [d[0], d[2], d[3], d[4], d[5], d[6], d[7], d[8]]
        else:
            blocks = d

        return blocks


class MidiClockOut(ZoiaModule):
    def __init__(self, version):
        self.module_id = 84
        self.name = "Midi Clock Out"
        self.version = version
        self.category = "Interface"
        self.description = """
            Generate MIDI clock to sync outside devices to your ZOIA.
            Clock sends directly to ZOIA's MIDI output.
            """
        self.default_blocks = 3
        self.min_blocks = 1
        self.max_blocks = 5
        self.params = 5
        self.cpu = 0.3
        self.blocks = {
            "tap_cv_control": {"isDefault": True, "isParam": True, "position": 0},
            "sent": {"isDefault": True, "isParam": True, "position": 1},
            "reset": {"isDefault": True, "isParam": True, "position": 2},
            "send_position": {"isDefault": False, "isParam": True, "position": 3},
            "song_position": {"isDefault": False, "isParam": True, "position": 4},
        }
        self.options = {
            "input": ["tap", "cv_control"],
            "run_in": ["enabled", "disabled"],
            "reset_in": ["enabled", "disabled"],
            "position": ["disabled", "enabled"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[1][1] == "enabled":
            blocks.append(d[1])
        if opt[2][1] == "enabled":
            blocks.append(d[2])
        if opt[3][1] == "enabled":
            blocks.append(d[3])
            blocks.append(d[4])

        return blocks


class TaptoCV(ZoiaModule):
    def __init__(self, version):
        self.module_id = 85
        self.name = "Tap to CV"
        self.version = version
        self.category = "CV"
        self.description = """
            Outputs a CV value proportional to the tap tempo input.	
            """
        self.default_blocks = 2
        self.min_blocks = 2
        self.max_blocks = 4
        self.params = 2
        self.cpu = 0.12
        self.blocks = {
            "tap_input": {"isDefault": True, "isParam": False, "position": 0},
            "min_time": {"isDefault": False, "isParam": True, "position": 1},
            "max_time": {"isDefault": False, "isParam": True, "position": 2},
            "output": {"isDefault": True, "isParam": False, "position": 3},
        }
        self.options = {"range": ["off", "on"], "output": ["linear", "exponential"]}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = [d[0]]
        if opt[0][1] == "on":
            blocks.append(d[1])
            blocks.append(d[2])
        blocks.append(d[3])

        return blocks


class MidiPitchBendIn(ZoiaModule):
    def __init__(self, version):
        self.module_id = 86
        self.name = "Midi Pitch Bend In"
        self.version = version
        self.category = "Interface"
        self.description = """
            Collects MIDI data from pitch bend wheel on keyboards,
            can be applied to oscillator frequency in parallel with MIDI note data,
            or used in other ways.	
            """
        self.default_blocks = 1
        self.min_blocks = 1
        self.max_blocks = 1
        self.params = 0
        self.cpu = 0.1
        self.blocks = {
            "pitch_bend": {"isDefault": True, "isParam": False, "position": 0}
        }
        self.options = {"midi_channel": list(range(1, 17))}
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        return self.blocks


class CVMixer(ZoiaModule):
    def __init__(self, version):
        self.module_id = 104
        self.name = "CV Mixer"
        self.version = version
        self.category = "CV"
        self.description = """
            """
        self.default_blocks = 5
        self.min_blocks = 5
        self.max_blocks = 17
        self.params = 16
        self.cpu = 0.7
        self.blocks = {
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
        }
        self.options = {
            "num_channels": list(range(1, 9)),
            "levels": ["summing", "average"],
        }
        self.saveable_data = {}
        super().__init__(version)

    def get_blocks(self):
        opt = list(self.options_new.items())
        d = list(self.blocks.items())

        blocks = []
        for i in range(1, opt[0][1] + 1):
            blocks.append(d[i - 1])
        for i in range(1, opt[0][1] + 1):
            blocks.append(d[i + 7])
        blocks.append(d[16])

        return blocks
