#coding: utf-8

# parse

import os
import sys
import argparse
import re
import operator


parser = argparse.ArgumentParser(description='Extract and sum up the information from S3 log files')
parser.add_argument('--folder', help='The folder to extract from', type=str, required=True)

args = vars(parser.parse_args())

log_parser = Parser()
pd = log_parser._parse_log_files(args['folder'])
log_parser._write_summary(args['folder'], pd)

print '\n'
print 'Parsing of the folder ' + args['folder'] + ' completed.'
sys.exit()


# sync
import os
import sys
import argparse

from boto.s3 import connect_to_region
from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.key import Key

parser = argparse.ArgumentParser(description='Sync the S3 log files to the local file system')
parser.add_argument('--key', help='Your S3 Access Key', type=str, required=True)
parser.add_argument('--secret', help='Your S3 Access Secret', type=str, required=True)
parser.add_argument('--bucket', help='Your S3 Bucket', type=str, required=True)
parser.add_argument('--region', help='S3 Region of bucket, required to use on python 2.7.9. (optional)', type=str)
parser.add_argument('--folder', help='Your folder within your S3 Bucket (optional)', type=str)
parser.add_argument('--target', help='Your local folder to dump files. Default="data/" (optional)', type=str)


args = vars(parser.parse_args())


syncer = SyncS3()
syncer._sync_log_files(prefix=args['folder'])

print '\n'
print 'Sync for the bucket ' + args['bucket'] + ' completed.'
sys.exit()


def main():
    pass
