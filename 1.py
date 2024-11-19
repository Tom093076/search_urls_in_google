import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Load search phrases from a text file (assuming it's CSV-like)
try:
    # Use on_bad_lines='warn' to skip bad lines while reading
    df = pd.read_csv("1.txt", on_bad_lines='warn', header=None)  # Specify header=None if there are no headers
except Exception as e:
    print(f"Error loading text file: {e}")
    exit()

# Print all column names to check for discrepancies
print("Column names in the DataFrame:", df.columns.tolist())

# Attempt to access the first column (0 index) since header=None means no headers
search_column_index = 0  # Change this if your search phrases are in a different column

if search_column_index not in df.columns:
    print(f"Column '{search_column_index}' not found in the text file.")
    exit()

search_phrases = df[search_column_index].tolist()  # Access the search phrases

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Prepare a list to hold results
results = []

for phrase in search_phrases:
    # Format the search URL for Google UK
    search_url = f"https://www.google.co.uk/search?q={phrase.replace(' ', '+')}"
    driver.get(search_url)

    # Wait for the page to load
    time.sleep(2)  # Adjust sleep time if necessary

    try:
        # Locate the first organic result link
        first_result = driver.find_element(By.CSS_SELECTOR, 'h3')
        url = first_result.find_element(By.XPATH, '..').get_attribute('href')
        results.append((phrase, url))
    except Exception as e:
        results.append((phrase, "No result found"))
        print(f"Error retrieving URL for phrase '{phrase}': {e}")

# Close the driver
driver.quit()

# Create a DataFrame and save to CSV or Excel
results_df = pd.DataFrame(results, columns=["Search Phrase", "Top URL"])
results_df.to_excel("search_results.xlsx", index=False)  # Save results to an Excel file

print("Scraping complete. Results saved to 'search_results.xlsx'.")