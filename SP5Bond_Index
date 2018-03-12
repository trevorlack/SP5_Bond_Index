from MySQL_Probe import *
from CALENDAR import *
import pymysql
from sqlalchemy import create_engine
from SP5MAIG_FTP import *

home_dir = '-:\\-\\-\\-\\-\\-\\-'
access_token = MySQL_Auth()
conn = pymysql.connect(host='localhost', port=-----, user='-----', passwd=access_token, db='-----')
engine = create_engine('mysql+pymysql://-----:%s@-----/------' %(access_token))


def check_file_type(file):

    '''Determine which index file is being inserted.  Distiguishing between the pro-forma
    and the daily index files allows the possibility calculate index performance over the rebal
    cycle.
        Result sent to `read_index()`
    '''

    daily_file = 'daily'
    proforma = 'pro-forma'
    last_day = 'daily_last_day'

    rebal_dates = ['20171229', '20171130', '20171031', '20170929', '20170831',
                   '20170731', '20170630', '20170531', '20170428', '20170331',
                   '20170228', '20170131', '20180131', '20180228', '20180330',
                   '20180430', '20180531', '20180629', '20180731', '20180831'
                   ]

    if file[-10:-6] == '_PRO':
        # pro-forma files may change leading up to rebal day
        print('Pro-Forma file detected.  Compare new files to previous versions as index constituents could change leading up to the rebal.')
        return proforma

    elif file[-10:-6] == '_CLS':
        # Delete any existing pro-forma record from table before insert
        if file[0:8] in rebal_dates:
            print('last_day')
            #if file[0:8] > rebal_dates[-1]:
                #print('Update Rebal Dates Calendar!!!!! (variable name = rebal_dates)')
            return last_day
        else:
            return daily_file

    else:
        print(file + 'Error: Unknown File Type')
        sys.exit()

def find_files():
    '''
    Check current Database records to find the last record date of data to find the
    next file date to insert.  Results need to account for the file_type.
    '''
    files = []
    os.chdir(home_dir)
    last_day = pull_last_PIG_index_date()
    next_day = get_next_day(last_day)
    today = date.today()

    if next_day == today:
        print('Database updated through yesterday')
        sys.exit()
    os.chdir('-:/-/-/Index Holdings')

    for file in list(glob.glob("*.SPFIC")):
        file_date = file[0:8]
        file_date = datetime.strptime(file_date, "%Y%m%d").strftime('%Y-%m-%d')
        if file_date == next_day:
            files.append(file)
        else:
            ###
            #Increase the range for eligible criteria
            ###
            continue
    if not files:
        print('No files returned with yesterdays date')
        sys.exit()
    else:
        return files

def index_to_mysql(df, file):

    df.to_sql('sp5maig_index', engine, if_exists='append', index=False)
    print(file + ' Success')

def read_index(file):

    index_df = pd.read_csv(file, delimiter='\t')
    # Drop cash line item
    index_df = index_df.loc[index_df['DESCRIPTION'] != 'CASH USD 0.00%']

    # Calculate index weights
    #index_df['weight'] = index_df['MARKET VALUE'] / index_df['MARKET VALUE'].sum()
    index_df.rename(columns={'EFFECTIVE DATE': 'EFFECTIVE_DATE',
                     'CUSIP': 'CUSIP',
                     'ISIN': 'ISIN',
                     'SEDOL': 'SEDOL',
                     'DESCRIPTION': 'DESCRIPTION',
                     'DESCRIPTION (OTHER)': 'DESCRIPTION_OTHER',
                     'STATE': 'STATE',
                     'COUNTRY': 'COUNTRY',
                     'COUPON': 'COUPON',
                     'MATURITY DATE': 'MATURITY_DATE',
                     'EFFECTIVE MATURITY': 'EFFECTIVE_MATURITY',
                     'PRICE TO DATE': 'PRICE_TO_DATE',
                     'CURRENCY CODE': 'CURRENCY_CODE',
                     'SP RATING': 'SP_RATING',
                     'MOODYS RATING': 'MOODYS_RATING',
                     'FITCH RATING': 'FITCH_RATING',
                     'GICS CODE': 'GICS_CODE',
                     'BEG MARKET VALUE': 'BEG_MARKET_VALUE',
                     'PAR AMOUNT': 'PAR_AMOUNT',
                     'PRICE': 'PRICE',
                     'PRICE WITH ACCRUED': 'PRICE_WITH_ACCRUED',
                     'CASH': 'CASH',
                     'FX RATE': 'FX_RATE',
                     'MARKET VALUE': 'MARKET_VALUE',
                     'AWF': 'AWF',
                     'ADJ MARKET VALUE': 'ADJ_MARKET_VALUE',
                     'INDEX WEIGHT': 'INDEX_WEIGHT',
                     'DAILY PRICE RETURN': 'DAILY_PRICE_RETURN',
                     'DAILY TOTAL RETURN': 'DAILY_TOTAL_RETURN',
                     'YEARS TO MATURITY': 'YEARS_TO_MATURITY',
                     'MODIFIED DURATION': 'MODIFIED_DURATION',
                     'EFFECTIVE DURATION': 'EFFECTIVE_DURATION',
                     'YIELD TO MATURITY': 'YIELD_TO_MATURITY',
                     'YIELD TO CALL': 'YIELD_TO_CALL',
                     'YIELD TO WORST': 'YIELD_TO_WORST',
                     'OA SPREAD': 'OA_SPREAD',
                     'PRICING DETAILS': 'PRICING_DETAILS'}, inplace=True)

    #add the file type to the dataframe
    file_code = check_file_type(file)
    index_df['record_type'] = file_code
    return index_df

def main():

    ftp_main()
    index_file = find_files()
    print(index_file)
    for file in index_file:
        index_DataFrame = read_index(file)
        index_to_mysql(index_DataFrame, file)


if __name__ == "__main__":
    # execute only if run as a script
    main()
