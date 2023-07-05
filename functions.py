import hashlib
import logging
import os
import shutil
import time


def configure_logging(log_file_name: str = None) -> None:
    """
    Configures logging to write messages to console and to a file with a given `lig_file_name`.

    Args:
        log_file_name (str): The name or path of the log file. Defaults to "mylog.log" if no filename is provided.
    Returns:
        None
    """
    if log_file_name is None:
        log_file_name = "mylog.log"

    log_file_path = get_log_file_path(log_file_name)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )


def get_log_file_path(log_file_name: str) -> str:
    """
    Returns the full file path for `log_file_name`.

    Args:
        log_file_name (str): The name or path of the log file.
    Returns:
        str: The full file path for the log file.
    """
    if os.path.isabs(log_file_name):
        return log_file_name
    else:
        project_folder = os.path.realpath(os.path.dirname(__file__))
        return os.path.join(project_folder, log_file_name)


def calculate_md5(file_path: str) -> str:
    """
    Calculates the MD5 signature of a file accessible via `file_path`.

    Args:
        file_path (str): The path of the input file.

    Returns:
        str: The MD5 signature of the file.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def delete_item(item_path: str) -> None:
    """
    Deletes a file or a directory at the specified `item_path`.

    Args:
        item_path (str): The path of the file or directory to delete.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified item path is not found.
        PermissionError: If permission is denied to delete the item.
        NotADirectoryError: If the item path is not a directory.
        OSError: If an error occurs while deleting the item.
    """

    try:
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
        logging.info(f"[-] Item {item_path} removed successfully")

    except FileNotFoundError:
        logging.info(f"[!] Unable to delete {item_path}: not found")
    except PermissionError:
        logging.info(f"[!] Unable to delete {item_path}: permission denied")
    except NotADirectoryError:
        logging.info(f"[!] Unable to delete {item_path}: not a directory")
    except OSError as error:
        logging.info(f"[!] Unable to delete {item_path}: {str(error)}")


def walk_folder_content(folder_path) -> list:
    """
    Recursively walks through `folder_path` and its subfolders to gather
    the relative paths of all files and directories.

    Args:
        folder (str): The path to the root folder.

    Returns:
        list: A list containing the paths of all files and directories within the specified folder and its subfolders.
    """
    content = []
    for root, dirs, files in os.walk(folder_path):
        relative_dir = os.path.relpath(root, folder_path)
        content.extend([os.path.join(relative_dir, item)
                       for item in files + dirs])
    return content


def delete_extra_items_from_replica(source_folder: str, replica_folder: str) -> None:
    """
    Deletes from `replica_folder` files and directories that don't exist in `source_folder`.

    Args:
        source_folder (str): Path to source folder
        replica_folder (str): Path to replica folder

    Returns:
        None
    """

    source_items = walk_folder_content(source_folder)
    replica_items = walk_folder_content(replica_folder)

    for item in replica_items:
        if item not in source_items:
            item_real_path = os.path.join(replica_folder, item)
            delete_item(item_real_path)


def copy_item(source_path: str, replica_path: str) -> None:
    """
    Copies a file or directory from `source_path` to `replica_path`.

    Args:
        source_path (str): The path of the source file or directory.
        replica_path (str): The path where the source item should be copied to.

    Returns:
        None
    """

    try:
        if os.path.isfile(source_path):
            shutil.copy2(source_path, replica_path)
            source_md5 = calculate_md5(source_path)
            replica_md5 = calculate_md5(replica_path)
            if source_md5 == replica_md5:
                logging.info(
                    f"[+] Item {source_path} copied [Integrity verified]")
            else:
                logging.info(
                    f"[!] Item {source_path} copied [Integrity compromised]")
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, replica_path)
            logging.info(
                f"[+] Item {source_path} copied to {replica_path} successfully.")
    except FileNotFoundError:
        logging.info(f"[!] Item {source_path} not found.")
    except PermissionError:
        logging.info(f"[!] Permission denied to copy item {source_path}.")
    except OSError as error:
        logging.info(f"[!] Error copying item: {str(error)}")


def copy_new_from_source_to_replica(source_folder: str, replica_folder: str) -> None:
    """
    Copies new files and directories from `source_folder` to `replica_folder`.

    Args:
        source_folder (str): The path to the source folder.
        replica_folder (str): The path to the replica folder.

    Returns:
        None
    """

    source_items = walk_folder_content(source_folder)
    replica_items = walk_folder_content(replica_folder)

    for item in source_items:
        if item not in replica_items:
            source_path = os.path.join(source_folder, item)
            replica_path = os.path.join(replica_folder, item)
            if os.path.isdir(source_path):
                replica_subfolder = os.path.join(replica_folder, item)
                replica_path = os.path.join(replica_folder, replica_subfolder)
            copy_item(source_path, replica_path)


def check_path_validity(path) -> None:
    """
    Checks the validity of a given `path`.

    Args:
        path (str): The path to be checked.

    Returns:
        None

    Raises:
        ValueError: If the path does not exist or is not a valid directory.
    """
    call_to_action = "Please enter a valid path in order to perform synchronization."
    if not os.path.exists(path):
        raise ValueError(f"Folder '{path}' does not exist. {call_to_action}")
    elif not os.path.isdir(path):
        raise ValueError(
            f"'{path}' is not a valid folder path. {call_to_action}")


def sync_folders(source_folder: str, replica_folder: str, sync_interval: int = None) -> None:
    """
    Synchronizes the contents of `source_folder` and `replica_folder` at a given `sync_interval`,
    so that the replica folder and its content become a full, identical copy of the source.

    Args:
        source_folder (str): The path to the source folder.
        replica_folder (str): The path to the replica folder.
        sync_interval (int, optional): The time interval (in seconds) between synchronization attempts. Defaults to None.

    Returns:
        None

    Raises:
        ValueError: If either the source_folder or replica_folder is invalid.
    """
    try:
        check_path_validity(source_folder)
        check_path_validity(replica_folder)
    except ValueError as error:
        logging.info(f"Error: {error}")
        return

    while True:
        delete_extra_items_from_replica(source_folder, replica_folder)
        copy_new_from_source_to_replica(source_folder, replica_folder)
        if sync_interval is not None:
            time.sleep(sync_interval)
        else:
            break
