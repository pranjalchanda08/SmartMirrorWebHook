# Stephen
Stephen is a AI assistant bot running over Raspberry pi 3 B+. Could be commanded to work according to the user with just a voice command trigger as "Stephen". This bot framework is open source and could be imported to any project to make good use to it. Any one wants to add custom intents can easily do it by following the steps in Tech section.

# Features added:
* Weather: We can command it to fetch weather of any location we want to.
* Device control: Control deices like fan, light over the cloud.

# Tech
Steps to add dev codes to add more intents:

1. Create a <fileName>.py file in "dev" folder.
2. The file must follow the following structure of coding.
	* "import common" to your file.
	* Create a global dictionary as in __dev/example.json__.
	* Add an entry point in the file "if \_\_name\_\_ == '\_\_main\_\_':" With a definite call of "common.exportJson(dictionary)" dictionary refers to the above created dictionary as argument and nothing else. 
	* When the code is executed it shall update the file json/fnReg.json with the above format of dictionary.
3. Now add your definations to the file and enjoy the execution. 
4. Deployment is automated and as soon as you push your commit and is merged to master branch a build process will work on heroku as required.
5. So please createa pull request to master branch.

# Dependencies
Following software dependencies shall be fulfiled:
* Python 3.6+
* Pip3
* Git

# Installation
* Clone the project.
* Perform the following shell command from the same folder location.
    ```sh
    $ pip3 install -r 'requirements.txt'
    $ cd dev
    $ python3 <filename>.py     //filename are all the intent files present in dev folder
    $ cd ../json
    $ cat fnReg.json
    ```
* fnReg.json shall be updated with all the intent dictionaries. 

# Run locally
Run the following command from the main cloned folder. 
```sh
$ python3 app.py
```