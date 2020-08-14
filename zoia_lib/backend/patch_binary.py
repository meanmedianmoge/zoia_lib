import struct

from zoia_lib.backend.patch import Patch


class PatchBinary(Patch):
    """T he PatchBinary class is a child of the Patch class. It is
    responsible for patch binary analysis.
    """

    def __init__(self):
        """

        """
        super().__init__()

    def parse_data(self, pch_data):
        """ Parses the binary data of a patch for information relating
        to the patch. This information is collected into a string that
        is returned such that it can be displayed via the frontend.
        The returned data will specify the following:
        - Preset size
        - Patch name (real name)
        - Module count
          - For each module:
            - Module type
            - Page number
            - Old color value
            - Grid position
            - Number of parameters on the grid
        - Connection count
          - For each connection:
            - Connection values and strength (as a %)
        - Number of pages
          - For each page:
            - The page name (if it has one)
        - The color of each module (not yet implemented).

        pch_data: The binary to be parsed and analyzed.
        Returns a formatted string that can be shown in the frontend.
        """

        # Massive credit to apparent1 for figuring this stuff out.
        # They did all the heavy lifting. Still a WIP.
        try:
            name = str(pch_data[4:]).split("\\")[0].split("\'")[1]
        except IndexError:
            name = str(pch_data[4:]).split("\\")[0]
        data = struct.unpack('i'*int(len(pch_data) / 4), pch_data)

        pch_viz = "Everything listed below is experimental and may not " \
                  "reflect the patch correctly.\n" \
                  "-----------------------------------------------------" \
                  "---------------------------\n"

        pch_viz += "Preset size = {}".format(data[0])
        pch_viz += "\nPatch name = {}".format(name)
        pch_viz += "\nModule count = {}".format(data[5])
        curr_step = 6
        for i in range(int(data[5])):
            size = data[curr_step]
            pch_viz += "\n  Module #{}".format(i)
            pch_viz += "\n\tModule size = {}".format(size)
            pch_viz += "\n\tModule type: {}".format(
                self.get_module_type(data[curr_step + 1]))
            pch_viz += "\n\tPage number: {}".format(data[curr_step + 3])
            pch_viz += "\n\tOld color value: {}".format(
                self.get_color_name(data[curr_step + 4]))
            pch_viz += "\n\tGrid position: {}".format(data[curr_step + 5])
            pch_viz += "\n\tNumber of parameters on grid: " \
                       "{}".format(data[curr_step + 6])
            curr_step += size

        pch_viz += "\nConnection count: {}".format(data[curr_step])
        for j in range(data[curr_step]):
            pch_viz += "\n  Connection #{}".format(j)
            pch_viz += "\n\t{}.{} -> {}.{} {}%".format(data[curr_step + 1],
                                                       data[curr_step + 2],
                                                       data[curr_step + 3],
                                                       data[curr_step + 4],
                                                       int(data[curr_step + 5]
                                                           / 100))
            curr_step += 5
        pch_viz += "\nNumber of pages = {}".format(data[curr_step + 1])

        return pch_viz

    def get_module_type(self, module_id):
        module = {
            0: "SV Filter",
            1: "Audio Input",
            2: "Audio Out",
            3: "Aliaser",
            4: "Sequencer",
            5: "LFO",
            6: "ADSR",
            7: "VCA",
            8: "Audio Multiply",
            9: "Bit Crusher",
            10: "Sample and Hold",
            11: "OD & Distortion",
            12: "Env Follower",
            13: "Delay line",
            14: "Oscillator",
            15: "Pushbutton",
            16: "Keyboard",
            17: "CV Invert",
            18: "Steps",
            19: "Slew Limiter",
            20: "MIDI Notes in",
            21: "MIDI CC in",
            22: "Multiplier",
            23: "Compressor",
            24: "Multi-filter",
            25: "Plate Reverb",
            26: "Buffer delay",
            27: "All-pass filter",
            28: "Quantizer",
            29: "Phaser",
            30: "Looper",
            31: "In Switch",
            32: "Out Switch",
            33: "Audio In Switch",
            34: "Audio Out Switch",
            35: "Midi pressure",
            36: "Onset Detector",
            37: "Rhythm",
            38: "Noise",
            39: "Random",
            40: "Gate",
            41: "Tremolo",
            42: "Tone Control",
            43: "Delay w/Mod",
            44: "Stompswitch",
            45: "Value",
            46: "CV Delay",
            47: "CV Loop",
            48: "CV Filter",
            49: "Clock Divider",
            50: "Comparator",
            51: "CV Rectify",
            52: "Trigger",
            53: "Stereo Spread",
            54: "Cport Exp/CV in",
            55: "Cport CV out",
            56: "UI Button",
            57: "Audio Panner",
            58: "Pitch Detector",
            59: "Pitch Shifter",
            60: "Midi Note out",
            61: "Midi CC out",
            62: "Midi PC out",
            63: "Bit Modulator",
            64: "Audio Balance",
            65: "Inverter",
            66: "Fuzz",
            67: "Ghostverb",
            68: "Cabinet Sim",
            69: "Flanger",
            70: "Chorus",
            71: "Vibrato",
            72: "Env Filter",
            73: "Ring Modulator",
            74: "Hall Reverb",
            75: "Ping Pong Delay",
            76: "Audio Mixer",
            77: "CV Flip Flop",
            78: "Diffuser",
            79: "Reverb Lite",
            80: "Room Reverb",
            81: "Pixel",
            82: "Midi Clock In",
            83: "Granular"
        }[module_id]

        return module

    def get_color_name(self, color_id):
        """ Determines the longform name of a color id.

        color_id: The id for the color.
        """
        color = {
            1: "Blue",
            2: "Green",
            3: "Red",
            4: "Yellow",
            5: "Aqua",
            6: "Magenta",
            7: "White",
            8: "Orange",
            9: "Lima",
            10: "Surf",
            11: "Sky",
            12: "Purple",
            13: "Pink",
            14: "Peach",
            15: "Mango"
        }[color_id]

        return color

    def get_parameter_name(self, module_id):
        """ Determines the longform name of a module id.

        module_id: The id for the module.
        """
        module = {
            0: "Module type",
            2: "Page number",
            3: "Old color value",
            4: "Grid position",
            5: "Number of parameters on grid",
            7: "Module options 1",
            8: "Module options 2"
        }[module_id]

        return module
