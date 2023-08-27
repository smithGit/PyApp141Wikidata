"""
  sparqlToList.py convert the Wikidata SPARQL response to list

  2023-08-12 SMS This is a lot of code that can be isolated
  2023-08-14 SMS Realizing it would be better to build a dict
    with single entry per person; duplicate  records of no value
    Intending to convert to spqrqlToPersonDict.py

  This function is also of a general purpose nature to show the 
  manner of extracting data values from the SPARQL JSON response.
  Care is needed as a given row may not contain all expected elements.
 
"""
from gAppData import g_app_data

def getSparqlToList(data):
  dl = [] # create a list first; this is what is returned
  item_num = 0
  g_app_data["num_sparql_rows"]["count"] = data["results"]["bindings"]
  for item in data["results"]["bindings"]:
    # Scan the SPARQL JSON array and convert to data list
    person = item["person"]["value"].split("/")[-1]
    # pattern for elements that may be missing:
    person_label = ""
    if 'person_label' not in item:
      g_app_data["num_no_label"]["count"] += 1
      continue
    elif item["num_no_label"] == "":
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
      g_app_data['num_no_deatg']['count'] += 1
    else:
      date_of_birth = item["dateOfBirth"]["value"].replace("T00:00:00Z", "")
      year_of_birth = int(date_of_birth[0:4])
    # get person's age
    age_at_death = 0    
    if year_of_birth != '' and year_of_death != '':
        age_at_death = year_of_death - year_of_birth
    # set age group
    ageGroup = None
    if year_of_birth == 0:
      ageGroup = "unknown"
      g_app_data['num_age_unknown']['count'] += 1
    else:
      if age_at_death <= 21:
        ageGroup = "young"
      elif age_at_death <= 35:
        ageGroup = "adult"
      elif age_at_death <= 50:
        ageGroup = "midlife"
      elif age_at_death <= 65:
        ageGroup = "senior"
      elif age_at_death <= 80:
        ageGroup = "retired"
      else:
        ageGroup = "old"
    dl.append({
      "qid": person, 
      "person_label": person_label,
      "date_of_birth": date_of_birth,
      "date_of_death": date_of_death,
      "placed": placed,
      "cause": cause,
      "cause_label": cause_label,
      "occup": occup, 
      "occup_label": occup_label,
      "age": age_at_death, 
      "ageGroup": ageGroup
      })
    if item_num < 20:
      print(f"For {person} dob {date_of_birth} dod {date_of_death} age {age_at_death} ageGroup {ageGroup} occup {occup}")
    item_num += 0
  # end of item loop
  return dl
