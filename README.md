# NEST 🪺
## _A safe place for your passwords_

[![Streamlit](https://global.discourse-cdn.com/streamlit/original/3X/3/c/3ccec8dae6656656087fdb9dfd5e30578050bf07.svg)](https://streamlit.io/)

Hey there 👋!
The main objective for our project was to create a program that aimed to convert
handwritten passwords into digital passwords in order to increase usability and convenience for
people. 

- ✨Pure Magic ✨

## Features 🛠️

- Ability to upload photos
- Search for passwords
- Safe storage inside of a cloud database (mongodb)
- Easy to use and user friendly interface
- Ability to edit passwords after they have been uploaded


> the main objective for our project was to create a program that aimed to convert
handwritten passwords into digital passwords in order to increase usability and convenience for
people. This project also was designed in a way that people with little experience of how 
digital technology works, such as the elderly, would be able to use and manage the product. The
project works by the user first uploading a piece of paper containing their username, password,
and the website. Once it has been uploaded, the picture is scanned and the information is
extracted. Now that the information is extracted it gets sent, stored, and organized inside of a
cloud based MongoDB server. From there the search bar on the left allows users to look up
accounts and find the corresponding passwords from the sheet that was uploaded.


Cool right?

## Tech 👨🏻‍💻

- NEST depends heavily on gpt4o-mini for computer vision capabilities
(Microsoft Azure Computer Vision is is not accurate enough for our usecase)

- Streamlit
A python library to quickly spin up frontend for apps
- MongoDb
 an open-source, non-relational database management system (DBMS) that stores and processes data in documents instead of tables and rows


And of course NEST itself is open source with a public repo on GitHub 💯

## Installation 💿

NEST requires you to install streanmlit (a python library) and a few other requirements to run.

Install the requirements.txt file to get started
```sh
pip install -r requirements.txt
```

Make sure to create an `.env` file and store the appropriate API keys 
```
OAPI = "YOUR-OPENAI-API-KEY"
MONGO_URI="YOUR-MONGO-URI" (Without quotes)
```
>NOTE: Mongo may block unrecognized IPs from connecting, make sure to whitelist your IP before running




## Development

Want to contribute? Sorry, It is a class project and closed for contribution

Suggestions are always welcome!!
