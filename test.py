# s = "101"
# res = 0
# for i in range(0, len(s)):
#     res = res + 2**(len(s)-i-1) * int(s[i])
# print(res)

# s = ['orange', 'orament', 'oracle']

# def find_smallest(li):
#     res = 1e+5
#     idx = -1
#     for i in range(0,len(s)):
#         if len(s[i]) < res:
#             res = len(s[i])
#             idx = i
#     return idx
# key =  s[find_smallest(s)]
# res = ""
# for idx , character  in  enumerate(key):
#     flag = True
#     for i in s:
#         if i[idx] != character:
#             flag = False
#     if flag:
#         res += character
#     else:
#         break
# print(res)

# #

import requests


USERNAME = 'Aswin'
PASS = 'Ash@41938'

data = requests.post(
    url='http://127.0.0.1:8000/api/token/',
    data={
        'username' : USERNAME,
        'password' : PASS
    }
)
access = data.json().get('access')

headers = {
    'Authorization': f'Bearer {access}'
}

with open("Screenshot (7).png", 'rb') as img_file:
    response = requests.post(
        url='http://192.168.0.107:8000/api/route/photo/',
        headers=headers,
        data={'key': 'value'},
        files={'photo': img_file}
    )


# response = requests.get(
#         url='http://127.0.0.1:8000/api/route/photo/',
#         headers=headers,
# )
print(response.json())
