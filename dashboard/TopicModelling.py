import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TopicModelling:
  def __init__(self, name):
    self.name = name
  
  def read_data(self):
    self.df = pd.read_csv('/Users/jovan/Documents/UOB-Financial-Loan-Analysis/topic_modelling/lda_results.csv', index_col=0)
    return self.df