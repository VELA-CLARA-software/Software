import simplejson as json
import yaml

f = open('cla.json', 'r')
jsonData = json.load(f)
f.close()

ff = open('CLA.yaml', 'w+')
yaml.dump(jsonData, ff, allow_unicode=True)
