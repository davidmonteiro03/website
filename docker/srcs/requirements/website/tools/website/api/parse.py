def ligaportugal(data):
	try:
		ret_data = data[0]['Classificacoes']
		for club in ret_data:
			club['DiferencaGolos'] = club['GolosMarcados'] - club['GolosSofridos']
		return ret_data
	except:
		return None
