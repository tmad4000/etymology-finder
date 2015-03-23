To run locally:
cd ./online
python main.py

To run scraper (saves to items.json):
cd ./tutorial
scrapy crawl wordinfo -o items.json



(outdated?)
to deploy on google app engine,
appcfg.py update .

to test locally,
dev_appserver.py .

and go to: http://localhost:8080/
