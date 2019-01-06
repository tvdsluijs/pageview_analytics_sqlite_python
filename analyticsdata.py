
# 103445821 = 40enfit
# 186740850 = api pure python
# 186615166 = pure python
# 186740850 = itheo
# 2943322 = www.vandersluijs.nl
# 170374547 = vandersluijs.nl
# 170374547 = legendsince1975

from datetime import datetime as dt

from functions.analytics import PageViews
from functions.sqlite_analytics import UrlViews

page_path = "/sollution-connect-problem-polar-m400-v800-en-h7/"
now = int(dt.utcnow().strftime("%s"))
new_time = now+43200        # time in 12 hours

view_id = '123456789'       # your analytics view ID
start_date = "2010-01-01"   # a date like Y-M-D
end_date = "today"

# first get the data from SQLite
u = UrlViews()
row = u.get_views_from_page([page_path, now])

# older than 12 hours or no data? Get data from Google analytics and save it in SQLite
if row is None:
    p = PageViews(view_id, page_path, start_date, end_date)

    data = p.parse_response()

    unique = int(data['ga:uniquePageviews'])
    pageviews = int(data['ga:pageviews'])

    u.replace_row([page_path, view_id, unique, pageviews, new_time])
else:
    unique = row['ga:uniquePageviews']
    pageviews = row['ga:pageviews']

print("Unique : {}".format(unique))
print("Page Views : {}".format(pageviews))
