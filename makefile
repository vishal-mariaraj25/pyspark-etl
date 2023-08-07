# Makefile for ETL process

# Variables
SOURCE_DATA = data/source_data.csv
TRANSFORMED_DATA = data/transformed_data.csv

# Targets and dependencies
all: load

extract:
	python scripts/etl_script.py extract $(SOURCE_DATA) $(TRANSFORMED_DATA)

transform: extract
	python scripts/etl_script.py transform $(TRANSFORMED_DATA)

load: transform
	python scripts/etl_script.py load $(TRANSFORMED_DATA)
