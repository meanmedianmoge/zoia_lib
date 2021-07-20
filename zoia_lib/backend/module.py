import sys


class Module:
    def __init__(self, version):
        """Base class for Module creation.

        enum {
          MODULE_SIZE_OFFSET = 0,    // size of serialized module including this int
          MODULE_ID_OFFSET = 1,
          MODULE_VERSION_OFFSET = 2,
          MODULE_PAGE_OFFSET = 3,
          MODULE_COLOUR_OFFSET = 4,
          MODULE_ORIGIN_OFFSET = 5,
          MODULE_NUMBER_OF_JACK_BIASES_OFFSET = 6,    // number of jack biases saved
          // the number of ints that saveable_data takes up will be this rounded up to the nearest
          // multiple of 4 and divided by 4. so if some saveable_data takes up 5 bytes, saveable_data
          // would have a size of 2 ints
          MODULE_SIZE_OF_SAVEABLE_DATA_IN_BYTES_OFFSET = 7,
          MODULE_OPTIONS_OFFSET = 8,                  // this is eight chars so 2 ints
          MODULE_CV_INPUT_JACK_BIASES_OFFSET = 10     // each cv_input jack bias gets it own int
                                               // then after this
                                               // SAVEABLE_DATA
                                               // MODULE_NAME  // 16 bytes, so 4 ints
        };
        """

        self.version = version
        self.module_dict = self.set_module()
        self.options_new = self.select_options()
        self.blocks_new = self.get_default_blocks()

    def set_module(self):
        """Creates dictionary from child module class."""
        return vars(self)

    def select_options(self):
        """Selects option for a module"""
        print("Selecting options for {}: ".format(self.name))
        options = {}
        for opt, values in self.options.items():
            print(opt, values)
            P1 = self._make_selection(values)
            options[opt] = P1
        return options

    @staticmethod
    def _make_selection(options):
        """Have the user select options for module-creation"""
        user_choice = input("")
        if str(user_choice) in str(options):
            return user_choice
        elif user_choice in ["quit", "exit", "leave"]:
            sys.exit()
        else:
            print("Please select an option")
            user_choice = input()
            if str(user_choice) in str(options):
                return user_choice
            else:
                print("Aborting the module creation process")
                sys.exit()

    def get_default_blocks(self):
        """Determines the blocks present after selecting module options"""
        tmp = {k: v for k, v in self.blocks.items() if v["isDefault"]}
        return tmp

    def get_params(self):
        """Use block/options to determine param count"""
        tmp = {k: v["isParam"] for k, v in self.blocks.items() if v["isParam"]}
        return len(tmp.keys())
