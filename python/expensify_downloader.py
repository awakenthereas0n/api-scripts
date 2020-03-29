#!/usr/local/bin/python3

# Download reports from Expensify.
# Use the expensify_report_export.py script to generate the spensy_outfile.txt file.

import json, requests, csv, os, urllib

class Expensify(object):
    _url = "https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations"

    def __init__(self, userid, secret):
        # Go to https://www.expensify.com/tools/integrations/ to generate your own userid/secret
        self._userid = userid
        self._secret = secret

    def _import_csv(self):
        with open('spensy_outfile.txt', 'r') as csv_file:
            reader = csv.reader(csv_file)
            row_count = 1
            print(row_count)

            for row in reader:
                for filename in row:
                    spensy._export_report(filename)

    def _export_report(self, filename):
            params = {
                "requestJobDescription": json.dumps({
                    "type":"download",
                    "credentials":{
                        "partnerUserID": self._userid,
                        "partnerUserSecret": self._secret,
                    },
                    "fileName": filename,
                    "fileSystem":"integrationServer"
                    })
                }
        
            response = requests.get(self._url, params = params)
            if response.status_code == 200:
                f = open(filename, "wb")
                f.write(response.content)
                f.close
            else:
                raise RuntimeError("Failed to export file from Expensify, API responded with: %s" % response.content)

if __name__ == "__main__":
    userid = os.environ['userid']
    secret = os.environ['secret']
    spensy = Expensify(userid, secret)
    spensy._import_csv()