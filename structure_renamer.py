# coding=utf-8
import os
import shutil

ROOT_PATH = "/mnt/wd/ZJUT/release/CDEHP/indoor"
EVENT_WIDTH = 1280
EVENT_HEIGHT = 800
ALLOW_DIRS = ["color_image", "depth_raw", "event_image", "color_label", "event_label"]


def extract_time_dir():
    for data_set in os.listdir(ROOT_PATH):
        set_path = os.path.join(ROOT_PATH, data_set)
        for action_person_pair in os.listdir(set_path):
            action_person_pair_path = os.path.join(set_path, action_person_pair)
            times_list = os.listdir(action_person_pair_path)
            assert len(times_list) == 1
            old_path = os.path.join(action_person_pair_path, times_list[0])
            new_path = "{}{}".format(action_person_pair_path, times_list[0])
            print("{} -> {}".format(old_path, new_path))
            shutil.move(old_path, new_path)

            times_list = os.listdir(action_person_pair_path)
            assert len(times_list) == 0
            os.rmdir(action_person_pair_path)


def rename_sub_dir():
    for data_set in os.listdir(ROOT_PATH):
        set_path = os.path.join(ROOT_PATH, data_set)
        for sub in os.listdir(set_path):
            sub_path = os.path.join(set_path, sub)
            dirs = os.listdir(sub_path)
            assert len(dirs) == 9
            assert "color" in dirs
            assert "depth_raw" in dirs
            assert "event" in dirs
            assert "image_event_binary" in dirs
            assert "label_color" in dirs
            assert "label_color_fill" in dirs
            assert "label_event" in dirs
            assert "label_event_fill" in dirs
            assert "vector_event_binary" in dirs

            shutil.move(os.path.join(sub_path, "color"), os.path.join(sub_path, "color_image"))
            # shutil.move(os.path.join(sub_path, "depth_raw"), os.path.join(sub_path, "depth_raw"))
            shutil.move(os.path.join(sub_path, "event"), os.path.join(sub_path, "event_raw"))
            shutil.move(os.path.join(sub_path, "image_event_binary"), os.path.join(sub_path, "event_image"))
            shutil.move(os.path.join(sub_path, "label_color"), os.path.join(sub_path, "color_label_before_verify"))
            shutil.move(os.path.join(sub_path, "label_color_fill"), os.path.join(sub_path, "color_label"))
            shutil.move(os.path.join(sub_path, "label_event"), os.path.join(sub_path, "event_label_before_verify"))
            shutil.move(os.path.join(sub_path, "label_event_fill"), os.path.join(sub_path, "event_label_before_unify"))
            shutil.move(os.path.join(sub_path, "vector_event_binary"), os.path.join(sub_path, "event_point_cloud"))

            print("{} done".format(sub_path))


def count_color_images():
    color_image_count = 0
    event_image_count = 0
    for data_set in os.listdir(ROOT_PATH):
        if data_set == "valid":
            continue
        set_path = os.path.join(ROOT_PATH, data_set)
        for sub in os.listdir(set_path):
            sub_path = os.path.join(set_path, sub)
            color_image_count += len(os.listdir(os.path.join(sub_path, "color_image")))
            event_image_count += len(os.listdir(os.path.join(sub_path, "event_image")))
            print("{} done".format(sub_path))
    print("{} color images in {}".format(color_image_count, ROOT_PATH))
    print("{} event images in {}".format(event_image_count, ROOT_PATH))


def unify_event_label():
    for data_set in os.listdir(ROOT_PATH):
        set_path = os.path.join(ROOT_PATH, data_set)
        for sub in os.listdir(set_path):
            sub_path = os.path.join(set_path, sub)
            old_path = os.path.join(sub_path, "event_label_before_unify")
            new_path = os.path.join(sub_path, "event_label")
            os.mkdir(new_path)
            for file in os.listdir(old_path):
                old_file = os.path.join(old_path, file)
                new_file = os.path.join(new_path, file)
                with open(old_file, "r") as f:
                    data = f.readlines()
                if len(data) != 15:
                    print("{} length={}", old_file, len(data))
                assert len(data) == 15
                assert data[0] == "13\n"
                assert data[1].startswith("color_name:")
                for i in range(2, 15):
                    coordinates = data[i].split(" ")
                    assert coordinates[0][0] == "["
                    assert coordinates[0][len(coordinates[0]) - 1] == "]"
                    assert coordinates[1][0] == "["
                    assert coordinates[1][len(coordinates[1]) - 2] == "]"
                    assert coordinates[1][len(coordinates[1]) - 1] == "\n"
                    # print("{} {}".format(coordinates[0], coordinates[1]), end="")
                    coordinates[0] = coordinates[0][1:len(coordinates[0]) - 1]
                    coordinates[1] = coordinates[1][1:len(coordinates[1]) - 2]
                    # print("{} {}".format(coordinates[0], coordinates[1]))
                    x = float(coordinates[0])
                    y = float(coordinates[1])
                    x = x / EVENT_WIDTH
                    y = y / EVENT_HEIGHT
                    # print("{} {}".format(x, y))
                    data[i] = "{} {}\n".format(x, y)
                with open(new_file, "w") as f:
                    f.writelines(data)
            print("{} done".format(sub_path))


def generate_include_list():
    cdehp_path = os.path.abspath(os.path.join(ROOT_PATH, "..", ".."))
    file_name = os.path.join(cdehp_path, "includes.txt")
    result = []
    for root, dirs, files in os.walk(ROOT_PATH):
        for dir in dirs:
            if dir in ALLOW_DIRS:
                relative_path = os.path.join(root, dir).replace(cdehp_path, ".")
                result.append("{}/*\n".format(relative_path))
    result.sort()
    with open(file_name, "w") as f:
        f.writelines(result)


if __name__ == "__main__":
    # extract_time_dir()
    # rename_sub_dir()
    count_color_images()
    # unify_event_label()
    # generate_include_list()
