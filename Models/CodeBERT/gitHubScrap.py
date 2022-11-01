from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

import pandas as pd

vulnerableList = []
nonVulnerableList = []
commitList = []
dfJava = pd.read_excel('dfJava.xlsx', header=None)
count = 0

for i in range (0,len(dfJava)):
    '''
    if count < 91:
        count += 1
        continue
    if count > 95:
        break
    '''


    count += 1
    print("###################")
    print("count")
    print(count)
    dfJavaLoc = dfJava.iloc[i].tolist()
    fileNameToSend = dfJavaLoc[4]
    print(fileNameToSend)
    commitLink = dfJavaLoc[2]
    print(commitLink)

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # driver.get("https://github.com/rhuss/jolokia/commit/5895d5c137c335e6b473e9dcb9baf748851bbc5f?diff=unified")
    driver.get(commitLink)

    driver.implicitly_wait(20)
    title = driver.title

    '''
    if 'Page not found' in title:
        print(title)
        commitList.append("")
    '''
    files = driver.find_elements(By.CSS_SELECTOR, "#files > div > div.file")
    #print("commit message H")



    if not files:
        print("wrong")
        commitList.append("")
        nonVulnerableList.append("")
        vulnerableList.append("")
        #commitList().append("")
        continue
    try:
        commitMessageH = driver.find_element(By.CSS_SELECTOR, ".commit.full-commit .commit-title").get_attribute("innerText")
    except:
        commitMessageH == ""
    try:
        commitMessageD = driver.find_element(By.CSS_SELECTOR, ".commit.full-commit .commit-desc").get_attribute("innerText")
    except:
        commitMessageD =""
    commitMessage = commitMessageH + commitMessageD

    for n, file in enumerate(files):
        h3 = file.find_elements(By.CSS_SELECTOR, ".file-header > .file-info > span.Truncate > a")
        fileName = h3[0].get_attribute("innerText")
        print(n, fileName)

        fileNameParsed = fileName.rsplit("/")[-1]
        print(fileNameParsed)


        if fileNameParsed == fileNameToSend:

            table_additions = file.find_elements(By.CSS_SELECTOR,
                                                 "table.diff-table > tbody > tr > td.blob-code-addition")
            table_deletions = file.find_elements(By.CSS_SELECTOR,
                                                 "table.diff-table > tbody > tr > td.blob-code-deletion")
            deletions = ""
            additions = ""
            for an, t in enumerate(table_additions):
                code = t.find_element(By.CSS_SELECTOR, "span.blob-code-inner")

                if code.get_attribute("innerText") != "\n":
                    additions += code.get_attribute("innerText") + "\n"


            for an, t in enumerate(table_deletions):
                code = t.find_element(By.CSS_SELECTOR, "span.blob-code-inner")

                if code.get_attribute("innerText") != "\n":
                    deletions += code.get_attribute("innerText") + "\n"

            nonVulnerableList.append(additions)

            vulnerableList.append(deletions)
            commitList.append(commitMessage)

            print("current length")
            print(len(vulnerableList))

            print(len(nonVulnerableList))
            break

        else:
            continue
    '''
    if count == 10:
        break
    '''

    if count%50 == 0:
        print("intermediate check")
        print(len(vulnerableList))
        print(vulnerableList)
        print(len(nonVulnerableList))
        print(nonVulnerableList)
        print(len(commitList))
        print(commitList)
        print("intermediate check end")

print(count)

print(len(vulnerableList))
print(vulnerableList)
print(len(nonVulnerableList))
print(nonVulnerableList)
print(len(commitList))
print(commitList)