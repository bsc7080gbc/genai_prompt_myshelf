# NEWS

* I have successfully implemented this v3 solution into a custom GPT. The core.json file is attached to the custom GPT and remains immutable. If it needs updating, you would need to do so externally and then uploaded to replace the previously attached core.json. The data.json is stored in a private git repository which I have an action that allows me to pull from the repo and into the custom GPT session. The update of the data.json within the private git repository works when in test mode (setting up the custom GPT) but in normal mode it does not - keeps barking about a disabled jit plugin ???
* I added a SHA entry under the Metadata Tracking with some automation to populate that value automatically as it is needed when pushing changes back.
* Due to the issues, currently any changes apply in my session only impact the current session. I would need to apply those changes manually to the git repo. The upside is that I can successfully retrieve my stored data.json file from the git repo. It's a start. 

# INSTRUCTIONS

* Copy the prompt markdown content and add as the prompt. Send it but don't do anything else.
* Download the core.json and attach as a file
* Download the data.json and attach as a file
* Type ```initialize``` and send it.
* It should load up the core.json and the data.json files both.
* Next type ```/verify --full``` and send it
* If you run into issues you can obtain feedback to correct the issue.You can also use ```/verify --fix``` which can some fix the issue(s).

Things you can ask:

* Ask about ```what is your name```
* Ask about ```commands``` to see some key system options.
* Ask about ```how do I add reminders```.
* Ask about ```how do I add new boxes```.
* Ask about ```what options can I change about your Persona```
* Ask about ```what configuration options are available for how you talk to me```
* Ask about ```can I set my name```
^ Ask for help on a command by appending ```--help``` to the command like ```/save --help```

and a lot more.

You can even discuss how to expand abiltities

```if I have ideas on new rules or automations, can you help me discuss, identify risks, and even implement them```

Ask about logs

```do you keep an activity log```

Most important part - periodic saving of your data.json - this is your user data.

```how do I save my current data.json```

Keep your saved copy up to date with periodic saves. In the event you run into a scenario where it seems "MyShelf" has fallen off the rails, you can simply start a new session, reapply the prompt and attach core and data - it will load the core.json and data.json again and you are back up and running where you left off. Since we have split the core and data, the data.json is able to change as needed and we do not risk corrupting the core functionality.

Experiment with snapshots as well ```tell me about myshelf snapshots ```

Hope you find it interesting.

