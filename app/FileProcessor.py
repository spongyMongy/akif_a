from pyspark.sql import SparkSession


class FileProcessor:
    def __init__(self, n, s3_handler, db_handler, metadata_extractor,
                 input_source="s3", file_list=None):
        self.n = n
        self.s3_handler = s3_handler
        self.db_handler = db_handler
        self.metadata_extractor = metadata_extractor
        self.spark = SparkSession.builder.getOrCreate()
        self.input_source = input_source
        self.file_list = file_list if file_list else []

    def process_files(self):
        files = self._get_files()

        file_paths = [self.s3_handler.download_file(file) for file in files]

        metadata = [self.metadata_extractor.extract(file_path) for file_path in
                    file_paths]

        self.db_handler.insert_metadata(metadata)

        print("Metadata successfully processed and stored.")

    def _get_files(self):
        """
        Retrieves files based on input source (S3 or local file).
        """
        if self.input_source == "s3":
            # List files from S3
            files = self.s3_handler.list_files(["0/", "1/"])[:self.n]
        elif self.input_source == "file" and self.file_list:
            # Read file paths from local file list
            with open(self.file_list, 'r') as f:
                files = f.readlines()
            files = [file.strip() for file in files[:self.n]]
        else:
            raise ValueError("No files provided for processing")
        return files
