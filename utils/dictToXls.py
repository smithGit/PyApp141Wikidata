"""
  dictToXls.py convert the Wikidata SPARQL result as Dict to
    a multi-sheet XLS workbook



  
  Create the Project Workbook with multiple sheets:
  ** re-think this: sparql raw response not currently store!
  SparqlResponse = the sparql response now in dl passed as input
  DistinctPersons = unique person person and label
    with person-data: dob, dod, placed, cause, age, (not occup may be multi) 
    8/12/23 also: add count for # records for this person
    note cause of death may be multiple but in this case only COVID
    Other fields may be dup (eg placed) but we use only one, the last encountered
  DistinctOccup = unique occup id and label along with countw:
    Total and broken down by age group
  
  2023-08-12 SMS completed dfToXls but decided to convert SPARQL to dict
  2023-08-12 SMS I realized I can create the whole workbook so why not?
  2023-08-14 SMS Taking the Wikidata SPARQL as dict and do all further processing

  """
import pandas as pd
import numpy as np
import pprint
import xlsxwriter
from utils.gAppData import g_app_data
pp = pprint.PrettyPrinter(indent = 2)

def get_person_occup_agegroup_pvtable():
  # use pivot table to aggregate the person-occupation pairs by Age Group
  # return: pivot_table result, which is a DataFrame
  # Process the Dict with a pivot table to aggregate occupation-holder ount by occupation
  # create a dataframe from the dict (what is header of key?)
  df = pd.DataFrame.from_dict(g_app_data['person_dict'], orient='index')
  print(f"len df............... = {len(df)}")
  print(df)
  # chat suggestion:
  # Create the pivot table to get the count by "occup" and "age"
  # pvTable_df = df.pivot_table(index="occup", columns="ageGroup", values="person", aggfunc="count", fill_value=0)
  print("trying pivot table")
  pvTable_df = df.pivot_table(index="occup", columns="ageGroup", aggfunc="count", fill_value=0)
  print("pivot table:")
  pp.pprint(pvTable_df)
  return pvTable_df


def setNotesSheet(notes_obj):
  # this is a lot of detail to move from the main code
  # the note_obj is a dict of stats and other info
  # todo: add date/time and put in Notes; show file name
  # returns: the dl_notes dict / list

  dl_notes = [ # 4 columns in all rows
      { "item": "", "sub-item": "", "description": "Notes on WD SPARQL Query - COVID Deaths and Occupaitons", "stat": "" },
      { "item": "2023-08-dd", "sub-item": "", "description": "", "stat": "" },
      { "item": "", "sub-item": "", "description": "", "stat": "" },
      { "item": "SHEET NAMES:", "sub-item": "", "description": "", "stat": "" },
      { "item": "1. sht_wd_covid", "sub-item": "", "description": "SPARQL Response data, unchanged", "stat": "" },
      { "item": "", "sub-item": "", "description": "If no english label, deleted", "stat": "" },
      { "item": "2. Notes", "sub-item": "", "description": "This sheet", "stat": "" },
      { "item": "3. distinctPeople", "sub-item": "", "description": "Each Person with person-data", "stat": "" },
      { "item": "4. distinctOccup", "sub-item": "", "description": "Distinct occup id, label and counts", "stat": "" },
      { "item": "5. personOccups", "sub-item": "", "description": "All occup for each person", "stat": "" },
      { "item": "", "sub-item": "", "description": "", "stat": "" },
      { "item": "Stats:", "sub-item": "", "description": "", "stat": "" },
      { "item": "", "sub-item": "", "description": f"Num SPARQL rows", "stat": notes_obj['num_sparql'] },
      { "item": "", "sub-item": "", "description": f"Num People", "stat": notes_obj['num_people'] },
      { "item": "", "sub-item": "", "description": f"Num Occupations", "stat": notes_obj['num_occup'] },
      { "item": "", "sub-item": "", "description": f"Num People without Occup", "stat": g_app_data['num_people_no_occup']['count'] },
      { "item": "", "sub-item": "", "description": f"Num People mutiple Occups", "stat": g_app_data['num_people_multi_occup']['count'] },
      { "item": "", "sub-item": "", "description": f"Num Occupations", "stat": notes_obj['num_occup'] },
      { "item": "", "sub-item": "", "description": "SPARQL Rows, purged rows, people, occup's", "stat": "" },
      { "item": "", "sub-item": "", "description": "", "stat": "" },
      { "item": "", "sub-item": "", "description": "", "stat": "" },
      { "item": "", "sub-item": "", "description": "", "stat": "" },
      { "item": "Occup Counts by Age:", "sub-item": "", "description": "", "stat": "" }, 
      { "item": "", "sub-item": "unknown", "description": "unknown", "stat": g_app_data["num_age_unknown"]['count'] }, 
      { "item": "", "sub-item": "young", "description": "<= 21", "stat": g_app_data["num_age_young"]['count']  }, 
      { "item": "", "sub-item": "adult", "description": "22 - 35", "stat": g_app_data["num_age_adult"]['count'] }, 
      { "item": "", "sub-item": "midlife", "description": "36 - 50", "stat": g_app_data["num_age_midlife"]['count'] }, 
      { "item": "", "sub-item": "senior", "description": "51 - 65", "stat": g_app_data["num_age_senior"]['count'] }, 
      { "item": "", "sub-item": "socsec", "description": "66 - 80", "stat": g_app_data["num_age_socsec"]['count'] }, 
      { "item": "", "sub-item": "old", "description": "Over 80", "stat": g_app_data["num_age_old"]['count'] }, 
    ]
  return dl_notes

def setDictToXls():
  # the dictionary is the dict derived from WD SPARQL query, one record per person
  # The dict is in g_app_data as person_dict
  # A person may have multiple occupations which are in a dict within the row
  # ..***
  # the dl is the data list corresponding row for row with SPARQL response,
  #   sort sequence: as received 
  # df is the data frame produced by the pivot_table with aggregate results
  #   in this case a count of occupation holders by age group

  # set output foler and filename
  out_folder = "C:/temp/QQTemp/PyOut/"
  out_filename = "WD COVID Occup Age (2023-08-dd).xlsx"
  out_path = out_folder + out_filename
  # Create an Excel writer object
  try:
    excel_writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
  except:
    print(f"Error opening output XLS file; it may be open.")
    return False
 
  ## PROBLEM!  we no longer have an occup column, as it is a dict
  # how to handle?  We really need list with each occup, I think -
  # the worksheet needs this info
  # Go back to where person dict is formed and where there is dup
  # show which fields are different
  # yuck: probably best to go back to passing the original list to this routine!!


  # process each output sheet
  # Sheet 1: sht_wd_covid - all data from the sparql_list
  # Create DataFrames
  df_sht_wd_covid = pd.DataFrame(g_app_data['sparql_list'])
  # Sheet 2: Notes (moved to create last when stats known)

  # Sheet 3: distinctPeople - distinct person with person-related data
  #   (using first-encountered row for person)
  """
  8/15/23 pm todo: decide whether to do this sheet from list 
or from dict and add a column for alt occup's
and do a join with commas...
  """
  # wait: we HAVE the person dict - in g_app_data.person_dict
  # Let's not use it for now, just re-create with first row
  # for the person
  dict_people = {}
  print(f"Doing sheet 3 person_dict in list len: {len(g_app_data['sparql_list'])}")
  for row in g_app_data['sparql_list']:
    person = row['person']
    if person not in dict_people:
      dict_people[person] = { 
        "person": row['person'], 
        "person_label": row['person_label'],
        "date_of_birth": row['date_of_birth'],
        "date_of_death": row['date_of_death'],
        "placed": row['placed'],
        "cause": row['cause'],
        "cause_label": row['cause_label'],
        "occup": row['occup'], 
        "occup_label": row['occup_label'],
        "age": row['age'], 
        "ageGroup": row['ageGroup']
      }
  df_people = pd.DataFrame(dict_people)
  df_people_transpose = df_people.transpose()

  # Sheet 4: distinctOccup - distinct occupations with count and count by age group
  # for this we need to pull in the occupation counts by age group
  # from df, which is the pivot table result with occup as key
  # 8/26 complication: where there are two rows with same person-occupation, it is counted twice
  # The easiest solution is to have a dict of each person-occup pair and
  # before counting ascertain the current pair is not in this dict
  dl_occup = {}
  person_occup_dict = {} # dict of only keys = personId + "+" + occupId
  # it looks like we are not using pivot table? df_pivot_age_group_by_occupn = get_person_occup_agegroup_pvtable()
  num_rows = 0
  for row in g_app_data['sparql_list']:
    occup = row['occup']
    personId = row['person']
    person_occup = occup + "+" + personId
    # if num_rows < 7:
    #   print(f"row occup pers: {person_occup}")
    if person_occup in person_occup_dict:
      print(f"dup person-occup {person_occup}")
      continue # do not count
    else:
      person_occup_dict[person_occup] = None
    if occup not in dl_occup: # store and keep count
      dl_occup[occup] = {
        "occup_label": row['occup_label'],
        "count": 1,
        "unknown": 0 if row['ageGroup'] != "unknown" else 1,
        "young": 0 if row['ageGroup'] != "young" else 1,
        "adult": 0 if row['ageGroup'] != "adult" else 1,
        "midlife": 0 if row['ageGroup'] != "midlife" else 1,
        "senior": 0 if row['ageGroup'] != "senior" else 1,
        "socsec": 0 if row['ageGroup'] != "socsec" else 1,
        "old": 0 if row['ageGroup'] != "old" else 1
      }
    else:  # occup is in dl_occup
      dl_occup[occup]['count'] += 1
      match row['ageGroup']:
        case 'unknown':
          dl_occup[occup]['unknown'] += 1        
        case 'young':
          dl_occup[occup]['young'] += 1
        case 'adult':
          dl_occup[occup]['adult'] += 1
        case 'midlife':
          dl_occup[occup]['midlife'] += 1
        case 'senior':
          dl_occup[occup]['senior'] += 1
        case 'socsec':
          dl_occup[occup]['socsec'] += 1
        case 'old':
          dl_occup[occup]['old'] += 1
        case _:
          pass
      num_rows += 1
  # end of row loop    
  df_occup = pd.DataFrame(dl_occup)
  df_occup_transpose = df_occup.transpose()
  df_occup_sorted = df_occup_transpose.sort_values(by="count", ascending=False)

  # Sheet 5: personOccups - all occupations for each person
  #   (using g_app_data element person_dict with dict of occup's)
  # first get the max num occups per person to have same # cols per row with header occup_n
  print("Doing sheet 5")
  max_num_occup = 0
  for key, value in g_app_data['person_dict'].items():
    num_occups = len(value['occup_list'])
    if num_occups > max_num_occup:
      max_num_occup = len(value['occup_list'])
    # get stats
    if num_occups == 0:
      g_app_data['num_people_no_occup']['count'] += 1
    if num_occups >1:
      g_app_data['num_people_multi_occup']['count'] += 1
  print(f"Max num occup for a person: {max_num_occup}")
  dict_personOccup = {}
  # get count of person-occup pairs to cross check distinct occup stats
  num_person_occup_pairs = 0  
  for personKey, value in g_app_data['person_dict'].items():
    # create each dataframe row personOccup as an object with personKey as key
    dict_personOccup[personKey] = {'person_label': value['person_label']}  # person qid
    num_cols_done = 0 # keep track of num occup columns filled
    for occupKey, occupValue in value['occup_list'].items():
      num_cols_done += 1
      hdr = 'occup_' + str(num_cols_done)
      num_person_occup_pairs += 1
      dict_personOccup[personKey][hdr] = occupKey + ': ' + occupValue
    if num_cols_done < max_num_occup:
      # problem: first occup being blanked without +1 - does this fix?
      for n in range(num_cols_done + 1, max_num_occup):
        hdr = 'occup_' + str(n)
        dict_personOccup[personKey][hdr] = ''
  df_people = pd.DataFrame(dict_personOccup)
  df_personOccup_transpose = df_people.transpose()
  print(f"New stat: num person occup pairs {num_person_occup_pairs}")
  # Sheet 2: Notes
  # Standard sheet for these apps; has date of creation and purpose
  # also a list of sheets and what they contain
  notes_obj = {
    "num_sparql": len(g_app_data['sparql_list']),
    "num_people": len(g_app_data['person_dict']),
    "num_occup": len(dl_occup),
    "num_no_birth": 0,

  }
  dl_notes = setNotesSheet(notes_obj)
  df_notes = pd.DataFrame(dl_notes)

  # Export the data frames as sheets in order and Save the Excel file
  df_sht_wd_covid.to_excel(excel_writer, sheet_name='sht_wd_covid', index=False)
  df_notes.to_excel(excel_writer, sheet_name='Notes', index=False)
  df_people_transpose.to_excel(excel_writer, sheet_name='distinctPeople', index=False)  
  df_occup_sorted.to_excel(excel_writer, sheet_name='distinctOccup', index=True)
  df_personOccup_transpose.to_excel(excel_writer, sheet_name='personOccups', index=True)
  try:
    excel_writer.close()
    print(f"Excel file written to temp > QQTemp > PyOut.")
    return True
  except:
    print(f"Something went wrong with save/close workbook.")
    return False
