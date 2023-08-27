"""
  sparqlToDict.py convert the Wikidata SPARQL person-response to dict
    in this case to the global personDict

  2023-08-12 SMS This is a lot of code that can be isolated
  2023-08-14 SMS Realizing it would be better to build a dict
    with single entry per person; duplicate  records of no value
    This is a successor to sparqlToList.py
  2023-08-15 SMS Reverting back to use sparqlToList.py as 
    dict within the row is really hard to use / display!
    ** MAYBE: keep forging ahead... 
    ** NO: Why not just have TWO objects in AppData - dict and list!

  This function is also of a general purpose nature to show the 
  manner of extracting data values from the SPARQL JSON response.
  Care is needed as a given row may not contain all expected elements.
 
"""
from utils.gAppData import g_app_data

def getSparqlToPersonDict(data):
  # creates a dict per person with multiple occups for person in dict
  lst = g_app_data['sparql_list']  # use a reference to object, sparql less blank label
  dct = g_app_data["person_dict"]  # use a refernece to object, row / person
  item_num = 0
  g_app_data["num_sparql_rows"]["count"] = len(data["results"]["bindings"])
  for item in data["results"]["bindings"]:
    # Scan the SPARQL JSON array and convert to data list
    person = item["person"]["value"].split("/")[-1]
    # pattern for elements that may be missing:
    person_label = ""
    if 'person_label' not in item or item['person_label'] == '':
      g_app_data["num_no_label"]["count"] += 1
      continue
    elif item["person_label"] == "":
      g_app_data["num_no_label"]["count"] += 1
      continue
    else:
      person_label = item['person_label']['value']
    placed = "" if 'placed' not in item \
      else item['placed']['value'].replace("http://www.wikidata.org/entity/","")
    cause = "" if 'cause' not in item \
      else item['cause']['value'].replace("http://www.wikidata.org/entity/","")
    cause_label = "" if 'cause_of_death_label' not in item \
      else item['cause_of_death_label']['value']
    occup = "" if 'occup' not in item \
      else item["occup"]["value"].replace("http://www.wikidata.org/entity/","")
    occup_label = "" if 'occup_label' not in item \
      else item['occup_label']['value']
    # quite a number have no date of birth; set to '' if missing
    date_of_birth = ''
    year_of_birth = ''
    if 'dateOfBirth' not in item or item['dateOfBirth'] == '':
      date_of_birth = ''
      g_app_data['num_no_birth']['count'] += 1
    else:
      date_of_birth = item["dateOfBirth"]["value"].replace("T00:00:00Z", "")
      year_of_birth = int(date_of_birth[0:4])
    date_of_death = ''
    year_of_death = ''
    if 'dateOfDeath' not in item or item['dateOfDeath'] == '':
      date_of_death = ''
      g_app_data['num_no_death']['count'] += 1
    else:
      date_of_death = item["dateOfDeath"]["value"].replace("T00:00:00Z", "")
      year_of_death = int(date_of_death[0:4])
    # get person's age
    age_at_death = 0    
    if year_of_birth != '' and year_of_death != '':
        age_at_death = year_of_death - year_of_birth
    # set age group
    ageGroup = None
    if age_at_death == 0:
      ageGroup = "unknown"
      g_app_data['num_age_unknown']['count'] += 1
    elif age_at_death <= 21:
      ageGroup = "young"
      g_app_data['num_age_young']['count'] += 1
    elif age_at_death <= 35:
      ageGroup = "adult"
      g_app_data['num_age_adult']['count'] += 1
    elif age_at_death <= 50:
      ageGroup = "midlife"
      g_app_data['num_age_midlife']['count'] += 1
    elif age_at_death <= 65:
      ageGroup = "senior"
      g_app_data['num_age_senior']['count'] += 1
    elif age_at_death <= 80:
      ageGroup = "socsec"
      g_app_data['num_age_socsec']['count'] += 1
    else:
      ageGroup = "old"
      g_app_data['num_age_old']['count'] += 1
    # Build the SPARQL List: cleaned fields and no blank labels
    if True:
      lobj =  {
        "person": person,
        "person_label": person_label,
        "date_of_birth": date_of_birth,
        "date_of_death": date_of_death,
        "placed": placed,
        "cause": cause,
        "cause_label": cause_label, # there could be multiple but only COVID in input
        "occup": occup,
        "occup_label": occup_label,
        "age": age_at_death, 
        "ageGroup": ageGroup,
      }
    lst.append(lobj) 
    # Build the Person Dict: take care of a new person
    if person not in dct:
      # create the person object with dict for multi occup
      pobj =  {
        "person_label": person_label,
        "date_of_birth": date_of_birth,
        "date_of_death": date_of_death,
        "placed": placed,
        "cause": cause,
        "cause_label": cause_label, # there could be multiple but only COVID in input
        "occup_list": {},
        "age": age_at_death, 
        "ageGroup": ageGroup,
        "num_rows": 1,
        "num_occups": 0
      }
      if occup != '':
        pobj['occup_list'][occup] = occup_label
        pobj["num_occups"] = 1
      # add person obj to person dict
      dct[person] = pobj
      g_app_data['num_people']['count'] += 1
    else:
      # process a duplicate person entry
      # for now only record multi-occup *** add other field checks!
      if occup != '' and occup not in dct[person]['occup_list']:
        dct[person]['occup_list'][occup] = occup_label
    item_num += 1
  # end of item loop
  return True # the global person_dict should be updated
