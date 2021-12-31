from Models.image_steganography import ImageSteganography
from Models import tools


class controller:
    
    def __init__(self, view):
        self._view = view
        self._connect_signals()

    def _connect_signals(self):
        """
        Assigns functionalities to buttons
        """
        self._view.folder.currentChanged.connect(self._view.get_tab)

        # For encode folder
        self._view.pushButton1.clicked.connect(lambda: self._view.browse_files(self._view.label2, self._view.dragDrop1))
        self._view.comboBox1.currentIndexChanged.connect(lambda: self._view.get_value(self._view.comboBox1))
        self._view.buttonBox1.accepted.connect(self.provide)
        self._view.buttonBox1.rejected.connect(self._view.quit_app)

        # For decode folder
        self._view.comboBox2.currentIndexChanged.connect(lambda: self._view.get_value(self._view.comboBox2))
        self._view.pushButton2.clicked.connect(lambda: self._view.browse_files(self._view.label3, self._view.dragDrop2))
        self._view.buttonBox2.accepted.connect(self.provide)
        self._view.buttonBox2.rejected.connect(self._view.quit_app)
    
    def check_input_encode(self):
        """
        Verifies user input for encoding
        """
        if self._view.fName == "":
            self._view.update_encode_label(104, None, None)
            print("File name cannot be empty")
            return False
        elif self._view.msg == "":
            self._view.update_encode_label(105, None, None)
            print("Message cannot be empty")
            return False
        elif len(self._view.sign) != 6:
            self._view.update_encode_label(103, None, None)
            print("Password must be 6 characters long")
            return False
        return True
    
    def check_input_decode(self):
        """
        Verifies user input for encoding
        """
        if self._view.fName == "":
            print("File name cannot be empty")
            self._view.update_decode_label(104, None)
            return False
        # elif len(self._view.sign) != 6:
        #     print("Password must be 6 characters long")
        #     self._view.update_decode_label(103, None)
        #     return False
        
        return True
    
    def provide(self):
        """
        Provides the functionality that the user demands
        """

        # When tab is set to encode
        if self._view.tab == 0:
            self._view.capture_text(self._view.textEdit1, self._view.textEdit2)
            self.print_all()
            
            if self._view.fType == "Image":

                if self.check_input_encode():
                    i = ImageSteganography()
                    path = tools.parse_path(self._view.fName)
                    filename = tools.get_output_filename("modified", "png", path)
                    res = i.encode(self._view.fName, self._view.sign, self._view.msg, filename)
                    if res:
                        print("File encoded succefully")
                        self._view.update_encode_label(False, filename.split("\\")[-1], path)
                    else:
                        self._view.update_encode_label(201, None, None)
                        print("Couldn't encode file")
                    
                    self._view.init_var(0, "Image")
                    del i
            
            elif self._view.fName == "Audio":
                pass

            elif self._view.fName == "Video":
                pass

            else:
                pass
                
            self._view.hide_label(self._view.label2)
        
        # When tab is set to decode
        else:
            self._view.capture_text(self._view.textEdit3, None)
            self.print_all()

            if self._view.fType == "Image":
                
                if self.check_input_decode():
                    i = ImageSteganography()
                    path = tools.parse_path(self._view.fName)
                    msg = i.decode(self._view.fName, self._view.sign)
                    if msg:
                        print(msg)
                        self._view.update_decode_label(False, msg)
                    else:
                        self._view.update_decode_label(106, None)

                    self._view.init_var(1, "Image")
                    del i
            
            elif self._view.fName == "Audio":
                pass

            elif self._view.fName == "Video":
                pass

            else:
                pass
                
            self._view.hide_label(self._view.label3)

        self._view.clear_all()

    
    def print_all(self):
        print("\n")
        print("tab : ", self._view.tab)
        print("file type : ", self._view.fType)
        print("file name : ", self._view.fName)
        print("message : ", self._view.msg)
        print("signature : ", self._view.sign)
        print("\n")
            