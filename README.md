# Resume Parser

## Intro

It is a python script to parse information from a cv or resume in pdf. It takes input from a folder `/data` and take
all `pdf` files then apply some hardcoded **rex** and **sudo** algorithms and parse information into a json file
in `/output` folder.

## Features

### Extract

- [x] Predict Name
- [x] Email address
- [x] Phone number
- [x] Linkedin link
- [x] Predict GitHub link
- [x] image

## How To Run

### Pre-requisite

- create dir and keep all resumes (**.pdf**) in `data/` directory
- install required packages :

    - `pip3 install requirements.txt`

### Installation

- commands :

  > python3 simple_resume_parser.py

- output will be saved in `output/` directory and images will be in `output/images/`

  ```json
  [
    {
      "cv": "data/Shifat_SWE.pdf",
      "data": {
        "phone_number": "+8801714986887",
        "email_address": "mhshifat757@gmail.com",
        "name": "Mehedi Hasan Shifat ",
        "github_link": "https://www.github.com/jspw",
        "linkedIn": "linkedin.com/in/mhshifat",
        "images": [],
        "github_repositories": [
          {
            "url": "github.com/jspw",
            "isProfile": true,
            "username": "jspw"
          },
          {
            "url": "github)",
            "isProfile": false,
            "username": ""
          }
        ],
        "metaData": {
          "predictedNames": [
            {
              "name": "I have worked on a resume parser which will extract the information like name, phone",
              "fontSize": 7.998463132003849,
              "algorithm": "Contain name"
            },
            {
              "name": "no, pro\ufb01le pic, email address, github username, linkedin pro\ufb01le, projects links etc for a",
              "fontSize": 7.998463132003849,
              "algorithm": "Contain name"
            },
            {
              "name": "Mehedi Hasan Shifat ",
              "fontSize": 23.081279323782496,
              "algorithm": "1st Paragraph"
            },
            {
              "name": "Mehedi Hasan Shifat ",
              "fontSize": 23.081279323782496,
              "algorithm": "Largest Font"
            }
          ],
          "urls": ["linkedin.com/in/mhshifat", "github.com/jspw", "github)"],
          "phone_number": ["+8801714986887"],
          "email_addresses": ["mhshifat757@gmail.com"]
        }
      }
    }
  ]
  ```
