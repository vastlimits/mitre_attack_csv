#!/usr/bin/python3 

import csv
import json
import requests
import markdown
extensions = ['markdown_link_attr_modifier', ]
extension_configs = {
    'markdown_link_attr_modifier': {
        'new_tab': 'on'
    },
}


url = "https://github.com/mitre/cti/raw/master/enterprise-attack/enterprise-attack.json"
outfile = "annotation_mitre_attack.csv"

print("Fetching latest enterprise-attack.json ...")
d = requests.get(url)
assert (d.status_code==200),"Failure fetching url"

print("Parsing file ...")
j = d.json()
assert ('spec_version' in j), "Failure reading version info in JSON file"
assert ('objects' in j), "Failure reading objects in JSON file"
assert (j['spec_version'] == '2.0'), "Unsupported STIX version"

o = {}	# dict objects
for i in j['objects']:
	assert ('type' in i), f"type information is missing in entry {i}"
	assert ('id' in i), f"id field is missing in entry {i}"

	# skip revoked or deprecated items
	if ('revoked' in i and i['revoked']==True) or ('x_mitre_deprecated' in i and i['x_mitre_deprecated']==True):
		continue

	id = i['id']
	t = i['type']

	if t not in o: o[t] = {}
	o[t][id] = i

print("Generating list of tactics ...")

# Generate a list of tactics
tactics = {}
for t in o['x-mitre-tactic']:
	short_name = o['x-mitre-tactic'][t]["x_mitre_shortname"]
	name = o['x-mitre-tactic'][t]["name"]
	id = o['x-mitre-tactic'][t]['external_references'][0]["external_id"]
	url = o['x-mitre-tactic'][t]['external_references'][0]["url"]

	tactics[short_name] = name

# Convert to html
def tohtml(s, encodeonly = False):
	if (encodeonly == True):
		if type(s) is str:
			result = s.encode('ascii', 'xmlcharrefreplace').decode()
		elif type(s) is list:
			result = []
			for i in s:
				i = i.encode('ascii', 'xmlcharrefreplace').decode()
				result.append(i)
		else:
			assert (s), "Unexptected type"

	else:
		if type(s) is str:
			s = s.replace('\\n*','\\n')	
			s = s.encode('ascii', 'xmlcharrefreplace').decode()
			result = markdown.markdown(s, extensions=extensions, extension_configs=extension_configs)
		elif type(s) is list:
			result = []
			for i in s:
				i = i.replace('\\n*','\\n')	
				i = i.encode('ascii', 'xmlcharrefreplace').decode()
				i = markdown.markdown(i, extensions=extensions, extension_configs=extension_configs)
				result.append(i)
		else:
			assert (s), "Unexptected type"

	return result

print("Generating list of techniques ...")
# Generate a list of techniques
tech = {}
for tn in o['attack-pattern']:
	t = o['attack-pattern'][tn]

	mitre_id = ""
	mitre_url = ""
	if 'external_references' in t:
		for r in t['external_references']:
			if 'source_name' in r and r['source_name'] == 'mitre-attack':
				mitre_id = r['external_id']
				mitre_url = r['url']
	assert mitre_id!="",f"Didn't find a mitre id for {t}"

	name = t['name'] if 'name' in t else ""
	name = tohtml(name, True)
	platforms = t['x_mitre_platforms'] if 'x_mitre_platforms' in t else []
	platforms = tohtml(platforms, True)
	kill_chain_phases = t['kill_chain_phases'] if 'kill_chain_phases' in t else []
	kill_chain_phases = [tactics[x['phase_name']] for x in kill_chain_phases if x['kill_chain_name']=="mitre-attack"]
	kill_chain_phases = tohtml(kill_chain_phases, True)
	data_sources = t['x_mitre_data_sources'] if 'x_mitre_data_sources' in t else [] 
	data_sources = tohtml(data_sources, True)
	description = t['description'] if 'description' in t else ""
	description = tohtml(description)
	detection = t['x_mitre_detection'] if 'x_mitre_detection' in t else ""
	detection = tohtml(detection)

	tech[mitre_id] = (name, tn, mitre_url, platforms, kill_chain_phases, data_sources, detection, description)

print("Generating CSV file ...")
with open(outfile,'w',newline='\n') as out:
	writer = csv.DictWriter(out, ['name', 'id', 'url', 'platforms', 'kill chain phases', 'description', 'data sources', 'detection'], quoting=csv.QUOTE_ALL)
	writer.writeheader()	

	for tid in sorted(tech.keys()):
		t = tech[tid]
	 
		name = t[0]
		tn = t[1]
		mitre_url = t[2]
		platforms = ', '.join(t[3])
		kill_chain_phases = ', '.join(t[4])
		data_sources = ', '.join(t[5])
		detection = t[6]
		description = t[7]

		writer.writerow({'name':name, 'id':tid, 'url':mitre_url, 'platforms':platforms, 'kill chain phases':kill_chain_phases, 'description':description, 'data sources':data_sources, 'detection':detection})
		
