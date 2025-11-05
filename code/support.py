from pygame import image
from csv import reader
from os import walk

def absolute_path(path):
    return f"C:/Users/soumy/OneDrive/Desktop/IdeaProjects BackUp/Zelda/{path}"

def import_csv_layout(path):
    path = absolute_path(path)
    terrain_map = []
    with open(path) as level_map:
        layout=reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
    
def import_folder(path):
    path = absolute_path(path)
    temp_list=[]
    for _, __, img_files in walk(path):
        for img in img_files:
            complete_path = path+'/'+img
            temp_list.append(image.load(complete_path))
    return temp_list