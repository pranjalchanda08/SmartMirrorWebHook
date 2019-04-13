Steps to add dev codes to add more intents:

1. Create a <fileName>.py file in "dev" folder.
2. The file must follow the following structure of coding.
	a. "import common" to your file.
	b. Create a global dictionary as below:
		{
			"<$key>":{											//$key can be any given name to your keys
				"import"  : "dev.$fileName"
				"intents" : {
					"$intentName":{								//Same as registered on dialogflow
					"func" : "$NameOfTheFunctionDef",			//Local function pointer
  					"module" : "dev.$fileName",					//This is always constant to all the intents in this series and same as value of "import" key
  					"include": $Boolean,						//If you want the function to be registered in main app
  					"alias" : "$AliasFunctionName"				//Alias to the defined function
					},
					"$intent2Name":{			
					"func" : "$NameOfTheFunction2Def",
  					"module" : "dev.$fileName",		
  					"include": $Boolean,			
  					"alias" : "$AliasFunction2Name"	
					},
					...
					...
					...		Add as much as you want to add
					...
					...
				}
			}
		}
	c. Add an entry point in the file "if __name__ == '__main__':" With a definite call of "common.exportJson(dictionary)" dictionary refers to the above created dictionary as argument and nothing else. 
	When the code is executed it shall update the file json/fnReg.json with the above format of dictionary.
3. Now add your definations to the file and enjoy the execution. 
4. Deployment is automated and as soon as you push your commit a build process will work on bitbucket as specified in bitbucket-pipelines.yml file.