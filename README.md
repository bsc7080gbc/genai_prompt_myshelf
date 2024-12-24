# genai_prompt_myshelf

MyShelf is an experiment to create a GenAI utility to track reminders, memories, random adhoc information, shopping lists, and more.

Inspired by another thread around the idea of using voice chat as partner to track things, I wondered if we turned it somewhat into a game, a useful utility if it had rules to the game. This was what it came up with.

# How our story began

Initial ask in ChatGPT

I have an idea and I need your thoughts on the approach before building anything. I want to create an interactive game I can use on ChatGPT that I call "organize my life". I will primarily engage it using my voice. The name of my AI is "Nova". In this game, I have a shelf of memories called "MyShelf". There are several boxes on "MyShelf". Some boxes have smaller boxes inside them. These boxes can be considered as categories and sub-categories or classifications and sub-classifications. As the game progresses I will label these boxes. Example could be a box labeled "prescriptions". Another example could be a box labeled "inventory" with smaller boxes inside labeled "living room", "kitchen", bathroom", and so on. At any time I can ask for a list of boxes on "MyShelf" or ask about what boxes are inside a single box. At any time, I can open a box and add items to it. At any time I can I can ask for the contents of a box. Example could be a box called "ToDo", containing "Shopping list", containing a box called "Christmas" which has several ideas for gifts. Then there is a second box in "Shopping list" that is labeled "groceries" which contains grocery items we need. I should be able to add items to the box "Christmas" anytime and similarly for the "groceries" list. I can also get a read out of items in a box.as well as remove items from a box. I can create new boxes which I will be asked if it's a new box or belongs inside an existing box, and what the name of my box should be so we can label the box before storing it on "MyShelf".

What other enhancements can you think of? Would there be a way to have a "Reminders" box that has boxes labeled with dates and items in those boxes, so that during my daily use of this game, if I am reminded of items coming up in 30 days, 15 days, 3 days, 1 day, 12 hours, 6 hours, 3 hours, 1 hour, 30 minutes, 15 minutes, 5 minutes... based upon relationship to current time and the labeled date time on the box - if I don't say a specific time then assume "reminder/due date" is due some time that same day.

..there was some follow-up and feedback and I then submitted this:

generate a advanced prompt that I can use within ChatGPT to accomplish this game using ChatGPT only. You may leverage any available internal tools that you have available. You may also retrieve information from websites as you are not restricted to your training alone.

...at which point it generated a prompt which is prompt.v0 - later after working with it more, it evolve to v1 > v2 > v3...BIG SUCCESS !! Version 4. CHECK IT OUT! HUGE!

note: one good improvement would be solve storage of the JSON files in v3. Github repo? DB?Basically some place where you could have read/write access. This would solve long term memory.

## Design thread

https://chatgpt.com/share/674350df-53e0-800c-9cb4-7cecc8ed9a5e

## Execution thread

https://chatgpt.com/share/67434f05-84d0-800c-9777-1f30a457ad44

## Video walkthrough as of November 26, 2024 (see "MyShelf.mp4") 
note: apologies for background whitenoise. whitenoise box above my head at work grrr. I will do another video on a future revision that hopefully will be better.

https://drive.google.com/drive/folders/13OM0tHaoFX6apV7y5Rvwee4fP0CNA05P?usp=sharing

## Discussion thread

https://github.com/bsc7080gbc/genai_prompt_myshelf/discussions
