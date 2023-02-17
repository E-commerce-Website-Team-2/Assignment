import unittest
import sys 
sys.path.append("..")
from Modules.database import *



class Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
        # test case function to check the Person.set_name function
    def test_0_set_name(self):
        print("Start reading test-1\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        products = read("products","*")
        if(products[0] == 200):
            if(len(products[1]) > 0):
                print("Successfully managed to read from database for products with no filters.")
        print("\nFinish reading test-1\n")





if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()