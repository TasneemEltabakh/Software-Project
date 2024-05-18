

class Cart:

    URL='https://badelha.azurewebsites.net/shop-cart'

    def __init__(self,browser):
        self.browser= browser

    def load(self):
        self.browser.get(self.URL)
        
    def getTotalPrice(self):
        #get total price from page
        return ''

    def getItemsPrice(self):
        return ''
    
    def enterPromoCode(self,Phrase):
        return []