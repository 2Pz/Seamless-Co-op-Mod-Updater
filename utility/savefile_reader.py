import os

def l_endian(val):
    l_hex = bytearray(val)
    l_hex.reverse()
    str_l = "".join(format(i, "02x") for i in l_hex)
    return int(str_l, 16)

def get_names(file):
    with open(file, "rb") as fh:
        dat1 = fh.read()

    hex_locations = [
        0x1901d0e,
        0x1901f5a,
        0x19021a6,
        0x19023f2,
        0x190263e,
        0x190288a,
        0x1902ad6,
        0x1902d22,
        0x1902f6e,
        0x19031ba
    ]
    names = []
    for idx in hex_locations:
        try:
            name = dat1[idx:idx+32].decode('utf-16')
            name = name.split('\x00')[0]
            names.append(name if name else None)
        except UnicodeDecodeError:
            names.append(None)

    return names

def get_levels(file):
    with open(file, "rb") as fh:
        dat = fh.read()

    ind = 0x1901D0E + 34
    lvls = []
    for i in range(10):
        l = dat[ind : ind + 2]
        lvls.append(l_endian(l))
        ind += 588
    return lvls

def get_slot_ls(file):
    with open(file, "rb") as fh:
        dat = fh.read()

        slot1 = dat[0x00000310 : 0x0028030F + 1]  # SLOT 1
        slot2 = dat[0x00280320 : 0x050031F + 1]
        slot3 = dat[0x500330 : 0x78032F + 1]
        slot4 = dat[0x780340 : 0xA0033F + 1]
        slot5 = dat[0xA00350 : 0xC8034F + 1]
        slot6 = dat[0xC80360 : 0xF0035F + 1]
        slot7 = dat[0xF00370 : 0x118036F + 1]
        slot8 = dat[0x1180380 : 0x140037F + 1]
        slot9 = dat[0x1400390 : 0x168038F + 1]
        slot10 = dat[0x16803A0 : 0x190039F + 1]
        return [slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10]
    
def get_stats(file, char_slot):
    lvls = get_levels(file)  
    lv = lvls[char_slot - 1]  
    slots = get_slot_ls(file)  

    start_ind = 0
    slot1 = slots[char_slot - 1]  
    indexes = []  

    for ind, b in enumerate(slot1):
        if ind > 120000:
            return None

        try:
            stats = [
                l_endian(slot1[ind : ind + 1]),
                l_endian(slot1[ind + 4 : ind + 5]),
                l_endian(slot1[ind + 8 : ind + 9]),
                l_endian(slot1[ind + 12 : ind + 13]),
                l_endian(slot1[ind + 16 : ind + 17]),
                l_endian(slot1[ind + 20 : ind + 21]),
                l_endian(slot1[ind + 24 : ind + 25]),
                l_endian(slot1[ind + 28 : ind + 29]),
            ]

            if sum(stats) == lv + 79 and l_endian(slot1[ind + 44 : ind + 46]) == lv:
                start_ind = ind
                lvl_ind = ind + 44
                break

        except:
            continue

    if start_ind == 0:
        return None

    stats_dict = {
        "Vigor": l_endian(slot1[start_ind : start_ind + 1]),
        "Mind": l_endian(slot1[start_ind + 4 : start_ind + 5]),
        "Endurance": l_endian(slot1[start_ind + 8 : start_ind + 9]),
        "Strength": l_endian(slot1[start_ind + 12 : start_ind + 13]),
        "Dexterity": l_endian(slot1[start_ind + 16 : start_ind + 17]),
        "Intelligence": l_endian(slot1[start_ind + 20 : start_ind + 21]),
        "Faith": l_endian(slot1[start_ind + 24 : start_ind + 25]),
        "Arcane": l_endian(slot1[start_ind + 28 : start_ind + 29])
    }

    return stats_dict

def get_id(file):
    with open(file, "rb") as f:
        dat = f.read()
        f.seek(26215348)  
        steam_id = f.read(8)  
    return l_endian(steam_id)

def read_save_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    names = get_names(file_path)
    levels = get_levels(file_path)
    ids = get_id(file_path)

    character_info = []

    for i, (name, level) in enumerate(zip(names, levels), 1):
        if name:
            stats = get_stats(file_path, i)
            if stats:
                character_info.append({
                    "slot": i,
                    "name": name,
                    "level": level,
                    "stats": stats,
                    "id": str(ids)
                })

    return character_info

def find_save_file(folder_path):
    co2_path = os.path.join(folder_path, "ER0000.co2")
    sl2_path = os.path.join(folder_path, "ER0000.sl2")
    
    if os.path.exists(co2_path):
        return co2_path
    elif os.path.exists(sl2_path):
        return sl2_path
    else:
        return None

def get_save_folders():
    appdata_path = os.path.join(os.environ['APPDATA'], 'EldenRing')
    if os.path.exists(appdata_path):
        return [f for f in os.listdir(appdata_path) if os.path.isdir(os.path.join(appdata_path, f))]
    return []
