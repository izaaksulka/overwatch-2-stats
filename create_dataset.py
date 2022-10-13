
import os
import sys
import json
sys.path.append('./')
import parse_scorescreen

def parse_all_data_directory(directory, winner_value):
    for file in os.listdir(directory):
        if file.endswith('.png'):
            full_path = os.path.join(directory, file)
            print('parsing: ', full_path, winner_value)

            data_from_screen = parse_scorescreen.parse_screenshot_2k_resolution(full_path)

            print(json.dumps(data_from_screen, indent=4))

def main():
    parse_all_data_directory('./game-data/wins', "team-1")
    parse_all_data_directory('./game-data/losses', "team-2")


if __name__ == '__main__':
    main()
