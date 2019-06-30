import webbrowser


def open_snappa_in_chrome():   
    url = "https://snappa.com/app/graphic/d8334e8f-a11a-467c-a4ca-52fd4f748f26"
#     webbrowser.open_new_tab(url)
    chrome_browser = webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s")
    chrome_browser.open_new_tab(url)
    
    
open_snappa_in_chrome()