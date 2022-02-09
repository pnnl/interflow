import yaml
import pkg_resources


def read_config(filetype: str):
    """Reads file path from configuration yaml file.

        :return:                        path to input data as a string

        """

    # open configuration file
    config_file = r"C:\Users\mong275\Local Files\Repos\flow\flow\data\config.yml"
    with open(config_file) as file:
        config_dict = yaml.safe_load(file)

    # determine file path
    file_path = config_dict[filetype]['path']

    return file_path
