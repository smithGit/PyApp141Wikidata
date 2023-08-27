"""
  pyApp141GetGoogle.py - initial version simply to get Google LLC item
  from: https://www.jcchouinard.com/wikidata-api-python/
  jean-christophe chouinard seo expert in quebec city

  2023-08-11 SMS First Python app to access Wikidata!
  Folder: cd "D:/All_Prog4_Python/PyApp141Wikidata/"

"""
import requests
import pprint
pp = pprint.PrettyPrinter(indent = 2)

def decode_wd_item(data):
  # get many common Wikidata attributes
  try:
    title = data['entities'][id]['labels']['en']['value']
  except:
    title = 'not_found'
  try:
      alternate_names = [v['value'] for v in data['entities'][id]['aliases']['en']]
  except:
      alternate_names = 'not_found'
  try:
      description = data['entities'][id]['descriptions']['en']['value'] 
  except:
      description = 'not_found'
  try:
      twitter = data['entities'][id]['claims']['P2002'][0]['mainsnak']['datavalue']['value']
  except:
      twitter = 'not_found'
  try:
      facebook = data['entities'][id]['claims']['P2013'][0]['mainsnak']['datavalue']['value']
  except:
      facebook = 'not_found'
  try:
      linkedin = data['entities'][id]['claims']['P4264'][0]['mainsnak']['datavalue']['value']
  except:
      linkedin = 'not_found'
  try:
      youtube = data['entities'][id]['claims']['P2397'][0]['mainsnak']['datavalue']['value']
  except:
      youtube = 'not_found'
  try:
      instagram = data['entities'][id]['claims']['P2003'][0]['mainsnak']['datavalue']['value']
  except:
      instagram = 'not_found'
  try:
      subreddit = data['entities'][id]['claims']['P3984'][0]['mainsnak']['datavalue']['value']
  except:
      subreddit = 'not_found'
  try:
      instance_of = [v['mainsnak']['datavalue']['value']['numeric-id'] for v in data['entities'][id]['claims']['P31']]
  except:
      instance_of = 'not_found'
  try:
      part_of = [v['mainsnak']['datavalue']['value']['id'] for v in data['entities'][id]['claims']['P361']]
  except:
      part_of = 'not_found'
  try:
      founded_by = [v['mainsnak']['datavalue']['value']['numeric-id'] for v in data['entities'][id]['claims']['P112']]
  except:
      founded_by = 'not_found'
  try:
      nick_names = [v['mainsnak']['datavalue']['value']['text'] for v in data['entities'][id]['claims']['P1449']]
  except:
      nick_names = 'not_found'
  try:
      official_websites = [v['mainsnak']['datavalue']['value']for v in data['entities'][id]['claims']['P856']]
  except:
      official_websites = 'not_found'
  try:
      categories = [v['mainsnak']['datavalue']['value']['numeric-id'] for v in data['entities'][id]['claims']['P910']]
  except:
      categories = 'not_found'
  try:
      inception = data['entities'][id]['claims']['P571'][0]['mainsnak']['datavalue']['value']['time']
  except:
      inception = 'not_found'
  try:
      latitude = data['entities'][id]['claims']['P625'][0]['mainsnak']['datavalue']['value']['latitude']
      longitude = data['entities'][id]['claims']['P625'][0]['mainsnak']['datavalue']['value']['longitude']
  except:
      latitude = 'not_found'
      longitude = 'not_found'
  
  result = {
      'wikidata_id':id,
      'title':title,
      'description':description,
      'alternate_names':alternate_names,
      'twitter':twitter,
      'linkedin':linkedin,
      'instagram':instagram,
      'youtube':youtube,
      'subreddit':subreddit,
      'instance_of':instance_of,
      'part_of':part_of,
      'founded_by':founded_by,
      'inception':inception,
      'nick_names':nick_names,
      'official_websites':official_websites,
      'main_categories':categories,
      'latitude':latitude,
      'longitude':longitude
      }
  
  return(result)

def get_recursively(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    # for key, value in search_dict.iteritems():
    for key, value in search_dict.items():

        if key == field:
            print(f"key is: {field}")
            fields_found.append(value)

        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                print(f"in dict: {result}")
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                print(f"in list: {type(item)}")
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        print(f'item in dict in list: {another_result}')
                        fields_found.append(another_result)

    return fields_found


def fetch_wikidata(my_params):
  url = 'https://www.wikidata.org/w/api.php'
  try:
    return requests.get(url, params = my_params)
  except:
    return "Error in Get command: is an error type returned?"
  
# What text to search for
query = 'Google LLC'
 
# Which parameters to use
params = {
  'action': 'wbsearchentities',
  'format': 'json',
  'search': query,
  'language': 'en'
}
if False: 
  # Fetch API
  data = fetch_wikidata(params)
  
  #show response as JSON
  data = data.json()
  print(f"resp for google: searchinfo: {data['searchinfo']}")
  print(f"resp for google: search: {data['search']}")
  print(f"resp for google: success: {data['success']}")
  for item in data['search']:
    for key, value in item.items(): # not working right; how to list dict?
      print(f"key {item} value======= {value}")
  print(f"first item {data['search'][0]['id']}")

  # Create parameters
  id = 'Q95'
  params = {
    'action': 'wbgetentities',
    'ids':id, 
    'format': 'json',
    'languages': 'en'
  }
 
# fetch the API
data = fetch_wikidata(params)

print('keys:')
pp.pprint(data['entities'][id]['claims'].keys())
# Show response
data = data.json()
print("fetched by id:")
print(data)
print("calling recurse")
ar = get_recursively(data, "id")
print(f"ar... {ar}")
result = decode_wd_item(data)
print("result attributes:")
pp.pprint(result)
