# API flask exposant des services REST

## Marmiton

Ce service permet de récupérer les plats avec les ingrédients associé à partir du site Marmiton.

**Exemple:**

       https://mg-services.herokuapp.com/api/scrapping/marmiton/fetch/ingredients?plat=tiramisu
**Résultat**

    {"items": [{"nom": "Glace au tiramisu (Italie)", "ingredients": [" : sucre", "oeuf", "mascarpone", "cr\u00e8me fra\u00eeche battue", "cacao en poudre", "extrait de caf\u00e9 fort m\u00e9lang\u00e9 avec 1 cuill\u00e8re \u00e0 soupe de rhum", "biscuit \u00e0 la cuill\u00e8re (\u00e0 volont\u00e9)", "sucre vanill\u00e9", "sel."]}], "next_page": "ingredients?plat=tiramisu&start=30&page=3"}

Le résultat contient une clé avec l'url relative pour la page suivante

**Exemple**

Avec  la clé next_page suivante :
   

     "next_page": "ingredients?plat=tiramisu&start=30&page=3"

Il est possible de d'obtenir d'autres résultats en ajoutant la clé next_page à l'url :

       https://mg-services.herokuapp.com/api/scrapping/marmiton/fetch/ingredients?plat=tiramisu&start=30&page=3