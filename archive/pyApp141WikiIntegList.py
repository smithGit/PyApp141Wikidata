"""
  pyApp141WikiIntegList.py - use WikiIntegrator to get list of people
    date of birth

  2023-08-11 SMS first use, thanks to chat

conda create -n wikidata python=3.8
conda activate wikidata
conda install -c conda-forge wikidataintegrator
 
https://github.com/SuLab/WikidataIntegrator 


"""




from wikidataintegrator import wdi_core

# Define the QIDs for the individuals
individual_qids = ["Q1850695", "Q111449480", "Q88181154", "Q91121930"]

# Define the property for date of birth (P569)
date_of_birth_property = "P569"

# Define the WikidataQueryEngine
query_engine = wdi_core.WDItemEngine.wikibase_item_engine_factory()

# Create a comma-separated string of QIDs
qid_list = " ".join([f"wd:{qid}" for qid in individual_qids])

# Construct and execute the SPARQL query
sparql_query = f"""
    SELECT ?individual ?date_of_birth WHERE {{
        VALUES ?individual {{ {qid_list} }}
        ?individual wdt:{date_of_birth_property} ?date_of_birth
    }}
"""
data = query_engine.execute_sparql_query(sparql_query)

# Extract and print the dates of birth
for item in data["results"]["bindings"]:
    individual = item["individual"]["value"].split("/")[-1]
    date_of_birth = item["date_of_birth"]["value"]
    print(f"Date of Birth for {individual}: {date_of_birth}")
