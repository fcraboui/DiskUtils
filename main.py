import os
import glob
import argparse
from collections import defaultdict


def list_files_by_size_descending(folder_path, min_size, extension):
    if extension == '*':
        pattern = os.path.join(folder_path, '*')
    else:
        pattern = os.path.join(folder_path, f'*.{extension}')

    files = glob.glob(pattern)
    files = [f for f in files if os.path.isfile(f) and os.path.getsize(f) >= min_size]
    files.sort(key=os.path.getsize, reverse=True)
    return files


def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def get_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='List files in a directory ordered by size.')
    parser.add_argument('--folder', type=str, default=os.path.expanduser('~/Downloads'),
                        help='Directory to list files from')
    parser.add_argument('--min-size', type=int, default=10 * 1024 * 1024, help='Minimum file size in bytes')
    parser.add_argument('--extension', type=str, default='*', help='File extension to filter by')
    parser.add_argument('--action', type=str, choices=['list', 'clean', 'size-by-extension', 'list-subdirs'],
                        help='Action to perform')
    args = parser.parse_args()
    if not args.action:
        parser.print_usage()
        exit(1)
    return args


def delete_files(files):
    for file in files:
        os.remove(file)
    print("Files deleted successfully.")


def get_total_size_by_extension(folder_path, min_size):
    pattern = os.path.join(folder_path, '*')
    files = glob.glob(pattern)
    files = [f for f in files if os.path.isfile(f) and os.path.getsize(f) >= min_size]

    size_by_extension = defaultdict(int)
    for file in files:
        ext = os.path.splitext(file)[1]
        size_by_extension[ext] += os.path.getsize(file)

    sorted_extensions = sorted(size_by_extension.items(), key=lambda x: x[1], reverse=True)
    for ext, total_size in sorted_extensions:
        print(f"Extension: {ext or 'No Extension'}, Total size: {format_size(total_size)}")


def list_subdirs_by_size_descending(folder_path):
    subdirs = [os.path.join(folder_path, d) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    subdir_sizes = []

    for subdir in subdirs:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(subdir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
        subdir_sizes.append((subdir, total_size))

    subdir_sizes.sort(key=lambda x: x[1], reverse=True)
    for subdir, total_size in subdir_sizes:
        print(f"Subdirectory: {subdir}, Total size: {format_size(total_size)}")


if __name__ == '__main__':
    args = get_parameters()

    if args.action == 'list':
        files = list_files_by_size_descending(args.folder, args.min_size, args.extension)
        total_size = sum(os.path.getsize(file) for file in files)
        total_files = len(files)
        print(
            f"Listing files in {args.folder} larger than {format_size(args.min_size)} bytes with extension *.{args.extension}")
        for file in files:
            print(f"{file}: {format_size(os.path.getsize(file))}")
        print(f"Total size: {format_size(total_size)}")
        print(f"Total number of files: {total_files}")

    elif args.action == 'clean':
        files = list_files_by_size_descending(args.folder, args.min_size, args.extension)
        total_size = sum(os.path.getsize(file) for file in files)
        total_files = len(files)
        print(
            f"Files to be deleted in {args.folder} larger than {format_size(args.min_size)} bytes with extension *.{args.extension}")
        for file in files:
            print(f"{file}: {format_size(os.path.getsize(file))}")
        print(f"Total size: {format_size(total_size)}")
        print(f"Total number of files: {total_files}")

        confirm = input("Are you sure you want to delete these files? (yes/no): ")
        if confirm.lower() == 'yes':
            delete_files(files)
        else:
            print("File deletion cancelled.")

    elif args.action == 'size-by-extension':
        get_total_size_by_extension(args.folder, args.min_size)

    elif args.action == 'list-subdirs':
        list_subdirs_by_size_descending(args.folder)