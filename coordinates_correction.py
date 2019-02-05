#!/usr/bin/env python3
import csv
import click

def read_names(coords_file_name):
	"""
	Read a data file and get `Species` names with `latitude`, longitude`.
	"""
	coordinates = [] 
	with open(coords_file_name, encoding="utf-8") as coords_file:
		data = csv.DictReader(coords_file, dialect="excel")
		for row in data:
			tripple = (row['Species'], row['latitude'], row['longitude'])
				
	return coordinates

def add_coordinates(target_file_name, coordinates, output_file_name):
	with open(target_file_name, encoding="utf-8") as target_file:
		with open(output_file_name,'w', encoding="utf-8") as output_file:
			data = csv.DictReader(target_file, dialect="excel")
			writer = csv.writer(output_file, dialect="excel", quoting=csv.QUOTE_MINIMAL)
			for row in data:
				tripple = (row['Species'], row['latitude'], row['longitude'])
				if tripple in coordinates:
					longitude_correct = str(-float(row['longitude']))
					row['longitude'] = longitude_correct
				writer.writerow(row.values())
					
					
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
	Correct for incorrect sign on coordinates (longitude)
	"""
	coords = read_names(coords_file)
	add_coordinates(target_file, coords, output_file)
	
	
if __name__ == '__main__':
	main()
