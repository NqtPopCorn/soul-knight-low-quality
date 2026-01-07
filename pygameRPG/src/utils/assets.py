

def get_asset_path(filename):
    """
    Get the full path to an asset file.
    :param filename: Name of the asset file
    :return: Full path to the asset file
    """
    import os
    return os.path.join('assets', filename)