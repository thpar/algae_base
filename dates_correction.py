
´´´

    djgfsg

´´´







#!/usr/bin/env python3
import csv
import click

def read_names(dates_file_name):
	"""
	Read a data and get `Species` names with `latitude`, longitude`.
	"""
	dates = [] 
	with open(dates_file_name, encoding="utf-8") as dates_file:
		data = csv.DictReader(dates_file, dialect="excel")
		for row in data:
			tripple = (row['Species'], row['latitude'], row['longitude'])
			dates.append(tripple)
				
	return dates

def add_dates(target_file_name, dates, output_file_name):
	with open(target_file_name, encoding="utf-8") as target_file:
		with open(output_file_name,'w', encoding="utf-8") as output_file:
			data = csv.DictReader(target_file, dialect="excel")
			writer = csv.writer(output_file, dialect="excel", quoting=csv.QUOTE_MINIMAL)
			for row in data:
				tripple = (row['Species'], row['latitude'], row['longitude'])
				if tripple in dates:
					dates_correct = 'Species','latitude','longitude',.'year'
					
					
					
@click.command()
@click.argument('coords_file',
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
def main(coords_file, target_file, output_file):
	"""
	Adds a "date" (year) column
	"""
	coords = read_names(coords_file)
	add_coordinates(target_file, coords, output_file)
	
	
if __name__ == '__main__':
	main()
