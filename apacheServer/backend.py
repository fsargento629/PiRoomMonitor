# The backend is responsible for taking the .csv data from the sensors and preparing them to be shwon in the website
import pandas as pd

def parseByTimeRange(df,timeRange_days,decimationFactor=0):
    """ Returns a smaller dataframe within the given time range

    Args:
        df : pandas dataframe with all the data
        timeRange : time range of new dataframe (string)
        decimationFactor : if 0, keep all the data, if 1, delete all. if 0.5, delete half (NOT implemented)
    """
    # Calculate the end date as the maximum date in the DataFrame
    end_date = df['date'].max()

    # Calculate the start date by subtracting the time range in days from the end date
    start_date = end_date - pd.DateOffset(days=timeRange_days)

    # Filter the DataFrame to include data within the specified time range
    cropped_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    return cropped_df


def csv2pandas(csv):
    """Reads the csv and returns the pandas dataframe with it. Also cleans it.
    
    Args:
        csv : file with data
    """
    df = pd.read_csv(csv)
    # Define column names
    column_names = ["date", "temperature", "humidity"]

    # Assign the column names to the DataFrame
    df.columns = column_names
    
    # clean dates
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second
    
    # exclude outliers. Rules:
    # 1) if temperature or humidity are outside of nominal values (-5 to 50 for temp, 10 to 95 for hum)
    # 2) if temp or humidity show a large change (divided by time) since last entry
    
    # rule 1) based on absolute thresholds  for temperature and humidity
    df = df[(df['temperature'] > -5) & (df['temperature'] < 50) & (df['humidity'] > 10) & (df['humidity'] < 95)]
    
    
    # rule 2) based on derivative value

    # Calculate the time difference (in seconds) between consecutive rows
    df['time_diff'] = (df['date'] - df['date'].shift()).dt.total_seconds()

    # Calculate the derivative (rate of change) of temperature and humidity
    df['temp_change'] = df['temperature'].diff() / df['time_diff']
    df['hum_change'] = df['humidity'].diff() / df['time_diff']


    # Define threshold for filtering 
    temp_threshold_value = 0.5 #(0.5 celsius per second)
    hum_threshold_value = 2 #(2 % second)


    # Apply the filtering condition
    df = df[df['temp_change'].abs() <= temp_threshold_value]
    df = df[df['hum_change'].abs() <= hum_threshold_value]
    # Remove the temporary columns (time_diff and temp_change) if not needed
    df = df.drop(columns=['time_diff', 'temp_change','hum_change'])

    return df

if __name__ == "__main__":
    
    # Constant variables
    csv_file_name = 'sensor_data.csv'
    
    
    # get csv
    df = csv2pandas(csv_file_name)
    
    # Create csvs for day, week, month, year analysis
    list_of_csvs = [
    {"name": "lastDay", "timeRange_days": 30},
    {"name": "lastWeek", "timeRange_days": 25},
    {"name": "lastMonth", "timeRange_days": 35},
    {"name": "lastYear", "timeRange_days": 35},
    ]
    
    for croppedCSVs in list_of_csvs:
        # get new Dataframe for given time range
        croppedDf =  parseByTimeRange(df,croppedCSVs["timeRange_days"])
        
        # save it as a csv 
        #TODO: check if this creates a conflict with java script (since jscript wants to read it)
        croppedDf.to_csv(croppedCSVs["name"] +'.csv', index=False)

        