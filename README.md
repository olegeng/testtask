# Description and notes
Simplest example of ETL.
## How it works?
Extracting from website - prepare data for load - load to different sources

!!!
Since methods here is quite simple - I decided substitute docstring by usual comment
in order to make whole script a bit more readable.
!!!

## How to change dependencies?
In order to change:
Website url - update SCRAPPING_URL in .env
Spreadsheet - update SPREADSHEET_URL in .env (also provide access to it or share it for everyone)
Credentials - add your credentials to root folder and name it creds.json or update path to it CRED_PATH (.env)


# How to start?

Dependencies which i used:
requests, gspread, pandas, dotenv, oauth2client.service_account
gspread_dataframe, bs4 (isn't my favorite tool for webscraping, but it was required)

You can install all dependencies by typing in terminal next command:

pip install -r requirements.txt

Also you can provide your own credentials as was described above
And after this, u're ready to run.

# How to run?

First of all make an instance of our class.
## And now you can run whole process by calling load() function

But further than that you can use transform and load func with different sources etc
just by passing it additional parameter (source/dataframe depends on func)
