#! /usr/bin/env python

import sys

import boto
from boto.s3.key import Key

S3_BUCKET="mphackathon"
S3_REGION="us-west-2"
LOCAL_TEMP="/tmp"

def download_s3(region, bucket, key_name, local_dest):
    """ Download S3 file 
    """
    conn = boto.s3.connect_to_region(region_name=region)
    bucket = conn.get_bucket(bucket)

    key = bucket.lookup(key_name)
    key.get_contents_to_filename(local_dest)

if __name__ == "__main__":
    def main():
        key, local_folder = sys.argv[1:3]
        download_s3(region=S3_REGION, bucket=S3_BUCKET, key_name=key, local_dest=local_folder)

    # MAIN program begins here
    main() 
