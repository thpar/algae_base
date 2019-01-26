
import csv
import click

def read_names(name_file):
    """
    Read a data file and get `Species` names with `Order`, `Family` and `Genus`.
    This file can either be the original "Accepted Names" file, or
    any other CSV file, as long as column headers are respected.
    """
    name_dict = {}
    with open(name_file, encoding="utf-8") as nf:
        data = csv.DictReader(nf, dialect="excel")
        for row in data:
            if row['Species'] not in name_dict:
                name_dict[row['Species']] = (row['Order'], row['Family'], row['Genus'])
                
    return name_dict

def fill_out(target_file, name_dict):
    """
    Using the name dictionary, loop over the target file and
    try to fill out missing Order, Family and Genus data.

    Species (column `tname`) that are not in found in the name dictionary
    are added to the missing names list.
    """
    missing_names = []
    new_data = []
    with open(target_file, encoding="utf-8") as tf:
        data = csv.DictReader(tf, dialect="excel")        
        for row in data:
            if not (row['Order'] and row['Family'] and row['Genus']):
                keyName = row['tname']
                if keyName in name_dict:
                    keyData = name_dict[keyName]
                    row['Order'] = keyData[0]
                    row['Family'] = keyData[1]
                    row['Genus'] = keyData[2]
                else:
                    if keyName not in missing_names:
                        missing_names.append(keyName)
            new_data.append(row.values())
            header = row.keys()
                
        return (new_data, header, missing_names)

def write_output(new_data, header):
    """
    Write a CSV file with new data, using the same header.
    """
    with open("output.csv", 'w', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(new_data)

def write_missing_names(missing_names):
    """
    Write a simple list of missing species names.
    """
    with open("missing.txt", 'w') as missing_file:        
        for name in missing_names:
            missing_file.write(name+'\n')

    
@click.command()
@click.argument('name_file',
              required = True,
              type=click.Path(exists=True)
)
@click.argument('target_file',
                required = True,
                type=click.Path(exists=True)
)
def main(name_file, target_file):
    """
    NAME_FILE : CSV file containing accepted species names and data.

    TARGET_FILE : the file with missing data to be completed.
    """
    names = read_names(name_file)
    (new_data, header, missing_names) = fill_out(target_file, names)
    write_output(new_data, header)
    write_missing_names(missing_names)

    
if __name__ == '__main__':
    main()
