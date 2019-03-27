#!/usr/bin/env python3
import csv
import click

def read_years(years_file_name):
	"""
	Create a dictionary to map species/longitude/latitude to a year.
	"""
	years = {} 
	with open(years_file_name, encoding="utf-8-sig") as years_file:
		data = csv.DictReader(years_file, dialect="excel")
		for row in data:
			triple = (row['scientificName'], row['decimalLatitude'], row['decimalLongitude'])
			if triple in years:
				print("Warning: found multiple entries for: {}".format(triple))
			years[triple] = row['year']
	return years

def add_years(target_file_name, years, output_file_name):
	"""
	Loop over rows of target files and add year column if found
	"""
	with open(target_file_name, encoding="utf-8-sig") as target_file:
		with open(output_file_name,'w', encoding="utf-8-sig") as output_file:
			with open("missing.txt", 'w') as missing_file:
				data = csv.DictReader(target_file, dialect="excel")
				writer = csv.writer(output_file, dialect="excel", quoting=csv.QUOTE_MINIMAL)
				## Write target header to output csv
				write.writerow(data.fieldnames)

				## Loop over target data and add year if found
				## If not found: add a missing.txt line
				## Write new row to output csv
				for row in data:
					triple = (row['Species'], row['latitude'], row['longitude'])
					current_row = row.values()
					if triple in years:
						year = years[triple]
					else:
						year = ''
						print(triple, file=missing_file)
					newrow = current_row + (year,)
					writer.writerow(newrow)



@click.command()
@click.argument('years_file',
				required=True,
				type=click.Path(exists=True)
)
@click.argument('target_file',
				required=True,
				type=click.Path(exists=True)
)
@click.option('-o', '--output_file',
				required=True,
				help="Output CSV file",
				type=click.Path()
)
def main(years_file, target_file, output_file):
	"""
	Adds a "date" (year) column
	"""
	years_dict = read_years(years_file)
	add_years(target_file, years_dict, output_file)

if __name__ == '__main__':
	main()
