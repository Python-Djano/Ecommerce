from storages.backends.s3boto3 import S3Boto3Storage



class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'media'
    
    


# class StaticRootS3Boto3Storage(S3Boto3Storage):
#     location = 'static'    