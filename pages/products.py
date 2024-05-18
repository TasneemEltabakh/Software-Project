class Prducts:

    URL='https://badelha.azurewebsites.net/productMain'

    def __init__(self,browser):
        self.browser= browser

    def load(self):
        self.browser.get(self.URL)

    def AddtoCart(self):

#adds an item to the cart 
        pass