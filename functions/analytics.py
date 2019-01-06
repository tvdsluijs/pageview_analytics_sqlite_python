"""
author: Pure Python
url: https://www.purepython.org
copyright: CC BY-NC 4.0
creation date: 11-12-2018

please put your client_screts.json in the same folder as this file.

You need the oauth2client and google-api-python-client for this to work.
Please install by :
pip install oauth2client
pip install google-api-python-client
"""
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class PageViews:

    def __init__(self, viewid=0, pagepath="None", startdate="1975-05-14", enddate="today"):
        """Initializes an Analytics Reporting API V4 service object.

          Creates self.analytics:
            An authorized Analytics Reporting API V4 service object.
          """

        API_URL = ['https://www.googleapis.com/auth/analytics.readonly']
        KEY_FILE_LOCATION = 'client_secrets.json'

        self.view_id = viewid
        self.pagePath = pagepath
        self.startdate = startdate
        self.enddata = enddate

        self.response = ""

        credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, API_URL)

        # Build the service object.
        self.analytics = build('analyticsreporting', 'v4', credentials=credentials)

        self.get_report()

    def get_report(self):
        """
        Queries the Analytics Reporting API V4.

        Usages of:
        self.analytics: An authorized Analytics Reporting API V4 service object.

        creates self.response:
        The Analytics Reporting API V4 response
        """
        pagePath = 'ga:pagePath=={}'.format(self.pagePath)
        body = {
            'reportRequests': [
                {
                    'viewId': self.view_id,
                    'dateRanges': [{'startDate': self.startdate, 'endDate': self.enddata}],
                    'metrics': [{'expression': 'ga:uniquePageviews'},
                                {'expression': 'ga:pageviews'}],
                    'filtersExpression': pagePath
                }]
        }

        self.response = self.analytics.reports().batchGet(body=body).execute()

    def parse_response(self):
        """
        Parse the data to something readable and return it.
        :return: dictionary with data
        """
        report = self.response['reports']
        metricHeaderEntries = report[0]['columnHeader']['metricHeader']['metricHeaderEntries']
        totals = report[0]['data']['totals']
        unique = totals[0]['values'][0]
        pageviews = totals[0]['values'][1]

        data = {}
        data[metricHeaderEntries[0]['name']] = unique
        data[metricHeaderEntries[1]['name']] = pageviews
        return data


if __name__ == '__main__':
    view_id = 'XXXXXXXXXXXXX'  # your analytics view ID
    startdate = "2010-01-01"  # a date like Y-M-D
    enddate = "today"
    page_path = "/Page/this_is_your_page_path.html"  # eg : /zwemmen-met-de-polar-m400/
    p = PageViews(view_id, page_path, startdate, enddate)
    p.get_report()
    data = p.parse_response()
    print(data)
