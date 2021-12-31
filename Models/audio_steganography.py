import wave
# from Models import tools
import tools
import traceback

class AudioSteganography:
    """
    Contains functions to implement audio steganography
    """
    def __init__(self):
        pass

    def list_to_bytes(self, frames: list):
        """
        Converts a list of integers into a string of hexadecimals
        """
        print(frames[:50])
        for i in range(len(frames)):
            frames[i] = hex(frames[i])
        
        frames = "".join(frames)

        frames = bytes(frames, encoding = "utf-8")
        # print(frames[:50])
        return frames


    def encode(self, audio: str, sign: str, msg: str, newName: str):
        """
        Encodes signature and a message into an wav audio file and save it on disk.\n
        """
        try:
            if tools.parse_type(audio).lower() not in ("wav"):
                print("Type not supported!")
                return False
            
            f = open(newName+".wav", "x")
            f.close()

            with wave.open(audio, "rb") as obj:
                params = obj.getparams()
                # print(obj.getparams())
                # print(obj.getnframes())
                # print(obj.readframes(50))

                # Check total length
                totalLength = obj.getnframes()//9 - 18
                if totalLength < len(sign) + len(msg) :
                    return False
                print("Total Length : ", totalLength)
                
                bits = tools.merge_bits(sign, msg)
                # print("Message : ", bits)
                frames = list(obj.readframes(obj.getnframes()))
                print(type(obj.readframes(obj.getnframes())))

                offset = 0
                count = 1
                for i in range(len(frames)):
                    # Check for every 9th bit, if msg is left mark the 9th bit as 1 otherwise 0 denoting the end of msg
                    if count == 9:
                        if offset == len(bits):
                            frames[i] = tools.modify_bit(frames[i], 0)
                            break

                        else:
                            frames[i] = tools.modify_bit(frames[i], 1)
                            count = 1

                    else:
                        # print(offset, count)
                        frames[i] = tools.modify_bit(frames[i], bits[offset])
                        offset += 1
                        count += 1
                
            # Store file in directory
            with wave.open(newName+".wav", "wb") as obj:
                obj.setparams(params)
                obj.writeframes(self.list_to_bytes(frames))
            
            return True
                


        except Exception as e:
            # print(e)
            traceback.print_exc()
            return False


    def decode(self):
        pass

a = AudioSteganography()
# a.encode("audioTest/HiHat.wav", "qwe", "qwe", "audioTest/qwe")
a.encode("audioTest/drums.wav", "q", "w", "audioTest/qwe1")
# a.encode("audioTest/Song1.wav", "qwe", "qwe", "audioTest/qwe")