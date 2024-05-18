import pytest
import selenium.webdriver

@pytest.fixture
def browser():

    cart= selenium.webdriver.Edge()

    cart.implicitly_wait(10)

    yield cart

    cart.quit()