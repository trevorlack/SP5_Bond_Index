# SP5_Bond_Index

This extracts the daily index files for SP5MAIG from FTP and inserts them into
a database.  In its current form, the script will start by finding the most recent index
file date saved on the R drive in the IVY folder in order to determine which days need
to be pulled down off of FTP.  Next the script will find what the last day of records are
in the database to establish the next record day to find.  This ensures that no days are
missed as all files have to be loaded sequentially by business day with holidays accounted
for.  All eligible csv index files are inserted into a list of file paths that are then
read into a dataframe and formatted before being inserted into the database.

Raw Index File Column Headers:
    EFFECTIVE DATE, CUSIP, ISIN, SEDOL, DESCRIPTION, DESCRIPTION (OTHER), STATE, COUNTRY,
    COUPON, MATURITY DATE, EFFECTIVE MATURITY, PRICE TO DATE, CURRENCY CODE, SP RATING,
    MOODYS RATING, FITCH RATING, GICS CODE, BEG MARKET VALUE, PAR AMOUNT, PRICE,
    PRICE WITH ACCRUED, CASH, FX RATE, MARKET VALUE, AWF, ADJ MARKET VALUE, INDEX WEIGHT,
    DAILY PRICE RETURN, DAILY TOTAL RETURN, YEARS TO MATURITY, MODIFIED DURATION,
    EFFECTIVE DURATION, YIELD TO MATURITY, YIELD TO CALL, YIELD TO WORST, OA SPREAD,
    PRICING DETAILS
