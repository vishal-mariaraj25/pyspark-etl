1. How would you efficiently extract the fields related to adverse events using PySpark from the datasets available at the provided link?

    I have used pagination technique to download the data from openFDA

2. How would you design the data partitioning strategy for optimizing performance in Spark?
    a. Write operation is optimized with spark configurations for delta lake
    b. I will use hash partitioning on the "patient ID"
    c. Coalesce before write operation


3. How would you create a Spark table and store the extracted data in an open-source platform? 
    Data is stored in deltalake in delta table format.  Other options are to use HDFS table and store the same

4. How would you use Makefile to manage the ETL process and dependencies?
     Makefile attached under the scripts folder with comments
