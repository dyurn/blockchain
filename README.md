Bitcoin Blockchain Dernier Bloc Info

Ce script Python permet de récupérer des informations sur le dernier bloc de la blockchain Bitcoin en utilisant l'API de Blockchain.info. Il fournit le hash du dernier bloc, le nombre de transactions qu'il contient, ainsi que les commissions (frais de transaction) payées aux mineurs, converties en Bitcoin (BTC).

Fonctionnalités

Récupération du hash du dernier bloc de la blockchain Bitcoin.
Extraction et affichage du nombre de transactions dans ce bloc.
Calcul et affichage des commissions des mineurs en BTC.

Prérequis

Pour exécuter ce script, vous avez besoin de Python 3 et de la bibliothèque requests. Vous pouvez installer requests en utilisant pip :
pip install requests

Fonctionnalités détaillées

get_latest_block_hash() : Cette fonction interroge l'API de Blockchain.info pour obtenir le hash du dernier bloc miné sur la blockchain Bitcoin.

get_block_info_from_api(block_hash) : Avec le hash d'un bloc spécifique obtenu, cette fonction interroge l'API pour extraire des informations détaillées sur ce bloc, telles que le nombre de transactions qu'il contient et les frais de transaction en BTC.