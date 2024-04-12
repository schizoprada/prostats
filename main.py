import pprint
import sys
import os
import json
import argparse
from termcolor import colored

def count_lines(file_path):
    total_lines = 0
    comment_lines = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith(('#', '//')):
                    comment_lines += 1
                elif line:
                    total_lines += 1
    except (UnicodeDecodeError, IOError):
        pass
    return total_lines, comment_lines

def process_directory(directory, recursive, output_file, sort_by, sort_order, filter_extensions):
    filetype_counts = {}
    total_lines_all = 0
    comment_lines_all = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file)
            extension = extension[1:] if extension else 'No Extension'
            if filter_extensions and extension.lower() not in [ext.lower() for ext in filter_extensions]:
                continue
            total_lines, comment_lines = count_lines(file_path)
            filetype_counts.setdefault(extension, {'total_lines': 0, 'comment_lines': 0})
            filetype_counts[extension]['total_lines'] += total_lines
            filetype_counts[extension]['comment_lines'] += comment_lines
            total_lines_all += total_lines
            comment_lines_all += comment_lines
        if not recursive:
            break
    
    if sort_by:
        sorted_counts = dict(sorted(filetype_counts.items(), key=lambda x: x[1][sort_by], reverse=sort_order == 'desc'))
    else:
        sorted_counts = filetype_counts
    
    if output_file:
        with open(output_file, 'w') as file:
            json.dump(sorted_counts, file, indent=4)
    
    return sorted_counts, total_lines_all, comment_lines_all

def main():
    parser = argparse.ArgumentParser(description='Count lines and comments for files and directories.')
    parser.add_argument('path', help='File path or directory path')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursively process subdirectories')
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('-s', '--sort', choices=['total_lines', 'comment_lines'], help='Sort results by total lines or comment lines')
    parser.add_argument('-d', '--order', choices=['asc', 'desc'], default='desc', help='Sort order (ascending or descending)')
    parser.add_argument('-f', '--filter', nargs='+', help='Filter results by file extensions')
    
    args = parser.parse_args()
    
    if os.path.isfile(args.path):
        total_lines, comment_lines = count_lines(args.path)
        _, extension = os.path.splitext(args.path)
        extension = extension[1:] if extension else 'No Extension'
        filetype_counts = {extension: {'total_lines': total_lines, 'comment_lines': comment_lines}}
        total_lines_all = total_lines
        comment_lines_all = comment_lines
    elif os.path.isdir(args.path):
        filetype_counts, total_lines_all, comment_lines_all = process_directory(args.path, args.recursive, args.output, args.sort, args.order, args.filter)
    else:
        print(colored(f"Invalid path: {args.path}", 'red'))
        sys.exit(1)
    
    for extension, counts in filetype_counts.items():
        total_lines = counts['total_lines']
        comment_lines = counts['comment_lines']
        print(colored(f"{extension}:", 'blue'))
        print(colored(f"  Total Lines: {total_lines}", 'green'))
        print(colored(f"  Comment Lines: {comment_lines}", 'yellow'))
    
    print(colored("Total Counts Across All Directories:", 'magenta'))
    print(colored(f"  Total Lines: {total_lines_all}", 'grey'))
    print(colored(f"  Comment Lines: {comment_lines_all}", 'red'))

if __name__ == '__main__':
    main()
