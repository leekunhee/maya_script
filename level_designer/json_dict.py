import json, os

json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
parsed_json = json.loads(json_string)
json_to_string = json.dumps(parsed_json)

print json_string
print parsed_json
print json_to_string

def export_json(dict, outdir, outputname):
    if not os.path.exists(outdir + '/json/'):
        os.mkdir(outdir + '/json/')
    filename = outdir + '/json/' + outputname + '.json'
    with open(filename, 'w') as outfile:
        json.dump(dict, outfile, indent=4, sort_keys=True)
        

#loading?
# with open('filename.txt', 'r') as handle:
#     parsed = json.load(handle)