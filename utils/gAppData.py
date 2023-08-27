"""
  gAppData.py - application data module used as global store
  available to any importing the module

  2023-08-14 SMS Second time I think to use this concept

"""

# main stats plus other data
g_app_data = {
  # stats: just keep as is not in stats obj for now
  "num_sparql_rows": {"label": "Num Rows from SPARQL ", "count": 0},
  "num_no_label": {"label": "Num No English label ", "count": 0},
  "num_people": {"label": "Num Distinct People ", "count": 0},
  "num_no_birth": {"label": "Num no Birth date ", "count": 0},
  "num_no_death": {"label": "Num no Death date ", "count": 0},
  "num_age_unknown": {"label": "Num age unknown ", "count": 0},
  "num_age_young": {"label": "Num age young ", "count": 0},
  "num_age_adult": {"label": "Num age adult ", "count": 0},
  "num_age_midlife": {"label": "Num age midlife ", "count": 0},
  "num_age_senior": {"label": "Num age senior ", "count": 0},
  "num_age_socsec": {"label": "Num age senior ", "count": 0},
  "num_age_old": {"label": "Num age old ", "count": 0},
  "num_people_multi_rows": {"label": "Num People multi rows ", "count": 0},
  "num_people_no_occup": {"label": "Num People without occup ", "count": 0},
  "num_people_multi_occup": {"label": "Num People multi occup ", "count": 0},
  "num_ocup": {"label": "Num distinct occupations ", "count": 0},

  # the main object - a dictionary for each distinct person with key = qid
  # List of all rows from SPARQL Query - only blank labels deleted
  "sparql_list": [],
  # Dictionary per person with multi occup's in dict within row
  "person_dict": {},
  "other": {
      
  }
}