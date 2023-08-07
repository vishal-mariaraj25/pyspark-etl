# example of unknown length iteration
# as with the first paging example, this code is a mockup and has not been testedimport requests
import json
import requests
from pyspark.sql.functions import udf, col, explode
from pyspark.sql import SparkSession
from pyspark.sql import Row
from Schema import get_schema

spark = SparkSession.builder.appName("AdverseEventsExtraction").getOrCreate()

# Enable Delta Lake optimization features
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")

# create an iterator to download all the data from the web service
body = json.dumps({})
MAX_PAGE_SIZE = 50 # total number of records per page
MAX_PAGES = 10 # total number pages per batch

RestApiRequestRow = Row("verb", "url", "body", "page")
firstDataFrame = True

api_queries = [
"https://api.fda.gov/drug/event.json?search=patient.drug.openfda.pharm_class_epc:'nonsteroidal+anti-inflammatory+drug'"
"https://api.fda.gov/drug/event.json?search=patient.drug.openfda.pharm_class_epc:'Thiazide+Diuretic'"
"https://api.fda.gov/drug/event.json?search=patient.drug.openfda.pharm_class_epc:'Tumor+Necrosis+Factor+Blocker'"
]

output_path = "dbfs:/mnt/delta_tables/adverse_effect"


# declare the function used by the UDF to execute HTTP requests
def executeRestApi(verb, url, body, page):
  #
  headers = {
      'Content-Type': "application/json",
      'User-Agent': "apache spark 3.x"
  }
  res = None
  # Make API request, get response object back, create dataframe from above schema.
  try:
    res = requests.get("{url}/{page}".format(url=url,page=page), data=body, headers=headers)
  except Exception as e:
    return e
  if res != None and res.status_code == 200:
    return json.loads(res.text)
  return None

# declare the UDF
udf_executeRestApi = udf(executeRestApi, get_schema())

# continue to iterate fetching records until one of the
# two conditions described above is true (HTTP status is not 200 or
#   the number of records returned is less than the expected record
#   size)
for query in api_queries:
    while True:
        pageRequestArray = []
        for iPages in range(1, MAX_PAGES):
            pageRequestArray.append(RestApiRequestRow("GET", query, body, iPages)) 

        request_df = spark.createDataFrame(pageRequestArray)
        result_df = request_df \
            .withColumn("result", udf_executeRestApi(col("verb"), col("url"), col("body"), col("page")))
        
        # Extract the 'patient.reaction' field and unnest the array
        extracted_df = result_df.select(explode(col("patient.reaction")).alias("patient_reaction"))

        # Now 'extracted_df' contains a DataFrame with a new column 'patient_reaction'
        # Each row represents a single element from the 'patient.reaction' array
        patient_df = extracted_df.select("patient_reaction.reactionmeddraversionpt", "patient_reaction.reactionmeddrapt")

        patient_df.cache()

        # save the DataFrame to storage
        if firstDataFrame == True:
            patient_df.write.format("delta").save(output_path)
            firstDateFrame = False
        else:
            patient_df.write.mode("append").format("delta").save(output_path)

        # test the responses - do we break out of the iteration loop or continue
        if result_df.count() < MAX_PAGE_SIZE:
            break

# now select the complete response dataframe from storage if needed
complete_df = spark.read.format("delta").load(output_path)