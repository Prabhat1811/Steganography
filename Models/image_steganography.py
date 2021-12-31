import cv2
import traceback
from Models import tools

class ImageSteganography:
    """
    Contains functions to implement image steganography
    """
    def __init__(self):
        pass
    
    # def get_binary(self, character: str) -> list:
    #     """
    #     Returns the list for a letter in binary representation
    #     """
    #     return list(map(int, list(format(ord(character), '08b'))))
    
    # def modify_bit(self, value: int, parity: bool) -> int:
    #     """
    #     Returns the modified value according to the parity.\n
    #     If parity = 0 ie even, the value returned will be the closest accepted even value passed
    #     to the function 
    #     """
    #     if parity == 0:
    #         if value % 2 == 0:
    #             return value
    #         else:
    #             return value-1
    #     elif parity == 1:
    #         if value % 2 != 0:
    #             return value
    #         else:
    #             return value+1
    
    # def merge_bits(self, sign: str, msg: str) -> list:
    #     """
    #     Merges sign and msg bits into a single list
    #     """
    #     bits = []

    #     for letter in sign:
    #         bits.extend(tools.get_binary(letter))

    #     for letter in msg:
    #         bits.extend(tools.get_binary(letter))
        
    #     return bits

    def encode(self, image: str, sign: str, msg: str, newName: str) -> list:
        """
        Encodes signature and a message into an image file and save it on disk.\n
        Uses Least significant bit algorithm to encode text on file.\n
        Accepts only .jpg .jpeg .png formats
        """
        try:
            if tools.parse_type(image).lower() not in ("jpg", "jpeg", "png"):
                print("Type not supported!")
                return False

            image = cv2.imread(image)

            # Check if given data is of appropriate length
            totalLength = len(image) * len(image[0]) // 3

            if totalLength < len(msg) + len(sign):
                return False
            
            bits = tools.merge_bits(sign, msg)
            offset = 0
            count = 0

            loop = True
            for row in range(len(image)):
                if not loop:
                    break

                for pixel in range(len(image[row])):
                    if not loop:
                        break
                    count += 1

                    # Check for every third pixel, modifies lsb of last color as 0 if end of message
                    if count == 3:
                        for i in range(2):
                            image[row][pixel][i] = tools.modify_bit(image[row][pixel][i], bits[offset])
                            offset += 1
                        
                        if offset == len(bits):
                            image[row][pixel][2] = tools.modify_bit(image[row][pixel][2], 0)
                            loop = False
                            break
                        else:
                            image[row][pixel][2] = tools.modify_bit(image[row][pixel][2], 1)
                        count = 0

                    # Every non third pixel
                    else:
                        for i in range(3):
                            image[row][pixel][i] = tools.modify_bit(image[row][pixel][i], bits[offset])
                            offset += 1

            # print(image)
            cv2.imwrite(newName, image)
            return True
        
        except Exception as e:
            # print(e2)
            traceback.print_exc()
            return False

    # def bin_to_chr(self, binList: list) -> str:
    #     """
    #     Converts 8 bit binary number to its corresponding ASCII character
    #     """
    #     words = []

    #     binList = list(map(lambda x: str(x), binList))
    #     for i in range(0, len(binList), 8):
    #         words.append(chr(int("".join(binList[i:i+8]), 2)))
        
    #     return "".join(words)

    def decode(self, image: str, sign: str) -> list:
        """
        Decodes the message from an image with the help of the signature.\n
        Accepts only .jpg .jpeg .png formats
        """
        try:
            if tools.parse_type(image).lower() != "png":
                print("Type not supported!")
                return False
            image = cv2.imread(image)
            # print(image)

            bits = []
            count = 0

            loop = True
            for row in image:
                if not loop:
                    break

                for pixel in row:
                    if not loop:
                        break
                    count += 1

                    # Check for every third pixel, modifies lsb of last color as 0 if end of message
                    if count == 3:
                        # print(pixel)
                        for i in range(2):
                            bits.append(pixel[i]%2)
                        if pixel[2] %2 == 0:
                            loop = False
                            break
                        count = 0

                    # Every non third pixel
                    else:
                        for i in range(3):
                            bits.append(pixel[i]%2)
            
            decodedMsg = tools.bin_to_chr(bits)
            dSign = decodedMsg[:6]
            dMsg = decodedMsg[6:]

            if dSign == sign:
                return dMsg

            return False
        
        except Exception as e:
            traceback.print_exc()
            return False
