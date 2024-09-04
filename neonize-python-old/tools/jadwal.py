import os, datetime

time_now = datetime.datetime.now()
path     = "data/owner-status.txt"


# -> Set Jadwal Offline
# def setup(msg):
#     try:os.remove(path)
#     except:pass
#     awal, akhir = msg.split(" ")[1].split("-")

#     jadwal = []
#     if int(akhir) < int(awal): new_akhir = int(akhir) + 24
#     else: new_akhir = int(akhir)


#     for x in range(int(awal), new_akhir + 1):
#         if x > 23: x = x - 24
#         if len(jadwal) < 1: open(path, "a").write(str(x))
#         else: open(path, "a").write("-" + str(x))
#         jadwal.append(x)


# -> Check status owner
def check():
    try:
        jadwal = open(path, "r").read()
        status = True if jadwal == "Online" else False
        return status

    except:
        return False


# -> Set status owner to oflline
def offline():
    open(path, "w").write("Offline")


# -> Set status owner to online
def online():
    open(path, "w").write("Online")