"""
  pyApp141WikiIntegCovid.py - use WikiIntegrator to get list of COVID deaths
    date of birth

  2023-08-11 SMS first use, thanks to chat
  2923-08-12 SMS Expanding to process all columns and write out Project Worksheet
  2023-08-14 SMS Refining processing and stats handling with glboal g_app_data
  2023-08-20 SMS Fix bugs, age groups, add sheet 5 personOccups
  
  Folder: cd "D:/All_Prog4_Python/PyApp141Wikidata/"
  Virtual Environment: conda activate env-wikidata
  Execute: python pyApp141WikiIntegCovid.py

conda create -n env-wikidata << the creation of the env for WikiIntegrator
conda activate env-wikidata
Not: conda install -c conda-forge wikidataintegrator
  Had to first conda install pip !!
Then: pip install wikidataintegrator

https://github.com/SuLab/WikidataIntegrator 


"""

from wikidataintegrator import wdi_core
import pandas as pd
import numpy as np
import pprint
from utils.sparqlToDict import getSparqlToPersonDict
from utils.dictToXls import setDictToXls
# from utils.dfToXls import setDfToXls
from utils.gAppData import g_app_data
pp = pprint.PrettyPrinter(indent = 2)

# Define the WikidataQueryEngine
query_engine = wdi_core.WDItemEngine.wikibase_item_engine_factory()

# Construct and execute the SPARQL query NOTE: f-string is not needed
sparql_query = """
SELECT ?person ?person_label ?dateOfBirth ?dateOfDeath ?placed ?cause ?cause_of_death_label ?occup ?occup_label
WHERE
{
  {
    SELECT ?person
    WHERE {
      ?person wdt:P31 wd:Q5 .
      # 8/15 duplicated below but note: here it is necessary! 7,649 what if opt?: ?person wdt:P570 ?dated .
      ?person wdt:P509 ?cause .  
      ?cause wdt:P279* wd:Q84263196 .  
    } 
  }
  ?person wdt:P106 ?occup .    # find items that have "occupation (P106): politician (Q82955)"
  ?person wdt:P509 ?cause .    # with a P509 (cause of death) claim
  ?cause wdt:P279* wd:Q84263196 .     # ... where the cause is a subclass of (P279*) COVID Q84263196
  # added 4/7/23
  OPTIONAL {?person wdt:P569 ?dateOfBirth .}
  OPTIONAL {?person wdt:P570 ?dateOfDeath .}  
  OPTIONAL {?person wdt:P20 ?placed .}
  OPTIONAL {?person rdfs:label ?person_label filter (lang(?person_label) = "en") .}
  OPTIONAL {?cause rdfs:label ?cause_of_death_label filter (lang(?cause_of_death_label) = "en").}
  OPTIONAL {?occup rdfs:label ?occup_label filter (lang(?occup_label) = "en") .}
} # limit 100

"""
data = query_engine.execute_sparql_query(sparql_query)

# Extract and print some dates of birth and buid a dataframe
result = getSparqlToPersonDict(data) # converrt sqarql results to a person_dict
print("done dict! now calling setDictToXls!")
# call dictToXls for further processing with data in global g_app_data
setDictToXls()
print("after dict to xls...")

"""
*** this write to XLS is now in dictToXls.py; retain if pivot table used(?)
df = pd.DataFrame(dl)
print(f"We have {len(df)} items!")
# create a pivot table to calculate the count of occups by age group
# pvTable = pd.pivot_table(df, values='occup', index=['occup'], 
#   columns=['occup', 'ageGroup'], margins=True, margins_name='Count')
# we just need count of items, not a function against numbers
# can values be omitted
# pvTable = pd.pivot_table(df, index=['occup'], 
#   columns=['occup', 'ageGroup'], margins=True, margins_name='Count')
# chat suggestion:
# Create the pivot table to get the count by "occup" and "age"
pvTable_df = df.pivot_table(index="occup", columns="ageGroup", values="qid", aggfunc="count", fill_value=0)
pp.pprint(pvTable_df)
isXlsOk = setDfToXls(dl, pvTable_df)
if isXlsOk:
  print("Workbook written.")
else:
  print("Error: Workbook was NOT written.")
"""
# print results from g_app_data
for key, value in g_app_data.items():
  if key[0:3] == 'num':  # bit of a kludge but avoids group name
    print(f"{value['label']}: {value['count']}")