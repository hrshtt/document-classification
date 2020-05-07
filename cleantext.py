from datetime import datetime

with open('./stats.csv', 'r') as f:
    text = f.read()
print(text)
newformat = '%d-%m-%Y %H:%M:%S'
newtext = text.split('\n')[0]
newlist = []
for line in text.split('\n')[1:]:
    line = line.split(', ')
    list_ = [datetime.strptime(line[0],"%Y-%m-%d %H:%M:%S.%f").strftime(newformat)] + line[1:]
    newtext += '\n' + ', '.join(list_)

print(newtext)
with open('./stats.csv', 'w') as f:
    text = f.write(newtext)