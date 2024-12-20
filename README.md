You can change number of elements to be processed by changing number 'n' in
    processor = FileProcessor(n=165, s3_handler=s3_handler,
                              db_handler=db_handler,
                              metadata_extractor=metadata_extractor)


Inside .env file put Aws credentials.
Run **docker-compose up**
