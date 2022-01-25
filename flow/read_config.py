import yaml
import pkg_resources


def read_config(name: str, file_number: str):
    """Reads file paths from configuration yaml file.

        :param name:                    either name of module or "baseline"
        :type name:                     str

        :param file_number:             file number associated with module name or baseline data
        :type file_number:              str

        :return:                        path to data

        """
    config_file = 'data/configuration_data/config.yml'
    with open(config_file) as file:
        config_dict = yaml.safe_load(file)

    file_path = config_dict[name][file_number]['path']

    return file_path
