import yaml
import pkg_resources


def read_config():
    """Reads file path from configuration yaml file.

        :return:                        path to input data as a string

        """

    # open configuration file
    config_file = 'flow/data/config.yml'
    with open(config_file) as file:
        config_dict = yaml.safe_load(file)

    # determine file path
    file_path = config_dict['input_data']['path']

    return file_path
