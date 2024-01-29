import json


class Achievements:
    def __init__(self, folder_path):
        self.achievement_names = [
            "openAchievements",
            "finishRound",
            "buyProperty",
            "buildHouse",
            "getMonopoly",
            "jailBird",
            "sellProperty",
            "finishGame",
            "loseGame",
            "winGame"]
        self.trophy_image_path = folder_path + r"/img/achievement/trophy.png"
        self.grey_trophy_image_path = folder_path + r"/img/achievement/trophy_grey.png"
        self.json_file_path = folder_path + r"/data/achievements.json"

    def get_achievement_data(self):
        # return a list of achievement data, read from the json file
        with open(self.json_file_path) as json_file:
            return json.load(json_file)

    def complete_achievement(self, API_Name):
        # complete the achievement with the given name
        achievement_data = self.get_achievement_data()
        index = self.achievement_names.index(API_Name)
        achievement_data[index]["Completed"] = True
        with open(self.json_file_path, "w") as json_file:
            json.dump(achievement_data, json_file, indent=4)
