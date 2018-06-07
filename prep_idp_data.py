import pandas as pd
import numpy as np
import sys
from IPython import embed
''' counts is a dictionary from word -> {nt: ntcount, nd: ndcount}'''
counts = {}

def get_counts(file, category):
    with open(file) as f:
        for line in f:
            if line.strip() != 'removed':
                for word in line.split():
                    # only alphabet, no numbers
                    if word.isalpha():
                        # if word exists, update
                        if word in counts:
                            c = counts[word]
                            # nt or nd already exists, so update
                            if category in c:
                                c[category] += 1
                            else:
                                c[category] = 1
                        # new entry  
                        else:
                            counts[word] = {category:1}

def idp(counts_df,col_name):
  """Takes in a df with raw counts for various words and returns a weight
  (association metric) for each word with the given column.
  counts_df: num_words x num_categories (e.g. -1,0,1) containing raw counts 
             of all the words in each category
  col_name: name of the category column

  returns: a pd.Series with the words as indices and the score as a float.
           The more positive a score, the more it's associated with the category.

  Source algorithm:
  Monroe, B. L., Colaresi, M. P., & Quinn, K. M. (2008). Fightin'words: Lexical feature 
     selection and evaluation for identifying the content of political conflict.
     Political Analysis, 16(4), 372-403.
  """
  counts = counts_df.copy()
  counts["all"] = counts.sum(axis=1)
  not_col_name = "not_col_name"
  counts[not_col_name] = counts[counts.columns.drop(["all",col_name])].sum(axis=1)
  sums = counts.sum(axis=0)

  f_col_name = sums[col_name]/sums['all']
  f_not_col_name = 1 - sums[col_name]/sums['all']

  l_col_name = (counts[col_name]+f_col_name*counts['all'])/((sums[col_name]+f_col_name*sums['all'])-counts[col_name]+f_col_name*counts['all'])

  l_not_col_name = (counts[not_col_name]+f_not_col_name*counts['all'])/((sums[not_col_name]+f_not_col_name*sums['all'])-counts[not_col_name]+f_not_col_name*counts['all'])

  sigma = np.sqrt(
    1.0/(counts[col_name]+f_col_name*counts['all']) + 1.0/(counts[not_col_name]+f_not_col_name*counts['all'])
  )
  delta = (np.log(l_col_name)-np.log(l_not_col_name))/sigma
  delta = delta.sort_values(ascending=False)
  return delta

def prep_df(df,agg_by):
  """If the data isn't aggregated by category, this will do that.
  E.g. the Matrices/verbs.csv file.
  """
  g = df.groupby(agg_by).sum().T
  return g
  
def WCs():
  """Cindy use this? It works with verbs.csv"""
  df = pd.DataFrame(data=counts)
  df = df.transpose()
  g = df.groupby('nt').sum().T

  nt = idp(df,"0NT")
  f30 = idp(df,"F30")
  f40 = idp(df,"F40")
  f50 = idp(df,"F50")
  x71 = idp(df,"X71")
  d = pd.DataFrame(index=nd.index)
  d["nt"] = nt
  d["f30"] =f30
  d["f40"] = f40
  d["f50"] =f50
  d["x71"] =x71
  return d

def clean_data():
    for key, value in counts.copy().items():
        if 'F30' not in value or 'nd' not in value:
            del counts[key]


if __name__ == "__main__":
    get_counts('v5_f30.txt', 'F30')
    get_counts('v5_nt.txt', '0NT')
    get_counts('v5_f40.txt', 'F40')
    get_counts('v5_f50.txt', 'F50')
    get_counts('v5_x71.txt', 'X71')
    clean_data()
    d = WCs()
    d.to_csv(path_or_buf='v5_idp')
