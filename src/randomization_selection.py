import random
import os


class RandomizationSelection():
    def __init__(self):
        pass

    def selection(self, object_name):
        place_name_list = ["living", "bedroom", "kitchen", "bathroom"]
        random.shuffle(place_name_list)
        print(place_name_list)
        self.save_data(object_name, place_name_list)
        return

    def save_data(self, object_name, place_name_list):
        # 推論結果をtxtでまとめて保存
        FilePath = "/root/HSR/catkin_ws/src/spco2_boo_problog/data/" + str(object_name)
        if not os.path.exists(FilePath):
            os.makedirs(FilePath)

        with open(FilePath + "/inference_result.txt", "w") as f:
            f.write("Result of place order:\n")
            f.write("{}\n".format(place_name_list))
            f.close()


if __name__ == '__main__':
    select = RandomizationSelection()
    select.selection()

