from os import walk, path, makedirs
from fnmatch import filter
from datetime import datetime, date
import csv

root_path = "E:\FR"  # replace with the root path of the disk you want to scan
file_patterns = ["*.pst"]
files = []
rows = []
MB = 1048576


def make_directory():
    directory_path = "data"

    if not path.isdir(directory_path):
        makedirs(directory_path)


def look_for_files():
    for root, _, filenames in walk(root_path):
        for file_pattern in file_patterns:
            for filename in filter(filenames, file_pattern):
                file_path = path.join(root, filename)
                files.append(file_path)


def extract_user_from_filepath(file_path):
    c = "\\"
    first_index = file_path.find(c)
    second_index = file_path.find(c, first_index + 1)
    third_index = file_path.find(c, second_index + 1)

    user = file_path[second_index + 1 : third_index]

    return user


def make_report():
    filename = "data/raport-" + datetime.now().strftime("%H_%M_%S-%d_%m_%Y") + ".csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        for file in files:
            modification_time = path.getmtime(file)
            formatted_date = datetime.fromtimestamp(modification_time).strftime(
                "%H:%M:%S %d.%m.%Y"
            )

            file_date = datetime.fromtimestamp(modification_time).date()

            current_date = date.today()

            if (
                file_date.year == current_date.year
                and file_date.month == current_date.month
                and file_date.day == current_date.day
            ):
                info = f"The file was modified today."
            else:
                info = f"The file was not modified today."

            file_size = path.getsize(file)
            file_size_mb = file_size / MB

            user = extract_user_from_filepath(file)

            rows.append([file, user, formatted_date, info, f"{file_size_mb} MB"])

        rows_sorted = sorted(rows, key=lambda row: path.getmtime(row[0]))
        for row in rows_sorted:
            writer.writerow(row)

    filename = (
        "data/raport-users-" + datetime.now().strftime("%H_%M_%S-%d_%m_%Y") + ".csv"
    )

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        rows_sorted = sorted(rows, key=lambda row: (row[1], path.getmtime(row[0])))
        for row in rows_sorted:
            writer.writerow(row)


def main():
    make_directory()

    print("Loading...")
    look_for_files()

    make_report()

    print("Success!")
    input("\nPress any button to exit")


if __name__ == "__main__":
    main()
