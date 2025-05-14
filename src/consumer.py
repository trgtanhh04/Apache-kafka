from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import from_json, col
import logging
import psycopg2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CONFIG = {
    'KAFKA_TOPIC': 'users_created',
    'KAFKA_BOOTSTRAP_SERVERS': 'localhost:29092',
    'USER_DB': 'postgres',
    'PASSWORD_DB': 'postgres',
    'NAME_DB': 'userdb'
}


def init_spark_session():
    spark = SparkSession.builder \
        .appName("Pipeline Kafka") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,org.postgresql:postgresql:42.2.23") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    logger.info("Spark session created successfully!")
    return spark

def connect_to_kafka(spark):
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", CONFIG["KAFKA_BOOTSTRAP_SERVERS"]) \
        .option("subscribe", CONFIG["KAFKA_TOPIC"]) \
        .option("startingOffsets", "earliest") \
        .load()

    
    logger.info("Connected to Kafka topic: %s", CONFIG["KAFKA_TOPIC"])
    return df

def parse_kafka_data(df):
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("first_name", StringType(), True),
        StructField("last_name", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("address", StringType(), True),
        StructField("post_code", StringType(), True),
        StructField("email", StringType(), True),
        StructField("username", StringType(), True),
        StructField("dob", StringType(), True),
        StructField("registered_date", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("picture", StringType(), True)
    ])
    df_parsed = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")
    df_parsed = df_parsed.filter(df_parsed.id.isNotNull())
    logger.info("Kafka data parsed successfully!")
    return df_parsed



def create_db_and_table():
    try:
        # Step 1: Connect to the default 'postgres' database to create a new database
        conn = psycopg2.connect(
            dbname="postgres",
            user=CONFIG['USER_DB'],
            password=CONFIG['PASSWORD_DB'],
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {CONFIG['NAME_DB']}")
        logger.info("Database created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        logger.info("Database already exists.")
    except Exception as e:
        logger.error("Error creating database: %s", str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()

    try:
        # Step 2: Connect to the new/existing database to create the 'users' table
        conn = psycopg2.connect(
            dbname=CONFIG['NAME_DB'],
            user=CONFIG['USER_DB'],
            password=CONFIG['PASSWORD_DB'],
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR PRIMARY KEY,
                first_name VARCHAR,
                last_name VARCHAR,
                gender VARCHAR,
                address VARCHAR,
                post_code VARCHAR,
                email VARCHAR,
                username VARCHAR,
                dob VARCHAR,
                registered_date VARCHAR,
                phone VARCHAR,
                picture VARCHAR
            )
        """)
        conn.commit()
        logger.info("Table created successfully.")

        cursor.execute("TRUNCATE TABLE users")
        conn.commit()
        logger.info("All data in 'users' table has been cleared.")

    except Exception as e:
        logger.error("Error creating table or clearing data: %s", str(e))
    finally:
        if conn:
            cursor.close()
            conn.close() 

def upload_to_postgres(df, epoch_id):
    try:
        logger.info("Starting batch upload...")
        df.show() 
        deduplicated_df = df.dropDuplicates(["id"])

        # Write to CSV
        deduplicated_df.coalesce(1).write \
            .mode("overwrite") \
            .option("header", "true") \
            .csv("data")
        
        # Write to PostgreSQL
        deduplicated_df.write \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://localhost:5432/{CONFIG['NAME_DB']}") \
            .option("dbtable", "users") \
            .option("user", CONFIG['USER_DB']) \
            .option("password", CONFIG['PASSWORD_DB']) \
            .option("driver", "org.postgresql.Driver") \
            .option("stringtype", "unspecified") \
            .mode("append") \
            .save()
        logger.info("Batch upload completed successfully.")
    except Exception as e:
        logger.error("Error during batch upload: %s", str(e))

if __name__ == "__main__":
    try:
        create_db_and_table()
        spark = init_spark_session()
        kafka_df = connect_to_kafka(spark)
        parsed_df = parse_kafka_data(kafka_df)

        # Ghi trực tiếp vào PostgreSQL
        parsed_df.writeStream \
            .foreachBatch(upload_to_postgres) \
            .outputMode("append") \
            .start() \
            .awaitTermination()

    except Exception as e:
        logger.error("Error occurred: %s", str(e))
        
# python3 src/consumer.py