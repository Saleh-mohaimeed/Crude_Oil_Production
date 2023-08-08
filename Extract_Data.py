import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_data():
    
    # Chrome driver
    driver = webdriver.Chrome("chromedriver.exe")
    
    # Data URL
    url = "http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93906"
    
    # Get the webpage using the data URL
    driver.get(url)
    
    # Wait for the table to load
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "TVDataTable")))
    
    # Read HTML table into DataFrame
    data = pd.read_html(driver.page_source, attrs={'class': 'TVDataTable'}, flavor='bs4', parse_dates=True, header=2)[0]
    
    # Update column name and remove row
    data = data.rename(columns={"Time": "Country"})
    data = data.drop(0, axis=0)
    
    # Melting the DataFrame
    data = pd.melt(data, "Country", var_name="Time", value_name="Value")
    
    # Extracting month and year from the "Time" column
    data[["Month", "Year"]] = data["Time"].str.extract(r'([A-Za-z]{3})(\d{4})')
    
    # Dropping the original "Time" column
    data = data.drop("Time", axis=1)
    
    # Rearranging the columns
    data = data[["Country", "Month", "Year", "Value"]]
    
    # Change the data type of Year and Value to int
    data = data.astype({"Year":"int", "Value":"int"})
    
    return(data)