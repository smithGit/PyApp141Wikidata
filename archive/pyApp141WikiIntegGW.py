"""
  pyApp141WikiIntegGW.py - use WikiIntegrator to get George Washington's Birthday

  2023-08-11 SMS first use, thanks to chat

conda create -n wikidata python=3.8
conda activate wikidata
conda install -c conda-forge wikidataintegrator
 
https://github.com/SuLab/WikidataIntegrator 


"""
from wikidataintegrator import wdi_core

# Define the QID for George Washington
george_washington_qid = "Q23"

# Define the property for date of birth (P569)
date_of_birth_property = "P569"

# Define the WikidataQueryEngine
query_engine = wdi_core.WDItemEngine.wikibase_item_engine_factory()

# Retrieve data for George Washington
data = query_engine.execute_sparql_query(
    f"SELECT ?date_of_birth WHERE {{ wd:{george_washington_qid} wdt:{date_of_birth_property} ?date_of_birth }}"
)

# Extract the date of birth
date_of_birth = data["results"]["bindings"][0]["date_of_birth"]["value"]

print("Date of Birth:", date_of_birth)
