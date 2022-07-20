import config
from twitchAPI.twitch import Twitch
import pandas as pd
import datetime as dt

# TWITCH CLIENT SETUP
client_id = config.TWITCH_CLIENT_ID
my_app_secret = config.TWITCH_CLIENT_SECRET
twitch = Twitch(client_id, my_app_secret)

# These May Still Have No Need
broadcasters_database = pd.read_csv(config.BROADCASTER_CSV, index_col=0)
games_database = pd.read_csv(config.GAMES_CSV, index_col=0)

# TODO Four programs: discord bot, twitch trend/activity monitor, Server, Client

# TODO Intelligent Video Scraping Process (BASED ON YT CHANNELS)


# def start():
# GET Database of Channels (What to look for in clips, last time upload, ect)
# GET Channel Databases (Maybe The Archive or implement that into the main database)


def scrape_videos_example():
    scrape_database = pd.read_csv(config.SCRAPE_CSV, index_col=0)
    archive_database = pd.read_csv(config.ARCHIVE_CSV, index_col=0)

    month_ago = dt.datetime.now() - dt.timedelta(days=30)
    clips = twitch.get_clips(broadcaster_id="94753024", first=10, started_at=month_ago)

    for clip in clips["data"]:
        if clip["id"] not in archive_database.index:
            scrape_database.loc[clip["id"]] = [clip["broadcaster_id"],
                                               clip["game_id"],
                                               clip["created_at"],
                                               clip["view_count"]]
            archive_database.loc[clip["id"]] = [clip["url"]]
        else:
            pass  # print(clip['id'] + ": Duplicate")

    scrape_database.to_csv(config.SCRAPE_CSV)
    archive_database.to_csv(config.ARCHIVE_CSV)

    # No TO DO Automate: Dataframe for each channel? (I WILL PROBABLY MAKE THIS)
    pass
# scrape_videos_example()


def twitch_vid_example():
    # Adds any new games that have reached the current top 10
    game_database = pd.read_csv(config.GAMES_CSV, index_col=0)
    games = twitch.get_top_games(first=10)  # sorted by current active viewers
    for n in games["data"]:
        game = n
        if int(game["id"]) not in game_database.index:
            game_database.loc[game["id"]] = [game["name"]]
    game_database.to_csv(config.GAMES_CSV)

    # Adds any new casters that have reached the current top 15 clips
    caster_database = pd.read_csv(config.BROADCASTER_CSV, index_col=0)
    month_ago = dt.datetime.now() - dt.timedelta(days=30)
    clip_by_id = twitch.get_clips(game_id="509658", first=15, started_at=month_ago)
    for clip in clip_by_id["data"]:
        if int(clip["broadcaster_id"]) not in caster_database.index:
            print(clip["broadcaster_id"] + "," + clip["broadcaster_name"])
            # caster_database.loc[clip["broadcaster_id"]] = [clip["broadcaster_name"]]
    caster_database.to_csv(config.BROADCASTER_CSV)


def scrape_request():
    # TODO ability to request a scrape of any type for any amount
    pass
