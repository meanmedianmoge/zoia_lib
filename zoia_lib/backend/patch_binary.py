import json
import struct

from zoia_lib.backend.patch import Patch
with open('zoia_lib/common/schemas/ModuleIndex.json', 'r') as f:
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
        - Patch name (real name)
        - Module count
          - For each module:
            - Module name (not yet implemented)
            - Module type
            - Page number
            - Old color value
            - New color value
            - Grid position
            - Number of parameters on the grid (deprecated)
            - Options 1 (needs to be expanded)
            - Options 2 (needs to be expanded)
        - Connection count
          - For each connection:
            - Connection values and strength (as a %)
        - Number of pages
          - For each page:
            - The page name (if it has one) (not yet implemented)
        - Number of starred parameters
          - For each param:
            - Parameter name (not yet implemented)
            - Parameter value
        - The color of each module

        pch_data: The binary to be parsed and analyzed.

        return: A formatted JSON that can be shown in the frontend.
        """

        # Massive credit to apparent1 for figuring this stuff out.
        # They did all the heavy lifting.

        # Extract the string name of the patch.
        try:
            name = str(pch_data[4:]).split("\\")[0].split("\'")[1]
        except IndexError:
            name = str(pch_data[4:]).split("\\")[0]

        # TODO Extract the string names of the pages of the patch.

        # Unpack the binary data.
        data = struct.unpack('i' * int(len(pch_data) / 4), pch_data)

        # Remove the binary identifier if it stuck.
        name = name.split("b\"")[-1]

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
                "options_1": "" if size <= 14 else data[curr_step + 8],
                "options_2": "" if size <= 14 else data[curr_step + 9]
            }
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
            curr_page = {
                "name": str(data[curr_step + 1])
            }
            pages.append(curr_page)
            curr_step += 4

        starred = []
        curr_step += 1
        # Extract the starred parameters in the patch.
        for l in range(data[curr_step]):
            curr_param = {
                "name": "",
                "value": data[curr_step + 1]
            }
            starred.append(curr_param)
            curr_step += 1

        colours = []
        # Extract the colors of each module in the patch.
        for m in range(len(modules)):
            curr_color = {
                "color": data[curr_step + 1]
            }
            colours.append(curr_color)
            curr_step += 1

        # Prepare a dict to pass to the frontend.
        json_bin = {
            "name": name,
            "modules": modules,
            "connections": connections,
            "pages": pages,
            "starred": starred,
            "colours": colours
        }

        return json_bin

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
