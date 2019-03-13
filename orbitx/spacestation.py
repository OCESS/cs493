from . import orbitx_pb2 as protos
  # physics module
from pathlib import Path
from orbitx.displayable import Displayable
import vpython
import orbitx.calculator as calc
import numpy as np


class SpaceStation(Displayable):
    def __init__(self, entity: protos.Entity, texture_path: Path) -> None:
        super(SpaceStation, self).__init__(entity, texture_path)
        _pos = calc.posn(entity)
        _radius = entity.r
        _axis = 2 * entity.r * \
            vpython.vector(np.cos(entity.heading), np.sin(entity.heading), 0)
        ship = vpython.cone(pos=vpython.vector(2, 0, 0),
                            axis=vpython.vector(-8, 0, 0),
                            radius=3,
                            opacity=0.7)
        entrance = vpython.extrusion(path=[vpython.vec(0, 0, 0),
                                           vpython.vec(-4, 0, 0)],
                                     shape=[vpython.shapes.circle(radius=1.5),
                                            vpython.shapes.rectangle(pos=[0, -0.3],
                                                                     width=1.5,
                                                                     height=1.5)],
                                     pos=vpython.vec(0, 0, 0))  # position

        self._obj = vpython.compound([ship, entrance])
        self._obj.pos = _pos
        self._obj.axis = _axis
        self._obj.radius = _radius
        self._obj.length = _radius
        self._obj.height = _radius
        self._obj.width = _radius

        self._obj.name = self._entity.name

        self._station_trail = vpython.attach_trail(self._obj, retain=100)

        self._station_trail.stop()
        self._station_trail.clear()

        self._draw_labels()
    # end of __init__

    def _draw_labels(self) -> None:
        self._label = self._create_label()
        self._label.text_function = lambda entity: entity.name
        self._label.text = self._label.text_function(self._entity)
    # end of _draw_labels

    def draw(self, entity: protos.PhysicalState):
        self._update_obj(entity)
    # end of draw

    def clear_trail(self) -> None:
        self._station_trail.clear()
    # end of clear_trail

    def trail_option(self, stop: bool = False) -> None:
        if stop:
            self._station_trail.start()
        else:
            self._station_trail.stop()
            self._station_trail.clear()
    # end of trail_option

# end of class SpaceStation

