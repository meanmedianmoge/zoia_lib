from zoia_lib.backend.zoia_module_decorators import *

class ZoiaModule:
    def __init__(self):

        self.colors = {}

        self.size = 0
        self.module_id = 0
        self.version = 0
        self.page_number = 0
        self.color = 0
        self.grid_position = []
        self.saveable_data = []
        self.options = []
        self.params = {}
        self.name = ""

        self.module_decorator_index = {
            "0": sv_filter_decorator,
            "1": AudioInput,
            "2": AudioOutput,
            "3": Aliaser,
            "4": Sequencer,
            "5": LFO,
            "6": ADSR,
            "7": VCA,
            "8": AudioMultiply,
            "9": BitCrusher,
            "10": SampleandHold,
            "11": ODandDistortion,
            "12": EnvFollower,
            "13": DelayLine,
            "14": Oscillator,
            "15": Pushbutton,
            "16": Keyboard,
            "17": CVInvert,
            "18": Steps,
            "19": SlewLimiter,
            "20": MidiNotesIn,
            "21": MidiCCIn,
            "22": Multiplier,
            "23": Compressor,
            "24": MultiFilter,
            "25": PlateReverb,
            "26": BufferDelay,
            "27": AllPassFilter,
            "28": Quantizer,
            "29": Phaser,
            "30": Looper,
            "31": InSwitch,
            "32": OutSwitch,
            "33": AudioInSwitch,
            "34": AudioOutSwitch,
            "35": MidiPressure,
            "36": OnsetDetector,
            "37": Rhythm,
            "38": Noise,
            "39": Random,
            "40": Gate,
            "41": Tremolo,
            "42": ToneControl,
            "43": DelaywMod,
            "44": Stompswitch,
            "45": Value,
            "46": CVDelay,
            "47": CVLoop,
            "48": CVFilter,
            "49": ClockDivider,
            "50": Comparator,
            "51": CVRectify,
            "52": Trigger,
            "53": StereoSpread,
            "54": CportExpCVIn,
            "55": CportCVOut,
            "56": UIButton,
            "57": AudioPanner,
            "58": PitchDetector,
            "59": PitchShifter,
            "60": MidiNoteOut,
            "61": MidiCCOut,
            "62": MidiPCOut,
            "63": BitModulator,
            "64": AudioBalance,
            "65": Inverter,
            "66": Fuzz,
            "67": Ghostverb,
            "68": CabinetSim,
            "69": Flanger,
            "70": Chorus,
            "71": Vibrato,
            "72": EnvFilter,
            "73": RingModulator,
            "74": HallReverb,
            "75": PingPongDelay,
            "76": AudioMixer,
            "77": CVFlipFlop,
            "78": Diffuser,
            "79": ReverbLite,
            "80": RoomReverb,
            "81": Pixel,
            "82": MidiClockIn,
            "83": Granular,
            "84": MidiClockOut,
            "85": TaptoCV,
            "86": MidiPitchBendIn,
            "104": CVMixer,
        }

    def decorate_module(self, module_id):
        """
        This method will be used by the application to allow for a single dependency
        which can decorate the ZoiaModule class instances with relevant module data.
        """
        self.module_decorator_index[str(module_id)](self)

    def set_module_type_and_version(self, module_id, version):
        self.module_id = module_id
        self.version = version
        self.decorate_module(module_id)

    def set_module_position(self, page, position):
        # ZoiaPatch class will do the QA checks to confirm that the
        # position is valid before calling this function
        pass

    def set_color(self, color):
        self.color = self.colors[str(color)]

    def set_option_value(self, option, value):
        self.option

    def set_param_value(self, param_index, value):
        pass

    def set_saveable_data_value(self, index, value):
        pass

    def encode(self):
        pass

    def decode(self, bin_array):
        self.bin_array = bin_array
        # Module size 4
        # Module type 4 - set by child
        # Module Version 4 - set by child
        # Page Number 4 -
        # Old Color 4
        # Grid Position 4 (array values indicating all of the zoia buttons that the module occupies)
        # Number of parameters 4
        # Size of Saveable Data 4
        # Options 8
        # Any number of params (4n)
        #   Dict of params w/ key like "param_1"
        #   and value should be presented to the app as the binary int / 65535, then rounded to 2 decimal places
        # Module Name 16

        # Unpack the binary data that wasn't unpacked in the patch
        self.page_number = self.convert_bin_to_int(self.bin_array[12:16])
        self.old_color = self.convert_bin_to_int(self.bin_array[16:20])
        self.grid_position = self.convert_bin_to_int(self.bin_array[20:24])
        self.options = self.bin_array[32:40]

        number_of_params = self.convert_bin_to_int(self.bin_array[24:28])
        cursor = 40 + number_of_params * 4
        self.params = self.bin_array[40:cursor]

        size_of_saveable_data = self.convert_bin_to_int(self.bin_array[28:32])
        cursor_end = cursor + size_of_saveable_data * 4
        self.saveable_data = self.bin_array[cursor:cursor_end]

        self.module_name = self.convert_bin_to_text(self.bin_array[cursor_end:cursor_end + 16])

        # ===========================================================================================
        #   Helper Functions used in module
        # ===========================================================================================
    @staticmethod
    def convert_bin_to_int(byte_string):
        # Force little-endian for cross-platform support
        return int.from_bytes(byte_string[0:4], "little")

    @staticmethod
    def convert_bin_to_text(string_tuple):
        string = ''
        for item in string_tuple:
            string += chr(item)
        return string

