import pandas as pd
import sys

if len(sys.argv) > 2:
    old_file_name = sys.argv[1]
    new_file_name = sys.argv[2]
else:
    print("Please append CSV filenames for old and new datasets. Terminating!")
    sys.exit()

seperator = input("enter CSV seperator character:")

try:
    old_df = pd.read_csv(old_file_name, encoding='utf-8', sep=seperator)
    new_df = pd.read_csv(new_file_name, encoding='utf-8', sep=seperator)
except Exception as e:
    print(e)
    sys.exit()

old_names = list(old_df['tgid'])#name
new_names = list(new_df['tgid'])#name


removed =  list(set(old_names) - set(new_names))
removed_df = old_df[old_df['tgid'].isin(removed)]#name
removed_df = removed_df.sort_values(by=['count'], ascending=False)
print("==========REMOVED==========")
print(removed_df[['name','title','location','category','count']].to_markdown())

removed_df.to_csv("removed.csv", sep=';', encoding='utf-8', index=False)

added =  list(set(new_names) - set(old_names))
added_df = new_df[new_df['tgid'].isin(added)]#name
added_df = added_df.sort_values(by=['count'], ascending=False)
print("==========ADDED==========")
print(added_df[['name','title','location','category','count']].to_markdown())

added_df.to_csv("added.csv", sep=';', encoding='utf-8', index=False)

# new_df['diff'] = 0

# for index, row in new_df.iterrows():
#     if row['tgid'] not in added:
#         old_row = old_df.loc[old_df['tgid'] == row['tgid']]#name
#         old_count = old_row['count'].values[0]
#         diff = row['count'] - old_count
#         new_df.loc[index,'diff'] =  int(diff)

def get_diff(row):
    if row['tgid'] not in added:
        old_row = old_df.loc[old_df['tgid'] == row['tgid']]#name
        if len(old_row) == 0:
            return 0
        old_count = old_row['count'].values[0]
        diff = row['count'] - old_count
        if pd.isna(diff):
            return 0
        else:
            return int(diff)
    else:
        return 0

new_df['diff'] = new_df.apply(get_diff, axis=1)
new_df['diff'] = new_df['diff'].astype(int)

new_df = new_df.sort_values(by=['diff'])
print("==========LOOSERS==========")
print(new_df.head(20))


new_df = new_df.sort_values(by=['diff'], ascending=False)
print("==========WINNERS==========")
print(new_df.head(20))

new_df.to_csv("diff.csv", sep=';', encoding='utf-8', index=False)