## Influencer Dashboard


### Setting up

```
pip install -r requirements.txt
```

### Updating MongoDB database

Will find new posts for the current influencers in the database.

```
cd scrapers
python update_database.py
```

Alternatively, can set a cronjob to preriodically update the database

Step 1: Insert a new cronjob using crontab (for Unix-based systems)

```
crontab -e
```

Step 2:
```
0 0 * * SUN /path/to/dir/scrape.sh
```
