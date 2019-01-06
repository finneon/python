# Search Dictionaries
> www.oxfordlearnersdictionaries.com/
> [REST API documentation](https://www.oxfordlearnersdictionaries.com/api/v1/documentation/html)
> [Register for app_key](https://developer.oxforddictionaries.com/)

* Using **requests** librabry

* How to install:
  * cp oxfordDict.py /usr/local/bin/oxfordDict
  * chmod +x /usr/local/bin/oxfordDict

* Raw command:
  * curl -X GET -H "Accept: application/json" https://od-api.oxforddictionaries.com:443/api/v1/entries/en/light -H 'app_id: 79b0bf7f' -H 'app_key: e1c41553a15e7ab359b36ec3a849e2b4'
