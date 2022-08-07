Various assumptions and prerequisites made while doing the development were listed in forth coming pages.


Prerequisites:

1.   Miniconda installed for package management and environment management.
2.   pgAdmin installed which open source PostgreSQL administration and development platform
       that runs on Linux.
3.   Sample data is handy with us i.e. csv file having pricing records from retail stores which
       contain Store ID, SKU, Product Name, Price, Date.
4.   Rest all common utilities like file editor, browser and other have to be present in system.




Assumptions:

1.    It is assumed that database i.e. retail_analytics and schema i.e. retail are already created
        in database server and git is installed in the system.

2.    When user will upload the data the response will show all data present in database sorted on
       the basis of Store ID.




3.    Search Operation for pricing records can be made by entering the details requested in pop up
       form on click Search button, where it basically asks user to enter Store ID, SKU, Product Name
       and Price. Out of these any of the fields can be left blank but it is recommended to have
       atleast enter value for one of them.
       Therefore, whatever information entered in form have to matched with ORM query in the
       method defined on its call and post matching within database it will show records that
       satisfies the given condition else it will return with a message “There are no records to
       display”.

4.    Update Operation for pricing records can be made by entering the details requested in pop
       up form on click Update button, where it was assumed that the details will not be auto
       populated and details have to entered manually by user in form which post interaction with
       corresponding ORM query  firsts find out whether record exists or not , if yes then it will
       update record ( can either update a single record or multiple records ) as per ORM update
       query and will display all results else it will return with a  message “There is no record to
       undergo update operation”.

5.    Delete Operation for pricing records can be made by entering the details requested in pop
       up form on click Delete button, where it was assumed that the details will not be auto
       populated and details have to entered manually by user in form which post interaction with
       corresponding ORM query  firsts find out whether record exists or not , if yes then it will
       delete record ( can either update a single record or multiple records ) as per ORM update
       query and will display all results else it will return with a  message “There is no record to
       undergo delete operation”.

6.     Since, it had been asked to make web application that could perform search for pricing
        records using various criteria so, for this it totally depends on ORM query that will be present
        in code. Therefore, I had tried to put on various formats of query that could do search
        operation but yeah there are many more also and I believe while doing PoC it is not
        possible to cover up all scenarios.

7.     As logging was implemented in application and it basically needs some location in system
        to create logs. Therefore, at the given path -
       “retail_analytics/utils/logger/config/applicationconfig.ini” , it requires a change in two
        parameters values i.e. logRoot and logDir and therefore was assumed their locations
        exists in system.

8.     Sample document is attached in retail_analytics_case_study/retail_analytics/retail.csv.

9.      It was assumed that post doing any operation user will have to move back to the
         page displaying all buttons.


ReadME.md --

# retail_analytics_case_study
This is about how the retail stores data is used for doing various kind of analysis which could be in turn to find out their most selled products or many more such occurrences.





Steps to run the application (Considering all prerequisites and assumptions listed above are met ) :

1.   We have to clone the repository using the command given below : 
        git clone https://github.com/amanag1/retail_analytics_case_study.git

2.   Go to retail_analytics_case_study/retail_analytics foler.

3.  Create conda environment using the command given below :
    conda create -n <ENV_NAME> python=3.9 , here replace <ENV_NAME>  with the nane of environnment you want to give, for reference see below:
      conda create -n retail_env python=3.9

	   To activate this environment, use
	      conda activate retail_env
	   To deactivate an active environment, use
	      conda deactivate

4.  Post successful creation of conda environment now it comes to install few more packages required to run the application.
    First, we need to activate the environment as mentioned in Step 1 and then have to execute the following commands in same terminal to install
    dependencies:
      pip install Flask-SQLAlchemy
      pip install pandas
      pip install jsonformatter
      pip install psycopg2
      pip install SQLAlchemy
      pip install Flask
      pip install pytest


5.  Now, open a terminal and activate respected conda environment using the command mentioned in Step 1.
    Post activation execute the following commands to start the flask application:

	export FLASK_APP=retail.py
	export FLASK_ENV=development
               export FLASK_DEBUG=1
	flask run

     Application will start on url : http://127.0.0.1:5000/home
     Therefore, user can perform file upload, search, update and delete operation.


6.     Now, open a terminal and activate respected conda environment using the command
        mentioned in Step 1.



    Post activation execute the following command to test for various test cases:
     pytest

      Moreover, test results and inputs and outputs of various operations of application can
      be seen in another document attached named as
      Retail_Case_Study_Test_Cases/Retail_Case_Study_Test_Results.docx
