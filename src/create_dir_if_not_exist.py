def create_dir_if_not_exist(directory):    
    """
    Create a directory if it does not exist already.

    Parameters:
    ----------
    directory : str
        The directory where the contents of the zip file will be extracted.
    Returns:
    -------
    path to the newly created file
    """
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)
    return directory