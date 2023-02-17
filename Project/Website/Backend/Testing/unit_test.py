import unittest
import sys 
sys.path.append("..")
from Modules.database import *



class Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
    total_elements = 0
        # test case function to check whether we can read a table or not 
    def test_0(self):
        print("Start reading test-1\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        products = read("products","*")
        if(products[0] == 200):
            if(len(products[1]) > 0):
                print("Successfully managed to read from database for products with no filters.")
                self.total_elements = len(products[1])
        print("\nFinish reading test-1\n")

    def test_1(self):
        print("Start reading test-2\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        products = read("productssdsds","*")
        if(products[0] == 400):
            print("The table does not exists as it should be")
        print("\nFinish reading test-2\n")

    def test_2(self):
        print("Start reading test-3\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        products = read("products",["uniqueid"])
        if(products[0] == 200):
            if(len(products[1][0]) == 1):
                print("The table is reading fields that we want as well.")
        print("\nFinish reading test-3\n")
    
    def test_3(self):
        print("Start reading test-4\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        products = read("products","*",{"catid":"3"})
        if(products[0] == 200):
            if(len(products[1]) > 1):
                if(len(products[1][0]) > 1):
                    print("The table is reading based on the condition that we want as well.")
                else:
                    print("There has been an error")
            else:
                print("This error is with reading the table ")
        print("\nFinish reading test-4\n")





if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()