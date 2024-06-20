# Function to parse JSON data
# :param data: JSON data
# :return: parsed data
def ligaportugal(data):
	try: # Try to parse JSON data
		ret_data = data[0]['Classificacoes'] # Get classificacoes from JSON data
		for club in ret_data: # Iterate over clubs
			club['DiferencaGolos'] = club['GolosMarcados'] - club['GolosSofridos'] # Calculate goal difference
		return ret_data # Return classificacoes
	except: # Catch exceptions
		return None # Return None
