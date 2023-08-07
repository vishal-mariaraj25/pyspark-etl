from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType

# Define the schema for the JSON data
json_schema = StructType([
    StructField("meta", StructType([
        StructField("disclaimer", StringType()),
        StructField("terms", StringType()),
        StructField("license", StringType()),
        StructField("last_updated", StringType()),
        StructField("results", StructType([
            StructField("skip", IntegerType()),
            StructField("limit", IntegerType()),
            StructField("total", IntegerType())
        ]))
    ])),
    StructField("results", ArrayType(StructType([
        StructField("safetyreportversion", StringType()),
        StructField("safetyreportid", StringType()),
        StructField("primarysourcecountry", StringType()),
        StructField("transmissiondateformat", StringType()),
        StructField("transmissiondate", StringType()),
        StructField("reporttype", StringType()),
        StructField("serious", StringType()),
        StructField("seriousnessother", StringType()),
        StructField("receivedateformat", StringType()),
        StructField("receivedate", StringType()),
        StructField("receiptdateformat", StringType()),
        StructField("receiptdate", StringType()),
        StructField("fulfillexpeditecriteria", StringType()),
        StructField("companynumb", StringType()),
        StructField("duplicate", StringType()),
        StructField("reportduplicate", StructType([
            StructField("duplicatesource", StringType()),
            StructField("duplicatenumb", StringType())
        ])),
        StructField("primarysource", StructType([
            StructField("reportercountry", StringType()),
            StructField("qualification", StringType())
        ])),
        StructField("sender", StructType([
            StructField("sendertype", StringType()),
            StructField("senderorganization", StringType())
        ])),
        StructField("receiver", StructType([
            StructField("receivertype", StringType()),
            StructField("receiverorganization", StringType())
        ])),
        StructField("patient", StructType([
            StructField("patientsex", StringType()),
            StructField("reaction", ArrayType(StructType([
                StructField("reactionmeddraversionpt", StringType()),
                StructField("reactionmeddrapt", StringType())
            ]))),
            StructField("drug", ArrayType(StructType([
                StructField("drugcharacterization", StringType()),
                StructField("medicinalproduct", StringType()),
                StructField("drugauthorizationnumb", StringType()),
                StructField("drugindication", StringType()),
                StructField("drugrecurreadministration", StringType()),
                StructField("drugadditional", StringType()),
                StructField("openfda", StructType([
                    StructField("application_number", ArrayType(StringType())),
                    StructField("brand_name", ArrayType(StringType())),
                    StructField("generic_name", ArrayType(StringType())),
                    StructField("manufacturer_name", ArrayType(StringType())),
                    StructField("product_ndc", ArrayType(StringType())),
                    StructField("product_type", ArrayType(StringType())),
                    StructField("route", ArrayType(StringType())),
                    StructField("substance_name", ArrayType(StringType())),
                    StructField("rxcui", ArrayType(StringType())),
                    StructField("spl_id", ArrayType(StringType())),
                    StructField("spl_set_id", ArrayType(StringType())),
                    StructField("package_ndc", ArrayType(StringType())),
                    StructField("nui", ArrayType(StringType())),
                    StructField("pharm_class_moa", ArrayType(StringType())),
                    StructField("pharm_class_cs", ArrayType(StringType())),
                    StructField("pharm_class_epc", ArrayType(StringType())),
                    StructField("unii", ArrayType(StringType()))
                ]))
            ])))
        ]))
    ])))
])

def get_schema():
    return json_schema

