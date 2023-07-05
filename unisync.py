import argparse
from functions import configure_logging, sync_folders


def main():
    argparser = argparse.ArgumentParser(
        prog="UniSync",
        description="UniSync synchronizes two folders (source and replica) and maintains a full, identical copy of source folder at replica folder")
    argparser.add_argument(
        "-s", "--source", help="Path to source folder", required=True)
    argparser.add_argument(
        "-r", "--replica", help="Path to replica folder", required=True)
    argparser.add_argument(
        "-i", "--interval", help="Interval (seconds) to wait before resync. If not provided, UniSync will run once and then exit", type=int)
    argparser.add_argument(
        "-l", "--logfile", help="Name of logging file. If not provided, the details about the creation/copying/removal operations will be saved to 'mylog.log'", type=str)
    args = argparser.parse_args()

    source_folder = args.source
    replica_folder = args.replica
    sync_interval = args.interval
    log_file = args.logfile

    configure_logging(log_file)
    sync_folders(source_folder, replica_folder, sync_interval)


if __name__ == "__main__":
    main()
