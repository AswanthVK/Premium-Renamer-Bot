async def fix_ext(newname, realname):
    if not "." in newname and "." in realname:
        extention = realname.rsplit(".", 1)[1]
        if len(extention) in range(2,6):
            newname = f"{newname[:62 - len(extention)]}.{extention}"
        else:
            newname = f"{newname[:59]}.mp4"

    elif "." in newname and "." in realname:
        extention = newname.rsplit(".", 1)
        old_ext = realname.rsplit(".", 1)[1]
        if len(extention[1]) not in range(2,6) and len(old_ext) in range(2,6):
            newname = f"{newname[:62-len(old_ext)]}.{old_ext}"
        elif len(extention[1]) in range(2,6):
            newname = f"{extention[0][:62-len(extention[1])]}.{extention[1]}"
        else:
            newname = f"{newname[:59]}.mp4"

    else:
        newname = f"{newname[:59]}.mp4"

    newname = newname.replace('/', ' ').replace('#', ' ').replace('\n', ' ')
    return newname
