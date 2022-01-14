import json
import struct

from zoia_lib.backend.patch import Patch
from zoia_lib.backend.utilities import meipass
from zoia_lib.common import errors

with open(meipass("zoia_lib/common/schemas/ModuleIndex.json")) as f:
    mod = json.load(f)


class PatchBinary(Patch):
    """The PatchBinary class is a child of the Patch class. It is
    responsible for ZOIA patch binary analysis.
    """

    def __init__(self):
        """"""
        super().__init__()

    def parse_data(self, byt):
        """Parses the binary data of a patch for information relating
        to the patch. This information is collected into a string that
        is returned such that it can be displayed via the frontend.
        The returned data will specify the following:
        - Preset size
        - Patch name
        - Module count
          - For each module:
            - Module name
            - Module type
            - Module version
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

        byt: The binary to be parsed and analyzed.

        return: A formatted JSON that can be shown in the frontend.
        """

        # Massive credit to apparent1 for figuring this stuff out.
        # They did all the heavy lifting.

        if byt is None:
            raise errors.BinaryError(None)

        # Extract the string name of the patch.
        name = self._qc_name(byt[4:])

        # Unpack the binary data.
        data = struct.unpack("i" * int(len(byt) / 4), byt)
        pch_size = data[0]

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
                "category": self._get_module_data(data[curr_step + 1], "category"),
                "mod_idx": data[curr_step + 1],
                "name": self._qc_name(
                    byt[
                        (curr_step + (size - 4)) * 4: (curr_step + (size - 4)) * 4 + 16
                    ]
                ),
                "cpu": self._get_module_data(data[curr_step + 1], "cpu"),
                "type": self._get_module_data(data[curr_step + 1], "name"),
                "size": data[curr_step],
                "size_of_saveable_data": data[curr_step + 7],
                "version": data[curr_step + 2],
                "page": int(data[curr_step + 3]),
                "position": [
                    x
                    for x in range(
                        int(data[curr_step + 5]),
                        int(data[curr_step + 5])
                        + self._get_module_data(data[curr_step + 1], "min_blocks"),
                    )
                ],
                "old_color": data[curr_step + 4],
                "new_color": "" if skip_real else self._get_color_name(colors[i]),
                "options": {},
                "options_binary": {},
                "options_copy": self._get_module_data(data[curr_step + 1], "options"),
                "options_list": list(
                    bytearray(byt[(curr_step + 8) * 4: (curr_step + 8) * 4 + 4])
                )
                + list(
                    bytearray(byt[(curr_step + 9) * 4: (curr_step + 9) * 4 + 4])
                ),
                "params": int(data[curr_step + 6]),
                # also can be fetched from self._get_module_data(data[curr_step + 1], "params")
                "parameters": dict(
                    zip(
                        ["param_{}".format(str(x)) for x in range(data[curr_step + 6])],
                        [
                            round(data[curr_step + x + 10] / 65535, 2)
                            for x in range(data[curr_step + 6])
                        ],
                    )
                ),
                "blocks": [],
                "connections": [],
                "starred": [],
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
                    curr_module["options_binary"][opt] = option
                    v += 1
            except IndexError:
                raise errors.BinaryError(byt[:10], 101)

            # Combine colors into one key
            curr_module["color"] = (
                self._get_color_name(curr_module["old_color"])
                if curr_module["new_color"] == ""
                else curr_module["new_color"]
            )

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
                "source": "{}.{}".format(
                    int(data[curr_step + 1]), int(data[curr_step + 2])
                ),
                "destination": "{}.{}".format(
                    int(data[curr_step + 3]), int(data[curr_step + 4])
                ),
                "strength": int(data[curr_step + 5] / 100),
            }
            connections.append(curr_connection)
            curr_step += 5

        pages = []
        curr_step += 1
        # Extract the page data for each page in the patch.
        for k in range(data[curr_step]):
            curr_page = self._qc_name(
                byt[(curr_step + 1) * 4: (curr_step + 1) * 4 + 16]
            )
            pages.append(curr_page)
            curr_step += 4
        # Get number of pages and fill with blank strings
        n_pages = modules[-1]["page"] + 1 if len(modules) != 0 else 1
        while len(pages) < n_pages:
            pages += [""]

        starred = []
        curr_step += 1
        # Extract the starred parameters in the patch.
        for l in range(data[curr_step]):
            byte2 = struct.unpack(
                "hh", byt[(curr_step + 1) * 4: (curr_step + 1) * 4 + 4]
            )
            curr_param = {
                "module": byte2[0],
                "block": byte2[1] % 128,
                "midi_cc": int(round(byte2[1] / 128) - 1)
                if byte2[1] >= 128
                else "None",
            }
            starred.append(curr_param)
            curr_step += 1

        colors = []
        # Extract the colors of each module in the patch.
        for m in range(len(modules)):
            curr_color = data[curr_step + 1]
            colors.append(curr_color)
            curr_step += 1

        # Block information
        for module in modules:
            module["blocks"] = self._calc_blocks(module)
            module["position"] = [
                x
                for x in range(
                    module["position"][0], module["position"][0] + len(module["blocks"])
                )
            ]
            self._rename_param_dict(module)

        # Append data to module list
        modules = self._add_connections(modules, connections)
        modules = self._add_starred_param(modules, starred)

        # Prepare a dict to pass to the frontend.
        json_bin = {
            "name": name,
            "size": pch_size,
            "modules": modules,
            "connections": connections,
            "pages": pages,
            "starred": starred,
            "colors": colors,
            "meta": {
                "name": name,
                "cpu": round(sum([k["cpu"] for k in modules]), 2),
                "n_modules": len(modules),
                "n_connections": len(connections),
                "n_pages": n_pages,
                "n_starred": len(starred),
                "i_o": self._get_io(modules),
            },
        }

        return json_bin

    @staticmethod
    def _qc_name(name):
        try:
            name = str(name).split("\\")[0].split("'")[1]
        except IndexError:
            name = str(name).split("\\")[0]

        return name.split('b"')[-1]

    @staticmethod
    def _get_module_data(module_id, key):
        """Determines metadata about a module.

        module_id: The id for the module.
        key: Metadata string to return

        return: The item within the module index.
        """

        return mod[str(module_id)][key]

    @staticmethod
    def _rename_param_dict(module):
        """Rewrites the param dict to use block names.

        module: Module dict object.

        return: Updated param dict.
        """

        tmp = {k: v["isParam"] for k, v in module["blocks"].items() if v["isParam"]}
        for param, n in zip(tmp.keys(), range(0, len(tmp))):
            module["parameters"][param] = module["parameters"].pop(
                "param_{}".format(n), None
            )

    @staticmethod
    def _get_block_name(blocks, number):
        """Determines the name of the block used in connections.

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
        """Determines the longform name of a color id.

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
            15: "Mango",
        }[color_id]

        return color

    def _add_connections(self, modules, connections):
        """Appends all applicable connections to each module.

        modules: List of modules in a patch.
        connections: List of connections in a patch.

        return: Module object.
        """

        for conn in connections:
            out_mod, out_block = conn["source"].split(".")
            in_mod, in_block = conn["destination"].split(".")
            data = "{}.{} > {}% > {}.{}".format(
                modules[int(out_mod)]["type"]
                if modules[int(out_mod)]["name"] == ""
                else modules[int(out_mod)]["name"],
                self._get_block_name(modules[int(out_mod)]["blocks"], out_block),
                conn["strength"],
                modules[int(in_mod)]["type"]
                if modules[int(in_mod)]["name"] == ""
                else modules[int(in_mod)]["name"],
                self._get_block_name(modules[int(in_mod)]["blocks"], in_block),
            )
            modules[int(out_mod)]["connections"].append(data)

        return modules

    def _add_starred_param(self, modules, starred):
        """Appends all applicable starred params to each module.

        modules: List of modules in a patch.
        starred: List of starred params in a patch.

        return: Module object.
        """

        for star in starred:
            data = "{}.{} CC {}".format(
                modules[star["module"]]["type"]
                if modules[star["module"]]["name"] == ""
                else modules[star["module"]]["name"],
                self._get_block_name(modules[star["module"]]["blocks"], star["block"]),
                star["midi_cc"],
            )
            modules[star["module"]]["starred"].append(data)

        return modules

    @staticmethod
    def _get_io(modules):
        """Figures out audio and MIDI I/O for a quick-view.

        modules: List of modules in a patch.

        return: Module object.
        """

        type_dict = {k["number"]: k["type"] for k in modules}
        counter = list(type_dict.values())
        in_count = counter.count("Audio Input")
        out_count = counter.count("Audio Output")
        midi_count = sum("midi" in s.lower() for s in counter)
        stomp_count = counter.count("Stompswitch")
        cv_count = sum("cport" in s.lower() for s in counter)

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
        if cv_count == 0:
            cvs = None
        elif cv_count > 1:
            cvs = []

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
            if "cport" in v.lower():
                try:
                    if cv_count == 1:
                        cvs = (
                            modules[k]["type"]
                            .title()
                            .split("Cport")[-1]
                            .strip()
                        )
                    elif cv_count > 1:
                        cvs.append(
                            modules[k]["type"]
                            .split("Cport")[-1]
                            .strip()
                        )
                except KeyError:
                    if cv_count == 1:
                        cvs = None

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

        if cv_count > 1:
            cvs = list(set(cvs))
            if len(cvs) == 1:
                cvs = cvs[0]
        if not cvs:
            cvs = None

        return {
            "inputs": in_type,
            "outputs": out_type,
            "midi_channel": midi,
            "stompswitches": stomps,
            "cport": cvs,
        }

    def _calc_blocks(self, module):
        """Calculates the number of blocks used for a given module,
        based on the current version in the module index and options
        selected.

        module: Module object.

        return: Block dict to overwrite blank.
        """

        idx = module["mod_idx"]
        ver = module["version"]
        start = self._get_module_data(idx, "min_blocks")
        stop = self._get_module_data(idx, "max_blocks")
        opt = list(module["options"].items())
        d = list(self._get_module_data(idx, "blocks").items())

        if idx == 0:
            blocks = [d[0], d[1], d[2]]
            for i, j in zip(opt, range(3, 6)):
                if i[1] == "on":
                    blocks.append(d[j])
        elif idx == 1:
            if opt[0][1] == "left":
                blocks = [d[0]]
            elif opt[0][1] == "right":
                blocks = [d[1]]
            else:
                blocks = [d[0], d[1]]
        elif idx == 2:
            if opt[1][1] == "left":
                blocks = [d[0]]
            elif opt[1][1] == "right":
                blocks = [d[1]]
            else:
                blocks = [d[0], d[1]]
            if opt[0][1] == "on":
                blocks.append(d[2])
        elif idx == 4:
            blocks = []
            for i in range(1, opt[0][1] + 1):
                blocks.append(d[i - 1])
            blocks.append(d[32])
            if opt[2][1] == "on":
                blocks.append(d[33])
            for i in range(1, opt[1][1] + 1):
                blocks.append(d[i + 33])
        elif idx == 5:
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
        elif idx == 6:
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
        elif idx == 7:
            blocks = [d[0]]
            if opt[0][1] == "stereo":
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            if opt[0][1] == "stereo":
                blocks.append(d[4])
        elif idx == 12:
            blocks = [d[0]]
            if opt[0][1] == "on":
                blocks.append(d[1])
                blocks.append(d[2])
            blocks.append(d[3])
        elif idx == 13:
            blocks = [d[0]]
            if opt[1][1] == "yes":
                blocks.append(d[2])
                blocks.append(d[3])
            else:
                blocks.append(d[1])
            blocks.append(d[4])
        elif idx == 14:
            blocks = [d[0]]
            if opt[1][1] == "on":
                blocks.append(d[1])
            if opt[2][1] == "on":
                blocks.append(d[2])
            blocks.append(d[3])
        elif idx == 16:
            blocks = []
            for i in range(1, opt[0][1] + 1):
                blocks.append(d[i - 1])
            blocks.append(d[40])
            blocks.append(d[41])
            blocks.append(d[42])
        elif idx == 19:
            blocks = [d[0]]
            if opt[0][1] == "linked":
                blocks.append(d[1])
            else:
                blocks.append(d[2])
                blocks.append(d[3])
            blocks.append(d[4])
        elif idx == 20:
            blocks = []
            for i in range(1, opt[1][1] + 1):
                blocks.append(d[4 * (i - 1)])
                blocks.append(d[4 * (i - 1) + 1])
                if opt[4][1] == "on":
                    blocks.append(d[4 * (i - 1) + 2])
                if opt[7][1] == "on":
                    blocks.append(d[4 * (i - 1) + 3])
        elif idx == 22:
            blocks = [d[0]]
            for i in range(2, opt[0][1] + 1):
                blocks.append(d[i - 1])
            blocks.append(d[8])
        elif idx == 23:
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
        elif idx == 24:
            blocks = [d[0]]
            if opt[0][1] in ["bell", "hi_shelf", "low_shelf"]:
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
        elif idx == 28:
            blocks = [d[0]]
            if opt[0][1] == "yes":
                blocks.append(d[1])
                blocks.append(d[2])
            blocks.append(d[3])
        elif idx == 29:
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
        elif idx == 30:
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
        elif idx == 31:
            blocks = []
            for i in range(1, opt[0][1] + 1):
                blocks.append(d[i - 1])
            blocks.append(d[16])
            blocks.append(d[17])
        elif idx == 32:
            blocks = [d[0], d[1]]
            for i in range(1, opt[0][1] + 1):
                blocks.append(d[i + 1])
        elif idx == 33:
            blocks = []
            for i in range(1, opt[0][1] + 1):
                blocks.append(d[i - 1])
            blocks.append(d[16])
            blocks.append(d[17])
        elif idx == 34:
            blocks = [d[0], d[1]]
            for i in range(1, opt[0][1] + 1):
                blocks.append(d[i + 1])
        elif idx == 36:
            blocks = [d[0]]
            if opt[0][1] == "on":
                blocks.append(d[1])
            blocks.append(d[2])
        elif idx == 37:
            blocks = [d[0], d[1], d[2]]
            if opt[0][1] == "on":
                blocks.append(d[3])
            blocks.append(d[4])
        elif idx == 39:
            blocks = []
            if opt[1][1] == "on":
                blocks.append(d[0])
            blocks.append(d[1])
        elif idx == 40:
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
        elif idx == 41:
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
        elif idx == 42:
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
        elif idx == 43:
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
        elif idx == 47:
            blocks = [d[0], d[1], d[2], d[3]]
            if opt[1][1] == "on":
                blocks.append(d[4])
                blocks.append(d[5])
            blocks.append(d[6])
            blocks.append(d[7])
        elif idx == 48:
            blocks = [d[0]]
            if opt[0][1] == "linked":
                blocks.append(d[1])
            else:
                blocks.append(d[2])
                blocks.append(d[3])
            blocks.append(d[4])
        elif idx == 49:
            if ver >= 1:
                blocks = [d[0], d[1], d[3], d[4], d[5]]
            else:
                blocks = [d[0], d[1], d[2], d[5]]
        elif idx == 53:
            if opt[0][1] == "haas":
                blocks = [d[0], d[3], d[4], d[5]]
            else:
                blocks = [d[0], d[1], d[2], d[4], d[5]]
        elif idx == 56:
            blocks = [d[0]]
            if opt[0][1] == "enabled":
                blocks.append(d[1])
        elif idx == 57:
            blocks = [d[0]]
            if opt[0][1] == "2in->2out":
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
        elif idx == 60:
            blocks = [d[0], d[1]]
            if opt[1][1] == "on":
                blocks.append(d[2])
        elif idx == 64:
            if opt[0][1] == "mono":
                blocks = [d[0], d[2], d[4], d[5]]
            else:
                blocks = d
        elif idx == 67:
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
        elif idx == 68:
            if opt[0][1] == "mono":
                blocks = [d[0], d[2]]
            else:
                blocks = d
        elif idx == 69:
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
        elif idx == 70:
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
        elif idx == 71:
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
        elif idx == 72:
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
        elif idx == 73:
            blocks = [d[0]]
            if opt[1][1] == "off":
                blocks.append(d[1])
            else:
                blocks.append(d[2])
            if opt[2][1] == "on":
                blocks.append(d[3])
            blocks.append(d[4])
            blocks.append(d[5])
        elif idx == 75:
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
        elif idx == 76:
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
        elif idx == 79:
            blocks = [d[0]]
            if opt[0][1] == "stereo":
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            if opt[0][1] != "1in->1out":
                blocks.append(d[5])
        elif idx == 81:
            if opt[0][1] == "cv":
                blocks = [d[0]]
            else:
                blocks = [d[1]]
        elif idx == 82:
            blocks = [d[0]]
            if opt[0][1] == "enabled":
                blocks.append(d[1])
            if opt[1][1] == "enabled":
                blocks.append(d[2])
            if opt[2][1] == "enabled":
                blocks.append(d[3])
        elif idx == 83:
            if opt[1][0] == "mono":
                blocks = [d[0], d[2], d[3], d[4], d[5], d[6], d[7], d[8]]
            else:
                blocks = d
        elif idx == 84:
            blocks = [d[0]]
            if opt[1][1] == "enabled":
                blocks.append(d[1])
            if opt[2][1] == "enabled":
                blocks.append(d[2])
            if opt[3][1] == "enabled":
                blocks.append(d[3])
                blocks.append(d[4])
        elif idx == 85:
            blocks = [d[0]]
            if opt[0][1] == "on":
                blocks.append(d[1])
                blocks.append(d[2])
            blocks.append(d[3])
        elif idx == 102:
            blocks = [d[0]]
            if opt[0][1] == "enabled":
                blocks.append(d[1])
            blocks.append(d[2])
            blocks.append(d[3])
            blocks.append(d[4])
            blocks.append(d[5])
            if opt[2][1] == "on":
                blocks.append(d[6])
            blocks.append(d[7])
        elif idx == 103:
            if opt[0][1] == "bypass":
                blocks = [d[0]]
            elif opt[0][1] == "stomp aux":
                blocks = [d[1]]
            else:
                blocks = [d[2]]
        elif idx == 104:
            blocks = []
            for i in range(1, opt[0][1] + 1):
                blocks.append(d[i - 1])
            for i in range(1, opt[0][1] + 1):
                blocks.append(d[i + 7])
            blocks.append(d[16])
        else:
            blocks = d

        if len(blocks) < start:
            raise ValueError("Block count cannot be below the minimum")
        elif len(blocks) > stop:
            raise ValueError("Block count cannot be above the maximum")
        else:
            return dict(blocks)
