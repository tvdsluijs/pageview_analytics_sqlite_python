# Pageview analytics in SQLite

author: Pure Python / Theo van der Sluijs

url: https://www.purepython.org

copyright: CC BY-NC 4.0

creation date: 11-12-2018

This is a script to retrieve the pageviews / unique views from the Google API v4 and put it in SQLite.

## SQLite helper

There is a SQLite helper function to create, destroy and test data.

When you go to your functions folder you can run the sqlite_analytics.py script with helpers.

```python sqlite_analytics.py -dd 1```
will drop the table

```python sqlite_analytics.py -cd 1```
will create the database and table

```python sqlite_analytics.py -dd 1```
Will insert some fake data

```python sqlite_analytics.py -gd 1```
Will get out some fake data
  

## Google Analytics Page Views into SQLite

Grab the analytics page views and unique page views per page and put them in a sqlite dbase.


### Enable the API

To get started using Analytics Reporting API v4, you need to first [use the setup tool](https://console.developers.google.com/start/api?id=analyticsreporting.googleapis.com&credential=client_key), which guides you through creating a project in the Google API Console, enabling the API, and creating credentials.

#### Create credentials

> **Note:** When prompted click  **Furnish a new private key**  and for the  _Key type_  select  **JSON**, and save the generated key as  `client_secrets.json`; you will need next to this script (**in the same folder**)


1.  Open the  [**Service accounts**  page](https://console.developers.google.com/iam-admin/serviceaccounts). If prompted, select a project.
2.  Click  **Create service account**.
3.  In the  **Create service account**  window, type a name for the service account, and select  **Furnish a new private key**. Then click  **Save**.

Your new public/private key pair is generated and downloaded to your machine; it serves as the only copy of this key. You are responsible for storing it securely.

#### Add service account to the Google Analytics account

The newly created service account will have an email address that looks similar to:

`quickstart@PROJECT-ID.iam.gserviceaccount.com  
`

Use this email address to  [add a user](https://support.google.com/analytics/answer/1009702)  to the Google analytics view you want to access via the API. For this tutorial only  [Read & Analyze](https://support.google.com/analytics/answer/2884495)  permissions are needed.
