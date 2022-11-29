# PokemonGeaux

This repo contains a few projects (Python and Data Science).


**data contents:**  
notebooks:
* PokemonWebScraping: used to gather data via scraping the site [serebii.net](https://serebii.net/pokemongo/). Each page is scraped, the data is converted into a pandas data frame, and then saved as a csv file.  
* CreatePokedexDatabase uses the csv files created by PokemonWebScraping to create a sqlite database.  

database: Pokemon database created by CreatePokedexDatabase  
This directory also contains csv files created by the notebook PokemonWebScraping  
<br>
<br>
**interactive-map contents:**  
PokemonMap_ipyleaflet: Notebook that creates an interactive map of Pokemon Go landmarks in North and South Carolina. Uses the data in NC_SC_PokemonGoData.csv to create the map.

The interactive map does not render in Github, but you can view it in [nbviewer](https://nbviewer.org/)
Check out this [link](https://stackoverflow.com/questions/53240378/folium-map-fail-to-render-in-notebook-on-github) from stackoverflow.
<br>
<br>  
**pokedex contents:**
The directory contains the code for an API that will eventually be used to predict Pokemon spawns based upon current weather conditions for specific GPS coordinates. Currently, the API gets the weather from [weather.gov](https://www.weather.gov/documentation/services-web-api) and [openweathermap.org](https://openweathermap.org/) and determines the weather boost. The weather boost can be used to predict the type of Pokemon spawn.

An [API key](https://openweathermap.org/api) from openweathermap.org is required for the API to function properly.