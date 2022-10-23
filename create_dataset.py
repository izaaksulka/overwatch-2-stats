import os
import sys
import json

sys.path.append('./')
import parse_scorescreen
import pandas

WIN_DIRECTORY = './game-data/wins'
LOSE_DIRECTORY = './game-data/losses'


def parse_all_data_in_directory(directory, winner_value):
    game_data = []
    for file in os.listdir(directory):
        if file.endswith('.png'):
            full_path = os.path.join(directory, file)
            print('parsing: ', full_path, winner_value)

            data_from_screen = parse_scorescreen.parse_screenshot_2k_resolution(full_path)
            data_from_screen['winner'] = winner_value

            print(json.dumps(data_from_screen, indent=4))
            game_data.append(data_from_screen)
    return game_data


"""
    The game data is in a dictionary with more dictionaries nested inside it.  pandas will want
    it to be flat to make a dataframe, so this flattens the dictionaries.
"""


def flatten_game_data(game_data):
    flat_dict = {}

    def flatten(root, name):
        if not type(root) is dict:
            flat_dict[name] = root
        else:
            for key in root:
                flatten(root[key], name + '_' + key)

    flatten(game_data, "")
    return flat_dict


def main():
    all_games = []
    all_games += parse_all_data_in_directory(WIN_DIRECTORY, "team-1")
    all_games += parse_all_data_in_directory(LOSE_DIRECTORY, "team-2")
    # all_games += parse_all_data_in_directory('example-data', 'team-1')

    for i in range(len(all_games)):
        all_games[i] = flatten_game_data(all_games[i])

    df = pandas.DataFrame(all_games)
    print(df)
    df.to_csv('output.csv')


if __name__ == '__main__':
    main()
