# Granary Finance - TVL by User

In this repo you will find the code responsible to calculate the remaining GRAIN vests by users.
The main scripts is generating an grain_user_data.csv file.
## Requirements
```
have python3 installed on your machine
```
## How to execute this project?

```
pip install -r requirements.txt
python 3 vest_finder.py
```

Now you can see the grain_user_data.csv file. That's it.

### Additional Files
grain_lge_wallets.csv contains a list of users that participated in any of the GRAIN LGEs and their respective chains.
oath_ftm_lge_buyers.csv contains a list of users that participated in the OATH FTM LGE.
find_oath_ftm_lge_terms.py finds all OATH FTM LGE participant shares.
