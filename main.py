from classes.repo import Repo
from classes.car import Car
from classes.cell import Cell, Decoration, Checkpoint, Obstacle, Wall, Mud, Ice, Bonus, Booster, Refuel, Road, StraightRoad, Turn90
import sys

if len(sys.argv) < 2:
  raise ValueError("Please enter a username.")
ARG1 = sys.argv[1] # like USER=<user>
USER = ARG1.split('=')[1] if ARG1.startswith('USER=') else None
if not USER:
  raise ValueError("Please enter username as 'USER=<username>'.")

Repo().components.register("Car", Car)
Repo().components.register("Cell", Cell)
Repo().components.register("Decoration", Decoration)
Repo().components.register("Checkpoint", Checkpoint)
Repo().components.register("Obstacle", Obstacle)
Repo().components.register("Wall", Wall)
Repo().components.register("Mud", Mud)
Repo().components.register("Ice", Ice)
Repo().components.register("Bonus", Bonus)
Repo().components.register("Booster", Booster)
Repo().components.register("Refuel", Refuel)
Repo().components.register("Road", Road)
Repo().components.register("StraightRoad", StraightRoad)
Repo().components.register("Turn90", Turn90)
Repo().components.list()

map_id = Repo.create(cols=10, rows=10, cellsize=64, bgcolor='green') # map has an id of 0
Repo.attach(map_id, USER)
Repo.listattached(USER) # 0 will be listed
map_instance = Repo.getObjectOfUser(map_id, USER)
map_instance[(0, 0)] = Repo().components.create("Decoration")
map_instance[(0, 0)].rotation = 0
for i in range(2, 8):
    map_instance[(1, i)] = Repo().components.create("StraightRoad")
    map_instance[(1, i)].rotation = 0
map_instance[(1, 7)] = Repo().components.create("Turn90")
map_instance[(1, 7)].rotation = 1
for i in range(2, 6):
    map_instance[(i, 7)] = Repo().components.create("StraightRoad")
    map_instance[(i, 7)].rotation = 1
map_instance[(8, 9)] = Repo().components.create("Obstacle")
map_instance[(8, 9)].rotation = 0
print(map_instance[(8, 9)].type())
del map_instance[(8, 9)]
print(map_instance.getxy(75, 150).type())
map_instance[(0, 1)] = Repo().components.create("Mud")
map_instance[(0, 1)].rotation = 0
map_instance[(0, 2)] = Repo().components.create("Ice")
map_instance[(0, 2)].rotation = 0
map_instance[(0, 3)] = Repo().components.create("Wall")
map_instance[(0, 3)].rotation = 0
map_instance[(0, 4)] = Repo().components.create("Checkpoint")
map_instance[(0, 4)].rotation = 0
refuel = Repo().components.create("Refuel")
refuel.rotation = 0
map_instance.place(refuel, 15, 500)
map_instance.draw()

volvo_XC60 = Repo().components.create("Car", model="Volvo-XC60", map_ref=map_instance, driver="batuhan", pos=(1,1), angle=0, topspeed=100, topfuel=100)
map_instance.place(volvo_XC60, 0, 0)

sub_map = map_instance.view(3, 1, 5, 5)
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
volvo_XC60.tick()
