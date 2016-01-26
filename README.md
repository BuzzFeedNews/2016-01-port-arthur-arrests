# Analysis of Jefferson County (TX) Jail Data

This repository contains data, methodologies, and analysis associated with the BuzzFeed News article, "[The Ticket Machine](http://www.buzzfeed.com/alexcampbell/the-ticket-machine)", published January 26, 2016.


## Data 

The analyses in this repository depend on data provided by Jefferson County, Texas, which runs the jail where Port Arthur police officers bring arrestees. The data includes arrests made by the Port Arthur Police Department (PAPD) for people charged with low-level offenses ("Class C misdemeanors") such as speeding and public intoxication, from January 2005 through November 2015.

The [raw datafile](data/PAPD Only Class C Only.xlsx.zip) was provided by Jefferson County in response to a Public Information Act request. The [`jail_data_cleanup.py` script](scripts/jail_data_cleanup.py) reformats the data and creates two clean data files for
analysis: 1) one with people who were arrested just for traffic offenses; 2) the other with all Class C misdemeanors.

Please note that some arrests in the data may have (a) been entered in error, or (b) later been dismissed. For this reason and because individual names were not essential to the analysis, BuzzFeed News has removed the columns containing defendants' names and addresses from the data published here.


## Analyses

The following three passages are supported by [BuzzFeed News' data analysis](notebooks/port_arthur_analysis.ipynb):

- "From 2009 to 2011, the height of the city’s traffic enforcement spree, about 1,500 people were booked into lockup for unpaid traffic fines."

- "Beyond those numbers lies a racial dimension: The people who Port Arthur police put behind bars for their traffic tickets are disproportionately black. While black people make up only 40% of the overall population — and are ticketed at about that rate — they accounted for about 70% of the arrests for these citations in 2014, according to a BuzzFeed News analysis."

- "Over the past decade, about 1,300 people have spent three days or more in jail for traffic tickets — and about 75% of those people were black."

The Python code that performs these analysis is [available in this Jupyter notebook](notebooks/port_arthur_analysis.ipynb). To re-run it yourself, you'll need to install the libraries listed in [`requirements.txt`](requirements.txt)


## Questions / Feedback?

Email the author at kendall.taggart@buzzfeed.com.
