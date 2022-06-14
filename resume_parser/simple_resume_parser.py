from pdfminer.high_level import extract_pages
from pdfminer.layout import LTFigure, LTTextContainer, LTChar, LTLine, LAParams, LTImage
import os
import glob
import re
import json
from datetime import datetime
from binascii import b2a_hex


# files = [file for file in glob.glob("data/new_sample/*.pdf")]
# files = [file for file in glob.glob("data/sample/*.pdf")]
# files = [file for file in glob.glob("data/dsi/*.pdf")]
files = [file for file in glob.glob("data/*.pdf")]

all_users = []


def isEmailAddress(str):
    if(re.fullmatch(email_regex, text)):
        return True
    return False


def isPhoneNumber(str):
    if(len(str) >= 11 and len(str) <= 14 and re.fullmatch(phoneNo_rex, str.replace(" ", '').replace("+", '').replace("-", "").replace("(", "").replace(")", ""))):
        return True
    return False


def write_file(folder, filename, filedata, flags='w'):
    """Write the file data to the folder and filename combination
    (flags: 'w' for write text, 'wb' for write binary, use 'a' instead of 'w' for append)"""
    result = False
    if os.path.isdir(folder):
        try:
            file_obj = open(os.path.join(folder, filename), flags)
            file_obj.write(filedata)
            file_obj.close()
            result = True
        except IOError:
            pass
    return result


def determine_image_type(stream_first_4_bytes):
    """Find out the image file type based on the magic number comparison of the first 4 (or 2) bytes"""
    file_type = None
    bytes_as_hex = str(b2a_hex(stream_first_4_bytes))
    print(bytes_as_hex)
    if 'ffd8' in bytes_as_hex:
        file_type = '.jpeg'
    elif bytes_as_hex == '89504e47':
        file_type = '.png'
    elif bytes_as_hex == '47494638':
        file_type = '.gif'
    elif bytes_as_hex.startswith('424d'):
        file_type = '.bmp'

    return file_type


def save_image(lt_image):
    """Try to save the image data from this LTImage object, and return the file name, if successful"""
    result = None
    if lt_image.stream:
        file_stream = lt_image.stream.get_rawdata()
        if file_stream:
            file_ext = determine_image_type(file_stream[0:4])
            if file_ext:
                file_name = ''.join(
                    [lt_image.name, "_", str(datetime.now().utcnow()), file_ext])
                if write_file("output/images", file_name, file_stream, flags='wb'):
                    result = file_name
            else:
                print("Unable to read file type!")
    return result


def extractGithubInfo(url):
    # TODO : extract "st3inum.github.io"
    brand = "github.com/"
    github_username = ""
    pos = url.find(brand)
    starting_pos = pos + len(brand)
    ending_pos = url.find("/", starting_pos)
    # print(starting_pos, ending_pos)
    if(ending_pos == -1):
        github_username = url[starting_pos:]

    else:
        github_username = url[starting_pos:ending_pos]

    # print(url, " => ", github_username)
    # print(starting_pos + len(github_username), len(url))
    return {
        "url": url,
        "isProfile": True if(starting_pos + len(github_username) == len(url)) else False,
        "username": github_username.lower()
    }


def predictGithubUserNameFromRepositoryUrl(githubLinks):
    githubInfo = []
    print(githubLinks)
    for githubLink in githubLinks:
        pos = next((index for (index, d) in enumerate(
            githubInfo) if d["username"] == githubLink["username"]), None)
        if(pos != None):
            githubInfo[pos].update({
                "username": githubLink["username"],
                "count": githubInfo[pos].get("count") + 1
            })

        else:
            githubInfo.append({
                "username": githubLink["username"],
                "count": 1
            })
    if(len(githubInfo) > 0):
        maxCountedUsername = max(githubInfo, key=lambda x: x['count'])
        minCountedUsername = min(githubInfo, key=lambda x: x['count'])
        # print(maxCountedUsername)
        return maxCountedUsername["username"]
    return "Unable to find"


def getOriginalNameFromNameField(name):
    str = "name"
    index = name.lower().find(str) + len(str)
    after_removing_name = name[index: -1]
    after_removing_name = after_removing_name[index: -1]
    return " ".join(after_removing_name.split())


def predictName(listOfNames, githubUsername):
    first = 0
    largest = 0

    first = next((index for (index, d) in enumerate(
        listOfNames) if d["algorithm"] == "1st Paragraph"), None)
    largest = next((index for (index, d) in enumerate(
        listOfNames) if d["algorithm"] == "Largest Font"), None)

    if(listOfNames[first]["name"] == listOfNames[largest]["name"]):
        return listOfNames[first]["name"]

    nameContainer = next((index for (index, d) in enumerate(
        listOfNames) if d["algorithm"] == "Contain name"), None)
    if(nameContainer != None):
        # TODO :  check if name is a field not a substring of word
        predictedName = getOriginalNameFromNameField(
            listOfNames[nameContainer]["name"])

        if(len(predictedName) < 20):
            print(len(predictedName) < 20)
            return predictedName

    if(githubUsername.lower() in listOfNames[first]["name"]):
        return listOfNames[first]["name"]
    if(githubUsername.lower() in listOfNames[largest]["name"]):
        return listOfNames[largest]["name"]
    # TODO : more validation to be done like github / linkedin

    return listOfNames[largest]["name"]


for cv in files:

    print("\n\n\t\t" + cv + "\n")

    Extract_Data = []
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phoneNo_rex = '^[0-9]*$'
    userInfo = {
        "phone_number": '',
        "email_address": "",
        "name": '',
        "github_link": '',
        "linkedIn": "",
        "images": [],
        "github_repositories": [],
        "metaData": {}

    }

    predictedNames = []
    urls = []
    phone_number = []
    email_addresses = []

    print(extract_pages(cv))

    for page_layout in extract_pages(cv):

        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if(str(type(text_line)) ==
                       "<class 'pdfminer.layout.LTTextLineHorizontal'>"):
                        for character in text_line:
                            if isinstance(character, LTChar):
                                Font_size = character.size

                        if(len(text_line.get_text().replace(" ", '').replace("\n", "").replace("\ue732", '').replace("\uf0b7", '').replace("\t", "")) > 0):
                            print(text_line)
                            Extract_Data.append(
                                [Font_size, (text_line.get_text())])

                            if("name" in text_line.get_text().lower()):

                                predictedNames.append({
                                    "name": text_line.get_text().replace("\n", ''),
                                    'fontSize': Font_size,
                                    "algorithm": "Contain name"
                                })
                for text in element.get_text().split():
                    if(isEmailAddress(text)):
                        email_addresses.append(text)
                        if(userInfo["email_address"] == ''):
                            userInfo["email_address"] = text
                    elif("linkedin" in text and len(text) > len("linkedin")):
                        urls.append(text)
                        if(userInfo["linkedIn"] == ""):
                            userInfo["linkedIn"] = text

                    elif("github" in text and len(text) > len("github")):
                        githubLink = extractGithubInfo(text)
                        urls.append(text)
                        # print(githubLink, "\n")
                        if(githubLink["isProfile"] == True and userInfo["github_link"] != ''):
                            userInfo["github_link"] = "https://www.github.com/" + \
                                githubLink["username"]
                        else:
                            userInfo["github_repositories"].append(
                                extractGithubInfo(text))

                    else:
                        for word in text.split(","):
                            if(isPhoneNumber(word)):
                                phone_number.append(word)
                                if(userInfo["phone_number"] == ""):
                                    userInfo["phone_number"] = word
            elif isinstance(element, LTFigure):
                for imageLTT in element:
                    if isinstance(imageLTT, LTImage):
                        image = save_image(imageLTT)
                        if(image != None):
                            userInfo["images"].append(image)

    # for data in Extract_Data:
    #     print(data)

    if(len(Extract_Data) > 0):

        predictedNames.append({
            "name": (Extract_Data[0][1]).replace("\n", '') if Extract_Data[0][1] != None else "NAN",
            'fontSize': Extract_Data[0][0],
            "algorithm": "1st Paragraph",

        })
        Extract_Data.sort(key=lambda x: x[0], reverse=True)
        predictedNames.append({
            "name": (Extract_Data[0][1]).replace("\n", ''),
            'fontSize': Extract_Data[0][0],
            "algorithm": "Largest Font"
        })
        if(userInfo["github_link"] == ''):
            userInfo["github_link"] = "https://www.github.com/" + \
                predictGithubUserNameFromRepositoryUrl(
                    userInfo["github_repositories"])
        userInfo["name"] = predictName(
            predictedNames, userInfo["github_link"])

    userInfo["metaData"] = {
        "predictedNames": predictedNames,
        "urls": urls,
        "phone_number": phone_number,
        "email_addresses": email_addresses,
        # "extracted_data": Extract_Data
    }
    print(userInfo)

    all_users.append({"cv":  cv, "data":  userInfo})

with open("output/dsi" + ".json", "w") as outfile:
    json.dump(all_users, outfile)
