
# USERIN ÇAĞIRMADIĞI FONKSİYONLARIN OUTPUTUNDAN USERI HABERDAR
#   ETMEK İÇİN NOTİFİCATİON LAZIM
# SERVERİ TEST ET
# MAPTAKİ KAYNAKLARA CONCURRENCY EKLE



from classes.repo import Repo
from classes.server import Server
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--port")
args = parser.parse_args()

""" Repo().components.register("Car")
Repo().components.register("Cell")
Repo().components.register("Decoration")
Repo().components.register("Checkpoint")
Repo().components.register("Obstacle")
Repo().components.register("Wall")
Repo().components.register("Mud")
Repo().components.register("Ice")
Repo().components.register("Bonus")
Repo().components.register("Booster")
Repo().components.register("Refuel")
Repo().components.register("Road")
Repo().components.register("StraightRoad")
Repo().components.register("Turn90")
# Repo().components.list()

map_id = Repo.create(cols=10, rows=10, cellsize=64, bgcolor='green') # map has an id of 0
# Repo.attach(map_id, USER)
# Repo.listattached(USER) # 0 will be listed
map_instance = Repo._maps[map_id]
map_instance[(0, 0)] = Repo().components.create("Decoration")
for i in range(2, 8):
    map_instance[(1, i)] = Repo().components.create("StraightRoad")
map_instance[(1, 7)] = Repo().components.create("Turn90")
map_instance[(1, 7)].rotation = 1
for i in range(2, 6):
    map_instance[(i, 7)] = Repo().components.create("StraightRoad")
    map_instance[(i, 7)].rotation = 1
map_instance[(8, 9)] = Repo().components.create("Obstacle")
# print(map_instance[(8, 9)].type())
del map_instance[(8, 9)]
# print(map_instance.getxy(75, 150).type())
map_instance[(0, 1)] = Repo().components.create("Mud")
map_instance[(0, 2)] = Repo().components.create("Ice")
map_instance[(0, 3)] = Repo().components.create("Wall")
map_instance[(2, 0)] = Repo().components.create("Checkpoint")
map_instance[(2, 1)] = Repo().components.create("Checkpoint")
map_instance[(2, 2)] = Repo().components.create("Checkpoint")
map_instance[(2, 3)] = Repo().components.create("Checkpoint")
# print(map_instance.checkpoints)
refuel = Repo().components.create("Refuel")
map_instance.place(refuel, 15, 500)
# map_instance.draw()
volvo_XC60 = Repo().components.create("Car", model="Volvo-XC60", map_ref=map_instance, driver="batuhan", pos=(1,1), angle=0, topspeed=100, topfuel=100)
map_instance.place(volvo_XC60, 128, 0)
# map_instance.draw()
audi_A4 = Repo().components.create("Car", model="Audi-A4", map_ref=map_instance, driver="ahmet", pos=(0,0), angle=0, topspeed=200, topfuel=80)
map_instance.place(audi_A4, 0, 0) """

""" sub_map = map_instance.view(3, 1, 5, 5)
sub_map.draw()

volvo_XC60.start()
volvo_XC60.tick()
volvo_XC60.accel()
volvo_XC60.tick()
volvo_XC60.tick()
volvo_XC60.left()
volvo_XC60.tick()
volvo_XC60.right()
volvo_XC60.tick()
volvo_XC60.right()
volvo_XC60.tick()
volvo_XC60.tick()
volvo_XC60.accel()
volvo_XC60.tick()
volvo_XC60.right()
volvo_XC60.tick()
volvo_XC60.right()
volvo_XC60.tick()
volvo_XC60.right()
volvo_XC60.tick()
volvo_XC60.right()
volvo_XC60.tick()
volvo_XC60.brake()
volvo_XC60.tick()
volvo_XC60.brake()
volvo_XC60.tick()
volvo_XC60.stop()
volvo_XC60.accel()
volvo_XC60.tick() """

""" map_instance.start()
volvo_XC60.start()
time.sleep(1)
volvo_XC60.accel()
time.sleep(1)
map_instance.place(volvo_XC60, 128, 64)
time.sleep(1)
map_instance.place(volvo_XC60, 128, 128)
time.sleep(1)
audi_A4.start()
time.sleep(1)
audi_A4.accel()
time.sleep(1)
map_instance.place(audi_A4, 128, 0)
time.sleep(1)
map_instance.place(audi_A4, 128, 64)
time.sleep(1)
map_instance.place(audi_A4, 128, 128)
time.sleep(1)
map_instance.place(audi_A4, 128, 192)
time.sleep(1)
map_instance.place(audi_A4, 128, 0)
time.sleep(1)
map_instance.stop()

print(map_instance.cars)
print(map_instance.checkpoints)
print(map_instance.cells)
print(audi_A4.checkpoint_times)
map_instance.draw()
Repo.saveMap(map_id)
map_instance = Repo.loadMap(map_id)
map_instance.draw() """

s = Server("127.0.0.1", int(args.port))
s.start_server()