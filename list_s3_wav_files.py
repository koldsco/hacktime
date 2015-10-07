#! /usr/bin/env python

import boto
from boto.s3.key import Key

S3_BUCKET="mphackathon"
S3_PREFIX="eddy_assets_16830000-16834999/"
S3_REGION="us-west-2"

def get_all_keys(region, bucket, prefix, extension):
    """ List all files in S3 bucket with specific prefix and extension
    """
    conn = boto.s3.connect_to_region(region_name=region)
    bucket = conn.get_bucket(bucket)

    key_list = bucket.list(prefix=prefix)

    for key in key_list:
        if key.name.endswith(extension):
            yield key.name

if __name__ == "__main__":
    def main():
        relevant_keys = get_all_keys(region=S3_REGION, bucket=S3_BUCKET, prefix=S3_PREFIX, extension='.wav')

        for key in relevant_keys:
            print "http://%s.s3.amazonaws.com/%s" % (S3_BUCKET, key)

    # MAIN program begins here
    main() 
