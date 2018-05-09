import pandas as pd
import numpy as np
import sys
from IPython import embed
''' counts is a dictionary from word -> {nt: ntcount, nd: ndcount}'''
counts = {}

def get_counts(file, category):
    with open(file) as f:
        for line in f:
            for word in line.split():
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

  nt = idp(df,"nt")
  nd = idp(df,"nd")
  d = pd.DataFrame(index=nd.index)
  d["nd"] = nd
  d["nt"] =nt
  return d

def clean_data():
    for key, value in counts.copy().items():
        if 'nt' not in value or 'nd' not in value:
            del counts[key]


if __name__ == "__main__":
    get_counts('nt_posts_scrubbing.txt', 'nt')
    get_counts('nd_posts_scrubbing.txt', 'nd')
    clean_data()
    d = WCs()
    d.to_csv(path_or_buf='idp')