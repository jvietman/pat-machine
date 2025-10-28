from PIL import Image, ImageOps
import json, glob, shutil, os, time

from gifconvert import *
from vector2 import *

# config
res = vector2(107, 109)

with open("config.json", "r") as f:
    config = json.load(f)
    f.close()

# import resources
anim = []
pats = gifconvert("base.gif", res)
img = Image.open(config["who gets the pats"]).resize((res.x, res.y))
blank = Image.new("RGB", (res.x, res.y), tuple(config["bgcolor"]))
if config["mirror"]:
    img = ImageOps.mirror(img)
frames = []


# methods
def merge(img1, img2, img3, id=0, pos1=vector2(0, 0), pos2=vector2(0, 0)):
    fg = img1.convert("RGBA")
    if config["squish"]:
        mg = img2.resize(
            (
                config["size"][0],
                config["size"][1] + (config["squishsteps"][id] * config["squishyness"]),
            )
        ).convert("RGBA")
    else:
        mg = img2.resize(config["size"][0], config["size"][1]).convert("RGBA")
    bg = img3.convert("RGBA")

    tmppos = (0, 0)
    if config["move"]:
        tmppos = config["movesteps"][id]
    if config["squish"]:
        posone = (
            pos2.x + config["center"][0] + tmppos[0],
            pos2.y
            + config["center"][1]
            + tmppos[1]
            - (config["squishsteps"][id] * config["squishyness"]),
        )
    else:
        posone = (
            pos2.x + config["center"][0] + tmppos[0],
            pos2.y + config["center"][1] + tmppos[1],
        )
    postwo = (pos1.x + config["hand"][0], pos1.y + config["hand"][1])

    bg.paste(mg, posone, mg)
    bg.paste(fg, postwo, fg)

    return bg


# merge all images
for i in range(len(pats)):
    tmp = merge(pats[i], img, blank, id=i, pos1=vector2(0, 0), pos2=vector2(8, 20))
    frames.append(tmp)

# generate gif
frameone = frames[0]
frameone.save(
    "output/" + config["filename"] + ".gif",
    format="GIF",
    append_images=frames,
    save_all=True,
    loop=0,
    duration=config["speed"],
)

# extra export settings
if config["exportresources"] or config["exportconfig"]:
    path = "output/" + config["filename"]

    if os.path.exists(path):
        shutil.rmtree(path)
    if os.path.exists(path + ".zip"):
        os.remove(path + ".zip")
    os.mkdir(path)
    os.mkdir(path + "/resources")
    shutil.copy("output/" + config["filename"] + ".gif", path)

    if config["exportresources"]:
        shutil.copy(config["who gets the pats"], path + "/resources")
        shutil.copy("base.gif", path + "/resources")

    if config["exportconfig"]:
        shutil.copy("config.json", path)

    shutil.make_archive("output/" + config["filename"], "zip", path)
    shutil.rmtree(path)

if config["open when done"]:
    os.system("start output/" + config["filename"] + ".gif")
