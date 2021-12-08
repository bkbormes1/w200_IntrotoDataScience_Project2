import pandas as pd
import numpy as np

def scrub():
    '''Set of rules designed to filter/scrub UFO data before analysis.'''

    def duration_scrub(dur):
        '''Converts the duration string into a number of minutes.
        Passes over the input from left-to-right. The first numerical
        character encountered starts building the number string. The number
        string ends when a non-numeric character is encountered, unless it is
        the first instance of a period in the number string.

        After completing a number string, the next step is to determine the
        type of units. Everything that is not an instance of an 'H/h', 'M/m',
        or 'S/s' is ignored until one of these is found. If none exists, then
        the default unit is minutes.

        A duration can have multiple units (e.g. '5 hours & 20 minutes') will
        work. Durataions displayed as a range (e.g. '5-10 mins') will be
        truncated to the first number in the duration (i.e. '5').

        Non-numeric data (e.g. 'five hours') can not be parsed with this
        method and will be represented as np.NaN. Entries greater than 72
        hours are also discarded as np.Nan based on a manual review.
        '''

        n = ['0','1','2','3','4','5','6','7','8','9']
        h = 0
        m = 0
        s = 0
        num_str = ''
        n_found = False
        p_found = False
        u_needed = False
        for c in str(dur):
            if n_found:
                if u_needed:
                    if c in 'Hh':
                        h += float(num_str)
                        num_str = ''
                        n_found, p_found, u_needed = False, False, False
                    elif c in 'Mm':
                        m += float(num_str)
                        num_str = ''
                        n_found, p_found, u_needed = False, False, False
                    elif c in 'Ss':
                        s += float(num_str)
                        num_str = ''
                        n_found, p_found, u_needed = False, False, False
            else:
                if c in n:
                    num_str += c
                elif c == '.' and not p_found and num_str != '':
                    p_found = True
                    num_str += c
                elif num_str != '':
                    n_found = True
                    u_needed = True
        if num_str != '':
            m += float(num_str)
        if 0 < h*60+m+s/60 <= 4320:
            return h*60+m+s/60
        return np.NaN

    def shape_clean(shape):
        '''This function is to clean the shape column by making it either one of the original top 15 shapes or making it unknown or other.'''
        top_shapes = ['light', 'circle', 'triangle', 'fireball', 'sphere', 'disk', 'oval', 'formation', 'changing', 'cigar', 'flash', 'rectangle', 'cylinder', 'diamond', 'chevron', 'other', 'unknown', '']
        if type(shape) == str:
            if shape.lower() not in top_shapes:
                shape = 'other'
            elif shape == '':
                shape = 'unknown'
        else:
            shape = 'other'
        return shape.lower()

    #Open file.
    ufo_data = pd.read_csv('ufo.csv', index_col=0)

    #Parse dates
    ufo_data.Date_Time = pd.to_datetime(ufo_data.Date_Time, errors='coerce')
    ufo_data.Posted = pd.to_datetime(ufo_data.Posted, errors='coerce')

    #Drop rows with invalid Date_Time.
    ufo_data = ufo_data[ufo_data.Date_Time.notnull()]

    #Only use data table rows that are US states
    US_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    ufo_data = ufo_data[ufo_data.State.apply(lambda x: x in US_states)]

    #Ensure city data value is a string
    ufo_data = ufo_data[ufo_data.City.apply(lambda x: type(x) == str)]

    #Make capitalization consistent.
    ufo_data['City'] = ufo_data['City'].apply(lambda x: x.lower())

    #Remove all bracketed text in city names and any leading/trailing spaces.
    ufo_data['City'] = ufo_data['City'].apply(lambda x: x.split('(')[0].strip())

    #Apply cleaning logic to duration.
    ufo_data['Duration_Mins'] = ufo_data['Duration'].apply(duration_scrub)

    #Extract and store year, month, day of month, day of week, and time.
    ufo_data['Year'] = ufo_data.Date_Time.dt.year
    ufo_data['Month'] = ufo_data.Date_Time.dt.month
    ufo_data['Day_Of_Month'] = ufo_data.Date_Time.dt.day
    ufo_data['Day_Of_Week'] = ufo_data.Date_Time.dt.day_name()
    ufo_data['Timestamp'] = ufo_data.Date_Time.dt.time
    
    #Remove data from years prior to 1940.
    ufo_data = ufo_data[ufo_data['Year'] >= 1940]

    #Clean shape data by applying function from above.
    ufo_data['Shape'] = ufo_data['Shape'].apply(shape_clean)

    return ufo_data

if __name__ == '__main__':


    #Display data
    ufo_data = scrub()
    print(ufo_data)
    print(ufo_data.describe())