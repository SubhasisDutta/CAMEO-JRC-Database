Python Tornado Script to launch a REST server to receive GET request and obtain the translation from database or get it from BABLENET.


Example URL for Donald Trump: 
http://babelnet.org/search?word=donald+trump&lang=EN&langTrans=AR&langTrans=ZH&langTrans=ES 
Presidents Profile: http://babelnet.org/synset?word=bn:03259764n&details=1&lang=EN&orig=donald%20trump  

API call for this : https://babelnet.io/v4/getSenses?word=donald_trump&lang=EN&pos=NOUN&filterLangs=AR&filterLangs=ES&key=284fd255-4315-4e6e-b6c9-f7a6409bc815 
We will have to parse the response and extract what we need.
In this example the query for Donald Trump also returns persons sharing Trump's name which can cause problem if the other person is more popular. 

Query for a less known person : http://babelnet.org/synset?word=MULLAH_MOHAMMAD_RABBANI&lang=EN&details=1&orig=MULLAH_MOHAMMAD_RABBANI  

About BabelNet : https://en.wikipedia.org/wiki/BabelNet  .

The data access limit is 1000 request per day. However they can increase the limit to 50000 request per day when we show them it is for research purpose from an institution.
http://babelnet.org/guide#access 


DBPedia
http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=narendra+modi

BableNet
API key: 7914e95c-2716-4cce-bb47-bbdab5e43f57
