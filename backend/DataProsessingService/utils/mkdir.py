import pathlib


def make_directory(directory):
    """
    This function perform creating directory
    :params directory: store path to make directory and subdirectory
    :return None:
    """

    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)