import os
import glob
import argparse


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
    parser.add_argument('--action', type=str, default='list', choices=['list', 'delete-files'],
                        help='Action to perform')
    return parser.parse_args()


def delete_files(files):
    for file in files:
        os.remove(file)
    print("Files deleted successfully.")


if __name__ == '__main__':
    args = get_parameters()

    files = list_files_by_size_descending(args.folder, args.min_size, args.extension)
    total_size = sum(os.path.getsize(file) for file in files)
    total_files = len(files)

    if args.action == 'list':
        print(
            f"Listing files in {args.folder} larger than {format_size(args.min_size)} bytes with extension *.{args.extension}")
        for file in files:
            print(f"{file}: {format_size(os.path.getsize(file))}")
        print(f"Total size: {format_size(total_size)}")
        print(f"Total number of files: {total_files}")

    elif args.action == 'delete-files':
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
