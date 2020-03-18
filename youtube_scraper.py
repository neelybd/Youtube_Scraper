from file_handling import *
from selection import *
import pafy
import os
import youtube_dl
import pandas as pd


# Select CSV to open
file_in = select_file_in()

# Ask for delimination
delimiter = input("Please input Delimiter: ")

# Open CSV
data = open_unknown_csv(file_in, delimiter)

# Get header list
headers = list(data)

# Select URL column
url_list = data[column_selection(headers, "YouTube URL scraping")]

# Specify folder names
outpt_fldr = 'output'

# If output folder doesn't exist, create it.
if not os.path.exists(outpt_fldr):
    print()
    print("Output folder doesn't exist. Create output folder now...")
    os.mkdir(outpt_fldr)
    print()

# Initialize list of dictionaries for stats
stats_dict_list = list()

# Quality list
quality_dict = {'16k': '15360', '8k': '7680', '4k': '3840', '1440P': '2560', '1080P': '1920', '720P': '1280', '480P': '854',
                '360P': '640', '240P': '426'}

# Ask for quality
if y_n_question("Use best quality (y/n): "):
    video_quality_selection = list(quality_dict.keys())[0]
else:
    # Ask for best quality to be used
    video_quality_selection = dict_selection(quality_dict, "Select the maximum video quality to download", "")

# Loop through urls and scrap
for index, url in enumerate(url_list):
    # Try to scrape video
    try:
        # Create video object
        video = pafy.new(url)

        # Get stats
        title = video.title
        views = video.viewcount
        author = video.author
        length = video.length
        likes = video.likes
        dislikes = video.dislikes
        description = video.description

        # Create dict of stats
        stats = dict()
        stats = {'title': title, 'views': views, 'author': author, 'length': length, 'likes': likes,
                 'dislikes': dislikes, 'description': description}

        # Create flag variables for quality finding
        max_quality = False
        quality_found = False

        # Loop through qualities
        for i in quality_dict:
            # If the quality selected is the same as the one in the dictionary, that selected and subsequent values
            # meet the required quality maximum.
            if i == video_quality_selection:
                max_quality = True

            # If quality meets the maximum
            if max_quality:
                # Loop through available video qualities
                for j in video.videostreams:
                    # Find if it matches the selected quality and is a mp4
                    if str(j).find(quality_dict[i]) != -1 and str(j).find('mp4') != -1:
                        # Set quality output as the first found
                        quality_for_title = str(i)

                        # Set video out
                        video_out = j

                        # Set flag to break the next loop
                        quality_found = True
                        break

            # If the highest quality is found, break the dictionary loop
            if quality_found:
                break

        print(title + ": " + str(video_out))

        # Make title
        extension = '.mp4'
        full_title = title + " - " + quality_for_title + extension

        # Download the video
        video_out.download(os.path.join(outpt_fldr, full_title))

        # Append stats to dict list
        stats_dict_list.append(stats)

        # Print Statement of progress
        print("Downloaded " + str(index + 1) + " of " + str(len(url_list)))
        print()
        print()
        print()

    except:
        print('Could not scrape: ' + url)

# Convert stats_dict_list to dataframe
stats_df = pd.DataFrame(stats_dict_list)

# Write stats to a csv
stats_df.to_csv('stats.csv')
