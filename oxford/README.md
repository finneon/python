# Search Dictionaries
 > www.oxfordlearnersdictionaries.com

 > https://en.oxforddictionaries.com

 > [REST API documentation](https://www.oxfordlearnersdictionaries.com/api/v2/documentation/html)

 > [Register for app_key](https://developer.oxforddictionaries.com/)

 > Users on a FREE account need to update to either PROTOTYPE or DEVELOPER to get access to v2

* Using **requests** librabry

* How to install:
  * cp oxfordDict.py /usr/local/bin/oxfordDict
  * chmod +x /usr/local/bin/oxfordDict

* Raw command:
  * app_id=79b0bf7f
  * app_key=ff161d54827d585f1453a425de3d40e0
  * curl -X GET -H "Accept: application/json" https://od-api.oxforddictionaries.com:443/api/v2/entries/en-us/<word> -H "app_id: ${app_id}" -H "app_key: ${app_key}"
