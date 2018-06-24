# coding=utf-8

from sc2.position import Point2


# calculates the distance between two coordinates
def distance(unit_a, unit_b):
    return unit_a.position.to2.distance_to(unit_b.position.to2)


# verify if determined unit is not contained a group of units
def contains_unit(unit, unit_group):
    for u in unit_group:
        if unit.tag == u.tag:
            return True
    return False


# get the mean location between two coordinates
def get_mean_location(pos1, pos2):
    x = (pos1.x + pos2.x) / 2
    y = (pos1.y + pos2.y) / 2
    return Point2((x, y))




