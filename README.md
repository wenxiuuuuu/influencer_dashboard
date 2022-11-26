## Influencer Dashboard

Influ-Finder is a influencer analytics tool to help small local business owners to explore and compare the profiles of various influencers in Singapore.

CZ4125 Developing Data Products - Capstone Project
Done by: Cammy Mun, Chua Zi Heng, Pooja Srinivas Nag, Tan Wen Xiu
Deployed via Heroku at https://influ-finder.herokuapp.com/

### Setting up

```
pip install -r requirements.txt
```

### Run Dash
```
python app.py
```

### Directory

`assets/`: Images and styles

`data/`: Data in the form of pickle and csv (alternative to MongoDB)

`data_extraction/`: Scraping instagram notebooks (might require login to run)

`machine_learning/`: machine learning model training/inferencing notebooks

`img_cluster/`: Image clustering layout

`models/`: ML pickled models

`update_db/`: Database update scripts







### Database update job

Will find new posts for the current influencers in the database.

```
cd update_db
python update_database.py
```

Alternatively, can set a cronjob to preriodically update the database

Step 1: Insert a new cronjob using crontab (for Unix-based systems)

```
crontab -e
```

Step 2: Indicate frequency of database update

The following cronjob will run at midnight every sunday.
```
0 0 * * SUN /path/to/dir/scrape.sh
```
