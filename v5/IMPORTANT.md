## DISCOVERIES

Just using this to jot things down that I have discovered along the way

- JSON formatting.. use 4 spaces, not 2 spaces. Apparently the Base64 encoded/decoding that happens during upload/download - handles small files just fine with 2 spaces which is a valid spacing on JSON. However when the file gets larger, the parsing becomes more strict and thus errors start happening during decoding with 2 spaces. If you set to 4 space, this works better because of how Base64 encoding/decoding works as it chunks things into 4's.

- UTF-8, GitHub doesn't like special characters - what happens is it ends up looking like gibberish and while understood by your AI Assistant doesn't make sense to you and I. I have updated the core.json to hopefully remediate this issue by forcing UTF-8 for all things except binaries like images and pdfs. I also created a workflow and python script that should detect non-UTF8 items being uploaded - and while it does work, it isn't failing when that shows up in a text file or markdown file. I will need to continue working on debugging that. I will leave it disabled for now under v5. Fix it later. It was intended as my back up plan should something sneak through the core.json rules. Let's hope that the core.json rules reign surpreme and I don't need it.
