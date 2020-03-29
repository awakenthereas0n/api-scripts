#!/usr/local/bin/python3

# Use this script to generate Expensify reports via their API.
# This script outputs a file called spensy_outfile.txt which is used with the expensify_downloader.py script to download the reports.

import json, requests, os, urllib

class Expensify(object):
    _url = "https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations"

    _template = """
<#if addHeader == true>
    Merchant,Original Amount,Category,Report number,Expense number<#lt>
</#if>
<#assign reportNumber = 1>
<#assign expenseNumber = 1>
<#list reports as report>
    <#list report.transactionList as expense>
        ${expense.merchant},<#t>
        <#-- note: expense.amount prints the original amount only -->
        ${expense.amount},<#t>
        ${expense.category},<#t>
        ${reportNumber},<#t>
        ${expenseNumber}<#lt>
        <#assign expenseNumber = expenseNumber + 1>
    </#list>
    <#assign reportNumber = reportNumber + 1>
</#list>"""

    def __init__(self, userid, secret, startDate, endDate, month_year):
        # Go to https://www.expensify.com/tools/integrations/ to generate your own userid/secret
        self._userid = userid
        self._secret = secret
        self._startDate = startDate
        self._endDate = endDate
        self._month_year = month_year
    
    def _generate_csv(self):
        params = {
            "requestJobDescription": json.dumps({
                "type": "file",
                "credentials": {
                    "partnerUserID": self._userid,
                    "partnerUserSecret": self._secret
                    },
                    "onReceive":{
                        "immediateResponse":["returnRandomFileName"]
                    },
                    "inputSettings":{
                        "type":"combinedReportData",
                        "filters":{
                            "startDate":self._startDate,
                            "endDate":self._endDate,
                            "markedAsExported":"Expensify Export"
                        }
                    },
                    "outputSettings":{
                        "fileExtension":"pdf",
                        "fileBasename": self._month_year,
                        "fileSystem":"integrationServer"
                    }
                }),
            "template": urllib.quote_plus(self._template)
        }

        thisresponse = requests.post(self._url, data=params)
        if thisresponse.status_code == 200:
            f = open('spensy_outfile.txt', 'w')
            f.write(thisresponse.text)
            f.close
        else:
            raise RuntimeError("Failed to fetch a file from Expensify, their API responded with: %s" % thisresponse.content)

if __name__ == "__main__":
    userid = os.environ['userid']
    secret = os.environ['secret']
    startDate = os.environ['startDate']
    endDate = os.environ['endDate']
    month_year = os.environ['month_year']
    spensy = Expensify(userid, secret, startDate, endDate, month_year)
    spensy._generate_csv()