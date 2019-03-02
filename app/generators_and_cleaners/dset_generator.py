import numpy as np
import pandas as pd
import datetime, random, string

""" This is a script used to generate datasets resembling real spatial occupancy
datasets. The script creates a Pandas DataFrame. Each row corresponds to a data
entry with date, time, metadata, and spatial occupancy data for each space.
Finally, a selected random proportion of data is corrupted to simulate partial
entries. """

# Generates name and languaage of the data collector
from faker import Faker
fk_author = Faker().name()
fk_email = Faker().email()
languages = ['EN', 'DE', 'FR', 'CN', 'ES', 'JP', 'KR']

def create_fake_dataset():
    fake = pd.DataFrame()

    # Lists for hours when the data was collected
    wkday_list = [10, 12, 14, 16, 18, 19, 20, 21, 22]
    wkend_list = [11, 12, 13, 14, 15, 16, 17, 18]

    # Generates a date and time data to be used for each entry
    def create_timeseries(a, b):
        dtime_list = []

        while a < b:
            if a.date().weekday() <= 4:
                for i in wkday_list:
                    temp = a + datetime.timedelta(hours = i)
                    dtime_list.append(temp.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                for i in wkend_list:
                    temp = a + datetime.timedelta(hours = i)
                    dtime_list.append(temp.strftime("%Y-%m-%d %H:%M:%S"))

            a = a + datetime.timedelta(days = 1)
        return pd.Series(dtime_list)

    strt = datetime.datetime(random.randrange(2017, 2018), random.randrange(1, 13), random.randrange(1, 28))
    end = datetime.datetime(random.randrange(2018, 2019), random.randrange(1, 13), random.randrange(1, 28))
    fake['StartDate'] = create_timeseries(strt, end)

    length = len(fake['StartDate'])

    fake['Duration (in seconds)'] = [random.randrange(300, 600) for i in range(0, length)]


    temp_enddate = fake['StartDate'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")) \
     + fake['Duration (in seconds)'].apply(lambda x: datetime.timedelta(seconds=x))

    fake['EndDate'] = temp_enddate.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))

    fake['RecordedDate'] = fake['EndDate'].copy()

    # Generates metadata for each entry
    fake['Status'] = pd.Series([1 for i in range(0, length)])
    IP_address = list(str(random.randrange(100, 200)) for i in range(4))
    fake['IPAddress'] = pd.Series([".".join(IP_address) for i in range(0, length)])
    fake['ResponseId'] = pd.Series([''.join(random.choices(string.ascii_letters + string.digits, k=16)) for i in range(0, length)])
    fake['RecipientLastName'] = fk_author.split()[1]
    fake['RecipientFirstName'] = fk_author.split()[0]
    fake['RecipientEmail'] = fk_email
    fake['ExternalReference'] = pd.Series([0 for i in range(0, length)])
    loc_lat, loc_long = random.uniform(-1,1) * 90, random.uniform(-1,1) * 180
    fake['LocationLatitude'] = pd.Series([loc_lat for i in range(0, length)])
    fake['LocationLongitude'] = pd.Series([loc_long for i in range(0, length)])
    fake['DistributionChannel'] = pd.Series(['unknown' for i in range(0, length)])
    user_lang = languages[random.randrange(0, len(languages))]
    fake['UserLanguage'] = pd.Series([user_lang for i in range(0, length)])

    fake['Q1'] = pd.Series([random.randrange(1,10) for i in range(0, length)])
    fake['Q2'] = fake['RecordedDate'].apply(lambda x: 1 if datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").weekday()<5 else 0)

    # Q8 - Weekend Time, Q11 - Weekday time
    fake['Q8'] = fake['RecordedDate'].apply(lambda x: np.NaN if datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").weekday()<5 \
        else wkend_list.index(datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").hour) + 1)
    fake['Q11'] = fake['RecordedDate'].apply(lambda x: np.NaN if datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").weekday()>=5 \
        else wkday_list.index(datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").hour) + 1)

    # Generates names for the columns corresponding to space occupancy data
    question_codes = ['Q10_1_'+str(i) for i in range(1,13)]
    max_capacities = {k: random.randrange(2, 60) for k in question_codes }

    # Occupancy data for each space
    for i in question_codes:
        fake[i] = pd.Series([(random.randrange(1, max_capacities[i]+1)) for k in range(0, length)])

    # Simulate random corruption of some rows to create a quasi-real dataset with partial entries.
    def random_corruption(dset):
        length = len(dset)
        corrupt_perc = random.uniform(0, 0.4)
        nrow_cor = round(length * corrupt_perc)
        cor_rows = random.choices([i for i in range(0,length)], k=nrow_cor)
        for cr in cor_rows:
            for i in question_codes:
                dset.loc[cr, i] = np.NaN

        return dset

    fake = random_corruption(fake)

    # Marks partial entries
    fake['Finished'] = fake[question_codes].notna().all(axis=1).astype(int)
    fake['Progress'] = fake['Finished'] * 100

    fake[question_codes] = fake[question_codes].astype(str)

    return fake, max_capacities

data, max_cap_dict = create_fake_dataset()
