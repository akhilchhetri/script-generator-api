import rarfile


def extract_rar(archive_path, extract_to):
    """
    Extracts files from a .rar archive.

    Args:
        archive_path (str): Path to the .rar archive file.
        extract_to (str): Directory to extract the files to.
    """
    with rarfile.RarFile("./slices.rar", "r") as rf:
        rf.extractall(extract_to)


# Example usage:
archive_path = "./slices.rar"
extract_to = "./"

extract_rar(archive_path, extract_to)
