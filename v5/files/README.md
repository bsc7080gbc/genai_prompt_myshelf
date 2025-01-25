# MyShelf

All of these files go into the root of your MyShelf. 

DON'T FORGET THESE THINGS:

* Update your core.json and change the {owner} to your github owner profile or org
* Set your MyShelf repo environment variables
  - CLEANUP_PERIOD and set to 10 (set this to longer if you want to keep backups of your data.json longer - personally I like 10 days)
  - DRYRUN and set to false (set to true for DRYRUNs)
  - KEYWORD_ATTEMPT_THRESHOLD and set to 10 (this is a good numbe to stay with)
  - KEYWORD_GOAL and set to 10 (initially you might adjust this higher to collect more keywords, but 10 is a good fit)
  - THEME_MINI_GRAPH_WEIGHT_THRESHOLD and set to 0.00  (adjust anywhere between 0.00 and 1.00, but I would start with 0.00 initially for a while)
* You also need to create your repo secret called MYSHELF and place the generated access token from your GitHub App or the Personal Access Token if you chose that route