#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 18:27:20 2024

@author: isabel_orlando
"""

#turn this string into chunks of useable information 

#slice up the string for each element (i) of the list 
#store the slices in variables,  which I pass to the dataframe, 
#then do it for each gym 

#ISSUE: HOW TO MAKE SURE THEY ARE A STRING??? 

import calendar 
from datetime import datetime
import pytz

def get_name(s):
    
    marker = ">"
    first = s.split(marker, 1)[1]
    last_marker = "<br/>"
    last = first.split(last_marker, 1)[0]
    return last

def get_count(s):
    
    marker = "Count:"
    first = s.split(marker, 1)[1].strip()
    last_marker = "<br/>"
    last = first.split(last_marker, 1)[0]
    return last
    

def get_date(s):
    
    marker = "Updated:"
    first = s.split(marker, 1)[1].strip()
    return first[:10]

def get_time(s):
    
    marker = "Updated:"
    first = s.split(marker, 1)[1].strip()
    return first[11:19]

def find_day(a):
    
    date=get_date(a)
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", 
            "Saturday", "Sunday"]
    month, day, year = (int(i) for i in date.split('/'))
    
    dayNumber=calendar.weekday(year, month, day)
    
    return days[dayNumber]

def is_current_date(a):
    '''
    

    Returns True if the extracted date from the string matches the actual 
    current date at the time of running the function. Else, returns False

    '''
    
    date = get_date(a)
    est=pytz.timezone('US/Eastern')
    
    month, day, year = (int(i) for i in date.split('/'))
    
    today = datetime.now(est)
    
    return today.month == month and today.day == day and today.year == year
    
    #'<div style="text-align:center;">Toni Morrison Fitness Center<br/>Last Count: 16<br/>Updated: 08/11/2024 05:06 PM</div>'
    
    
    
