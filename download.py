import os
# READ the download list
ac_movies=[]
bi_movies=[]
for line in open("DOWNLOAD_DIRECTORY.txt"):

    if line[1] =='c':
        ac_movies.append(line.strip())
    else:
        bi_movies.append(line.strip())
print ac_movies
print bi_movies

# DOWNLOAD

for movie in ac_movies:
    os.system("python acfun.py "+movie)
for movie in bi_movies:
    os.system("python bilibili.py "+movie)