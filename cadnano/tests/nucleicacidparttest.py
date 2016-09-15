# -*- coding: utf-8 -*-
import pytest
import math

from .cntestcase import CNTestApp

@pytest.fixture()
def cnapp():
    app = CNTestApp()
    yield app
    app.tearDown()

from cadnano.part.nucleicacidpart import NucleicAcidPart

@pytest.mark.parametrize('direction', [(0, 0, 1), (0, 1, 0)])
def testVirtualHelixCreate(cnapp, direction):
    doc = cnapp.document
    part = NucleicAcidPart(document=doc)
    assert len(part.getidNums()) == 0
    radius = part.radius()
    origin_pt0 = (0, 0, 0)
    origin_pt90 = (0, 2*radius, 0)
    theta = math.radians(30)
    origin_pt60 = (2*radius*math.cos(-theta), 2*radius*math.sin(-theta), 0)
    color = part.getColor()
    part.createHelix(0, origin_pt0, direction, 42, color)
    part.createHelix(1, origin_pt60, direction, 42, color)
    part.createHelix(2, origin_pt90, direction, 42, color)
    id_nums = part.getidNums()
    assert len(id_nums) == 3
    return part


