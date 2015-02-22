# Port-Knocking A port knocking application build on Flask. This was
an assignment given Prof Doupe for his class CSE 591- Security and
vulnerabilty analysis. 
The numbers assigned to pages are as follows:
[
  0 : /user/register,
  1 : /user/login,
  2 : /message/add,
  3 : /message/list,
]

The knock-sequence generated is as follows :
Given a username, which is a string, take the md5 hash of the
username. Convert it to hexadecimal (there should be 32 hexadecimal
digits). The first hexadecimal digit of the hash modulo 4 will be the
first element of the knock sequence (using the mapping above), the
second hexadecimal digit of the hash modulo 4 will be the second
element of the knock sequence, and so on for a knock sequence with
total length of 4.

Consider the following example:

For the user who registers with the username “ObMaX” (without quotes),
the md5 of this username is “b86ec61e49774117d6ba2b4f183a4a8e” (again,
without the quotes). The first four digits of the md5 are [b, 8, 6,
e], these digits modulo 4 are [3, 0, 2, 2], so the knock sequence will
be [ /message/list, /user/register, /message/add, and /message/add ]

Steps to run application:
1) Clone the application
2) Download and install virtualenv
3) activate the virtualenv for the downloaded repo by 
. venv/bin/activate
4)Now run views.py inside app folder
5) App should be running by now. 


Change the path to db in app/views.py



