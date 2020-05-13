# API flask exposant des services REST

Liste des serivices disponibles : https://mg-services.herokuapp.com/api/spec.html

## Scrapping Marmiton

Ce service permet de récupérer les plats avec les ingrédients associés à partir du site Marmiton.

## Open data pollution de l'air

Ce service permet de récupérer les données de mesure des concentrations de polluants atmospheriques reglementés
[text]([https://link](https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/))

** les samples points sont stockés dans une base MONGODB ATLAS en free tier, les requêtes mettent du temps du fait que le cluster est hébergé sur aws us-east-1 ** 