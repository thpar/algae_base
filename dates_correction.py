#!/usr/bin/env python3
import csv
import click

def read_years(years_file_name):
	"""
	Create a dictionary to map species/longitude/latitude to a list of years.
	"""
	years = {} 
	with open(years_file_name, encoding="utf-8-sig") as years_file:
		data = csv.DictReader(years_file, dialect="excel")
		for row in data:
			triple = (row['scientificName'], row['decimalLatitude'], row['decimalLongitude'])
			if triple not in years:
				years[triple] = []
			years[triple].append(row['year'])
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
				header = data.fieldnames + ["year",]
				writer.writerow(header)

				## Loop over target data and add year if found
				## If not found or if we have more matches than years: add a missing.txt line
				for row in data:
					triple = (row['Species'], row['latitude'], row['longitude'])
					current_row = tuple(row.values())
					if triple in years:
						if len(years[triple]) > 0:
							## Take and remove first year we found
							year = years[triple].pop(0)
						else:
							## We ran out of years for this triple
							print("Number of hits mismatch: {}".format(triple), file=missing_file)
							year = ''
					else:
						year = ''
						print("Triple not found: {}".format(triple), file=missing_file)
						
					## Write new row to output csv
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
