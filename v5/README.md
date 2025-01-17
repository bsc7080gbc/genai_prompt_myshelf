v5 brings several changes to MyShelf

* Introduction of using the raw files from GitHub when peforming the GET operations, e.g. retrieving the data.json file as opposed to using the normal APIs. This increased stability and accuracy of the file retrieval from the GitHub repository.
* Ability to save enriched context session files to your private github repository, e.g. save enriched context. These are timestamped.
* Ability to retrieve enriched context session files for a particular date, series of dates, or date range. Unify them into a single enriched narrative this is enough to carry on the conversation you were having several ago or a month ago.
* Single workflow called 'data workflow' than handles all the processing operations and cleanups.
* Adjust environment variable for the auto-purging of the archive to keep it clean. Note we do not auto-purge the context session files because we recognize you may wish to refer back to them later. Use your judgement on how far back you wish to go.
* Introduction of yaml validator workflows which are useful during your customizations of the yaml workflows if choose to do so
* Introduction of json schema validations and template validations for the data.json. These are intended to prevent bad changes of flowing into the root path data.json file resulting in temporary loss of information. We say temporary because we do archive all new inbound data.json files uploaded to the updates path - the copies go to an archive path.
* Several python scripts have been added to the root path whic hsupport the schema and template adherance.
* Personas ** no longer need to be attached to the custom GPT with exception of the defaultmode and personamodetemplate. Instead we have created a personas path in our private github repository and placed all personas in there. MyShelf now has two commands: `switchmode {mode}`
* Recipes ** folder has been added to the GitHub repo as well. Under that we have indexes for breakfast, lunch, dinner, etc. even a cocktails folder which works in concert with the "MyBar" in the data.json

* And I think an actual cognitive graph map of the filesystem in your private github repo.


** IMPORTANT **

The folders: 'persona' and 'recipies' are important additions  and evolutions of the MyShelf. Previously we would store these items in the data.json and watch it expand. This would evetually cause our data.json file to become too large and performance would be impacted among other things. Now for data needs changes, but not very often, we can ceate a folder on our private repository. that repository would contain a README, possibly an index.json file showing what is the structure of the folder. This approach allows for a wealth of opportunties.
