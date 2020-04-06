Purpose:
    A simple python script to compare two folders and output the difference into a CSV file
    Check out the code and run the tests to see how it works

config.yml
    configure two source folder to compare; the folder can be abosolute or relative path
    confgure the result csv file storage
    listFolder2: if you want to show the diff files of Folder2 in the CSV output file, use "True"
    listCommonFiles: if you want to show all the common files in the CSV output file, use "Ture"

run:
    python3 compFolders.py
    