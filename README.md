# Yelp-Dataset-Project

This project builds a Python application which gives the user a platform to access real-world business data. The project uses the yelp open dataset to develop to populate a database. The dataset used is available in the .json files.  The data is first cleansed and prepared for insertion into the database. The dickinson_parser_v3.py is used to parse the data and create .txt files. Additional changes are made to the .txt files to produce the .sql files. The prepared .sql files are ran to insert the data into the database. The database is queried in PostreSQL in the application milestone3.py which contains the Python source code and a UI.

To run the application, the user should:
1. Clone the repository to obtain all files. At minimum, you will need all .sql files, milestone3.py, and milestone3App.ui.
2. Create a database. You will have to change the milestone3.py file to match the credentials for your database.
3. Construct and populate the database using the .sql files. In order, the following files should be run:
  1) dickinson_RELATIONS.sql
  2) zipData.sql
  3) insertBusiness.sql
  4) insertCategories.sql & insertReviews.sql
  5) reviewUpdate.sql
  6) updateCheckins.sql
  7) updatePopularity-Success.sql
4. run milestone3.py
