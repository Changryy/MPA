VERSION = "3.0.5"
DATA_PATH = "data.yml"


# ---------- MODULES ---------- #
import os
import re
import sys
import requests
import json
import string
import secrets
import asyncio
from emoji import emojize
from datetime import datetime
from copy import deepcopy
from glob import glob
from shutil import copyfile
from filecmp import cmp
from difflib import ndiff
from textdistance import hamming,mlipns,levenshtein,damerau_levenshtein,\
    jaro,strcmp95,needleman_wunsch,gotoh,smith_waterman,jaccard,sorensen,\
    tversky,overlap,tanimoto,cosine,monge_elkan,bag,lcsseq,lcsstr,\
    ratcliff_obershelp,arith_ncd,rle_ncd,bwtrle_ncd,sqrt_ncd,entropy_ncd,\
    bz2_ncd,lzma_ncd,zlib_ncd,mra,editex,prefix,postfix,length,identity,matrix
# ---------- MODULES ---------- #





# ---------- LOAD TOKEN ---------- #
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
# ---------- LOAD TOKEN ---------- #





# ---------- INITIALISE YAML ---------- #
import ruamel
from ruamel.yaml import YAML
yaml = YAML()
yaml.default_flow_style = False
# ---------- INITIALISE YAML ---------- #





# ---------- DISCORD CLIENT ---------- #
import discord
from discord.ext import tasks
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
# ---------- DISCORD CLIENT ---------- #





# ---------- CONSTANTS ---------- #
# data dependencies
DATA_DEPENDENCIES = [
    "paths > data > file",
    "paths > log > file",
    "paths > users > file",
    "paths > roles > file",
    "paths > messages > file",
    "server id",
    "debug > status",
    "debug > user",
    "debug > update time",
    "whitelist",
    "channels > debug",
    "channels > roles",
    "channels > status",
    "date format",
    "text comparison > algorithm",
    "text comparison > threshold",
    "role system > separators",
    "role system > finished emoji",
    "role system > role types",
    "verification > channel id",
    "verification > message id",
    "verification > emoji id",
    "embeds > role > question",
    "embeds > role > suggestion",
    "embeds > role > create",
    "embeds > role > created",
    "embeds > status > server",
    "embeds > status > bot",
    "embeds > help > role",
    "embeds > help > whitelist",
    "embeds > whitelist",
    "embeds > bot > shutdown",
    "embeds > error",
    "messages > verification > start verification",
    "messages > verification > send code",
    "messages > verification > new code",
    "messages > verification > completed",
    "messages > verification > verified user",
    "messages > whitelist > remove",
    "messages > whitelist > remove failed",
    "messages > whitelist > add",
    "messages > whitelist > add failed",
    "messages > updated file",
    "messages > changed nick",
    "messages > bot > update",
    "messages > bot > reboot",
    "messages > bot > shutdown",
    "input messages > role > change name",
    "input messages > role > change type",
    "commands > status > server",
    "commands > status > bot",
    "commands > help > role",
    "commands > help > whitelist",
    "commands > role > create",
    "commands > whitelist > view",
    "commands > whitelist > add",
    "commands > whitelist > remove",
    "commands > file > get",
    "commands > file > replace",
    "commands > bot > update",
    "commands > bot > reboot",
    "commands > bot > shutdown",
    "errors"
]

ERROR_DEPENDENCIES = [100,101,102,103,104,105,200,201,202,203,204,205,206,207,300,301,302]

# text comparison algorithms
ALGORITHMS = {
    "hamming": hamming,
    "mlipns": mlipns,
    "levenshtein": levenshtein,
    "damerau_levenshtein": damerau_levenshtein,
    "jaro": jaro,
    "strcmp95": strcmp95,
    "needleman_wunsch": needleman_wunsch,
    "gotoh": gotoh,
    "smith_waterman": smith_waterman,
    "jaccard": jaccard,
    "sorensen": sorensen,
    "tversky": tversky,
    "overlap": overlap,
    "tanimoto": tanimoto,
    "cosine": cosine,
    "monge_elkan": monge_elkan,
    "bag": bag,
    "lcsseq": lcsseq,
    "lcsstr": lcsstr,
    "ratcliff_obershelp": ratcliff_obershelp,
    "arith_ncd": arith_ncd,
    "rle_ncd": rle_ncd,
    "bwtrle_ncd": bwtrle_ncd,
    "sqrt_ncd": sqrt_ncd,
    "entropy_ncd": entropy_ncd,
    "bz2_ncd": bz2_ncd,
    "lzma_ncd": lzma_ncd,
    "zlib_ncd": zlib_ncd,
    "mra": mra,
    "editex": editex,
    "prefix": prefix,
    "postfix": postfix,
    "length": length,
    "identity": identity,
    "matrix": matrix
}

# Debug mode
DEBUG_MODE = True
DEBUG_USER = 398730959186427916


# Guild ID
GUILD = 621764824417959937

# Channel IDs
CHANNEL = {
    "debug": 621769084152971346,
    "role": 0,
    "status": 0
}

# Paths
PATH = {
    "data": {
        "file": DATA_PATH,
        "backup": "backup/data"
    }
}

# Errors
ERRORS = [ # Built-in File Errors
    {
        "id": 100,
        "title": "Failed To Load Dependencies",
        "description": "Shutting down..."
    },
    {
        "id": 101,
        "title": "File Not Found",
        "description": "Could not find $1."
    },
    {
        "id": 102,
        "title": "Invalid JSON",
        "description": "Invalid JSON in file $1."
    },
    {
        "id": 103,
        "title": "Invalid YAML",
        "description": "Invalid YAML in file $1."
    },
    {
        "id": 104,
        "title": "Missing Properties",
        "description": "Missing properties in file $1.\nFailed to load:\n$2"
    },
    {
        "id": 105,
        "title": "Invalid Key",
        "description": "Invalid key $1 in $2."
    }
]

# Text Comparison
THRESHOLD = 0.0
ALGORITHM_SEQUENCE = "hamming"

# Role System
ROLES = []
ROLE_SYSTEM = {}
roles_updating = False

# Verification System
VERIFICATION = {}

# Text
EMBEDS = {
    "error": { # Built-in error structure to send the built-in errors
        "title": "{self.title}",
        "color": 0xff0000,
        "description": "{self.description}",
        "footer": {"text": "Error {self.id}"}
    }
}
MESSAGES = {}
COMMANDS = {}
INPUTS = {}

# Other
DATE_FORMAT = ""
ONLINE = False
STARTED = False
# ---------- CONSTANTS ---------- #





# ---------- VARIABLES ---------- #
active_codes = {}
users = {}
whitelist = []
start_time = datetime.utcnow()
messages = None
# ---------- VARIABLES ---------- #





# ---------- GLOBAL FUNCTIONS ---------- #
def write_log(text):
    try:
        with open(PATH["log"]["file"], "a", encoding="utf-8") as f:
            f.write(str(datetime.now())+" --> "+text+"\n")
    except: pass

async def error(error_id, *inputs, user=None, send=True):
    err = Error()
    await err.new(error_id, inputs, user, send)
    return err

# returns the debug channel
async def get_debug():
    guild = client.get_guild(GUILD)
    if DEBUG_MODE:
        try:
            debug_user = guild.get_member(DEBUG_USER)
            if not debug_user.dm_channel:
                await debug_user.create_dm()
            return debug_user.dm_channel
        except: return
    elif guild: return guild.get_channel(CHANNEL["debug"])
    else: return

def get_data(name, data):
    for key in name.split(" > "):
        try: key = int(key)
        except ValueError: pass
        data = data[key]
    return data

# sends a question and waits for an answer, then returns the answer and the user
async def get_input(message_type, channel, *, user=None):
    data = get_data(message_type, INPUTS)
    message = data["message"]
    timeout = data["timeout"] if "timeout" in data else 60
    delete = data["delete"] if "delete" in data else 3
    
    bot_msg = await channel.send(message)
    
    def check(msg):
        return (user == None) or (msg.author == user)
    try:
        user_msg = await client.wait_for('message', timeout=timeout, check=check)
    except asyncio.TimeoutError:
        await bot_msg.delete()
        return None
    else:
        result = user_msg.content, user_msg.author
        if delete > 1:
            await user_msg.delete()
            delete -= 2
        if delete == 1:
            await bot_msg.delete()
        return result

# ---------- GLOBAL FUNCTIONS ---------- #





# ---------- CLASSES ---------- #
class Role:
    def __init__(self, role_type, role=None):
        self.role = role
        self.type = role_type
        self.name = role.name if role else ""
        self.id = role.id if role else 0
        self.colour = role.colour if role else self.type["colour"]
        self.match = 0.0
        self.distance = []
        self.aliases = [self.name]
        if role_type["name"] in ROLES and self.id != 0:
            self.aliases = ROLES[role_type["name"]][str(self.id)]
            self.aliases.append(self.name)
        
    def compare(self, text):
        text = text.lower()
        algorithms = ALGORITHM_SEQUENCE.split(" > ")
        for a_name in algorithms:
            if a_name in ALGORITHMS:
                algorithm = ALGORITHMS[a_name]
                best_distance = float("inf")
                for alias in self.aliases:
                    alias = alias.lower()
                    if a_name is algorithms[0]:
                        self.match = max(self.match, algorithm.normalized_distance(alias, text))
                    best_distance = min(best_distance, algorithm.distance(alias, text))
                self.distance.append(best_distance)

class Embed:
    def __init__(self, embed_type, variables, *, create_fields=True):
        self.type = embed_type
        self.variables = variables
        self.data = self.get_data(embed_type)
        self.embed = self.create_embed(create_fields)
        self.message = None
        self.user = None
        self.channel = None

    def cmp(self, a, b):
        a = a.to_dict()
        b = b.to_dict()
        for x in a:
            if x in b:
                if a[x] != b[x]:
                    return False
        return True

    async def send(self, *, channel=None, message=None):
        if "message" in self.variables and channel == None:
            channel = self.variables["message"].channel
        if not channel: return
        self.channel = channel
        self.user = self.variables["user"] if "user" in self.variables else None

        if message:
            if len(message.embeds) > 0 and not self.cmp(message.embeds[0], self.embed):
                self.message = await message.edit(embed=self.embed)
        else:
            self.message = await channel.send(embed=self.embed)
        
        err = await self.activate_buttons()
        if err and self.data["timeout"] != None:
            await self.message.delete(delay=self.data["timeout"])
        
    async def activate_buttons(self):
        if self.user == None: return True
        if self.message == None: return True
        if "buttons" not in self.data: return True
        if len(self.data["buttons"]) == 0: return True

        try:
            await self.message.clear_reactions()
        except: pass

        # create buttons
        for button in self.data["buttons"]:
            button["emoji"] = emojize(button["emoji"], use_aliases=True)
            await self.message.add_reaction(button["emoji"])


        # check if button is clicked
        def check(reaction, user):
            buttons = [x["emoji"] for x in self.data["buttons"]]
            if str(reaction.emoji) in buttons:
                return (self.user == None) or (user == self.user)
            else: return False 
        
        try:
            reaction, _ = await client.wait_for('reaction_add', timeout=self.data["timeout"], check=check)
        except asyncio.TimeoutError:
            await self.message.delete()
        else: # if clicked
            button = self.get_button(reaction.emoji)
            if not button: button = {}
            if "function" in button:
                await self.function(button["function"])
                        
            if "delete" not in button or button["delete"]:
                await self.message.delete()
    
    def get_button(self, emoji):
        if "buttons" not in self.data: return
        
        for button in self.data["buttons"]:
            if button["emoji"] == str(emoji): return button
    
    def create_embed(self, create_fields):
        data = deepcopy(self.data)

        self.variables["time"] = datetime.utcnow().strftime(DATE_FORMAT)
        if "color" in data and type(data["color"]) is str:
            data["color"] = int(data["color"].format(**self.variables))

        embed = discord.Embed.from_dict(deepcopy(data))
        embed.clear_fields()

        if embed.title: embed.title = embed.title.format(**self.variables)
        if embed.description: embed.description = embed.description.format(**self.variables)
        if embed.footer.text: embed.set_footer(text=embed.footer.text.format(**self.variables))

        if create_fields and "fields" in data:
            for field in data["fields"]:
                embed.add_field(name=field["name"].format(**self.variables),
                value=field["value"].format(**self.variables), inline=field["inline"])
        return embed
    
    def get_data(self, embed_type):
        data = deepcopy(get_data(embed_type, EMBEDS))
        if "timeout" not in data or data["timeout"] <= 0:
            data["timeout"] = None
        return data

    async def function(self, function):
        variables = self.variables.copy()
        guild = variables["guild"]
        user = guild.get_member(self.user.id)
        if not user: user = self.user
        role = variables["role"] if "role" in variables else None
        debug = await get_debug()
        if not debug: return
        
        async def create_role():
            global roles_updating, ROLES
            roles_updating = True
            new_role = await guild.create_role(name=role.name, colour=role.colour)
            
            if role.type["name"] in ROLES:
                roles_in_group = [guild.get_role(int(x)) for x in ROLES[role.type["name"]]]
                roles_in_group = list(filter(None, roles_in_group))
                idx = roles_in_group[0].position
                for r in roles_in_group:
                    idx = min(idx, r.position)
                roles_in_group.append(new_role)
                roles_in_group.sort(key=lambda x: x.name.lower())
                roles_in_group.reverse()
                idx += roles_in_group.index(new_role)
                idx -= 1
                roles_in_group.sort()
                ROLES[role.type["name"]][str(new_role.id)] = [role.name]
                write_log(f"Role: Created new {role.type['name']} - {role.name}")
                
            else:
                ROLES["other"][str(new_role.id)] = [role.name]
                write_log(f"Role: Created new role - {role.name}")
            embed = Embed("role > created", variables)
            await embed.send(channel=debug)
            
            if role.type["name"] in ROLES:
                await guild.edit_role_positions({new_role:idx})
            await FileHandler.save_roles()
            roles_updating = False
            return new_role


        if self.type == "role > question":
            if function.find("add role") == 0:
                idx = int(re.findall(r"-?\d+", function)[0])
                new_role = guild.get_role(role[idx].id)
                try:
                    await user.add_roles(new_role)
                    write_log(f"Role: Added {role[idx].type['name']} - {role[idx].name} to {user.display_name}")
                except: write_log(f"Role: Failed to add {role[idx].type['name']} - {role[idx].name} to {user.display_name}")
            elif function == "suggest role":
                variables["role"] = role[0]
                embed = Embed("role > suggestion", variables)
                write_log(f"Role: {user.display_name} suggested {role[0].type['name']} - {role[0].name}")
                await embed.send(channel=debug)
    

        elif self.type == "role > create":
            if function == "accept":
                await create_role()
        

        elif self.type == "role > suggestion":
            if function == "accept":
                new_role = await create_role()
                await user.add_roles(new_role)
                write_log(f"Role: Added {role.type['name']} - {role.name} to {user.display_name}")
            elif function == "change name":
                new_name = await get_input("role > change name", self.channel, self.user)
                if new_name:
                    self.variables["role"].name = new_name
                await self.send(message=self.message)
            elif function == "change type":
                new_type = await get_input("role > change type", self.channel, self.user)
                if new_type:
                    self.variables["role"].type = None
                await self.send(message=self.message)

        elif self.type == "bot > shutdown":
            if function == "accept":
                await variables["message"].channel.send(get_data("bot > shutdown", MESSAGES))
                await client.close()

class Server: # [Only for generating] YAML [variables]
    def __init__(self, guild):
        self.guild = guild
        self.emoji_count = len(guild.emojis)
        self.channel_count = len(guild.channels)
        self.voice_channel_count = len(guild.voice_channels)
        self.stage_channel_count = len(guild.stage_channels)
        self.text_channel_count = len(guild.text_channels)
        self.category_count = len(guild.categories)
        self.premium_subscriber_count = len(guild.premium_subscribers)
        self.role_count = len(guild.roles)
        self.created_at = guild.created_at.strftime(DATE_FORMAT)

class Bot: # YAML
    def __init__(self):
        self.uptime = re.sub(r"\.\d+", "", str(datetime.utcnow() - start_time))
        self.start_time = start_time.strftime(DATE_FORMAT)
        self.version = VERSION
        self.user_count = len(users)
        self.role_count = 0
        for role_type in ROLES:
            self.role_count += len(ROLES[role_type])

class Error:
    def __init__(self):
        self.id = 0
        self.user = None
        self.title = "-"
        self.description = "-"

    async def new(self, error_id, inputs, user, send):
        self.id = error_id
        self.user = user
        inputs = list(inputs)
        inputs.insert(0,None)

        # Replaces $n with input n
        def format_text(text):
            return re.sub(r"\$(\d+)", r"`{inputs[\1]}`", text).format(inputs=inputs)
        
        # Find error details
        for x in ERRORS:
            if "id" not in x: continue
            if error_id == x["id"]:
                if ("title" in x) and x["title"]:
                    self.title = format_text(x["title"])
                if ("description" in x) and x["description"]:
                    self.description = format_text(x["description"])
                break
        
        if send:
            await self.send()
    
    async def send(self):
        channel = await get_debug()
        if not channel: return
        if self.user:
            if not self.user.dm_channel:
                await self.user.create_dm()
            channel = self.user.dm_channel
            write_log(f"Error: Sent error to {self.user.name}: {self.id} - {self.title} | {self.description}")
        else: write_log(f"Error: Sent error: {self.id} - {self.title} | {self.description}")
        embed = Embed("error", locals())
        await embed.send(channel=channel)

        if self.id == 201:
            print(get_data("verification > new code", MESSAGES))
            await channel.send(get_data("verification > new code", MESSAGES).format(user=self.user))
            await channel.send(f"`{generate_code(self.user)}`")
            write_log("Verification: Activation codes: "+str(active_codes))

class Messages:
    def __init__(self, messages: list = []):
        if type(messages) != list: raise TypeError(f"Got '{type(messages).__name__}', expected 'list'")
        self.all = messages

    def get_by(self, key, *args):
        result = self.get_as_list_by(key, *args)
        if len(result) == 0: return None
        elif len(result) == 1: return result[0]
        else: return result
    
    def get_as_list_by(self, key, *args):
        result = []
        for msg in self.all:
            if msg[key] in args: result.append(msg)
        return Messages(result)

    def __len__(self): return len(self.all)
    def __getitem__(self, key): return self.all[key]
    def __iter__(self): return self.all.__iter__()
    def append(self, msg_type, msg_id, **kwargs):
        msg = {
            "type": msg_type,
            "id": msg_id
        }
        for kw in kwargs:
            msg[kw] = kwargs[kw]
        self.all.append(msg)

    def remove(self, item): self.all.remove(item)

class FileHandler:
    async def failed():
        global ONLINE
        ONLINE = False
        
        err = await error(100)
        print(err.message)
        await client.close()
        return True

    def get_file_data(path):
        with open(path, "r", encoding="utf-8") as f:
            if path.endswith(".yml") or path.endswith(".yaml"):
                return yaml.load(f)
            if path.endswith(".json"):
                return json.load(f)
            else: return f
    
    def get_missing_properties(data, *properties):
        if ( len(properties) == 1 
        and hasattr(properties[0], "__getitem__")
        and type(properties[0]) is not str ):
            properties = properties[0]
        
        result = []
        for key in properties:
            try:
                get_data(key, data)
            except KeyError: result.append(key)
        
        if len(result) == 0: return None
        else: return result

    def get_backup(directory, extensions, oldest=False):
        if directory.endswith("/"): directory = directory[:-1]
        all_files = []
        for x in extensions:
            if x.startswith("."): x = x[1:]
            all_files += glob(f"{directory}/*.{x}")
        if not all_files: return
        
        if oldest: return min(all_files, key=os.path.getmtime)
        else: return max(all_files, key=os.path.getmtime)

    async def try_loading(path, *, is_data=False, send_errors=True):
        async def load_yaml(path, send_errors):
            try:
                return FileHandler.get_file_data(path)
            except FileNotFoundError:
                await error(101, path, send=send_errors)
            except ruamel.yaml.scanner.ScannerError:
                await error(103, path, send=send_errors)
            except ruamel.yaml.parser.ParserError:
                await error(103, path, send=send_errors)
        
        async def load_json(path, send_errors):
            try:
                return FileHandler.get_file_data(path)
            except FileNotFoundError:
                await error(101, path, send=send_errors)
            except json.JSONDecodeError:
                await error(102, path, send=send_errors)

        
        if is_data:
            data = await load_yaml(path, send_errors)
            if data is None: return

            missing_properties = FileHandler.get_missing_properties(data, DATA_DEPENDENCIES)
            if missing_properties:
                await error(104,path,"`\n`".join(missing_properties), send=send_errors)
                return

            invalid_keys = [None if x in ("seconds","minutes","hours") else x for x in get_data("debug > update time", data)]
            invalid_keys = list(filter(None, invalid_keys))
            if invalid_keys:
                await error(105, invalid_keys[0], path + " > debug > update time", send=send_errors)
                return
            
            loaded_errors = [x["id"] for x in get_data("errors", data)]
            missing_errors = [None if x in loaded_errors else str(x) for x in ERROR_DEPENDENCIES]
            missing_errors = list(filter(None, missing_errors))
            if missing_errors:
                await error(104, path, "errors > " + "`\n`errors > ".join(missing_errors), send=send_errors)
                return
            return data
        
        else:
            data = await load_json(path, send_errors)
            return data

    async def load_file(filedict, *extensions, is_data=False, send_errors=True):
        data = await FileHandler.try_loading(filedict["file"], is_data=is_data, send_errors=send_errors)
        if data is not None: await FileHandler.backup(filedict)
        else:
            if ("backup" not in filedict) or (not filedict["backup"]): return
            backup = FileHandler.get_backup(filedict["backup"], extensions)
            if backup is None: return
            data = await FileHandler.try_loading(backup, is_data=is_data, send_errors=send_errors)
            if data is None: return
        return data

    async def load():
        global users, ROLES, messages
        def assign_data(data):
            global ERRORS, GUILD, DEBUG_MODE, CHANNEL, DEBUG_USER, whitelist,\
            PATH, VERIFICATION, ROLE_SYSTEM, THRESHOLD, ALGORITHM_SEQUENCE,\
            EMBEDS, DATE_FORMAT, MESSAGES, COMMANDS, INPUTS

            for key in data["paths"]:
                PATH[key] = data["paths"][key]
            ERRORS = get_data("errors", data)
            GUILD = get_data("server id", data)
            DEBUG_MODE = get_data("debug > status", data) == "on"
            DEBUG_USER = get_data("debug > user", data)
            CHANNEL = get_data("channels", data)
            DATE_FORMAT = get_data("date format", data)
            ALGORITHM_SEQUENCE = get_data("text comparison > algorithm", data)
            THRESHOLD = get_data("text comparison > threshold", data)
            ROLE_SYSTEM = get_data("role system", data)
            VERIFICATION = get_data("verification", data)
            EMBEDS = get_data("embeds", data)
            MESSAGES = get_data("messages", data)
            INPUTS = get_data("input messages", data)
            COMMANDS = get_data("commands", data)
            whitelist = get_data("whitelist", data)
            update_status.change_interval(**get_data("debug > update time", data))


        data = await FileHandler.load_file(PATH["data"], "yml", "yaml", is_data=True)
        if data is None: return await FileHandler.failed()
        assign_data(data)

        data = await FileHandler.load_file(PATH["users"], "json")
        if data is None: return await FileHandler.failed()
        users = data

        data = await FileHandler.load_file(PATH["roles"], "json")
        if data is None: return await FileHandler.failed()
        ROLES = data

        data = await FileHandler.load_file(PATH["messages"], "json")
        if data is None: return await FileHandler.failed()
        messages = Messages(data)

    def get_filename(filedict):
        match = re.fullmatch(r"(?:.+\/)?(.+)\.(.+)", filedict["file"])
        name = match.group(1)
        extension = match.group(2)
        return name, extension

    async def backup(filedict):
        name, extension = FileHandler.get_filename(filedict)
        is_data = extension in ("yaml", "yml")
        loaded = await FileHandler.try_loading(filedict["file"], is_data=is_data, send_errors=False)
        if loaded and "backup" in filedict and filedict["backup"]:
            backup = FileHandler.get_backup(filedict["backup"], ("yaml","yml") if is_data else [extension])
            if backup and cmp(filedict["file"], backup, shallow=False): return
            time = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
            copyfile(filedict["file"], f"{filedict['backup']}/{name}_{time}.{extension}")
            write_log(f"File: Backed up {name}.{extension}")

    async def save_file(filedict, data):
        await FileHandler.backup(filedict)
        name, extension = FileHandler.get_filename(filedict)
        try:
            prev_data = FileHandler.get_file_data(filedict["file"])
            if data == prev_data: return
        except: pass            
        with open(filedict["file"], "w", encoding="utf-8") as f:
            if extension == "json":
                json.dump(data, f, indent=2)
            elif extension in ("yml","yaml"):
                yaml.dump(data, f)
        write_log(f"File: Updated {name}.{extension}")

    async def save_data():
        global whitelist
        with open(PATH["data"]["file"], "r", encoding="utf-8") as f: data = yaml.load(f)
        data["whitelist"] = whitelist
        await FileHandler.save_file(PATH["data"], data)

    async def save_users(): await FileHandler.save_file(PATH["users"], users)
    async def save_roles(): await FileHandler.save_file(PATH["roles"], ROLES)

    async def replace(filedict, discord_file):
        name, extension = FileHandler.get_filename(filedict)
        await FileHandler.backup(filedict)
        with open(filedict["file"], "wb") as f:
            await discord_file.save(f)
        write_log(f"File: Replaced {name}.{extension}")

class Command:
    def __init__(self, message: discord.Message) -> None:
        self.message = message
        self.is_private = str(message.channel.type) == "private"
        self.user = message.author.id
        self.args = {}
        self.is_whitelisted = self.user in whitelist
    
    def is_command(self, command: str) -> bool:
        command = get_data(command, COMMANDS)
        if command is None: return True
        arg_pos = re.findall(r"(?<=\$)\d+", command)
        arg_pos = [int(x) for x in arg_pos]

        command = re.sub(r"\$\d+(\?)?", r"(.+\1)", command)
        command = command.lower().encode("unicode_escape").decode()
        
        match = re.fullmatch(command, self.message.content.lower())
        if match:
            self.args.clear()
            for i in range(len(arg_pos)):
                self.args[arg_pos[i]] = match.group(i+1)
            return True
        else: return False
# ---------- CLASSES ---------- #





# ---------- DISCORD CONNECTION ---------- #
@client.event
async def on_connect():
    global start_time, ONLINE, STARTED
    ONLINE = True
    if STARTED: return write_log("Connected")
    STARTED = True
    await client.wait_until_ready()
    err = await FileHandler.load()
    if err: return
    print(f'Online - {VERSION}')
    write_log("Online - "+VERSION)
    start_time = datetime.utcnow()

@client.event
async def on_disconnect():
    global ONLINE
    if not ONLINE: return
    ONLINE = False
    try:
        await client.wait_for("resumed", timeout=3600)
    except asyncio.TimeoutError:
        if not ONLINE:
            if client.latency == float("inf"):
                write_log("Disconnected")
                await client.close()
            else: ONLINE = True
    else: ONLINE = True

@tasks.loop(seconds=10)
async def update_status():
    try:
        if not ONLINE: return
        try:
            guild = client.get_guild(GUILD)
            channel = guild.get_channel(CHANNEL["status"])
        except: return
        if messages is None: return

        found_bot_status = False
        found_server_status = False
        for msg in messages.get_as_list_by("type", "bot status", "server status"):
            try:
                message = await channel.fetch_message(msg["id"])
            except discord.errors.NotFound: pass
            else:
                if msg["type"] == "bot status":
                    found_bot_status = True
                    bot = Bot()
                    embed = Embed("status > bot", locals())
                    await embed.send(message=message)
                if msg["type"] == "server status":
                    found_server_status = True
                    guild = client.get_guild(GUILD)
                    server = Server(guild)
                    embed = Embed("status > server", locals())
                    await embed.send(message=message)


        if not found_bot_status:
            bot = Bot()
            embed = Embed("status > bot", locals())
            await embed.send(channel=channel)
            messages.append("bot status", embed.message.id)
        if not found_server_status:
            guild = client.get_guild(GUILD)
            server = Server(guild)
            embed = Embed("status > server", locals())
            await embed.send(channel=channel)
            messages.append("server status", embed.message.id)
        await FileHandler.save_file(PATH["messages"], messages.all)
    except: pass
# ---------- DISCORD CONNECTION ---------- #





# ---------- VERIFICATION ---------- #
def generate_code(user):
    global active_codes
    alphabet = string.ascii_letters + string.digits
    code = "".join(secrets.choice(alphabet) for i in range(6))
    active_codes[user.id] = code
    return code

async def send_verification(user):
    await user.create_dm()
    await user.dm_channel.send(MESSAGES["verification"]["start verification"].format(**locals()))
    await user.dm_channel.send(MESSAGES["verification"]["send code"].format(**locals()))
    await user.dm_channel.send(f"`{generate_code(user)}`")
    write_log("Verification: Activation codes: "+str(active_codes))

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id: return
    channel = client.get_channel(payload.channel_id)
    if payload.message_id == VERIFICATION["message id"] and channel.id == VERIFICATION["channel id"] and payload.emoji.id == VERIFICATION["emoji id"]:
        user = client.get_user(payload.user_id)
        if str(user.id) in users:
            await error(206,user=user)
        else: await send_verification(user)

async def recieve_link(variables):
    global users, active_codes
    message = variables["message"]
    guild = variables["guild"]
    debug = variables["debug"]
    user = variables["user"]
    member = guild.get_member(user.id)
    errors = []
    
    # ERRORS no active codes
    if len(active_codes) == 0: return await error(201,user=user)

    # ERRORS no active code for current user
    if user.id not in active_codes:
        return await error(201,user=user)

    key = active_codes[user.id]
    link = "http"+re.findall(r"://aminoapps.com/\S+", message.content)[0] # get link
    link_url = requests.get(link).url
    
    # ERRORS link already used
    for x in users:
        if users[x] == link_url:
            if x == str(user.id): return await error(206,user=user)
            else: return await error(202,users[x],user=user)
    
    site = requests.get(link).text
    title_end = site.find('</title>  <meta name="description"')

    # ERRORS no title
    if title_end <= 0: return await error(203,link,user=user)

    # ERRORS wrong title
    elif site[title_end-22:title_end] != "Music Production Amino": return await error(204,link,user=user)

    # ERRORS no code on site
    elif site.find(key) <= 0: return await error(200,key,link,user=user)
    
    codes = re.findall(key, site)
    found_on_wall = False
    for _ in codes:
        key_pos = site.find(key)
        if site[key_pos-40:key_pos].find('<div class="comment-text article"><p>') >= 0:
            found_on_wall = True
            break
        else: site = site.replace(key, "??????", 1)
    
    # ERRORS code not on wall
    if not found_on_wall: return await error(205,key,link,user=user)
    
    # find profile owner
    start = site.find("user-name-truncate")+22
    end = start+site[start:].find("  </span>  ")
    username = site[start:end]
    
    # find commenter
    comment = site.find(key)
    start = site[:comment].rfind('<span class="content">')+22
    end = start+site[start:].find("</span>  ")
    commenter = site[start:end]
    
    # ERRORS commenter is not profile owner
    if username != commenter: return await error(207,username,commenter,user=user)


    ### Verified ###

    # save discord id and url
    users[str(user.id)] = link_url
    del active_codes[user.id]
    
    # Add MPA Member Role
    role = discord.utils.get(guild.roles, name="MPA Member") # get MPA Member role
    try: await member.add_roles(role) # add role
    except: pass
    try:
        member_role = discord.utils.get(guild.roles, name="Member") # get Member role
        await member.remove_roles(member_role) # remove member role
    except: pass

    # Change Nick
    nickname = emojize(username, use_aliases=True)
    if user.name != nickname:
        if len(nickname) <= 32: # change nickname
            try:
                await member.edit(nick=nickname)
                await debug.send(MESSAGES["changed nick"].format(**locals()))
                write_log("Nickname: Changed nickname of user "+user.name+" to "+nickname)
            except: pass
        else:
            await error(301,member.display_name,nickname)
    await FileHandler.save_users()
    await user.dm_channel.send(MESSAGES["verification"]["completed"].format(**locals()))
    await debug.send(MESSAGES["verification"]["verified user"].format(**locals()))
    write_log(f"Verification: Verified {user.name} with the link {link}")
    return None
# ---------- VERIFICATION ---------- #





# ---------- ROLES ---------- #

# Sorting algorithm for roles based on text distance
def sort_roles(a, b):
    for i in range(len(a.distance)):
        if a.distance[i] != b.distance[i]:
            return a.distance[i] - b.distance[i]
    return 0

# Returns the name and the colour of role type that matches "text"
def get_role_type(text):
    default = {"name":"", "colour":0}
    if not text: return default
    algorithm = ALGORITHM_SEQUENCE.split(" > ")[0]
    for role_type in ROLE_SYSTEM["role types"]:
        if algorithm in ALGORITHMS:
            match = ALGORITHMS[algorithm].normalized_similarity(text.lower(), role_type["name"].lower())
            if match > THRESHOLD:
                return role_type
    return default

# Sync internal and external roles and sort the hierarchy
async def update_roles():
    global ROLES, roles_updating
    roles_updating = True
    guild = client.get_guild(GUILD)
    write_log("Role: Updating roles...")
    # Delete nonexistend roles
    role_ids = [str(x.id) for x in guild.roles]
    for role_type in ROLES:
        nonexistent_roles = []
        for role in ROLES[role_type]:
            if role not in role_ids:
                nonexistent_roles.append(role)
        for role in nonexistent_roles:
            write_log(f"Role: Removed {role} from roles.json because the role does not seem to exist")
            del ROLES[role_type][role]
    await FileHandler.save_roles()

    # Rearrange roles
    role_types = [x["name"] for x in ROLE_SYSTEM["role types"]]
    role_types.reverse()
    idx = guild.self_role.position
    roles = {} # sort roles by role type
    for role in guild.roles:
        if role.position >= guild.self_role.position: continue
        role_type = None
        for x in ROLES:
            for y in ROLES[x]:
                if y == str(role.id):
                    role_type = x
                    break
            if role_type: break
        if role_type == "other": role_type = None
        if role_type not in roles: roles[role_type] = []
        roles[role_type].append(role)
        if role_type in role_types: idx = min(idx, role.position)
    
    # Sort role lists canonically and append the roles with new positions
    positions = {}
    for role_type in role_types:
        roles[role_type].sort(key=lambda x: x.name.lower())
        roles[role_type].reverse()
        for role in roles[role_type]:
            positions[role] = idx
            idx += 1
            # Make sure the role has the right colour
            for x in ROLE_SYSTEM["role types"]:
                new_col = hex(x['colour']).replace("0x", "#")
                if x["name"] == role_type and str(role.colour) != new_col:
                    write_log(f"Role: Changed colour for {role.name} from {role.colour} to {new_col}")
                    await role.edit(colour=x["colour"])
                    break
    await guild.edit_role_positions(positions)
    write_log("Role: Finished updating roles")
    roles_updating = False

@client.event
async def on_guild_role_update(before, after):
    if not roles_updating:
        await update_roles()
# ---------- ROLES ---------- #





# ---------- COMMANDS ---------- #

@client.event
async def on_message(message):
    global whitelist
    if message.author == client.user: return
    cmd = Command(message)

    #info
    guild = client.get_guild(GUILD)
    debug = await get_debug()
    if not debug: return

    user = message.author
    is_private = str(message.channel.type) == "private"
    #info


    # AMINO LINK
    if message.content.find("://aminoapps.com/") >= 0 and is_private:
        await recieve_link(locals())

    # SERVER STATUS
    if cmd.is_command("status > server"):
        server = Server(guild)
        embed = Embed("status > server", locals())
        await embed.send()

    # BOT STATUS
    if cmd.is_command("status > bot"):
        bot = Bot()
        embed = Embed("status > bot", locals())
        await embed.send()




    
    
    # Check for the most accurate role
    # If accuracy is over a threshold, add role
    # Else send embed
    # Embed function saves data

    ### ADD ROLES
    if message.channel.id == CHANNEL["roles"] or (DEBUG_MODE == True and message.channel.id == debug.id):
        
        # Split input text into roles
        separators_regex = "|".join([re.escape(x) for x in ROLE_SYSTEM["separators"]])
        text = re.split(separators_regex, message.content.lower())
        
        current_role_type = None
        for word in text:
            if len(word) < 2: continue
            current_role_type = get_role_type(word)["name"] or current_role_type
            
            # Go through each role
            # for role in ROLES
            role = []
    

    ### ROLE MANAGEMENT
    member = guild.get_member(user.id)
    if member != None and (member.guild_permissions.manage_roles or member.guild_permissions.administrator):
        # HELP ROLE
        if cmd.is_command("help > role"):
            embed = Embed("help > role", locals())
            await embed.send()

        # CREATE ROLE
        if cmd.is_command("role > create"):
            role = Role(get_role_type(cmd.args[2]))
            role.name = cmd.args[1]
            if not role.type["name"]: role.name += " as " + cmd.args[2]

            embed = Embed("role > create", locals())
            await embed.send()
            

                


    ### WHITELIST COMMANDS
    if user.id in whitelist:

        # GET FILE
        if cmd.is_command("file > get") and is_private:
            filename = cmd.args[1]
            found_file = False
            for filedict in (PATH[x] for x in PATH):
                if filedict["file"].find(filename) >= 0:
                    with open(filedict["file"], "rb") as f:
                        await message.channel.send(file=discord.File(f, filename))
                        found_file = True
                        write_log(f"File: Sent {filename} to {user.name}")
            if not found_file: await error(101,filename,user=user)

        # REPLACE FILE
        if cmd.is_command("file > replace") and is_private:
            for message_file in message.attachments:
                found_file = False
                for filedict in (PATH[x] for x in PATH):
                    if filedict["file"].find(message_file.filename) >= 0:
                        await FileHandler.replace(filedict, message_file)
                        await message.channel.send(MESSAGES["updated file"].format(**locals()))
                        found_file = True
                        err = await FileHandler.load()
                        if err: return
                if not found_file: await error(101,message_file.filename,user=user)

        # GET WHITELIST
        if cmd.is_command("whitelist > view"):
            embed = Embed("whitelist", locals(), create_fields=False)

            field = EMBEDS["whitelist"]["fields"][0]
            for user_id in whitelist:
                try:
                    user = guild.get_member(user_id)
                    if user == None: user = client.get_user(user_id)
                    embed.embed.add_field(name=field["name"].format(user=user),value=field["value"].format(user=user),inline=field["inline"])
                except:
                    write_log(f"Whitelist: Could not find user {user_id}")
            await embed.send()

        # REMOVE FROM WHITELIST
        if cmd.is_command("whitelist > remove"):
            for who in message.mentions:
                if who.id in whitelist:
                    whitelist.remove(who.id)
                    write_log(f"Whitelist: Removed {who.display_name}")
                    await message.channel.send(MESSAGES["whitelist"]["remove"].format(**locals()))
                else:
                    write_log(f"Whitelist: Attempted to remove {who.display_name}, but the user does not exist in the whitelist")
                    await message.channel.send(MESSAGES["whitelist"]["remove failed"].format(**locals()))
            await FileHandler.save_data()

        # ADD TO WHITELIST
        if cmd.is_command("whitelist > add"):
            for who in message.mentions:
                if who.id not in whitelist:
                    whitelist.append(who.id)
                    write_log(f"Whitelist: Added {who.display_name}")
                    await message.channel.send(MESSAGES["whitelist"]["add"].format(**locals()))
                else:
                    write_log(f"Whitelist: Attempted to add {who.display_name}, but the user is already in the whitelist")
                    await message.channel.send(MESSAGES["whitelist"]["add failed"].format(**locals()))
            await FileHandler.save_data()

        # HELP WHITELIST
        if cmd.is_command("help > whitelist"):
            files = ", ".join([PATH[x]["file"] for x in PATH])
            embed = Embed("help > whitelist", locals())
            await embed.send()

        # UPDATE DATA
        if cmd.is_command("bot > update"):
            await FileHandler.load()
            await update_roles()
            await message.channel.send(get_data("bot > update", MESSAGES))

        # REBOOT
        if cmd.is_command("bot > reboot"):
            await message.channel.send(get_data("bot > reboot", MESSAGES))
            await client.close()
            os.execv(sys.executable, ['python'] + sys.argv)
        
        # SHUTDOWN
        if cmd.is_command("bot > shutdown"):
            embed = Embed("bot > shutdown", locals())
            await embed.send()


        # TEST
        if message.content.lower() == "a":
            embed = Embed("role > question", locals())
            await embed.send()



update_status.start()
client.run(token)