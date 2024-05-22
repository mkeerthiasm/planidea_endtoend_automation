import os
import time
import pytest
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager 
driver = None # This is a global variable


@pytest.fixture(autouse=True) # This fixture will run before every test case

def setup(request, browser, url):
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://planidea.netlify.app/")
    driver.maximize_window()
    yield # This will run after every test case
    driver.quit()

def pytest_addoption(parser): # This will get the value from CLI
    parser.addoption("--browser", action="store", default="chrome") # This will get the browser name from CLI
    parser.addoption("--url", action="store", default="https://planidea.netlify.app/") # This will get the URL from CLI 

def pytest_generate_tests(metafunc):
    if 'browser' in metafunc.fixturenames: 
        metafunc.parametrize("browser", [metafunc.config.getoption('browser')])
    if 'url' in metafunc.fixturenames: 
        metafunc.parametrize("url", [metafunc.config.getoption('url')])     

@pytest.fixture(scope= 'class', autouse=True) # This fixture will run before the class

def browser(request): # This fixture will return the browser name   
    return request.config.getoption("--browser")

@pytest.fixture(scope= 'class', autouse=True) # This fixture will run before the class

def url(request): # This fixture will return the URL
    return request.config.getoption("--url") 

@pytest.hookimpl(hookwrapper=True)  
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html') #
    outcome = yield  # Run all other pytest_runtest_makereport non wrapped hooks
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep) 
    extra = getattr(item, "extra", []) 

    if rep.when == "call":
        extra.append(pytest_html.extras.url("https://planidea.netlify.app/")) # This will add the URL in the HTML report
        xfail = hasattr(rep, "wasxfail") # This will check if the test case is xfailed
        if rep.failed and not xfail:
            report_directory = os.path.dirname(item.config.option.htmlpath) # This will get the directory of the report
            file_name = os.path.basename(item.config.option.htmlpath) # This will get the name of the report    
            screenshot_name = file_name.replace(".html", ".png")
            destinationFile = os.path.join(report_directory, screenshot_name) # This will create the path of the screenshot
            driver.save_screenshot(destinationFile)

            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name # This will add the screenshot in the HTML report
                link = screenshot_name
                extra.append(pytest_html.extras.url(link))
    report = item.config.pluginmanager.getplugin('html').pytest_report_teststatus(item, call) # This will add the status of the test case in the HTML report
    report.extra = extra

def pytest_html_report_title(report):
    report.title = "PlanIdea Test Report" # This will add the title in the HTML report  