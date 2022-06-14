# Resume Parser

It is a python script to parse information from a cv or resume in pdf.

## Features

### Extract

- [x] Predict Name
- [x] Email address
- [x] Phone number
- [x] Linkedin link
- [x] Predict Github link
- [x] image

## How To Run

### Pre-requisite

- store resumes (**.pdf**) in `data/` directory
- install required packages :

  - `pip3 install requirements.txt`

### Installation

- commands :

  > cd resume_parser

  > python3 simple_resume_parser.py

- output will be saved in `output/` directory and images will be in `output/images/`

```json
[
  {
    "cv": "data/2017831017.pdf",
    "data": {
      "phone_number": "+8801714986887",
      "email_address": "mhshifat757@gmail.com",
      "name": "Mehedi Hasan",
      "github_link": "https://www.github.com/jspw",
      "linkedIn": "linkedin.com/in/mhshifat",
      "images": ["Im7_2022-01-05 08:09:49.933569.jpeg"],
      "github_repositories": [
        {
          "url": "github.com/jspw",
          "isProfile": true,
          "username": "jspw"
        },
        {
          "url": "https://github.com/jspw/Paper",
          "isProfile": false,
          "username": "jspw"
        },
        {
          "url": "https://github.com/jspw/cp-tool",
          "isProfile": false,
          "username": "jspw"
        },
        {
          "url": "https://github.com/jspw/Ubuntu-Launcher",
          "isProfile": false,
          "username": "jspw"
        },
        {
          "url": "https://github.com/jspw/HackTheVerse_SUST_Tetrahedron",
          "isProfile": false,
          "username": "jspw"
        },
        {
          "url": "https://github.com/jspw/CodeNerd",
          "isProfile": false,
          "username": "jspw"
        }
      ],
      "metaData": {
        "predictedNames": [
          {
            "name": "Mehedi Hasan",
            "fontSize": 23.09002663941783,
            "algorithm": "1st Paragraph"
          },
          {
            "name": "Mehedi Hasan",
            "fontSize": 23.09002663941783,
            "algorithm": "Largest Font"
          }
        ],
        "urls": [
          "linkedin.com/in/mhshifat",
          "github.com/jspw",
          "https://github.com/jspw/Paper",
          "https://github.com/jspw/cp-tool",
          "https://github.com/jspw/Ubuntu-Launcher",
          "https://github.com/jspw/HackTheVerse_SUST_Tetrahedron",
          "https://github.com/jspw/CodeNerd"
        ],
        "phone_number": ["+8801714986887"],
        "email_addresses": ["mhshifat757@gmail.com"]
      }
    }
  }
]
```
