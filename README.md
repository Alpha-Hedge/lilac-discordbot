# lilac-discordbot
A discord bot for the dogspotter discord server

---

## Help Documentation

### Syntax

`&&` = Command prefix

`::` = Required argument

`<>` = Optional argument

Example: `&&score_add :user: :amount: <modifier>`

---

### Command Modifiers

Current available modifiers:  
`-u`

+ Takes all string arguments and replaces underscores with spaces.  

+ Example:  
  + `&&score_add null_user 5`
  + Adds 5 points to the score of “null_user”.
  + `&&score_add null_user 5 -u`  
  + Adds 5 points to the score of “null user”. 

---

### Commands

---

### Score Interaction

**(Only users with the “scorekeeper” role can use the commands below.)**

`&&score_add :user: :amount: <modifier>`  
Adds `:amount:` to score of `:user:`.  
Valid modifiers:  
`-u`

`&&score_del :user: :amount: <modifier>`  
Removes `:amount:` from the score of `:user:`.  
Valid modifiers:  
`-u`

`&&score_get :user: <modifier>`  
-OR-  
`&&score_get --all`  
Returns the score of `:user:`.  
The second option (`--all`) displays all scores.  
Valid modifiers:  
`-u`  


---

### Userbase

`&&user_register :user: <modifier>`  
Adds `:user:` into the userbase.  
Valid modifiers:  
`-u`

`&&alias_add :user: :alias: <modifier>`
Assigns `:alias:` to `:user:`, allowing `:user:` to be referred by `:alias:` in other commands.  
Example:

+ `&&score_get barfoo`
+ This results in the user not being found. However...
+ `&&alias_add barfoo foobar`
+ `&&score_get barfoo`
+ This will obtain the score of `foobar`, since It knows that `barfoo` is just referring to `foobar`.

`&&alias_remove :alias:`  
Removes `:alias:` from the user it was assigned to.
