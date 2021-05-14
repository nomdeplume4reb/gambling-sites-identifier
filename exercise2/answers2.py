#installation as needed:
#import sys
#import subprocess

# implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'pandas'])

#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'json'])

import pandas as pd
import json

#1. Create a CSV file, with a header, that contains the fullname, age, address and occupation.

data = pd.read_json (r'C:/Users/rache/Downloads/Junior Content Analyst/exercise2/data.json')
df = data.transpose().rename_axis('fullname').reset_index()
df.to_csv (r'C:/Users/rache/Downloads/Junior Content Analyst/exercise2/data.csv', index = None)

#2. Generate statistics (in JSON format)

# new data frame with split value columns
new = df["fullname"].str.split(" ", expand = True)

# making separate firstname and lastname columns from new data frame
df["firstname"]= new[0]
df["lastname"]= new[1]

#drop fullname and lastname columns
df = df.drop(columns=['fullname', 'firstname'])

#get counts for each lastname
s = df.groupby(['lastname']).size()

#create dataframe of counts for each variable grouped by lastname
df2 = df.melt(id_vars=["lastname"])
df2 = df2.groupby(['lastname', 'variable', 'value'], as_index = False).size()

#set up dictionary with keys for count, age, address, occupation
stats_dict = {}

for i, v in s.items():
    stats_dict.update({i: {'count': v, 'age': {}, 'address': {}, 'occupation': {}}})

#update dictionary with counts from dataframe
for index, row in df2.iterrows():
    stats_dict[row['lastname']][row['variable']].update({row['value']:row['size']})

#convert to json
stats_json = json.dumps(stats_dict, indent = 4)

print(stats_json)

#3. Imagine you are now given 20 JSON inputs. How will you minimize the runtime for the above tasks?

#I'm assuming all 20 JSON inputs already have the same format.

#create function to repeat for more JSON inputs. The function accepts a list of file paths

def get_stats_json(filepathlist):
    # read folder where jsons are located

    #set up dictionary with keys for count, age, address, occupation
    stats_dict = {}

    for filepath in filepathlist:
        #repeat steps above
        data = pd.read_json (filepath)
        df = data.transpose().rename_axis('fullname').reset_index()

        #2. Generate statistics (in JSON format)

        # new data frame with split value columns
        new = df["fullname"].str.split(" ", expand = True)

        # making separate firstname and lastname columns from new data frame
        df["firstname"]= new[0]
        df["lastname"]= new[1]
        del new
        #drop fullname and lastname columns
        df = df.drop(columns=['fullname', 'firstname'])

        #get counts for each lastname
        s = df.groupby(['lastname']).size()

        #create dataframe of counts for each variable grouped by lastname
        df2 = df.melt(id_vars=["lastname"])
        df2 = df2.groupby(['lastname', 'variable', 'value'], as_index = False).size()

        for i, v in s.items():
            stats_dict.update({i: {'count': v, 'age': {}, 'address': {}, 'occupation': {}}})

        #update dictionary with counts from dataframe
        for index, row in df2.iterrows():
            stats_dict[row['lastname']][row['variable']].update({row['value']:row['size']})

    stats_json = json.dumps(stats_dict, indent = 4)
    print(stats_json)

path = ['C:/Users/rache/Downloads/Junior Content Analyst/exercise2/data.json']
get_stats_json(path)

# I reduce runtime by keeping most variables local within the function and avoid slower loops like while
