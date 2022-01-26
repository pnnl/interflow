import yaml
import pkg_resources


def read_config(name: str, file_number: str):
    """Reads file paths from configuration yaml file.

        :param name:                    The name of the specific module for the input paramater data or "baseline" for
                                        the baseline data.
        :type name:                     str

        :param file_number:             file number associated with module name or baseline data (file1 or file2)
        :type file_number:              str

        :return:                        path to data as a string

        """

    # open configuration file
    config_file = 'data/configuration_data/config.yml'
    with open(config_file) as file:
        config_dict = yaml.safe_load(file)

    # determine file path
    file_path = config_dict[name][file_number]['path']

    return file_path
