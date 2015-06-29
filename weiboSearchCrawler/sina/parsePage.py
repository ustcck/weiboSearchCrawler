__author__ = 'bfy'

def getContent(html):
    needLine = ''
    lines = html.splitlines()
    for line in lines:
        if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct"'):
            needLine = line
            break
    startPos = needLine.find('html":"')
    if startPos != -1:
        content = needLine[startPos + 7: -12].encode('utf-8').decode('unicode_escape').encode('utf-8').replace("\\", "").decode('utf-8')
        return content

    return None

# if search is no result, then return True.
def isThereResult(soup):
    if soup.find('div', class_="pl_noresult"):
        return False
    return True
