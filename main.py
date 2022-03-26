from templates import (code2nl, fix_bugs, get_api_request_code,
                       get_error_explanation, nl2sql, sql2nl, code2docstring, get_oneliner, code2ut,complete_code)

# result = get_api_request_code(api_name="Google Translate", task="Translate from German to English",
#                               params="Ich bin dein vater")
# print(result)

# sql2nl
# query = """SELECT DISTINCT department.name
# FROM department
# JOIN employee ON department.id = employee.department_id
# JOIN salary_payments ON employee.id = salary_payments.employee_id
# WHERE salary_payments.date BETWEEN '2020-06-01' AND '2020-06-30'
# GROUP BY department.name
# HAVING COUNT(employee.id) > 10;"""
# explanation = sql2nl(query)
# print(explanation)

# nl2sql
# """
# # Table albums, columns = [AlbumId, Title, ArtistId]
# # Table artists, columns = [ArtistId, Name]
# # Table media_types, columns = [MediaTypeId, Name]
# # Table playlists, columns = [PlaylistId, Name]
# # Table playlist_track, columns = [PlaylistId, TrackId]
# # Table tracks, columns = [TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice]

# # Create a query for all albums by Adele
# """
# table_names = ["albums", "artists", "media_types",
#                "playlists", "playlist_track", "tracks"]
# col_names = [["AlbumId", "Title", "ArtistId"], ["ArtistId", "Name"], ["MediaTypeId", "Name"], ["PlaylistId", "Name"],
#              ["PlaylistId", "TrackId"], ["TrackId", "Name", "AlbumId", "MediaTypeId", "GenreId", "Composer", "Milliseconds", "Bytes", "UnitPrice"]]
# task = "all albums by Adele"
# sql = nl2sql(table_names, col_names, task)
# print(sql)

# code2nl
# C
# prompt = '''int reverse(int n)
# {
#     int rev = 0;
#     while (n != 0)
#     {
#         rev = rev * 10 + n % 10;
#         n /= 10;
#     }
#     return rev;
# }'''

# code = code2nl(prompt, language='C')
# print(code)



# fix_bugs
# function = '''
# def check(n):
#     """
#     Check if a given number is less than twice the value of its reverse.
#     """
#     return n - 1 == int(str(n)[::-1])
# '''

# # only returns function body
# code = fix_bugs(function, 'python')
# print(code)

#get_error_explanation
# code="""
# def is_prime(num):
#     if num % i == 0:
#         return False
#     return True"""
# ee=get_error_explanation(code)
# print(ee)

# code2docstring
# code="""def reverseQueue(q):
#     Stack = []
#     while (not(q.empty())):
#         Stack.append(q.queue[0])
#         q.get()
#     while (len(Stack) != 0):
#         q.put(Stack[-1])
#         Stack.pop()
# """
# doc=code2docstring(code)
# print(doc)

# get_oneliner
# code="""
# def is_prime(num):
#     for i in range(2, num):
#         if num % i == 0:
#             return False
#     return True"""
# ol=get_oneliner(code,'python')
# print(ol)

# code2ut
# code="""
# def is_prime(num):
#     for i in range(2, num):
#         if num % i == 0:
#             return False
#     return True"""
# ut=code2ut(code,'python')
# print(ut)

# complete_code
# code="""
# def is_prime(num):
#     for i in range(2, num):"""        
# cc=complete_code(code,'check is numbers is prime')
# print(cc)