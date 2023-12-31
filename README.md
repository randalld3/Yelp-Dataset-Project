# Yelp-Dataset-Project

This project builds a Python application which gives the user a platform to access real-world business data. The project uses the yelp open dataset to develop to populate a database. The dataset used is available in the .json files.  The data is first cleansed and prepared for insertion into the database. The dickinson_parser_v3.py is used to parse the data and create .txt files. Additional changes are made to the .txt files to produce the .sql files. The prepared .sql files are ran to insert the data into the database. The database is queried in PostreSQL in the application milestone3.py which contains the Python source code and a UI.

To run the application, the user should:
1. Clone the repository to obtain all files. At minimum, you will need all .sql files, milestone3.py, and milestone3App.ui.
2. Unzip insertReviews.zip.
3. Create a database. You will have to change the milestone3.py file to match the credentials for your database.
4. Construct and populate the database using the .sql files. In order, the following files should be run:
  a) dickinson_RELATIONS.sql
  b) zipData.sql
  c) insertBusiness.sql
  d) insertCategories.sql & insertReviews.sql
  e) reviewUpdate.sql
  f) updateCheckins.sql
  g) updatePopularity-Success.sql
5. run milestone3.py
