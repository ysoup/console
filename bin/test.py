import json
myfile=open('a.txt','w')

a=[1,2,3,{'4': 5, '6': 7}]
json.dump(a,myfile, indent=4)

myfile.close()