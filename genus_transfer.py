
import csv
import click

def read_names(name_file):
    name_dict = {}
    with open(name_file, encoding="utf-8") as nf:
        data = csv.DictReader(nf, dialect="excel")
        for row in data:
            if row['Species'] not in name_dict:
                name_dict[row['Species']] = (row['Order'], row['Family'], row['Genus'])
                
    return name_dict
                
def fill_out(target_file, name_dict):
    missing_names = []
    new_data = []
    with open(target_file, encoding="utf-8") as tf:
        data = csv.DictReader(tf, dialect="excel")        
        for row in data:
            if not row['Order']:
                keyName = row['tname']
                if keyName in name_dict:
                    row['Order'] = keyName[0]
                    row['Family'] = keyName[1]
                    row['Genus'] = keyName[2]
                else:
                    missing_names.append(keyName)
            new_data.append(row)
                
        return (new_data, missing_names)

def write_output(output):
    with open("output.csv", 'w', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
        for row in output:
            writer.writerow(row)

    
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
    names = read_names(name_file)
    (new_data, missing_names) = fill_out(target_file, names)
    for row in new_data:
        print(new_data)
    write_output(new_data)

    
if __name__ == '__main__':
    main()
