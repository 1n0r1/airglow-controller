


def write_config(azi, zeni):
   
    file1 = open('/home/airglow/airglow/airglow-controller/config.py', 'r')
    Lines = file1.readlines()
    for idx, line in enumerate(Lines):
        if ("'azi_offset'" in line):
            key, val = line.split(":")
            Lines[idx] = key + ': ' + str(azi) + ',\n'
        elif ("'zeni_offset'" in line):
            key, val = line.split(":")
            Lines[idx] = key + ': ' + str(zeni) + ',\n'      
    file1.close()

    file2 = open('/home/airglow/airglow/airglow-controller/configScripts/tempConfig.py', 'w')
    file2.writelines(Lines)
    file2.close()