# import Python modules
import requests # HTTP library

def get_club_data(club):
	return {
		'rank': club['Posicao'],
		'team': club['DesignacaoMinima'],
		'points': club['Pontos'],
		'played': club['NumJogos'],
		'won': club['Vitorias'],
		'drawn': club['Empates'],
		'lost': club['Derrotas'],
		'goals_for': club['GolosMarcados'],
		'goals_against': club['GolosSofridos'],
		'goals_difference': club['GolosMarcados'] - club['GolosSofridos']
	}

def ligaportugal():
	try:
		response = requests.get('https://www.ligaportugal.pt/pt/liga/standings/1')
		json_data = response.json()
		clubs = json_data[0]['Classificacoes']
		ret_data = [get_club_data(club) for club in clubs]
		return ret_data
	except:
		return None
