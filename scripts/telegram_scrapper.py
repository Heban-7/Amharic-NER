import os, sys
import csv
import telethon
from telethon import TelegramClient
from dotenv import load_dotenv

# get working directory 
sys.path.append(os.path.abspath('..'))

# Load environment variables 
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('PHONE')

# Function to scrape data from a telegram channel 
async def scrape_channel(client, channel_username, writer, media_dir):
    """
    Scrapes messages from specified Telegram channel and writes   them to a csv file

    Args:
        client(TelegramClient): The active telegram client instance
        channel_username(str): username or link of the telegram channel to scrape 
        writer (csv.writer): csv writer object to save the scraped data
        media_dir(str): Directory to store downloaded media files
    """

    # Get channel entity and title 
    entity = await client.get_entity(channel_username)
    channel_title = entity.title # get the channel's name 
    print(f"Scraping Messages from Channel: {channel_title} ({channel_username})")

    # Itrate through messages in the channel 
    async for message in client.iter_messages(entity, limit = 10000):
        media_path = None

        # Check if message has media and download it 
        if message.media and hasattr(message.media, 'photo'):
            filename = f"{channel_username}_{message.id}.jpg" # create a unique filename for photo media
            media_path = os.path.join(media_dir, filename)
            await client.download_media(message.media, media_path) # save photo in media path direction

        # Message details for the csv file
        writer.writerow([
            channel_title,
            channel_username,
            message.id,
            message.message if message.message else "",
            message.date,
            media_path
        ])

# initialize the telegram client
client = TelegramClient('scraping_session', api_id, api_hash)

# Main function to manage scraping tasks
async def main():
    """
    Main Function to initialize the telegram client and scrape data from multiple channels.
    """

    # Start the telegram client
    await client.start()
    print("Telegram Client Started Successfully...")

    # create a directory to store media files 
    media_dir ='../data/photos'
    os.makedirs(media_dir, exist_ok=True)
    print(f"media file will be saved to: {media_dir}")

    # Open a csv file to save scraped data 
    output_file = '../data/telegram_data.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'Message Id', 'Message Text', 'Message Date', 'Media Path'])

        # List of channels to scrape 
        channels = (['@gebeyaadama',
                     '@ethio_brand_collection'])
        
        # Scrape data from each channel
        for channel in channels:
            await scrape_channel(client, channel, writer, media_dir)
            print(f"Finneshed scraping data from: {channel}")

    print(f"Scraped data saved to: {output_file}")


# Run the main function
with client:
    client.loop.run_until_complete(main())

