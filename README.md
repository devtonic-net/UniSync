# UniSync CLI App

UniSync is a command-line interface (CLI) application that synchronizes two folders, maintaining a full and identical copy of the source folder at the replica folder.

## Usage

To use UniSync, follow the instructions below:

- Clone/download this repository to your local machine.

- Open a terminal and navigate to the project directory.

- Run the UniSync application by executing the `unisync.py` file:

```python
python unisync.py -s [source_folder] -r [replica_folder] [-i SYNC_INTERVAL] [-l LOG_FILE]
```

## Command-line Arguments

The UniSync application accepts the following command-line arguments:

- -s, --source [source_folder]: Specifies the path to the source folder.
- -r, --replica [replica_folder]: Specifies the path to the replica folder.
- -i, --interval [SYNC_INTERVAL] (optional): Specifies the interval (in seconds) to wait before resynchronizing the folders. If not provided, UniSync will run once and then exit.
- -l, --logfile [LOG_FILE] (optional): Specifies the name of the logging file. If not provided, the details about the creation, copying, and removal operations will be saved to `mylog.log`.

**Note:** The -s/--source and -r/--replica arguments are required.

Examples

## Here are a few examples of how to use UniSync

- Synchronize the folders once and exit:

```python
python unisync.py -s /path/to/source/folder -r /path/to/replica/folder
```

- Synchronize the folders and wait for 60 seconds before resyncing:

```python
python unisync.py -s /path/to/source/folder -r /path/to/replica/folder -i 60
```

- Synchronize the folders and specify a custom log file name:

```python
python unisync.py -s /path/to/source/folder -r /path/to/replica/folder -l custom.log
```

- Synchronize the folders every 3 minutes and specify a custom log file name:

```python
python unisync.py -s /path/to/source/folder -r /path/to/replica/folder -i 180 -l custom.log
```

**Happy synchronizing!**
