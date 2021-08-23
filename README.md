# MPA Bot
Source code of the official Discord-bot of [Music Production Arena](https://musicproductionarena.com/)

## Table of Contents
- [Dependencies](#dependencies)
- Basic YAML Syntax
  - [Introduction](#introduction)
  - [Colour](#colour)
  - [Lists](#lists)
  - [Text](#text)
  - [Multiline Text](#multiline-text)
  - [Variables](#variables)
    - [user](#the-user-variable)
- Configuration File Structure
  - [Paths](#paths)
  - [Server ID](#server-id)
  - [Debug](#debug)
  - [Whitelist](#whitelist)
  - [Channels](#channels)
  - [Date Format](#date-format)
  - [Text Comparison](#text-comparison)
  - [Role System](#role-system)
  - [Verification](#verification)
  - [Embeds](#embeds)
    - [See All](#embed-types)
  - [Messages](#messages)
    - [See All](#message-types)
  - [Questions](#questions)
    - [See All](#question-types)
  - [Commands](#commands)
    - [See All](#command-types)
  - [Errors](#errors)
    - [See All](#error-types)

## Dependencies
Use `pip3 install ` to install the modules.
- regex
- requests
- emoji
- textdistance
- python-dotenv
- ramuel.yaml

## Basic YAML Syntax
### Introduction
You can learn the basics of YAML here:  
[YAML Reference](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)

Please note that some features were removed in YAML 1.2  
*Avoid using:*
- `yes`
- `no`
- `y`
- `n`
- `on`
- `off`

*Instead use:*
- `true`
- `false`

**(Unless specified otherwise)**

---

### Colour
Colour is written as a hex number with the prefix `0x`  
```yaml
Green: 0x00ff00
```


---

### Lists
List items are defined with `-`  

```yaml
Food:
  - Banana
  - Apple
  - Tomato
```

---

### Text
Text can be written with or without quotation marks.  
There are some special characters in YAML, so if the text does not start with a letter or has a colon in it
I recommend adding quotation marks around it.
```yaml
Some text: Hello World!
More text: "{ <-- that is not a letter"
Even more text: "This text has a colon : in it"
```

---

### Multiline Text
Start with `|-` then write your text on the next line.  
Indentation will be ignored, but the new lines will be added.  
You can use `>-` instead of `|-` if you want the new lines to be replaced with spaces.
```yaml
Some multiline text: |-
  Hello There
  This text has
  multiple lines
```

---

### Variables
You can add variables to text with `{var_name}`
```yaml
"Some text with a {variable}"
```

#### The `user` Variable
`user` is usually the user that triggers the command, but there are some exceptions.  
If `user` is listed as an available variable then you can use these:
| Variable | Description |
| -------- | ----------- |
| `user.name` | *The name of the user* |
| `user.display_name` | *The users nickname.</br>If the user does not have a nickname the username will automatically be used instead* |
| `user.id` | *The ID of the user* |
| `user.mention` | *Pings the user* |

---

## Configuration File Structure

### Paths
The file path to each of the required files.

---

### Server ID
ID of the discord server.

---

### Debug
`status` can either be `on` or `off`, and only those two, do **not** use `true` and `false`.  
This tells the bot if it should run in debug mode.  
When in debug mode the bot will send all debug messages to the specified `user`  
and channel specific functions will be available for testing in the PM channel with said user.  
`user` is the ID of the debug user.  
`update time` is the time it takes for the bot to update the status embeds.

---

### Whitelist
A list with IDs of everyone who has access to the bot moderation commands.

---

### Channels
IDs of specific server channels.

---

### Date Format
How date and time is formatted in text.  
[Format Codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)

---

### Text Comparison
`threshold` tells the minimum % amount (as a float from 0 to 1) the role has to match the input text
for the role to be added to the user.  
So if the `treshold` is `0.8` and the role matches the input text by `81%`, the role will be added to the user.  
If no role matches the text with a % above the treshold the bot will send the [role question embed](#role-question-embed).

`algorithm` is a string with text comparison algorithms separated by ` > `.
```yaml
algorithm: damerau_levenshtein > mra > editex > jaccard > entropy_ncd
```
The bot will use the first algorithm first, and if the values are identical it will use the next algorithm, etc.
The first algorithm will be used alone for everything that does not require a percise comparison.

*Available algorithms:*
- hamming
- mlipns
- levenshtein
- damerau_levenshtein
- jaro
- strcmp95
- needleman_wunsch
- gotoh
- smith_waterman
- jaccard
- sorensen
- tversky
- overlap
- tanimoto
- cosine
- monge_elkan
- bag
- lcsseq
- lcsstr
- ratcliff_obershelp
- arith_ncd
- rle_ncd
- bwtrle_ncd
- sqrt_ncd
- entropy_ncd
- bz2_ncd
- lzma_ncd
- zlib_ncd
- mra
- editex
- prefix
- postfix
- length
- identity
- matrix

[Read more](https://www.kdnuggets.com/2019/01/comparison-text-distance-metrics.html) about the different types of algorithms.  
Click the algorithms on [this page](https://pypi.org/project/textdistance/) to read about the specific algorithms

---

### Role System
`separators` is a list with separators used to separate roles and role types.  
`role types` is a list with role types.
- `name` is the name of the role type. A role type can for example be `DAW`, `Occupation`, etc.
- `colour` is the colour for the roles of the specified type. All roles under a specific type will automatically be applied this colour. 

---

### Verification
`channel id` is the ID of the channel with the verification button.  
`message id` is the ID of the message that has the verification button.  
`emoji id` is the ID of the emoji used for the verification button.

---

### Embeds
Customise all the embeds that the bot can send.  
*Each embed can contain:*
- `title`
- `colour`  
  The colour of the line on the left side of the embed.  
  Pure white does not work, use "0xfefefe" instead.
- `timeout`  
  Seconds until the embed automatically gets deleted.  
  Leave as 0 if you dont want it to be deleted automatically.
- `description`
- `fields`  
  List with fields in the embed.  
  A field must contain all of the things below, leaving one of these empty will throw an error.
  - `name`  
    The big text.  
    Does not support mentions.
  - `value`  
    The small text.
  - `inline`  
    True or false.  
    If inline is set to false the field will be on a new line.  
    Even if inline is true discord will still wrap the fields.  
    So if the text is too long it will be on a new line.
- `footer`  
  The small text at the bottom.  
  You have to put `text` on a new line with the text that should be in the footer.  
  See example below.
- `buttons`  
  A list of buttons.  
  This adds reactions to the embed that the user can use as buttons.  
  Each button needs:
  - `emoji`  
    The reaction it will add
  - `function`  
    A function.  
    Each embed type will have its own set of functions.
  - `delete`  
    If true the embed will be deleted when the button is pressed.  
    Delete will automatically be set to true if not specified.

```yaml
embed:
  title: This is an embed
  colour: 0x00abf4
  timeout: 10
  description: |
    This description
    has multiple lines
  fields:
    - name: Banana
      value: Do you like banana?
      inline: false
    - name: Apple
      value: No I like apple
      inline: false
    - name: Tomato
      value: Well at least we both hate tomato
      inline: false
  footer:
    text: ❌ <- close this embed
  buttons:
    - emoji: 1️⃣
      function: eat apple
      delete: false
    - emoji: ❌
      delete: true
```
[Read more](https://discord.com/developers/docs/resources/channel#embed-object) about the embed object.

---

### Embed Types
- Role
  - [Question](#role-question-embed)
  - [Suggestion](#role-suggestion-embed)
  - [Create](#role-create-embed)
  - [Created](#role-created-embed)
- Status
  - [Server](#status-server-embed)
  - [Bot](#status-bot-embed)
- Help
  - [Role](#help-role-embed)
  - [Whitelist](#help-whitelist-embed)
- [Whitelist](#whitelist-embed)
- Bot
  - [Shutdown](#shutdown-embed)
- [Error](#error-embed)

---

### Role Question Embed
Gets sent when a role request does not match with any existing roles.

Each `role` variable can have a number inside square brackets `[]` as a suffix. Like for example `{role[3]}`.  
The number indicates how close the role is to the requested role.  
Negative numbers will take the roles that matched the least.  
`-1` is the role with least simliarities with the requested role.  
`role[0]` is what the user requested.  
Typing just `role` without any number will not work in this embed.

Replace `n` with the index of the role. Can be any integer except for `0`.  
| Variable | Description |
| -------- | ----------- |
| `role[0].name` | What the user wrote. |
| `role[0].type` | The role type. For example `DAW`, `Genres`, etc. |
| `role[n].name` | The name of the role. |
| `role[n].id` | The ID of the role. |
| `role[n].colour` | The colour of the role. |
| `role[n].match` | How close the role is to the requested role in %. |
| `role[n].type` | The role type. For example `DAW`, `Genres`, etc. |
| `user` | [Reference](#the-user-variable) |


| Function | Description |
| -------- | ----------- |
| `add role n` | Adds the specified role to the user.</br>Replace `n` with the index of the role.</br>Can be any integer except for `0`. |
| `suggest role` | Suggests the requested role to the staff. |
| `change name` | Rewrite the role name. |
| `change type` | Change the role type. |
