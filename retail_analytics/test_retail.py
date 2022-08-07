import unittest
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import requests



class ApiTest(unittest.TestCase):
    API_URl="http://127.0.0.1:5000"
    SEARCH_URL = "{}/search".format(API_URl)
    UPDATE_URL = "{}/update".format(API_URl)
    DELETE_URL = "{}/delete".format(API_URl)

    def test_search(self):
        response = requests.post(ApiTest.SEARCH_URL,data={'store_id':1,'product_name':'A','sku':'','price':''})
        scode = response.status_code
        self.assertEqual(scode,200)

    def test_search_no_record(self):
        response = requests.post(ApiTest.SEARCH_URL,data={'store_id':10,'product_name':'A','sku':'','price':''})
        scode = response.status_code
        self.assertEqual(scode,200)


    def test_update(self):
        response = requests.post(ApiTest.UPDATE_URL,data={'store_id':2,'product_name':'C','sku':'','price':22})
        scode = response.status_code
        self.assertEqual(scode,200)


    def test_update_no_record(self):
        response = requests.post(ApiTest.UPDATE_URL,data={'store_id':7,'product_name':'A','sku':'','price':542})
        scode = response.status_code
        self.assertEqual(scode,200)



    def test_delete(self):
        response = requests.post(ApiTest.DELETE_URL,data={'store_id':5,'product_name':'I','sku':'','price':''})
        scode = response.status_code
        self.assertEqual(scode,200)


    def test_delete_no_record(self):
        response = requests.post(ApiTest.DELETE_URL,data={'store_id':6,'product_name':'A','sku':'','price':''})
        scode = response.status_code
        self.assertEqual(scode,200)



if __name__ == "__main__":
    unittest.main()
