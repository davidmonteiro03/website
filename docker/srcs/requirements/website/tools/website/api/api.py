# import Python modules
import requests # HTTP library

# import data
from . import data # import data

# Function to get Liga Portugal data
# :param: None
# :return: Liga Portugal data
def ligaportugal():
	try: # Try to get Liga Portugal data
		response = requests.get('https://www.ligaportugal.pt/pt/liga/standings/1') # Send GET request
		return data.ligaportugal(response.json()) # Return data
	except: # Catch exceptions
		return None # Return None
