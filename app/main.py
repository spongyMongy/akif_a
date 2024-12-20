import os

from S3_handler import S3Handler
from DatabaseHandler import DatabaseHandler
from MatadataExtractor import MetadataExtractor
from FileProcessor import FileProcessor

if __name__ == "__main__":
    s3_handler = S3Handler(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        bucket="s3-nord-challenge-data"
    )

    db_handler = DatabaseHandler(
        host="db",
        port=5432,
        user="postgres",
        password="example",
        database="filedb"
    )

    metadata_extractor = MetadataExtractor()

    processor = FileProcessor(n=165, s3_handler=s3_handler,
                              db_handler=db_handler,
                              metadata_extractor=metadata_extractor)
    processor.process_files()
