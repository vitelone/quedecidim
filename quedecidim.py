#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests, time, re, csv

URL0="https://participaciointerna.diba.cat/processes/la-intradiba/f/223/proposals?component_id=223&participatory_process_slug=la-intradiba&per_page=100"
CSV_FILE="QueDecidim.csv"

data = requests.get(URL0).text
soup = BeautifulSoup(data, features="html.parser")

# open or create CSV to append new results
with open(CSV_FILE, mode='a+') as results_file:
    results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for proposal in soup.find_all("article", {"class": "card card--proposal muted"}):
        # get the fields
        proposal_id = proposal.div.a["href"].split("/")[6]
        proposal_name = repr(proposal.div.a.h5.string)[12:]
        proposal_user = proposal.find("span", {"class": "author__nickname"}).string    
        proposal_votes= proposal.find("span", {"class": "progress__bar__number"}).string
        # print them and appende them to the opened CSV file
        print proposal_id, proposal_votes, proposal_user, proposal_name
        results_writer.writerow([time.strftime('%d/%m/%Y %H:%M:%S'), proposal_id, proposal_votes, proposal_user, proposal_name])

results_file.close()    