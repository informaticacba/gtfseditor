#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import Base
from .entity import Entity
from sqlalchemy import orm, Column, types, ForeignKey



class StopTime(Base, Entity):

    __tablename__ = 'stop_times'

    trip_id = Column(types.Integer,
                     ForeignKey("trips.trip_id", onupdate="CASCADE"),
                     primary_key=True)
    stop_id = Column(types.Integer,
                     ForeignKey("stops.stop_id", onupdate="CASCADE", ondelete="CASCADE"),
                     primary_key=True)
    stop_sequence = Column(types.Integer, primary_key=True)
    arrival_time = Column(types.String(50))
    departure_time = Column(types.String(50))
    shape_dist_traveled = Column(types.Float(precision=53))
