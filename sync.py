#coding: utf-8

import os
import sys
import argparse

from boto.s3.connection import S3Connection
from boto.s3.key import Key

parser = argparse.ArgumentParser(description='Sync the S3 log files to the local file system')
parser.add_argument('--key', help='Your S3 Access Key', type=str, required=True)
parser.add_argument('--secret', help='Your S3 Access Secret', type=str, required=True)
parser.add_argument('--bucket', help='Your S3 Bucket', type=str, required=True)
parser.add_argument('--folder', help='Your folder within your S3 Bucket (optional)', type=str)

args = vars(parser.parse_args())


class SyncS3():

    AWS_ACCESS_KEY = args['key']
    AWS_SECRET_KEY = args['secret']
    BUCKET_NAME = args['bucket']
    DATA_FOLDER_PATH = 'data/'

    def _get_s3_bucket(self):
        '''
        Create an S3 connection to the department bucket
        '''
        conn = S3Connection(self.AWS_ACCESS_KEY, self.AWS_SECRET_KEY)
        bucket = conn.get_bucket(self.BUCKET_NAME)
        return bucket

    def _sync_log_files(self, prefix=None):
        '''
        Download all log files which aren't on the disk already
        '''

        # Make sure the download folder exists
        if not os.path.exists(os.path.join(self.DATA_FOLDER_PATH, prefix)):
            os.mkdir(os.path.join(self.DATA_FOLDER_PATH, prefix))

        for key in self._get_s3_bucket().list(prefix=prefix):
            key_str = str(key.key)

            # check if file exists locally otherwise download
            if not os.path.exists(os.path.join(self.DATA_FOLDER_PATH, key_str)):
                key.get_contents_to_filename(os.path.join(self.DATA_FOLDER_PATH, key_str))
                print key_str

syncer = SyncS3()
syncer._sync_log_files(prefix=args['folder'])

print '\n'
print 'Sync for the bucket ' + args['bucket'] + ' completed.'
sys.exit()