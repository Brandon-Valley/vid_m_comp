from selenium import webdriver


PHANTOM_JS_PATH = 'C:/Users/Brandon/Downloads/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe' ## SET YOU PATH TO phantomjs

print('  Setting up phanomJS browser (needed for some vid duration stuff)...')
driver = webdriver.PhantomJS(PHANTOM_JS_PATH)
# driver.open('https://youtu.be/g05hCckM4G0')
driver.get('https://youtu.be/g05hCckM4G0')
print (driver.current_url)