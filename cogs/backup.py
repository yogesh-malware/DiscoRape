import discord
import requests
import random
import time
import sys
import os
from discord.ext import commands
import json
from colorama import Fore, init

with open("./data/config.json") as f:
    config = json.load(f)

token = config.get("TOKEN")
headers = {"authorization": token}
connect = requests.get(
    "https://canary.discordapp.com/api/v6/users/@me", headers=headers
)


class backup(commands.Cog):
    """Uhhh it backs up your acocunt kinda but offbrand"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def backupfriends(self, ctx):
        saved_friends = 0

        friends = requests.get(
            "https://discord.com/api/v6/users/@me/relationships", headers=headers
        )
        for friend in friends.json():
            if friend["type"] == 1:
                username = "Username: %s#%s | User ID: %s\n" % (
                    friend["user"]["username"],
                    friend["user"]["discriminator"],
                    friend["id"],
                )
                print(username)
                with open("Discord Friends.txt", "a", encoding="UTF-8") as f:
                    f.write(username)
                saved_friends += 1

        with open("Discord Friends.txt", "r", encoding="UTF-8") as f:
            fixed = f.read()[:-1]
        with open("Discord Friends.txt", "w", encoding="UTF-8") as f:
            f.write(fixed)

        print(f"\n> Successfully saved all %s Discord friends.\n\n{saved_friends}")

    # NOTE: Shameless copy paste for both of these commands got the src from a friend

    @commands.command()
    async def backupservers(self, ctx):
        saved_servers = 0
        attempts = 0
        server_info_all = ""

        servers = requests.get(
            "https://discordapp.com/api/v6/users/@me/guilds", headers=headers
        )
        for server in servers.json():
            server_info_all += "%s|||%s\n" % (server["id"], server["name"])

        payload = {"max_age": "0", "max_uses": "0", "temporary": False}

        for server_info in server_info_all.splitlines():
            server_id = server_info.split("|||")[0]
            server_name = server_info.split("|||")[1]

            channels = requests.get(
                "https://discord.com/api/v6/guilds/%s/channels" % (server_id),
                headers=headers,
            )
            for channel in channels.json():
                if channel["type"] == 0:
                    channel_id = channel["id"]
                    invite = requests.post(
                        "https://discord.com/api/v6/channels/%s/invites" % (channel_id),
                        json=payload,
                        headers=headers,
                    )

                    if invite.status_code == 403:
                        attempts += 1
                        sys.stdout.write(
                            "Discord Server: %s | Channel ID: %s | Retrying . . .\n"
                            % (server_name, channel_id)
                        )
                        if attempts == 5:
                            sys.stdout.write("%s has a Vanity URL.\n" % (server_name))
                            with open(
                                "Discord Servers.txt", "a", encoding="UTF-8"
                            ) as f:
                                f.write(
                                    "Discord Server: %s | Vanity URL\n" % (server_name)
                                )
                            saved_servers += 1
                            attempts = 0
                            break
                        else:
                            pass
                        time.sleep(4)

                    elif invite.status_code == 429:
                        sys.stdout.write("Rate limited.\n")
                        time.sleep(9)

                    else:
                        invite_url = "https://discord.gg/%s" % (
                            str(invite.json()["code"])
                        )
                        sys.stdout.write(
                            "Discord Server: %s | Invite Link: %s\n"
                            % (server_name, invite_url)
                        )
                        with open("Discord Servers.txt", "a", encoding="UTF-8") as f:
                            f.write(
                                "Discord Server: %s | Channel ID: %s | Invite Link: %s\n"
                                % (server_name, channel_id, invite_url)
                            )
                        saved_servers += 1
                        time.sleep(4)
                        break

        sys.stdout.write(
            "\n> Successfully saved all %s Discord servers.\n\n" % (saved_servers)
        )

    @commands.command()
    async def recoverservers(self, ctx):
        joined_servers = 0

        if os.path.exists("Discord Servers.txt"):
            with open("Discord Servers.txt", "r", encoding="UTF-8") as f:
                for line in f.readlines():
                    while True:
                        try:
                            line = line.replace("\n", "")
                            if "Vanity URL" in line:
                                server_name = line.split("Discord Server: ")[1].split(
                                    " | Vanity URL"
                                )[0]
                                print(
                                    f"{Fore.RED}[-] RECOVERY_SERVERS >{Fore.RESET} {server_name} Server has a Vanity URL."
                                )
                                break
                            else:
                                invite_code = line.split("https://discord.gg/")[1]
                                server_name = line.split("Discord Server: ")[1].split(
                                    " | Channel ID"
                                )[0]
                        except IndexError:
                            print(f"Invalid syntax at line: {line}")
                            break

                        join = requests.post(
                            "https://discord.com/api/v6/invites/%s" % (invite_code),
                            headers=headers,
                        )
                        if join.status_code == 429:
                            print(
                                f"{Fore.GREEN}[-] RECOVERY_SERVERS >{Fore.RESET} Rate limited | Timeout for 10 seconds"
                            )
                            time.sleep(10)
                        elif join.status_code == 200:
                            print(
                                f"{Fore.GREEN}[-] RECOVERY_SERVERS >{Fore.RESET} Successfully joined {server_name}"
                            )
                            joined_servers += 1
                            break
                        elif join.status_code == 403:
                            print(
                                f"{Fore.RED}[-] RECOVERY_SERVERS >{Fore.RESET} Verify your Discord account.\n"
                            )
                            break
                        else:
                            print(
                                f"{Fore.RED}[-] RECOVERY_SERVERS >{Fore.RESET} Error: {join.text}"
                            )
                            break

            print(
                f"{Fore.GREEN}[-] RECOVERY_SERVERS >{Fore.RESET} Successfully joined {joined_servers} Discord Servers... "
            )

        else:
            print(
                f"{Fore.RED}[-] RECOVERY_SERVERS >{Fore.RESET} You have not saved any servers.\n\n"
            )


### Add cog lmao
def setup(bot):
    bot.add_cog(backup(bot))
