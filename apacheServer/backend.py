# The backend is responsible for taking the .csv data from the sensors and preparing them to be shwon in the website
import pandas as pd

def parseByTimeRange(df,timeRange,decimationFactor=0):
    """ Returns a smaller dataframe within the given time range

    Args:
        df : pandas dataframe with all the data
        timeRange : time range of new dataframe (string)
        decimationFactor : if 0, keep all the data, if 1, delete all. if 0.5, delete half
    """
    pass

def csv2pandas(csv):
    """Reads the csv and returns the pandas dataframe with it. Also cleans it
    
    Args:
        csv : file with data
    """
    df = pd.read_csv(csv)
    return df

if __name__ == "__main__":
    
    # Constant variables
    csv_file_name = 'sensor_data.csv'
    
    
    # get csv
    df = csv2pandas(csv_file_name)
    
    