import requests

def get_latest_block_hash():
    url = "https://blockchain.info/latestblock"
    
    try:
        response = requests.get(url)
        latest_block_data = response.json()
        
        latest_block_hash = latest_block_data['hash']
        return latest_block_hash
    
    except Exception as e:
        return f"Erreur lors de la récupération du hash du dernier bloc : {str(e)}"

def get_block_info_from_api(block_hash):
    url = f"https://blockchain.info/rawblock/{block_hash}"
    
    try:
        response = requests.get(url)
        block_data = response.json()
        hash = block_data['hash']
        nb_transactions = block_data['n_tx']
        
        # Les frais sont déjà fournis par l'API dans le champ 'fee', en satoshis
        # Convertir les frais de Satoshi en BTC
        miner_fees_btc = block_data['fee'] / 1e8
        
        return {
            "Block" : hash,
            "Nombre de transactions": nb_transactions,
            "Commission du mineur (BTC)": miner_fees_btc
        }
    
    except Exception as e:
        return f"Erreur lors de la récupération des informations du bloc : {str(e)}"

#block_hash = "00000000000000000000396136a25694ee9ae7acdc5401bcae130a331c2b3e65"
print(get_block_info_from_api(get_latest_block_hash()))
    
#print(get_latest_block_hash())