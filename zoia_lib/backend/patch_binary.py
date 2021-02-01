import json
import struct

from zoia_lib.backend.patch import Patch
from zoia_lib.common import errors

with open("zoia_lib/common/schemas/ModuleIndex.json", "r") as f:
    mod = json.load(f)


class PatchBinary(Patch):
    """The PatchBinary class is a child of the Patch class. It is
    responsible for ZOIA patch binary analysis.
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
        - Patch name
        - Module count
          - For each module:
            - Module name
            - Module type
            - Estimated CPU
            - Page number
            - Color
            - Grid position(s)
            - Parameter count
            - Parameter values
            - Options
        - Connection count
          - For each connection:
            - Out/In Module & Block pair
            - Connection strength
        - Number of pages and their names
        - Number of starred parameters
          - For each param:
            - Module and block
            - MIDI CC (if applicable)

        pch_data: The binary to be parsed and analyzed.

        return: A formatted JSON that can be shown in the frontend.
        """

        # Massive credit to apparent1 for figuring this stuff out.
        # They did all the heavy lifting.

        if pch_data is None:
            raise errors.BinaryError(None)

        # Extract the string name of the patch.
        name = self._qc_name(pch_data[4:])

        # Unpack the binary data.
        data = struct.unpack("i" * int(len(pch_data) / 4), pch_data)

        # Get a list of colors for the modules
        # (appears at the end of the binary)
        temp = [i for i, e in enumerate(data) if e != 0]
        last_color = temp[-1] + 1
        first_color = last_color - int(data[5])
        colors = []
        skip_real = False
        for j in range(first_color, last_color):
            if int(data[j]) > 15:
                skip_real = True
                colors = []
                break
            colors.append(data[j])

        modules = []
        # Extract the module data for each module in the patch.
        curr_step = 6
        for i in range(int(data[5])):
            size = data[curr_step]
            curr_module = {
                "number": i,
                "mod_idx": data[curr_step + 1],
                "name": self._qc_name(pch_data[(curr_step+(size-4))*4:
                                               (curr_step+(size-4))*4+16]),
                "cpu": self._get_module_data(data[curr_step + 1], "cpu"),
                "type": self._get_module_data(data[curr_step + 1], "name"),
                "page": int(data[curr_step + 3]),
                "position": [x for x in range(
                    int(data[curr_step + 5]),
                    int(data[curr_step + 5]) + self._get_module_data(
                        data[curr_step + 1], "min_blocks"))],
                "old_color": self._get_color_name(data[curr_step + 4]),
                "new_color": "" if skip_real else self._get_color_name(
                    colors[i]),
                "options": {},
                "options_copy": self._get_module_data(data[curr_step + 1], "options"),
                "options_list": list(
                    bytearray(pch_data[(curr_step+8)*4:(curr_step+8)*4+4])) + list(
                    bytearray(pch_data[(curr_step+9)*4:(curr_step+9)*4+4])),
                "parameters": dict(zip(
                    ["param_{}".format(str(x)) for x in range(data[curr_step + 6])],
                    [round(data[curr_step + x + 10] / 64560, 2) for x in range(data[curr_step + 6])]
                )),
                "blocks": [],
                "connections": [],
                "starred": []
            }

            # TODO edit behavior of the options selector, since modules are versioned
            # Select appropriate options from list
            try:
                v = 0
                for opt in list(curr_module["options_copy"]):
                    if not opt:
                        continue
                    option = curr_module["options_list"][v]
                    value = curr_module["options_copy"][opt][option]
                    curr_module["options"][opt] = value
                    v += 1
            except IndexError:
                raise errors.BinaryError(pch_data[:10], 101)

            # Combine colors into one key
            curr_module["color"] = curr_module["old_color"] if \
                curr_module["new_color"] == "" else curr_module["new_color"]

            # Remove extra keys from module dict
            curr_module.pop("new_color", None)
            curr_module.pop("old_color", None)
            curr_module.pop("options_copy", None)
            curr_module.pop("options_list", None)

            modules.append(curr_module)
            curr_step += size

        connections = []
        # Extract the connection data for each connection in the patch.
        for j in range(data[curr_step]):
            curr_connection = {
                "source": "{}.{}".format(int(data[curr_step + 1]),
                                         int(data[curr_step + 2])),
                "destination": "{}.{}".format(int(data[curr_step + 3]),
                                              int(data[curr_step + 4])),
                "strength": int(data[curr_step + 5] / 100)
            }
            connections.append(curr_connection)
            curr_step += 5

        pages = []
        curr_step += 1
        # Extract the page data for each page in the patch.
        for k in range(data[curr_step]):
            curr_page = self._qc_name(pch_data[(curr_step+1)*4:
                                               (curr_step+1)*4+16])
            pages.append(curr_page)
            curr_step += 4
        # Pad list with empty strings so that viz doesn't blow up
        n_pages = len(pages)
        pages += [""] * (64 - len(pages))

        starred = []
        curr_step += 1
        # Extract the starred parameters in the patch.
        for l in range(data[curr_step]):
            byte2 = struct.unpack('hh', pch_data[(curr_step+1)*4:(curr_step+1)*4+4])
            curr_param = {
                "module": byte2[0],
                "block": byte2[1] % 128,
                "midi_cc": int(round(byte2[1]/128)-1) if byte2[1] >= 128 else "None",
            }
            starred.append(curr_param)
            curr_step += 1

        colours = []
        # Extract the colors of each module in the patch.
        for m in range(len(modules)):
            curr_color = data[curr_step + 1]
            colours.append(curr_color)
            curr_step += 1

        # Block information
        for module in modules:
            module['blocks'] = self._calc_blocks(module)
            module['position'] = [x for x in range(
                module['position'][0], module['position'][0] + len(module['blocks']))]
            self._rename_param_dict(module)

        # Append data to module list
        modules = self._add_connections(modules, connections)
        modules = self._add_starred_param(modules, starred)

        # Prepare a dict to pass to thee frontend.
        json_bin = {
            "name": name,
            "modules": modules,
            # "connections": connections,
            "pages": pages,
            # "starred": starred,
            # "colours": colours
            "meta": {
                "name": name,
                "cpu": round(sum([k["cpu"] for k in modules]), 2),
                "n_modules": len(modules),
                "n_connections": len(connections),
                "n_pages": n_pages,
                "n_starred": len(starred),
                "i_o": self._get_io(modules)
            }
        }

        return json_bin

    @staticmethod
    def _qc_name(name):
        try:
            name = str(name).split("\\")[0].split("\'")[1]
        except IndexError:
            name = str(name).split("\\")[0]

        return name.split("b\"")[-1]

    @staticmethod
    def _get_module_data(module_id, key):
        """ Determines metadata about a module.

        module_id: The id for the module.
        key: Metadata string to return

        return: The item within the module index.
        """

        return mod[str(module_id)][key]

    @staticmethod
    def _rename_param_dict(module):
        """ Rewrites the param dict to use block names.

        module: Module dict object.

        return: Updated param dict.
        """

        tmp = {k: v["isParam"] for k, v in module['blocks'].items() if v["isParam"]}
        for param, n in zip(tmp.keys(), range(0, len(tmp))):
            module['parameters'][param] = \
                module['parameters'].pop('param_{}'.format(n), None)

    @staticmethod
    def _get_block_name(blocks, number):
        """ Determines the name of the block used in connections.

        blocks: Dictionary with block names and positions.
        number: Numerical index.

        return: Block name.
        """

        block = int(number)
        tmp = {k: v["position"] for k, v in blocks.items()}

        block_name = ""
        for key, value in tmp.items():
            if isinstance(value, int):
                if block == value:
                    block_name = key
            if isinstance(value, list):
                if block in value:
                    block_name = key

        return block_name

    @staticmethod
    def _get_color_name(color_id):
        """ Determines the longform name of a color id.

        color_id: The id for the color.

        return: The string that matches the passed color_id.
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

    def _add_connections(self, modules, connections):
        """ Appends all applicable connections to each module.

        modules: List of modules in a patch.
        connections: List of connections in a patch.

        return: Module object.
        """

        for conn in connections:
            out_mod, out_block = conn["source"].split(".")
            in_mod, in_block = conn["destination"].split(".")
            data = "{}.{} > {}% > {}.{}".format(
                modules[int(out_mod)]["type"] if modules[int(out_mod)]["name"] == ""
                    else modules[int(out_mod)]["name"],
                self._get_block_name(modules[int(out_mod)]["blocks"], out_block),
                conn["strength"],
                modules[int(in_mod)]["type"] if modules[int(in_mod)]["name"] == ""
                    else modules[int(in_mod)]["name"],
                self._get_block_name(modules[int(in_mod)]["blocks"], in_block)
            )
            modules[int(out_mod)]["connections"].append(data)

        return modules

    def _add_starred_param(self, modules, starred):
        """ Appends all applicable starred params to each module.

        modules: List of modules in a patch.
        starred: List of starred params in a patch.

        return: Module object.
        """

        for star in starred:
            data = "{}.{} CC {}".format(
                modules[star["module"]]["type"] if modules[star["module"]]["name"] == ""
                    else modules[star["module"]]["name"],
                self._get_block_name(modules[star["module"]]["blocks"], star["block"]),
                star["midi_cc"])
            modules[star["module"]]["starred"].append(data)

        return modules

    @staticmethod
    def _get_io(modules):
        """ Figures out audio and MIDI I/O for a quick-view.

        modules: List of modules in a patch.

        return: Module object.
        """

        type_dict = {k["number"]: k["type"] for k in modules}
        counter = list(type_dict.values())
        in_count = counter.count("Audio Input")
        out_count = counter.count("Audio Output")
        midi_count = sum("midi" in s.lower() for s in counter)
        stomp_count = counter.count("Stompswitch")

        if in_count == 0:
            in_type = None
        elif in_count > 1:
            in_type = []
        if out_count == 0:
            out_type = None
        elif out_count > 1:
            out_type = []
        if midi_count == 0:
            midi = None
        elif midi_count > 1:
            midi = []
        if stomp_count == 0:
            stomps = None
        elif stomp_count > 1:
            stomps = []

        for k, v in type_dict.items():
            if v == "Audio Input":
                if in_count == 1:
                    in_type = modules[k]["options"]["channels"].title()
                elif in_count > 1:
                    in_type.append(modules[k]["options"]["channels"].title())
            if v == "Audio Output":
                if out_count == 1:
                    out_type = modules[k]["options"]["channels"].title()
                elif out_count > 1:
                    out_type.append(modules[k]["options"]["channels"].title())
            if "midi" in v.lower():
                try:
                    if midi_count == 1:
                        midi = modules[k]["options"]["midi_channel"]
                    elif midi_count > 1:
                        midi.append(modules[k]["options"]["midi_channel"])
                except KeyError:
                    if midi_count == 1:
                        midi = None
            if v == "Stompswitch":
                if stomp_count == 1:
                    stomps = modules[k]["options"]["stompswitch"].title()
                elif stomp_count > 1:
                    stomps.append(modules[k]["options"]["stompswitch"].title())

        if midi_count > 1:
            midi = list(set(midi))
            if len(midi) == 1:
                midi = midi[0]
        if not midi:
            midi = None

        if stomp_count > 1:
            stomps = list(set(stomps))
            if len(stomps) == 1:
                stomps = stomps[0]
            else:
                stomps = sorted(stomps)
                stomps = json.dumps(stomps).replace('"', "")

        return {"inputs": in_type,
                "outputs": out_type,
                "midi_channel": midi,
                "stompswitches": stomps}

    def _calc_blocks(self, module):
        """ Calculates the number of blocks used for a given module,
        based on the current version in the module index and options
        selected.

        module: Module object.

        return: Block dict to overwrite blank.
        """

        idx = module['mod_idx']
        start = self._get_module_data(idx, 'min_blocks')
        stop = self._get_module_data(idx, 'max_blocks')
        opt = list(module['options'].items())
        d = list(self._get_module_data(idx, 'blocks').items())

        if idx == 0:
            blocks = [d[0], d[1], d[2]]
            for i, j in zip(opt, range(3, 6)):
                if i[1] == 'on':
                    blocks.append(d[j])
        elif idx == 1:
            if opt[0][1] == 'left':
                blocks = [d[0]]
            elif opt[0][1] == 'right':
                blocks = [d[1]]
            else:
                blocks = [d[0], d[1]]
        elif idx == 2:
            if opt[1][1] == 'left':
                blocks = [d[0]]
            elif opt[1][1] == 'right':
                blocks = [d[1]]
            else:
                blocks = [d[0], d[1]]
            if opt[0][1] == 'on':
                blocks.append(d[2])
        elif idx == 4:
            blocks = d
            # blocks = []
            # for i in range(1, opt[0][1] + 1):
            #     blocks.append(d[i - 1])
            # blocks.append(d[2])
            # if opt[2][1] == 'on':
            #     blocks.append(d[3])
            # for i in range(1, opt[1][1] + 1):
            #     blocks.append(d[3])
        elif idx == 5:
            blocks = [d[0]]
            if opt[1][1] == 'on':
                blocks.append(d[1])
            if opt[4][1] == 'on':
                blocks.append(d[2])
            if opt[5][1] == 'on':
                blocks.append(d[3])
            blocks.append(d[4])
        elif idx == 6:
            blocks = [d[0]]
            if opt[0][1] == 'on':
                blocks.append(d[1])
            if opt[1][1] == 'on':
                blocks.append(d[2])
            blocks.append(d[3])
            if opt[2][1] == 'on':
                blocks.append(d[4])
            blocks.append(d[5])
            blocks.append(d[6])
            if opt[4][1] == 'on':
                blocks.append(d[7])
            blocks.append(d[8])
            blocks.append(d[9])
        elif idx == 7:
            blocks = [d[0]]
            if opt[0][1] == 'stereo':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            if opt[0][1] == 'stereo':
                blocks.append(d[4])
        elif idx == 12:
            blocks = [d[0]]
            if opt[0][1] == 'on':
                blocks.append(d[1])
                blocks.append(d[2])
            blocks.append(d[3])
        elif idx == 13:
            blocks = [d[0]]
            if opt[1][1] == 'yes':
                blocks.append(d[2])
                blocks.append(d[3])
            else:
                blocks.append(d[1])
            blocks.append(d[4])
        elif idx == 14:
            blocks = [d[0]]
            if opt[1][1] == 'on':
                blocks.append(d[1])
            if opt[2][1] == 'on':
                blocks.append(d[2])
            blocks.append(d[3])
        elif idx == 16:
            blocks = d
            # blocks = []
            # for i in range(1, opt[0][1] + 1):
            #     blocks.append(d[i - 1])
            # blocks.append(d[1])
            # blocks.append(d[2])
            # blocks.append(d[3])
        elif idx == 19:
            blocks = [d[0]]
            if opt[0][1] == 'linked':
                blocks.append(d[1])
            else:
                blocks.append(d[2])
                blocks.append(d[3])
            blocks.append(d[4])
        elif idx == 20:
            blocks = d
            # blocks = []
            # for i in range(1, opt[1][1] + 1):
            #     blocks.append(d[i - 1])
            #     blocks.append(d[0])
            #     blocks.append(d[1])
            #     if opt[4][1] == 'on':
            #         blocks.append(d[2])
            #     if opt[7][1] == 'on':
            #         blocks.append(d[3])
        elif idx == 22:
            blocks = [d[0], d[1]]
            for i in range(0, opt[0][1] + 1):
                blocks.append(d[2])
            blocks.append(d[3])
        elif idx == 23:
            blocks = [d[0]]
            if opt[3][1] == 'stereo':
                blocks.append(d[1])
            blocks.append(d[2])
            if opt[0][1] == 'on':
                blocks.append(d[3])
            if opt[1][1] == 'on':
                blocks.append(d[4])
            if opt[2][1] == 'on':
                blocks.append(d[5])
            if opt[4][1] == 'external':
                blocks.append(d[6])
            blocks.append(d[7])
            if opt[3][1] == 'stereo':
                blocks.append(d[8])
        elif idx == 24:
            blocks = [d[0]]
            if opt[0] in ['bell', 'hi_shelf', 'low_shelf']:
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
        elif idx == 28:
            blocks = [d[0]]
            if opt[0] == 'yes':
                blocks.append(d[1])
                blocks.append(d[2])
            blocks.append(d[3])
        elif idx == 29:
            blocks = [d[0]]
            if opt[0] == '2in->2out':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            blocks.append(d[5])
            blocks.append(d[6])
            if opt[0][1] != '1in->1out':
                blocks.append(d[7])
        elif idx == 30:
            blocks = [d[0], d[1], d[2]]
            if opt[7][1] == 'yes':
                blocks.append(d[3])
            blocks.append(d[4])
            if opt[1][1] == 'on':
                blocks.append(d[5])
                blocks.append(d[6])
            if opt[5][1] == 'yes':
                blocks.append(d[7])
            blocks.append(d[8])
        elif idx == 31:
            blocks = d
            # blocks = []
            # for i in range(1, opt[0][1] + 1):
            #     blocks.append(d[i - 1])
            # blocks.append(d[1])
            # blocks.append(d[2])
        elif idx == 32:
            blocks = d
            # blocks = [d[0], d[1]]
            # for i in range(1, opt[0][1] + 1):
            #     blocks.append(d[i - 1])
        elif idx == 33:
            blocks = d
            # blocks = []
            # for i in range(1, opt[0][1] + 1):
            #     blocks.append(d[i - 1])
            # blocks.append(d[1])
            # blocks.append(d[2])
        elif idx == 34:
            blocks = d
            # blocks = [d[0], d[1]]
            # for i in range(1, opt[0][1] + 1):
            #     blocks.append(d[i - 1])
        elif idx == 36:
            blocks = [d[0]]
            if opt[0][1] == 'on':
                blocks.append(d[1])
            blocks.append(d[2])
        elif idx == 37:
            blocks = [d[0], d[1]]
            if opt[0][1] == 'on':
                blocks.append(d[2])
            blocks.append(d[3])
        elif idx == 39:
            blocks = []
            if opt[1][1] == 'on':
                blocks.append(d[0])
            blocks.append(d[1])
        elif idx == 40:
            blocks = [d[0]]
            if opt[2][1] == '2in-2out':
                blocks.append(d[1])
            blocks.append(d[2])
            if opt[0][1] == 'on':
                blocks.append(d[3])
            if opt[1][1] == 'on':
                blocks.append(d[4])
            if opt[3][1] == 'external':
                blocks.append(d[5])
            blocks.append(d[6])
            if opt[2][1] != '1in->1out':
                blocks.append(d[7])
        elif idx == 41:
            blocks = [d[0]]
            if opt[0][1] == '2in->2out':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            if opt[0][1] != '1in-1out':
                blocks.append(d[5])
        elif idx == 42:
            blocks = [d[0]]
            if opt[0][1] == '2in->2out':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            if opt[1][1] == 2:
                blocks.append(d[5])
                blocks.append(d[6])
            blocks.append(d[7])
            blocks.append(d[8])
            if opt[0][1] != '1in->1out':
                blocks.append(d[9])
        elif idx == 43:
            blocks = [d[0]]
            if opt[0][1] == '2in->2out':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            blocks.append(d[5])
            blocks.append(d[6])
            blocks.append(d[7])
            if opt[0][1] != '1in->1out':
                blocks.append(d[8])
        elif idx == 47:
            blocks = [d[0], d[1], d[2], d[3]]
            if opt[1][1] == 'on':
                blocks.append(d[4])
                blocks.append(d[5])
            blocks.append(d[6])
            blocks.append(d[7])
        elif idx == 48:
            blocks = [d[0]]
            if opt[0][1] == 'linked':
                blocks.append(d[1])
            else:
                blocks.append(d[2])
                blocks.append(d[3])
            blocks.append(d[4])
        elif idx == 53:
            if opt[0][1] == 'haas':
                blocks = [d[0], d[3], d[4], d[5]]
            else:
                blocks = [d[0], d[1], d[2], d[4], d[5]]
        elif idx == 56:
            blocks = [d[0]]
            if opt[0][1] == 'enabled':
                blocks.append(d[1])
        elif idx == 57:
            blocks = [d[0]]
            if opt[0][1] == '2in->2out':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
        elif idx == 60:
            blocks = [d[0], d[1]]
            if opt[1][1] == 'on':
                blocks.append(d[2])
        elif idx == 64:
            if opt[0][1] == 'mono':
                blocks = [d[0], d[2], d[4], d[5]]
            else:
                blocks = d
        elif idx == 67:
            blocks = [d[0]]
            if opt[0][1] == 'stereo':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            blocks.append(d[5])
            blocks.append(d[6])
            if opt[0][1] != '1in>1out':
                blocks.append(d[7])
        elif idx == 68:
            if opt[0][1] == 'mono':
                blocks = [d[0], d[2]]
            else:
                blocks = d
        elif idx == 69:
            blocks = [d[0]]
            if opt[0][1] == 'stereo':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            blocks.append(d[5])
            blocks.append(d[6])
            blocks.append(d[7])
            if opt[0][1] != '1in>1out':
                blocks.append(d[8])
        elif idx == 70:
            blocks = [d[0]]
            if opt[0][1] == 'stereo':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            blocks.append(d[5])
            blocks.append(d[6])
            if opt[0][1] != '1in>1out':
                blocks.append(d[7])
        elif idx == 71:
            blocks = [d[0]]
            if opt[0][1] == 'stereo':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            if opt[0][1] != '1in>1out':
                blocks.append(d[5])
        elif idx == 72:
            blocks = [d[0]]
            if opt[0][1] == 'stereo':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            blocks.append(d[5])
            blocks.append(d[6])
            if opt[0][1] != '1in>1out':
                blocks.append(d[7])
        elif idx == 73:
            blocks = [d[0]]
            if opt[1][1] == 'off':
                blocks.append(d[1])
            else:
                blocks.append(d[2])
            if opt[2][1] == 'on':
                blocks.append(d[3])
            blocks.append(d[4])
            blocks.append(d[5])
        elif idx == 75:
            if opt[0][1] == '1in->1out':
                blocks = [d[0], d[2], d[3], d[4], d[5], d[6], d[7]]
            else:
                blocks = d
        elif idx == 76:
            blocks = d
            # mixer is difficult..
        elif idx == 79:
            blocks = [d[0]]
            if opt[0][1] == 'stereo':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            if opt[0][1] != '1in->1out':
                blocks.append(d[5])
        elif idx == 82:
            blocks = [d[0]]
            for i, j in zip(opt, range(1, 4)):
                if i[1] == 'enabled':
                    blocks.append(d[j])
        elif idx == 83:
            if opt[1][0] == 'mono':
                blocks = [d[0], d[2], d[3], d[4], d[5], d[6], d[7], d[8]]
            else:
                blocks = d
        elif idx == 84:
            blocks = [d[0], d[1]]
            for i, j in zip(opt, range(1, 5)):
                if i[0] == 'input':
                    continue
                if i[1] == 'enabled':
                    blocks.append(d[j])
        elif idx == 85:
            blocks = [d[0]]
            if opt[0][1] == 'on':
                blocks.append(d[1])
                blocks.append(d[2])
            blocks.append(d[3])
        elif idx == 87:
            blocks = [d[0]]
            if opt[0][1] == 'enabled':
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            blocks.append(d[5])
            if opt[2][1] == 'on':
                blocks.append(d[6])
            blocks.append(d[7])
        elif idx in [3, 8, 9, 10, 11, 15, 17, 18, 21, 25,
                     26, 27, 35, 38, 44, 45, 46, 49, 50,
                     51, 52, 54, 55, 58, 59, 61, 62, 63,
                     65, 66, 74, 76, 77, 78, 80, 81, 86]:
            blocks = d
        else:
            raise ValueError('No module found')

        if len(blocks) < start:
            raise ValueError('Block count cannot be below the minimum')
        elif len(blocks) > stop:
            raise ValueError('Block count cannot be above the maximum')
        else:
            return dict(blocks)
