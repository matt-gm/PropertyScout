'''
Convert and CSV to Apache Parquet
Requires format .ini file
'''
import sys
from pyarrow.csv import read_csv

def city_csv_to_parqut(city, file_source, file_destination):
    df = read_csv(input_file=file_source)


if __name__ == "__main__":

    FILE_SOURCE = str(sys.argv[1])
    FILE_DESTINATION = str(sys.argv[2])

    DF = read_csv(input_file=FILE_SOURCE)
    COLUMNS_TO_DROP = ['ZIPcode', "AIN", "AssessorID", "PropertyLocation",
                       "SpecificUseDetail1", "SpecificUseDetail2", "totBuildingDataLines",
                       "YearBuilt", "Units", "RecordingDate", "HomeownersExemption",
                       "RealEstateExemption", "FixtureValue", "FixtureExemption",
                       "PersonalPropertyValue", "PersonalPropertyExemption", "isTaxableParcel?",
                       "netTaxableValue", "TotalExemption", "SpecialParcelClassification",
                       "AdministrativeRegion", "ParcelBoundaryDescription", "HouseFraction",
                       "StreetDirection", "UnitNo", "City", "rowID", "Location 1"]
    DF = DF.drop(*COLUMNS_TO_DROP)
    DF.write.parquet(FILE_DESTINATION)
