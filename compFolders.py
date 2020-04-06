import os
import filecmp
import csv
import yaml

def read_config():
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
    return cfg["folder1"], cfg["folder2"], cfg["csv"], cfg["listFolder2"], cfg["listCommonFiles"]

def compare(folder1, folder2, output, listFolder2, listCommonFiles):
    # make path OS-agnostic
    folder1=folder1.replace('\\','/')   
    folder2=folder2.replace('\\','/')
    report =_recursive_dircmp(folder1, folder2)
    _write_to_csv(folder1, folder2, output, listFolder2, listCommonFiles, report)

def _str2bool(v):
    return v.lower() in ("true","True","TRUE", "yes", "Yes", "YES", "1")

def _recursive_dircmp(folder1, folder2, prefix='.'):
    print("===== start compare:")
    print(folder1)
    print(folder2)
    print(prefix)
    comparison=filecmp.dircmp(folder1, folder2)

    # The comparison results will be summarized in a dictionary with the keys left, right, and both. Each file analyzed will be formatted with a full filepath relative to the root folders compared (denoted as .) and the / path separator.
    data = {
        'left': [r'{}/{}'.format(prefix, i) for i in comparison.left_only],
        'right': [r'{}/{}'.format(prefix, i) for i in comparison.right_only],
        'both': [r'{}/{}'.format(prefix, i) for i in comparison.same_files],
        'both_diff': [r'{}/{}'.format(prefix, i) for i in comparison.diff_files],
    }

    for datalist in data.values():
        datalist.sort()

    if comparison.common_dirs:
        for folder in comparison.common_dirs:
            # compare common folder and add results to the report
            sub_folder1=os.path.join(folder1, folder)
            sub_folder2=os.path.join(folder2, folder)
            sub_report = _recursive_dircmp(sub_folder1,sub_folder2, prefix + "/"+folder)
            # add results from sub_report to main report
            for key, value in sub_report.items():
                data[key] += value
    print("----- end compare")
    return data

def _write_to_csv(folder1, folder2, output, listFolder2, listCommonFiles, report):
    """Write the comparison report to a CSV file for use in Excel."""

    filename = output
    with open(filename, 'w') as file:
        csv_writer = csv.writer(file, dialect='excel', lineterminator='\r')

        # Write header data to the first row
        headers = (
            "Files only in folder '{}'".format(folder1),
            "Files only in folder '{}'".format(folder2),
            "Files in both folders",
            "Files in both folders but different"
        )
        csv_writer.writerow(headers)

        # Order report data to match with headers
        data = (
            report['left'],
            report['right'] if _str2bool(listFolder2) else "",
            report['both'] if _str2bool(listCommonFiles) else "",
            report['both_diff'],
        )

        # Write comparison data row by row to the CSV
        row_index = 0
        row_max = max(len(column) for column in data)
        while row_index < row_max:
            values = []
            for column in data:
                # Use data from column if it exists, otherwise use None
                try:
                    values += [column[row_index]]
                except IndexError:
                    values += [None]

            csv_writer.writerow(values)
            row_index += 1


folder1, folder2, output, listFolder2, listCommonFiles =read_config()
compare(folder1, folder2, output, listFolder2, listCommonFiles)
print("Comparison is generated and output to " + output )