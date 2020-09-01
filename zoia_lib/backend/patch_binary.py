import json
import struct

from zoia_lib.backend.patch import Patch
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
            - Page number
            - Old color value
            - New color value
            - Grid position
            - Number of parameters
            - Options 1
            - Options 2
            - Parameter values
        - Connection count
          - For each connection:
            - Connection values and strength (as a %)
        - Number of pages and their names
        - Number of starred parameters
          - For each param:
            - Parameter name (not yet implemented)
            - Parameter value

        pch_data: The binary to be parsed and analyzed.

        return: A formatted JSON that can be shown in the frontend.
        """

        # Massive credit to apparent1 for figuring this stuff out.
        # They did all the heavy lifting.

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
                "name": self._qc_name(pch_data[(curr_step+(size-4))*4:
                                               (curr_step+(size-4))*4+16]),
                "cpu": self._get_module_data(data[curr_step + 1], "cpu"),
                "type": self._get_module_data(data[curr_step + 1], "name"),
                "page": int(data[curr_step + 3]),
                "position": [x for x in range(
                    int(data[curr_step + 5]),
                    int(data[curr_step + 5]) + self._get_module_data(
                        data[curr_step + 1], "max_blocks"))],
                "old_color": self._get_color_name(data[curr_step + 4]),
                "new_color": "" if skip_real else self._get_color_name(
                    colors[i]),
                "parameters": data[curr_step + 6],
                "options": {},
                "options_copy": self._get_module_data(data[curr_step + 1], "options"),
                "options_list": list(
                    bytearray(pch_data[(curr_step+8)*4:(curr_step+8)*4+4])) + list(
                    bytearray(pch_data[(curr_step+9)*4:(curr_step+9)*4+4])),
                "connections": []
            }

            # Create parameter keys if they exist
            for param in range(curr_module["parameters"]):
                curr_module["param_{}".format(param)] = data[curr_step + param + 10]

            # Select appropriate options from matrix
            v = 0
            for opt in list(curr_module["options_copy"]):
                if not opt:
                    continue
                option = curr_module["options_list"][v]
                value = curr_module["options_copy"][opt][option]
                curr_module["options"][opt] = value
                v += 1

            # Remove extra keys from module dict
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
            curr_param = {
                "name": self._qc_name(pch_data[(curr_step+1)*4:
                                               (curr_step+1)*4+16]),
                "value": data[curr_step + 1]
            }
            starred.append(curr_param)
            curr_step += 1

        colours = []
        # Extract the colors of each module in the patch.
        for m in range(len(modules)):
            curr_color = data[curr_step + 1]
            colours.append(curr_color)
            curr_step += 1

        # Prepare a dict to pass to the frontend.
        json_bin = {
            "name": name,
            "modules": self._add_connections(modules, connections),
            # "connections": connections,
            "pages": pages,
            "starred": starred,
            # "colours": colours
            "meta": {
                "name": name,
                "cpu": round(sum([k["cpu"] for k in modules]), 2),
                "n_modules": len(modules),
                "n_connections": len(connections),
                "n_pages": n_pages,
                "n_starred": len(starred)
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
        """ Determines metadata about a module

        module_id: The id for the module.
        key: Metadata string to return

        return: The item within the module index.
        """

        return mod[str(module_id)][key]

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

    @staticmethod
    def _add_connections(modules, connections):
        """ Appends all applicable connections to each module.

        modules: List of modules in a patch.
        connections: List of connections in a patch.

        return: Module object.
        """

        for conn in connections:
            out_mod, out_block = conn["source"].split(".")
            in_mod, in_block = conn["destination"].split(".")
            data = {
                "out_block": int(out_block),
                "in_mod": int(in_mod),
                "in_block": int(in_block),
                "strength": conn["strength"]
            }
            modules[int(out_mod)]["connections"].append(data)

        return modules
