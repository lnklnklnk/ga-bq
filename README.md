# Google Analytics -> BigQuery streaming
Stream raw hit-level Google Analytics data into BigQuery

##Installation

1. Create new project here https://console.developers.google.com/project
1. Create new dataset in Google BigQuery https://bigquery.cloud.google.com
1. Download and install Google App Engine python SDK https://cloud.google.com/appengine/downloads
1. git clone https://github.com/lnklnklnk/ga-bq.git
1. Create new app from source in Google SDK
1. Add app-id in app.yaml
1. Change gifPath in js/gabq.js to [your-project].appspot.com/collect
1. Set app_id, dataset_id, table_id in bqloader.py
1. Deploy application
1. Visit [your-app].appspot.com/tasks/create_bq_table to create BigQuery table
1. Include plugin on your website. Add line:  <code>&lt;script async src="http://[your-app].appspot.com/js/gabq.js"&gt;&lt;/script&gt;</code> after GA code and <code>ga('require', 'gabqplugin');</code> after <code>ga('create',..)</code>
1. Now you raw GA data collects in BigQuery table

Note: Ecomerce data is currently not supported, it will be added soon
