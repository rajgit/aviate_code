Simple drf application with candidate module

Candidate module has candidate table


Api end points to create, update and delete candidate
Api end point to search 
Logic for search is captured in the code.

Have used and added sqlite file , it should have test data used below.

---
Installation
install django rest framework and that is it.
Ran below examples using django runserver

----

###Sample working api calls


-------------
create candidate
$  curl -X POST http://localhost:8000/candidates/  -H "Content-Type: application/json"  -X POST --data '{"email":"user1@test.com","name":"Ajay Kumar Yadav", "age":30,"gender":"M","phone_number":"919999999999"}' | more
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   216  100   111  100   105   6514   6162 --:--:-- --:--:-- --:--:-- 13500
{"id":1,"email":"user1@test.com","name":"Ajay Kumar Yadav","age":30,"gender":"M","phone_number":"919999999999"}


----
update candidate

$  curl -X PATCH http://localhost:8000/candidates/7/  -H "Content-Type: application/json"  -X PATCH --data '{"name":"updated delete Ajay singh"}' | more
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   157  100   121  100    36   7302   2172 --:--:-- --:--:-- --:--:--  9235
{"id":7,"email":"user99@test.com","name":"updated delete Ajay singh","age":30,"gender":"M","phone_number":"919999999999
"}

---
delete candidate

$ curl -X DELETE http://localhost:8000/candidates/7/  -H "Content-Type: application/json" | more

---

search candidate

case 1 - 3 word name search "ajay kumar yadav"
$ curl -X POST http://localhost:8000/candidates/search/  -H "Content-Type: application/json"  -X POST --data '{"name":"Ajay Kumar Yadav"}' | more
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   163  100   136  100    27  19520   3875 --:--:-- --:--:-- --:--:-- 27166
{"candidates":["Ajay Kumar Yadav","Kumar Ajay Yadav","Ajay Kumar","Ajay Yadav","Kumar Yadav","Ramesh Yadav","Ajay Singh
","Kumar Singh"]}

case 2 - two word name search - "ajay kumar"
$ curl -X POST http://localhost:8000/candidates/search/  -H "Content-Type: application/json"  -X POST --data '{"name":"Ajay kumar"}' | more
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   142  100   121  100    21  21992   3816 --:--:-- --:--:-- --:--:-- 28400
{"candidates":["Ajay Kumar","Ajay Kumar Yadav","Kumar Ajay Yadav","Kumar Singh","Kumar Yadav","Ajay Singh","Ajay Yadav"
]}


case 3- one word name search - "ajay"

$ curl -X POST http://localhost:8000/candidates/search/  -H "Content-Type: application/json"  -X POST --data '{"name":"Ajay"}' | more
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   108  100    93  100    15  25999   4193 --:--:-- --:--:-- --:--:-- 36000
{"candidates":["Ajay Kumar","Ajay Kumar Yadav","Ajay Singh","Ajay Yadav","Kumar Ajay Yadav"]}

---
