from os import path
import unittest
from Models.image_steganography import ImageSteganography
from Models import tools

class Test_1(unittest.TestCase):
    """
    Test cases for image_steganography
    """
    
    def test_encode_decode(self):
        """
        Test for checking the encode and decode functionalities
        """
        # PATH = "C:/Users/bipin/Documents/Prabhat/College/MiniProjects/Steganography application for mp3, mp4, image, document etc/Project/imgTest"
        image1 = "imgTest/1.jpg"
        image2 = "imgTest/2.PNG"
        image3 = "imgTest/3.png"
        image4 = "imgTest/4.jpg"

        fName = "modified"
        ext = "png"
        path = "imgTest"

        image1m = "imgTest/modified.png"
        image2m = "imgTest/modified1.png"
        image3m = "imgTest/modified2.png"
        image4m = "imgTest/modified3.png"
        msg1 = "aZ.$#"*100
        msg2 = "aZ.$#!@*()Az"*1000000
        sign1 = "1#Q@we"
        sign2 = "1#@Qwe"

        i = ImageSteganography()

        self.assertFalse(i.encode(image1, sign1, msg1, tools.get_output_filename(fName, ext, path)))

        i.encode(image2, sign1, msg1, tools.get_output_filename(fName, ext, path))
        # print(i.decode(image2m, sign1))
        self.assertEqual(i.decode(image2m, sign1), msg1)
        self.assertFalse(i.decode(image2m, sign2))
        self.assertFalse(i.encode(image2, sign1, msg2, image2m))

        i.encode(image3, sign1, msg1, tools.get_output_filename(fName, ext, path))
        self.assertEqual(i.decode(image3m, sign1), msg1)
        self.assertFalse(i.decode(image3m, sign2))
        self.assertFalse(i.encode(image3, sign1, msg2, image3m))

        i.encode(image4, sign1, msg1, tools.get_output_filename(fName, ext, path))
        self.assertEqual(i.decode(image4m, sign1), msg1)
        self.assertFalse(i.decode(image4m, sign2))
        self.assertFalse(i.encode(image4, sign1, msg2, image4m))


class Test_2(unittest.TestCase):
    """
    Test cases for tools
    """
    def test_get_output_file_name(self):
        path1 = r"C:\Users\bipin\Documents\Prabhat\College\MiniProjects\Steganography application for mp3, mp4, image, document etc\Project\imgTest\input_images"
        path2 = r"C:\Users\bipin\Documents\Prabhat\College\MiniProjects\Steganography application for mp3, mp4, image, document etc\Project\imgTest\output_images"

        self.assertEqual(tools.get_output_filename("", "jpg", path1), path1+r"\1.jpg")
        self.assertEqual(tools.get_output_filename("1", "jpg", path1), path1+r"\11.jpg")

        self.assertEqual(tools.get_output_filename("mod-", "jpg", path2), path2+r"\mod-1.jpg")

    def test_parse_path(self):
        path1 = r"Desktop\images\MyImages"
        path2 = r"MyImages"

        self.assertEqual(tools.parse_path(path1+"/image1.jpg"), path1)
        self.assertEqual(tools.parse_path(path2+r"/image1.jpg"), path2)
    
    def test_get_binary(self):
        self.assertEqual(tools.get_binary("a"), [0, 1, 1, 0, 0, 0, 0, 1])
        self.assertEqual(tools.get_binary("z"), [0, 1, 1, 1, 1, 0, 1, 0])
        self.assertEqual(tools.get_binary("A"), [0, 1, 0, 0, 0, 0, 0, 1])
        self.assertEqual(tools.get_binary("Z"), [0, 1, 0, 1, 1, 0, 1, 0])
        self.assertEqual(tools.get_binary(" "), [0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(tools.get_binary("~"), [0, 1, 1, 1, 1, 1, 1, 0])
    
    def test_modify_bit(self):
        self.assertEqual(tools.modify_bit(0, 1), 1)
        self.assertEqual(tools.modify_bit(0, 0), 0)
        self.assertEqual(tools.modify_bit(255, 1), 255)
        self.assertEqual(tools.modify_bit(255, 0), 254)


if __name__ == '__main__':
    unittest.main()