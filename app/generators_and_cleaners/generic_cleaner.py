import numpy as np
import pandas as pd

from dset_generator import data, max_cap_dict

""" For library's data """
# dset = pd.read_csv('datasets/test1.csv')
# max_cap = {'Q10_1_1': 31, 'Q10_1_2': 47, 'Q10_1_3': 12, 'Q10_1_4': 35,
#         'Q10_1_5': 45, 'Q10_1_6': 42, 'Q10_1_7': 17, 'Q10_1_8': 17,
#         'Q10_1_9': 29, 'Q10_1_10': 22, 'Q10_1_11': 44, 'Q10_1_12': 6}

dset = data
max_cap = max_cap_dict

print(dset.head())
print(len(dset))

#
# # Drop first two rows which aren't needed
# # dset = dset.drop([0, 1], axis=0)
# # dset = dset.reset_index(drop=True)
#
# """
# Q1 -
# Q2 - Weekday (1) or Weekend (0)
# Q8 - Weekend Time
# Q11 - Weekday Time
# """
#
# # Drop irrelevant columns
# dset = dset.drop(['StartDate', 'EndDate', 'Status', 'IPAddress',
#         'Duration (in seconds)', 'Finished', 'ResponseId',
#         'RecipientLastName', 'RecipientFirstName', 'RecipientEmail',
#         'ExternalReference', 'LocationLatitude', 'LocationLongitude',
#         'DistributionChannel', 'UserLanguage', 'Q1'], axis=1)
#
# # print(dset.head())
#
# # Renaming Columns
# dset = dset.rename({'RecordedDate': 'Date',
#             'Q2': 'Weekday',
#             'Q8': 'W-End Time',
#             'Q10_1_1':'Space1',
#             'Q10_1_2': 'Space2',
#             'Q10_1_3': 'Space3',
#             'Q10_1_4': 'Space4',
#             'Q10_1_5': 'Space5',
#             'Q10_1_6': 'Space6',
#             'Q10_1_7': 'Space7',
#             'Q10_1_8': 'Space8',
#             'Q10_1_9': 'Space9',
#             'Q10_1_10': 'Space10',
#             'Q10_1_11': 'Space11',
#             'Q10_1_12': 'Space12',
#             'Q11': 'W-Day Time'
#         }, axis='columns')
#
# """ Drops partial entries. MUST INCLUDE WHEN SHOWING MISSING DATA """
# dset['Progress'] = pd.to_numeric(dset['Progress'])
# perc_partial = len(dset[dset['Progress'] != 100]) / len(dset) * 100
# dset = dset[dset['Progress'] == 100]
# dset = dset.drop(['Progress'], axis=1)
# dset = dset.reset_index(drop=True)
# # print("Percentage of unfinished data entries: {} ".format(str(perc_partial)))
#
# """ Convert to numeric """
# for i in ['Weekday', 'W-End Time', 'W-Day Time']:
#     dset[i] = pd.to_numeric(dset[i])
#
# """Set up dates, years, months, hours"""
# import datetime
#
# dset['Date'] = pd.to_datetime(dset['Date'])
# dset['Year'] = dset['Date'].copy().apply(lambda x: x.year)
# dset['Month'] = dset['Date'].copy().apply(lambda x: x.month)
#
# """ INEFFICIENT. MUST REWRITE """
# """ USE OF MaxCapacity is unrealistic """
#
#
# # IMPORTED FROM DATASET GENERATOR
# space_names = ['Space1', 'Space2', 'Space3', 'Space4', 'Space5', 'Space6', 'Space7',
#                 'Space8', 'Space9', 'Space10', 'Space11', 'Space12']
# MaxCapacity = {k: v for (k, v) in zip(space_names, max_cap.values())}
#
# import re
# numeric_match = r'[0-9]+'
#
# """ FIX THIS SECTION """
# # test = dset.loc[57, 'Space5']
# # print(type(test))
# # print(dset['Space5'].head())
# # print(test.decode('UTF-8'))
# # print(re.match(numeric_match, test))
# #
# # exit_codes = {"NaN treatment": 0,
# #             "Out of bounds": 0,
# #             "Normal": 0,
# #             "Error": 0}
# #
# # for i in space_names:
# #          for j in range(dset.shape[0]):
# #              try:
# #                  if dset.loc[j, i] != dset.loc[j, i]:
# #                      dset.loc[j, i] = 0
# #                      exit_codes["NaN treatment"] = exit_codes["NaN treatment"] + 1
# #
# #                  elif re.match(numeric_match, dset[i][j]):
# #                      if int(re.match(numeric_match, dset[i][j]).group()) < 0 or int(re.match(numeric_match, dset[i][j]).group())> MaxCapacity[i]:
# #                          # print("Out of bounds:")
# #                          # print(dset.loc[j, i])
# #                          dset.loc[j, i]= MaxCapacity[i]/2
# #                          exit_codes["Out of bounds"] = exit_codes["Out of bounds"] + 1
# #                      else:
# #                         dset.loc[j, i] = int(re.match(numeric_match, dset[i][j]).group())
# #                         exit_codes["Normal"] = exit_codes["Normal"] + 1
# #                  else:
# #                      # print("Random string:")
# #                      # print(i,j)
# #                      # print(dset[i][j])
# #                      dset.loc[j, i] = MaxCapacity[i]/2
# #                      exit_codes["Error"] = exit_codes["Error"] + 1
# #              except Exception as e:
# #                  exit_codes["Error"] = exit_codes["Error"] + 1
# #                 # print("Error. MUST BE INSPECTED")
# #                 # print(dset.loc[j, i])
# #                 # print(i,j)
# #                 # print(e)
# #                 # print('-----------------')
# #
# # # print(dset.head())
# # print("Success!")
# # print(exit_codes)
# #
# # # """ Aggregate Group Study Rooms """
# # # dset['Spaces'] = dset['Space2'] + dset['Space3'] + dset['Space4']
# # # dset['Spacs'] = dset['Space5'] + dset['Space7'] + dset['Space8'] + dset['Space9']
# # #
# """ Calculate total occupancy for each entry """
# dset['Total'] = dset[space_names].sum(axis=1)
#
# """ Creating a new dataset, which includes percentage occupancies for library
#     and separate spaces within it """
# data_to_plot = dset.filter(['Year', 'Month', 'Weekday', 'W-End Time', 'W-Day Time'], axis=1)
#
# total_cap = sum(MaxCapacity.values())
# data_to_plot['Total_perc'] = dset['Total'] / total_cap * 100
# # MaxCapacity (decleared earlier) is used for specific spaces.
#
# for i in space_names:
#         data_to_plot[i+"_perc"] = dset[i] / MaxCapacity[i] * 100
#
# """ REMEMBER TO UNCOMMENT"""
# # data_to_plot.to_csv('datasets/perc_occup_data.csv')
# data_to_plot.to_csv('datasets/test2.csv')
# print(data_to_plot.head())
# print("Success!")
