from zoia_lib.backend.zoia_modules import *

class ZoiaModuleFactory:
"""
This class will be used by the application to provide a single
dependency which can generate instances of zoia_modules. The factory's only
method "create_module" is built to accept module_id and version as arguments,
allowing for this factory to generate a module instance directly from a bin
file or from a ZOIA Libarrian UI call.
"""
    def __init__(self):
        self.module_index = {
            "0": SVFilter
            "1": AudioInput
            "2": AudioOutput
            "3": Aliaser
            "4": Sequencer
            "5": LFO
            "6": ADSR
            "7": VCA
            "8": AudioMultiply
            "9": BitCrusher
            "10": SampleandHold
            "11": ODandDistortion
            "12": EnvFollower
            "13": DelayLine
            "14": Oscillator
            "15": Pushbutton
            "16": Keyboard
            "17": CVInvert
            "18": Steps
            "19": SlewLimiter
            "20": MidiNotesIn
            "21": MidiCCIn
            "22": Multiplier
            "23": Compressor
            "24": MultiFilter
            "25": PlateReverb
            "26": BufferDelay
            "27": AllPassFilter
            "28": Quantizer
            "29": Phaser
            "30": Looper
            "31": InSwitch
            "32": OutSwitch
            "33": AudioInSwitch
            "34": AudioOutSwitch
            "35": MidiPressure
            "36": OnsetDetector
            "37": Rhythm
            "38": Noise
            "39": Random
            "40": Gate
            "41": Tremolo
            "42": ToneControl
            "43": DelaywMod
            "44": Stompswitch
            "45": Value
            "46": CVDelay
            "47": CVLoop
            "48": CVFilter
            "49": ClockDivider
            "50": Comparator
            "51": CVRectify
            "52": Trigger
            "53": StereoSpread
            "54": CportExpCVIn
            "55": CportCVOut
            "56": UIButton
            "57": AudioPanner
            "58": PitchDetector
            "59": PitchShifter
            "60": MidiNoteOut
            "61": MidiCCOut
            "62": MidiPCOut
            "63": BitModulator
            "64": AudioBalance
            "65": Inverter
            "66": Fuzz
            "67": Ghostverb
            "68": CabinetSim
            "69": Flanger
            "70": Chorus
            "71": Vibrato
            "72": EnvFilter
            "73": RingModulator
            "74": HallReverb
            "75": PingPongDelay
            "76": AudioMixer
            "77": CVFlipFlop
            "78": Diffuser
            "79": ReverbLite
            "80": RoomReverb
            "81": Pixel
            "82": MidiClockIn
            "83": Granular
            "84": MidiClockOut
            "85": TaptoCV
            "86": MidiPitchBendIn
            "104": CVMixer
        }
   
    def create_module(self, module_id, version):
        return self.module_index[module_id](version)