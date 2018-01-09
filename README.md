# lilac-discordbot
A discord bot for the dogspotter discord server

---

## Help Documentation

### General Notes

1. Lilac's commands and arguments are **case sensitive!** Please keep this in mind while using the bot.  
2. Lilac's commands **do not support spaces in arguments**. If you require the argument to have a space (e.g "Foo Bar"), please substitute spaces for underscores and use the `-u` modifier at the end of the command. (See: [Command Modifiers](https://github.com/Alpha-Hedge/lilac-discordbot#command-modifiers))

### Syntax

`+` = Command prefix

`::` = Required argument

`<>` = Optional argument

Example: `&&score_add :user: :amount: <modifier>`

---

### Command Modifiers

Current available modifiers:  
`-u`

+ Takes all string arguments and replaces underscores with spaces.  

+ Example:  
  + `+scoreAdd null_user 5`
  + Adds 5 points to the score of “null_user”.
  + `+scoreAdd null_user 5 -u`  
  + Adds 5 points to the score of “null user”. 

---

### Commands

---

### Score Interaction

**(Only users with the “scorekeeper” role can use the commands below.)**

`+scoreAdd :user: :amount: <modifier>`  
Adds `:amount:` to score of `:user:`.  
Valid modifiers:  
`-u`

`+scoreAdd :user: :amount: <modifier>`  
Removes `:amount:` from the score of `:user:`.  
Valid modifiers:  
`-u`

`+scoreGet :user: <modifier>`  
-OR-  
`+scoreGet --all`  
Returns the score of `:user:`.  
The second option (`--all`) displays all scores.  
Valid modifiers:  
`-u`  


---

### Userbase

`+registerUser :user: <modifier>`  
Adds `:user:` into the userbase.  
Valid modifiers:  
`-u`

`+aliasAdd :user: :alias: <modifier>`
Assigns `:alias:` to `:user:`, allowing `:user:` to be referred by `:alias:` in other commands.  
Example:

+ `+scoreGet foobar`
+ This results in the user not being found. However...
+ `+aliasAdd foobar barfoo`
+ `+scoreGet foobar`
+ This will obtain the score of `foobar`, since It knows that `barfoo` is just referring to `foobar`.

`+aliasRemove :alias:`  
Removes `:alias:` from the user it was assigned to.

---

### Miscellaneous Functions

### Math

`+math.FtoP :fraction:` - **F**raction **to** **P**ercentage  
Converts :fraction: to a percentage (fraction format: x/y; e.g 1/2)

`+math.FtoD :decimal:` - **F**raction **to** **D**ecimal
Converts :fraction: to a decimal (float) number (fraction format: x/y; e.g 1/2)