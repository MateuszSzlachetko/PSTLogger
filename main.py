from os import walk,path,makedirs
from fnmatch import filter
from datetime import datetime,date

root_path = 'C:\\'  # replace with the root path of the disk you want to scan
file_patterns = ['*.pst']
files  = []

def make_directory():
    directory_path = 'data'

    if not path.isdir(directory_path):
        makedirs(directory_path)

def look_for_files():
    for root, _, filenames in walk(root_path):
        for file_pattern in file_patterns:
            for filename in filter(filenames, file_pattern):
                file_path = path.join(root, filename)
                files.append(file_path)

def make_report(filename):
    with open(filename,'w') as report:
        for file in files:
            modification_time = path.getmtime(file)
            formatted_date = datetime.fromtimestamp(modification_time).strftime("%H:%M:%S %d.%m.%Y")
            report.write(f"File:    {file}\n")
            report.write(f"Last modified time:  {formatted_date}\n")
            report.write("\n")

            file_date = datetime.fromtimestamp(modification_time).date()

            current_date = date.today()

            if file_date.year == current_date.year and file_date.month == current_date.month and file_date.day == current_date.day:
                report.write("The file was modified today.\n\n")
            else:
                report.write("The file was not modified today.\n\n")

def main():
    make_directory()

    print("Loading...")
    look_for_files()

    filename = "data/raport-" + datetime.now().strftime("%H_%M_%S-%d_%m_%Y") + ".txt"  

    make_report(filename)

    input("\nPress any button to exit") 

if __name__ == "__main__":
    main()
