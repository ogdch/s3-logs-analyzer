#coding: utf-8

import os
import sys
import argparse
import re
import operator

parser = argparse.ArgumentParser(description='Extract and sum up the information from S3 log files')
parser.add_argument('--folder', help='The folder to extract from', type=str, required=True)

args = vars(parser.parse_args())


class Parser():

    DATA_FOLDER_PATH = 'data/'

    def _list_files_in_folder(self, folder):
        '''
        Return all the filenames for the log files in the given folder
        '''
        (_, _, filenames) = os.walk(self.DATA_FOLDER_PATH + folder).next()
        return filenames


    def _parse_log_files(self, folder):
        '''
        '''

        # copied from http://blog.kowalczyk.info/article/a1e/Parsing-s3-log-files-in-python.html - START
        s3_line_logpats  = r'(\S+) (\S+) \[(.*?)\] (\S+) (\S+) ' \
                   r'(\S+) (\S+) (\S+) "([^"]+)" ' \
                   r'(\S+) (\S+) (\S+) (\S+) (\S+) (\S+) ' \
                   r'"([^"]+)" "([^"]+)"'

        s3_line_logpat = re.compile(s3_line_logpats)

        (S3_LOG_BUCKET_OWNER, S3_LOG_BUCKET, S3_LOG_DATETIME, S3_LOG_IP,
        S3_LOG_REQUESTOR_ID, S3_LOG_REQUEST_ID, S3_LOG_OPERATION, S3_LOG_KEY,
        S3_LOG_HTTP_METHOD_URI_PROTO, S3_LOG_HTTP_STATUS, S3_LOG_S3_ERROR,
        S3_LOG_BYTES_SENT, S3_LOG_OBJECT_SIZE, S3_LOG_TOTAL_TIME,
        S3_LOG_TURN_AROUND_TIME, S3_LOG_REFERER, S3_LOG_USER_AGENT) = range(17)

        s3_names = ("bucket_owner", "bucket", "datetime", "ip", "requestor_id", 
        "request_id", "operation", "key", "http_method_uri_proto", "http_status", 
        "s3_error", "bytes_sent", "object_size", "total_time", "turn_around_time",
        "referer", "user_agent")
        # END

        parsed_data = {}

        files = self._list_files_in_folder(folder)
        for filename in files:
            with open(os.path.join(self.DATA_FOLDER_PATH, folder, filename), 'r') as log_file:
                for log_line in log_file:
                    match = s3_line_logpat.match(log_line)
                    if match is not None:
                        parsed = [match.group(1+n) for n in range(17)]
                        is_get_request = False
                        date = ''
                        for (name, val) in zip(s3_names, parsed):
                            if name == 'operation' and val == 'REST.GET.OBJECT':
                                is_get_request = True
                            if name == 'datetime':
                                date = val[0:11]
                                if not re.search(r"^\d{2}/[A-Za-z]{3}/\d{4}", date):
                                    raise TypeError
                            if name == 'key' and val is not '-' and val[-1:] is not '/' and is_get_request:
                                if val in parsed_data.keys():
                                    if date in parsed_data[val]:
                                        parsed_data[val][date] = parsed_data[val][date] + 1
                                    else:
                                        parsed_data[val][date] = 1
                                else:
                                    parsed_data[val] = {}
                                date = ''
        return parsed_data


    def _write_summary(self, folder, parsed_data):
        '''
        '''

        sorted_by_requests = sorted(parsed_data.iteritems(), key=operator.itemgetter(1), reverse=True)
        with open(os.path.join(self.DATA_FOLDER_PATH, folder + '.csv'), 'w') as summary_file:
            summary_file.write('file,date,downloads\n')
            for line in sorted_by_requests:
                (request, dates_and_downloads) = line
                sorted_dates_and_downloads = sorted(dates_and_downloads.iteritems(), key=operator.itemgetter(1))
                for date, downloads in sorted_dates_and_downloads:
                    summary_file.write("%s,%s,%s\n" % (request, date, downloads))


log_parser = Parser()
pd = log_parser._parse_log_files(args['folder'])
log_parser._write_summary(args['folder'], pd)

print '\n'
print 'Parsing of the folder ' + args['folder'] + ' completed.'
sys.exit()
