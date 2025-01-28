This is your main library. In here you will find various libraries related to your AI Assistant. We have started a few out for you on your behalf to give you an idea. To build these out, you may find it easiest to replicate and modify as needed for new areas in your library that you wish to track. Things that you change frequently, like reminders and grocery lists, those are well suited for your data.json while other items, though they may change - they do so far less frequently. These items can go here and can still be accessed by your AI Assistant. The added benefit to this approach, is it keeps your data.json pretty small and efficient and easy to read. You will become quite comfortable working with GitHub if you are new to it. It isn't that bad to be honest. I find myself working between the both of them - AI Assistant and GitHub proper. Just depends upon the activity at play.

Important to notice is that we leverage "indexes"  along with the Dewey Decimal system to help the AI locate items within your library.

Starter areas of your library

* personas
  - contains all the different persona modes you have available to choose from
  ```
  switchmode carlsaganmode
  ```
  
* recipes
  - contains cocktails, breakfast, lunch, dinner, dessert, snack recipies
  ```
  i need recipe for dinner, something with chicken. check MyLibrary recipies
  ```
  
* mybar
  - contains your current stash to support the persona mode 'mixologistmode' as you can tell it to reference your bar to determine what to suggest.
  ```
  switchmode remote mixologistmode
  suggest something interesting using the items i have in MyLibrary mybar
  ```
