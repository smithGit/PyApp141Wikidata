"""
  dfToXls.py convert a dataframe to a multi-sheet XLS workbook

  2023-08-12 SMS I realized I can create the whole workbook so why not?

  Create the Project Workbook with multiple sheets:
  SparqlResponse = the sparql response now in dl passed as input
  DistinctPersons = unique person qid and label
    with person-data: dob, dod, placed, cause, age, (not occup may be multi) 
    8/12/23 also: add count for # records for this person
    note cause of death may be multiple but in this case only COVID
    Other fields may be dup (eg placed) but we use only one, the last encountered
  DistinctOccup = unique occup id and label along with countw:
    Total and broken down by age group
  
  """
import pandas as pd
import xlsxwriter 

def setNotesSheet(notes_obj):
  # this is a lot of detail to move from the main code
  # the note_obj is a dict of stats and other info
  # todo: add date/time and put in Notes; show file name
  # returns: the dl_notes dict / list
  dl_notes = [ # 4 columns in all rows
      { "col1": "", "col2": "", "col3": "Notes on WD SPARQL Query - COVID Deaths and Occupaitons", "col4": "" },
      { "col1": "2023-08-dd", "col2": "", "col3": "", "col4": "" },
      { "col1": "", "col2": "", "col3": "", "col4": "" },
      { "col1": "sht_wd_covid", "col2": "", "col3": "SPARQL Response data, unchanged", "col4": "" },
      { "col1": "", "col2": "", "col3": "If no english label, deleted", "col4": "" },
      { "col1": "Notes", "col2": "", "col3": "This sheet", "col4": "" },
      { "col1": "distinctPeople", "col2": "", "col3": "Each Person with person-data", "col4": "" },
      { "col1": "distinctOccup", "col2": "", "col3": "Distinct occup id, label and counts", "col4": "" },
      { "col1": "", "col2": "", "col3": "", "col4": "" },
      { "col1": "Stats:", "col2": "", "col3": "", "col4": "" },
      { "col1": "", "col2": "", "col3": f"Num SPARQL rows", "col4": notes_obj['num_sparql'] },
      { "col1": "", "col2": "", "col3": f"Num People", "col4": notes_obj['num_people'] },
      { "col1": "", "col2": "", "col3": f"Num Occupations", "col4": notes_obj['num_occup'] },
      { "col1": "", "col2": "", "col3": "SPARQL Rows, purged rows, people, occup's", "col4": "" },
      { "col1": "", "col2": "", "col3": "", "col4": "" },
      { "col1": "", "col2": "", "col3": "", "col4": "" },
      { "col1": "", "col2": "", "col3": "", "col4": "" },
      { "col1": "Occup Counts by Age:", "col2": "", "col3": "", "col4": "" }, 
      { "col1": "", "col2": "young", "col3": "<= 21", "col4": "" }, 
      { "col1": "", "col2": "adult", "col3": "22 - 35", "col4": "" }, 
      { "col1": "", "col2": "midlife", "col3": "36 - 50", "col4": "" }, 
      { "col1": "", "col2": "senior", "col3": "51 - 80", "col4": "" }, 
      { "col1": "", "col2": "old", "col3": "Over 80", "col4": "" }, 
    ]
  return dl_notes

def setDfToXls(dl, df):
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
    print(f"Error opening output XLS file.")
    return False
  # process each output sheet
  # Sheet 1: sht_wd_covid - all data from dl
  # Create DataFrames
  df_sht_wd_covid = pd.DataFrame(dl)
  # Sheet 2: Notes (moved to create last when stats known)

  # Sheet 3: distinctPeople - distinct person with person-related data
  #   (using first-encountered row for person/qid)
  dl_people = {}
  for row in dl:
    qid = row['qid']
    if qid not in dl_people:
      dl_people[qid] = { 
        "qid": row['qid'], 
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
  df_people = pd.DataFrame(dl_people)
  df_people_transpose = df_people.transpose()
  # Sheet 4: distinctOccup - distinct occupations with count and count by age group
  # for this we need to pull in the occupation counts by age group
  # from df, which is the pivot table result with occup as key
  dl_occup = {}
  for row in dl:
    occup = row['occup']
    if occup not in dl_occup: # store and keep count
      dl_occup[occup] = {
        "occup_label": row['occup_label'],
        "count": 0,
        "young": 0 if row['ageGroup'] != "young" else 1,
        "adult": 0 if row['ageGroup'] != "adult" else 1,
        "midlife": 0 if row['ageGroup'] != "midlife" else 1,
        "senior": 0 if row['ageGroup'] != "senior" else 1,
        "retired": 0 if row['ageGroup'] != "retired" else 1,
        "old": 0 if row['ageGroup'] != "old" else 1
      }
    else:  # occup is in dl
      dl_occup[occup]['count'] += 1
      match row['ageGroup']:
        case 'young':
          dl_occup[occup]['young'] += 1
        case 'adult':
          dl_occup[occup]['adult'] += 1
        case 'midlife':
          dl_occup[occup]['midlife'] += 1
        case 'senior':
          dl_occup[occup]['senior'] += 1
        case 'retired':
          dl_occup[occup]['retired'] += 1
        case 'old':
          dl_occup[occup]['old'] += 1
        case _:
          pass
  # end of row loop    
  df_occup = pd.DataFrame(dl_occup)
  df_occup_transpose = df_occup.transpose()
  df_occup_sorted = df_occup_transpose.sort_values(by="count", ascending=False)
  # Sheet 2: Notes
  # Standard sheet for these apps; has date of creation and purpose
  # also a list of sheets and what they contain
  notes_obj = {
    "num_sparql": len(dl), # update later
    "num_people": len(dl_people),
    "num_occup": len(dl_occup),
    "num_no_birth": 0,

  }
  dl_notes = setNotesSheet(notes_obj)
  df_notes = pd.DataFrame(dl_notes)

  # Export the data frames as sheets in order and Save the Excel file
  df_sht_wd_covid.to_excel(excel_writer, sheet_name='sht_wd_covid', index=False)
  df_notes.to_excel(excel_writer, sheet_name='Notes', index=False)
  df_people_transpose.to_excel(excel_writer, sheet_name='distinctPeople', index=False)  
  df_occup_sorted.to_excel(excel_writer, sheet_name='distinctOccup', index=False)
  try:
    excel_writer.close()
    print(f"Excel file written to temp > QQTemp > PyOut.")
    return True
  except:
    print(f"Something went wrong with save/close workbook.")
    return False