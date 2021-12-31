import os

"""
Contains usefull functions like finding the next name for a file etc.
"""

def get_output_filename(fileName : str, extension : str, path : str) -> str:
    """
    Takes file name, the extension (without dot) and an absolute path\n
    Returns the next valid file name.
    """

    try:
        post = 1
        for dirpath, dirname, filename in os.walk(path):
            for name in filename:
                
                if name[:len(fileName)] == fileName and name.split(".")[-1] == extension:
                    try:
                        post = max(post, int(name[len(fileName):len(name)-len(extension)-1]) + 1)
                    except:
                        pass
        validFileName = path+ "\\" +fileName + str(post) + "." + extension
        # print(f"Valid FileName found : {validFileName}\n")
                        
        return validFileName
    except Exception as e:
        print(e)
        return False


def get_binary(character: str) -> list:
    """
    Returns the list for a letter in binary representation
    """
    return list(map(int, list(format(ord(character), '08b'))))


def bin_to_chr(binList: list) -> str:
    """
    Converts 8 bit binary number to its corresponding ASCII character
    """
    words = []

    binList = list(map(lambda x: str(x), binList))
    for i in range(0, len(binList), 8):
        words.append(chr(int("".join(binList[i:i+8]), 2)))
    
    return "".join(words)


def merge_bits(sign: str, msg: str) -> list:
    """
    Merges sign and msg bits into a single list
    """
    bits = []

    for letter in sign:
        bits.extend(get_binary(letter))

    for letter in msg:
        bits.extend(get_binary(letter))
    
    return bits


def modify_bit(value: int, parity: bool) -> int:
    """
    Returns the modified value according to the parity.\n
    If parity = 0 ie even, the value returned will be the closest accepted even value passed
    to the function 
    """
    if parity == 0:
        if value % 2 == 0:
            return value
        else:
            return value-1
    elif parity == 1:
        if value % 2 != 0:
            return value
        else:
            return value+1


def parse_type(fileName):
    """
    Returns the file type from string
    """
    return fileName.split(".")[-1]


def parse_path(fileName):
    """
    Returns the file path from string
    """
    pathList = fileName.split("/")
    del pathList[-1]

    pathStr = "\\".join(pathList)

    return pathStr

def parse_name(fileName):
    """
    Returns the file name from full path
    """
    pathList = fileName.split("/")
    name = pathList[-1]

    return name