# Google Analytics -> BigQuery streaming

Stream raw hit-level Google Analytics data into BigQuery

## Installation

1. Create new project here https://console.developers.google.com/project
1. Create new dataset in Google BigQuery https://bigquery.cloud.google.com
1. Download and install Google App Engine python SDK https://cloud.google.com/appengine/downloads
1. git clone https://github.com/lnklnklnk/ga-bq.git
1. Create new app from source in Google SDK
1. Add app-id in app.yaml
1. Change gifPath in js/gabq.js to ga-tracker-dot-[your-project].appspot.com/collect
1. Set app_id, dataset_id, table_id in bqloader.py
1. Deploy application
1. Visit ga-tracker-dot-[your-project].appspot.com/tasks/create_bq_table to create BigQuery table
1. Include plugin on your website. Add line: `<script async src="http://ga-tracker-dot-[your-project].appspot.com/js/gabq.js"></script>` after GA code and `ga('require', 'gabqplugin');` after `ga('create',..)`
1. Now you raw GA data collects in BigQuery table

Note: Ecomerce data is currently not supported, it will be added soon

## Tuning

In case you have more than 1000 events per minute you may duplicate number of cron workers by copy pasting them in cron.yaml, e.g. something like this:

```
cron:
- description: process queue
  url: /tasks/process_queue
  schedule: every 1 mins

- description: process queue
  url: /tasks/process_queue
  schedule: every 1 mins

- description: process queue
  url: /tasks/process_queue
  schedule: every 1 mins  

- description: process queue
  url: /tasks/process_queue
  schedule: every 1 mins  

- description: process queue
  url: /tasks/process_queue
  schedule: every 1 mins  
```

Take in mind that there is an limit - you can not lease more than 1000 rows from queue at once, so we are scaling this by number of cronjobs, so now each minute we will be able to proccess 5000 events. While playing around we have noticed that there is an limit to number of cronjobs at 60 - so with this in mind, you may grow up to 60 000 per minute.

## Troubleshooting

# Internal Server error (UnknownQueueError) when sending data to /collect

If you don't see your `pull-queue` queue in the Cloud Tasks underneath Pull queues display on the developer console, try deploying the queue config explicitly:

```
gcould app deploy queue.yaml --project [your-project]
```
