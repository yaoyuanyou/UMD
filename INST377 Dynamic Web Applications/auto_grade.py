#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 16:14:43 2024

@author: tonyyao
"""

import pandas as pd
import re
import os

#Read student roster    
grade_csv = pd.read_csv('/Users/tonyyao/Desktop/University of Maryland - College Park/INST377 Dynamic Web Applications/2024-02-05T1606_Grades-INST377.csv'
                        ,index_col="Student")
#Read student submission
path = '/Users/tonyyao/Desktop/University of Maryland - College Park/INST377 Dynamic Web Applications/lab1/'
file_names = [f for f in os.listdir(path) if f.endswith('.html')]

for name in grade_csv.index[2:-1]:
    points = 20 #Full points
    note = '' #Reason for losing points
    re_name = re.sub('[, \-()]','',name.lower()) #Student lastname + firstname
    file_name = [x for x in file_names if re_name in x] #Find corresponding submission
    
    if len(file_name) == 0: #If no submission
        grade_csv.loc[name, 'Lab 1 (6677450)'] = 0
        grade_csv.loc[name, 'Lab 2 (6677451)'] = "No Submission"
        continue
    
    file_name = file_name[0]
    html_file = open(path + file_name)
    html_str = html_file.read()
    if "</title>" not in html_str:
        points -= 1
        note += "No Title; "
    if "<img" not in html_str:
        points -= 2
        note += "No Image; "
    if "</h1>" not in html_str:
        points -= 1
        note += "No h1; "
    if "</h2>" not in html_str:
        points -= 1
        note += "No h2; "
    if "</h3>" not in html_str:
        points -= 1
        note += "No h3; "
    if "</ul>" not in html_str and "</li>" not in html_str:
        points -= 2
        note += "No Unordered List; "
    if "</ol>" not in html_str:
        points -= 2
        note += "No Ordered List; "
    if "</table>" not in html_str:
        points -= 6
        note += "No Table; "
    elif html_str.count("</tr>") < 2:
        points -= 2
        note += "Not Enough rows; "
    elif html_str.count("</td>") < 2:
        points -= 2
        note += "Not Enough columns; "    
    elif "</th>" not in html_str:
            points -= 2
            note += "No Row Heading; "
    if "&#" not in html_str and len([dec for dec in html_str if ord(dec) > 127]) == 0:    
        points -= 1
        note += "No Emoji; "
    if "background" not in html_str:
        points -= 1
        note += "No Background Color; "
    if "</blockquote>" not in html_str:
        points -= 1
        note += "No Blockquote; "
    if "</a>" not in html_str:
        points -= 1
        note += "No Hyperlink; "
    html_file.close()
    grade_csv.loc[name, 'Lab 1 (6677450)'] = points
    grade_csv.loc[name, 'Lab 2 (6677451)'] = note

#Output result
grade_csv.to_csv('/Users/tonyyao/Desktop/grade.csv')
