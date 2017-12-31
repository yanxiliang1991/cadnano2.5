import struct

from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QQuaternion
from PyQt5.QtGui import QVector3D, QVector4D

from PyQt5.Qt3DCore import QEntity, QTransform
from PyQt5.Qt3DExtras import QCuboidMesh
from PyQt5.Qt3DExtras import QCylinderMesh
from PyQt5.Qt3DExtras import QPhongAlphaMaterial
from PyQt5.Qt3DExtras import QGoochMaterial
from PyQt5.Qt3DExtras import QPerVertexColorMaterial
from PyQt5.Qt3DExtras import QSphereMesh
from PyQt5.Qt3DRender import QAttribute
from PyQt5.Qt3DRender import QBuffer
from PyQt5.Qt3DRender import QGeometry, QGeometryRenderer

from cadnano.gui.palette import getColorObj


class Triangle(QEntity):
    def __init__(self, parent_entity):
        super(Triangle, self).__init__(parent_entity)
        self._mesh = mesh = QGeometryRenderer(parent_entity)
        self._geometry = geo = QGeometry(mesh)

        vertex_buffer = QBuffer(QBuffer.VertexBuffer)
        normal_buffer = QBuffer(QBuffer.VertexBuffer)
        color_buffer = QBuffer(QBuffer.VertexBuffer)

        # Vertices
        v0 = QVector3D(0.0, 0.0, 0.0)
        v1 = QVector3D(2.0, 0.0, 0.0)
        v2 = QVector3D(0.0, 2.0, 0.0)
        v3 = QVector3D(2.0, 2.0, 0.0)
        vertices = [v0, v1, v2, v3]
        vertex_bytes = bytes()
        for v in vertices:
            vertex_bytes += struct.pack('f', v.x())
            vertex_bytes += struct.pack('f', v.y())
            vertex_bytes += struct.pack('f', -v.z())
        vertex_bytearray = QByteArray(vertex_bytes)
        vertex_buffer.setData(vertex_bytearray)

        # n0 = QVector3D(0.0, 1.0, 0.0)
        # n1 = QVector3D(0.0, 1.0, 0.0)
        # n2 = QVector3D(0.0, 1.0, 0.0)
        # n3 = QVector3D(0.0, 0.0, 1.0)
        # n4 = QVector3D(0.0, 0.0, 1.0)
        # n5 = QVector3D(1.0, 0.0, 0.0)
        # n6 = QVector3D(0.0, 1.0, 0.0)
        # n7 = QVector3D(1.0, 0.0, 0.0)
        # normals = [n0, n1, n2, n3, n4, n5, n6, n7]
        # normal_bytes = bytes()
        # for n in normals:
        #     normal_bytes += struct.pack('!f', n.x())
        #     normal_bytes += struct.pack('!f', n.y())
        #     normal_bytes += struct.pack('!f', -n.z())
        # normal_bytearray = QByteArray(normal_bytes)
        # normal_buffer = QBuffer(QBuffer.VertexBuffer)
        # normal_buffer.setData(normal_bytearray)
        # self._norm_attr = norm_attr = QAttribute()
        # norm_attr.setAttributeType(QAttribute.VertexAttribute)
        # norm_attr.setBuffer(normal_buffer)
        # norm_attr.setVertexBaseType(QAttribute.Float)
        # norm_attr.setVertexSize(3)
        # norm_attr.setByteOffset(0)
        # norm_attr.setByteStride(3)
        # norm_attr.setCount(28)
        # norm_attr.setName(QAttribute.defaultNormalAttributeName())
        # geo.addAttribute(norm_attr)

        c0 = QVector3D(1.0, 0.0, 0.0)
        c1 = QVector3D(0.0, 1.0, 0.0)
        c2 = QVector3D(0.0, 0.0, 1.0)
        c3 = QVector3D(1.0, 1.0, 0.0)
        colors = [c0, c1, c2, c3]

        color_bytes = bytes()
        for c in colors:
            color_bytes += struct.pack('f', c.x())
            color_bytes += struct.pack('f', c.y())
            color_bytes += struct.pack('f', c.z())
            # color_bytes += struct.pack('!f', c.w())
        color_bytearray = QByteArray(color_bytes)
        color_buffer.setData(color_bytearray)

        # interleave = [v0, v1, n01, c0, v2, v3, n23, c1, v4, v5, n45, c2]
        # interleave = [v0, n01, c0, v1, n01, c0, v2, n23, c1, v3, n23, c1, v4, n45, c2, v5, n45, c2]
        # vertices = interleave

        # element_size = 3 + 4  # vec3 pos, vec4 col
        # float_size = 1  # len(struct.pack('!f', 1.0))  # 4
        # stride = element_size * float_size
        # Attributes
        self._pos_attr = pos_attr = QAttribute()
        pos_attr.setAttributeType(QAttribute.VertexAttribute)
        pos_attr.setBuffer(vertex_buffer)
        pos_attr.setVertexBaseType(QAttribute.Float)
        pos_attr.setVertexSize(3)
        pos_attr.setByteOffset(0)
        pos_attr.setByteStride(3)
        pos_attr.setCount(28)
        pos_attr.setName(QAttribute.defaultPositionAttributeName())

        self._norm_attr = norm_attr = QAttribute()
        norm_attr.setAttributeType(QAttribute.VertexAttribute)
        norm_attr.setBuffer(normal_buffer)
        norm_attr.setVertexBaseType(QAttribute.Float)
        norm_attr.setVertexSize(3)
        norm_attr.setByteOffset(0)
        norm_attr.setByteStride(3)
        norm_attr.setCount(28)
        norm_attr.setName(QAttribute.defaultNormalAttributeName())

        self._col_attr = col_attr = QAttribute()
        col_attr.setAttributeType(QAttribute.VertexAttribute)
        col_attr.setBuffer(color_buffer)
        col_attr.setVertexBaseType(QAttribute.Float)
        col_attr.setVertexSize(3)
        col_attr.setByteOffset(0)
        col_attr.setByteStride(3)
        col_attr.setCount(28)
        col_attr.setName(QAttribute.defaultColorAttributeName())

        # idx_buffer = QBuffer(QBuffer.IndexBuffer, geo)
        # idx_bytes = bytes()
        # idx_bytes += struct.pack('H', 0)
        # idx_bytes += struct.pack('H', 1)
        # idx_bytes += struct.pack('H', 2)
        # idx_bytes += struct.pack('H', 3)
        # idx_bytearray = QByteArray(idx_bytes)
        # idx_buffer.setData(idx_bytearray)
        # idx_attr = QAttribute()
        # idx_attr.setAttributeType(QAttribute.IndexAttribute)
        # idx_attr.setBuffer(idx_buffer)
        # idx_attr.setVertexBaseType(QAttribute.UnsignedShort)
        # idx_attr.setVertexSize(1)
        # idx_attr.setByteOffset(0)
        # idx_attr.setByteStride(2)
        # idx_attr.setCount(4)

        geo.addAttribute(pos_attr)
        geo.addAttribute(norm_attr)
        geo.addAttribute(col_attr)
        # geo.addAttribute(idx_attr)

        # mesh.setPrimitiveRestartEnabled(True)

        mesh.setFirstInstance(0)
        mesh.setFirstVertex(0)
        mesh.setInstanceCount(1)
        # mesh.setVerticesPerPatch(3)
        # mesh.setVertexCount(6)
        mesh.setGeometry(geo)
        mesh.setPrimitiveType(QGeometryRenderer.Points)

        trans = QTransform()
        mat = QPerVertexColorMaterial(parent_entity)

        self.addComponent(mesh)
        self.addComponent(trans)
        self.addComponent(mat)
    # end def

    def setPosVertexSize(self, val):
        self._pos_attr.setVertexSize(val)

    def setPosByteOffset(self, val):
        self._pos_attr.setByteOffset(val)

    def setPosByteStride(self, val):
        self._pos_attr.setByteStride(val)

    def setPosCount(self, val):
        self._pos_attr.setPosCount(val)

    def setColVertexSize(self, val):
        self._col_attr.setVertexSize(val)

    def setColByteOffset(self, val):
        self._col_attr.setByteOffset(val)

    def setColByteStride(self, val):
        self._col_attr.setByteStride(val)

    def setColCount(self, val):
        self._col_attr.setCount(val)

    def setByteStride(self, val):
        self._pos_attr.setByteStride(val)
        # self._norm_attr.setByteStride(val)
        self._col_attr.setByteStride(val)

# end class


class TriStrip(QEntity):
    def __init__(self, parent_entity):
        super(TriStrip, self).__init__(parent_entity)
        self._mesh = mesh = QGeometryRenderer(parent_entity)
        self._geometry = geo = QGeometry(mesh)

        vertex_buffer = QBuffer(QBuffer.VertexBuffer, geo)
        normal_buffer = QBuffer(QBuffer.VertexBuffer, geo)
        color_buffer = QBuffer(QBuffer.VertexBuffer, geo)

        # Vertices
        v0 = QVector3D(0.0, 0.0, 0.0)
        v1 = QVector3D(2.0, 0.0, 0.0)
        v2 = QVector3D(0.0, 2.0, 0.0)
        v3 = QVector3D(2.0, 2.0, 0.0)
        vertices = [v0, v1, v2, v3]
        vertex_bytes = bytes()
        for v in vertices:
            vertex_bytes += struct.pack('f', v.x())
            vertex_bytes += struct.pack('f', v.y())
            vertex_bytes += struct.pack('f', -v.z())
        vertex_bytearray = QByteArray(vertex_bytes)
        vertex_buffer.setData(vertex_bytearray)

        # Faces Normals
        n012 = QVector3D.normal(v0, v1, v2)
        # n123 = QVector3D.normal(v1, v2, v3)
        # print(n012, n123)
        # Vertex Normals
        # n0 = QVector3D(n012 + n123).normalized()
        # n1 = QVector3D(n012 + n123).normalized()
        # n2 = QVector3D(n012 + n123).normalized()
        # n3 = QVector3D(n012 + n123).normalized()
        # normals = [n012, n012, n123, n123]
        # print(n0, n1, n2, n3)
        normals = [n012, n012, n012]
        normal_bytes = bytes()
        for n in normals:
            normal_bytes += struct.pack('f', n.x())
            normal_bytes += struct.pack('f', n.y())
            normal_bytes += struct.pack('f', n.z())

        normal_bytearray = QByteArray(normal_bytes)
        normal_buffer.setData(normal_bytearray)

        c0 = QVector3D(1.0, 0.0, 0.0)
        c1 = QVector3D(0.0, 1.0, 0.0)
        c2 = QVector3D(0.0, 0.0, 1.0)
        colors = [c0, c1, c2]

        color_bytes = bytes()
        for c in colors:
            color_bytes += struct.pack('f', c.x())
            color_bytes += struct.pack('f', c.y())
            color_bytes += struct.pack('f', c.z())
            # color_bytes += struct.pack('!f', c.w())
        color_bytearray = QByteArray(color_bytes)
        color_buffer.setData(color_bytearray)

        # interleave = [v0, v1, n01, c0, v2, v3, n23, c1, v4, v5, n45, c2]
        # interleave = [v0, n01, c0, v1, n01, c0, v2, n23, c1, v3, n23, c1, v4, n45, c2, v5, n45, c2]
        # vertices = interleave

        # element_size = 3 + 4  # vec3 pos, vec4 col
        # float_size = 1  # len(struct.pack('!f', 1.0))  # 4
        # stride = element_size * float_size
        # Attributes
        self._pos_attr = pos_attr = QAttribute()
        pos_attr.setAttributeType(QAttribute.VertexAttribute)
        pos_attr.setBuffer(vertex_buffer)
        pos_attr.setVertexBaseType(QAttribute.Float)
        pos_attr.setVertexSize(3)
        pos_attr.setByteOffset(0)
        pos_attr.setByteStride(3)
        pos_attr.setCount(28)
        pos_attr.setName(QAttribute.defaultPositionAttributeName())

        self._norm_attr = norm_attr = QAttribute()
        norm_attr.setAttributeType(QAttribute.VertexAttribute)
        norm_attr.setBuffer(normal_buffer)
        norm_attr.setVertexBaseType(QAttribute.Float)
        norm_attr.setVertexSize(3)
        norm_attr.setByteOffset(0)
        norm_attr.setByteStride(3)
        norm_attr.setCount(28)
        norm_attr.setName(QAttribute.defaultNormalAttributeName())

        self._col_attr = col_attr = QAttribute()
        col_attr.setAttributeType(QAttribute.VertexAttribute)
        col_attr.setBuffer(color_buffer)
        col_attr.setVertexBaseType(QAttribute.Float)
        col_attr.setVertexSize(3)
        col_attr.setByteOffset(0)
        col_attr.setByteStride(3)
        col_attr.setCount(28)
        col_attr.setName(QAttribute.defaultColorAttributeName())

        # idx_buffer = QBuffer(QBuffer.IndexBuffer, geo)
        # idx_bytes = bytes()
        # idx_bytes += struct.pack('H', 0)
        # idx_bytes += struct.pack('H', 1)
        # idx_bytes += struct.pack('H', 2)
        # idx_bytes += struct.pack('H', 3)
        # idx_bytearray = QByteArray(idx_bytes)
        # idx_buffer.setData(idx_bytearray)
        # idx_attr = QAttribute()
        # idx_attr.setAttributeType(QAttribute.IndexAttribute)
        # idx_attr.setBuffer(idx_buffer)
        # idx_attr.setVertexBaseType(QAttribute.UnsignedShort)
        # idx_attr.setVertexSize(1)
        # idx_attr.setByteOffset(0)
        # idx_attr.setByteStride(2)
        # idx_attr.setCount(4)

        geo.addAttribute(pos_attr)
        geo.addAttribute(norm_attr)
        geo.addAttribute(col_attr)
        # geo.addAttribute(idx_attr)

        # mesh.setPrimitiveRestartEnabled(True)

        mesh.setFirstInstance(0)
        mesh.setFirstVertex(0)
        mesh.setInstanceCount(1)
        # mesh.setVerticesPerPatch(3)
        # mesh.setVertexCount(6)
        mesh.setGeometry(geo)
        mesh.setPrimitiveType(QGeometryRenderer.Points)

        trans = QTransform()
        mat = QPerVertexColorMaterial(parent_entity)

        self.addComponent(mesh)
        self.addComponent(trans)
        self.addComponent(mat)
    # end def

    def setPosVertexSize(self, val):
        self._pos_attr.setVertexSize(val)

    def setPosByteOffset(self, val):
        self._pos_attr.setByteOffset(val)

    def setPosByteStride(self, val):
        self._pos_attr.setByteStride(val)

    def setPosCount(self, val):
        self._pos_attr.setPosCount(val)

    def setColVertexSize(self, val):
        self._col_attr.setVertexSize(val)

    def setColByteOffset(self, val):
        self._col_attr.setByteOffset(val)

    def setColByteStride(self, val):
        self._col_attr.setByteStride(val)

    def setColCount(self, val):
        self._col_attr.setCount(val)

    def setByteStride(self, val):
        self._pos_attr.setByteStride(val)
        # self._norm_attr.setByteStride(val)
        self._col_attr.setByteStride(val)
# end class


class Cube(QEntity):
    """docstring for Cube"""

    def __init__(self, x, y, z, l, w, h, color, parent_entity):
        super(Cube, self).__init__(parent_entity)
        self._x = x
        self._y = y
        self._z = z
        self._l = l
        self._w = w
        self._h = h
        self._color = color
        self._parent_entity = parent_entity
        self._mesh = mesh = QCuboidMesh()
        self._trans = trans = QTransform()
        self._mat = mat = QPhongAlphaMaterial()
        mesh.setXExtent(l)
        mesh.setYExtent(w)
        mesh.setZExtent(h)
        trans.setTranslation(QVector3D(x, y, z))
        mat.setDiffuse(getColorObj(color))
        mat.setAlpha(0.25)
        self.addComponent(mesh)
        self.addComponent(trans)
        self.addComponent(mat)
    # end def

    def setAlpha(self, value):
        self._mat.setAlpha(value)
    # end def
# end class


class TetrahedronMesh(QEntity):
    """docstring for TetrahedronMesh"""

    def __init__(self, x, y, z, parent_entity):
        super(TetrahedronMesh, self).__init__(parent_entity)
        self._x = x
        self._y = y
        self._z = -z
        self._parent_entity = parent_entity

        self._mesh = mesh = QGeometryRenderer(parent_entity)
        self._geometry = geo = QGeometry(mesh)

        vertex_buffer = QBuffer(QBuffer.VertexBuffer, geo)
        idx_buffer = QBuffer(QBuffer.IndexBuffer, geo)

        # Vertices
        v0 = QVector3D(-1.0, 0.0, -1.0)
        v1 = QVector3D(1.0, 0.0, -1.0)
        v2 = QVector3D(0.0, 1.0, 0.0)
        v3 = QVector3D(0.0, 0.0, 1.0)

        # Faces Normals
        n023 = QVector3D.normal(v0, v2, v3)  # 0.816, -0.408, -0.408
        n012 = QVector3D.normal(v0, v1, v2)  # 0.0, -0.707,  0.707
        n310 = QVector3D.normal(v3, v1, v0)  # 0.0, 1.0, 0.0
        n132 = QVector3D.normal(v1, v3, v2)  # -0.816, -0.408, -0.408

        # Vector Normals
        n0 = QVector3D(n023 + n012 + n310).normalized()  # 0.931, -0.132, 0.341
        n1 = QVector3D(n132 + n012 + n310).normalized()  # -0.931, -0.132, 0.341
        n2 = QVector3D(n132 + n012 + n023).normalized()  # 0.0, -0.997, -0.072
        n3 = QVector3D(n132 + n310 + n023).normalized()  # 0.0, 0.219, -0.976

        # Colors
        c0 = QVector3D(1.0, 0.0, 0.0, 1.0)  # red
        c1 = QVector3D(0.0, 1.0, 0.0, 1.0)  # green
        c2 = QVector3D(0.0, 0.0, 1.0, 1.0)  # blue
        c3 = QVector3D(1.0, 1.0, 1.0, 1.0)  # white

        vertices = [v0, n0, c0, v1, n1, c1, v2, n2, c2, v3, n3, c3]
        # vertices = [v0, v1, v2, v3]
        # normals = [n0, n1, n2, n3]
        # colors = [c0, c1, c2, c3]

        vert_bytes = bytes()
        for v in vertices:
            vert_bytes += struct.pack('f', v.x())
            vert_bytes += struct.pack('f', v.y())
            vert_bytes += struct.pack('f', v.z())
            if isinstance(v, QVector4D):
                print("Color", v)
                vert_bytes += struct.pack('f', v.w())

        # See if we can unpack our stored values
        # i = 0
        # vals = []
        # for val in struct.iter_unpack('!f', vert_bytes):
        #     vals.append(val[0])
        #     i += 1
        #     if i % 9 == 0:
        #         print(vals)
        #         vals = []

        vertex_bytearray = QByteArray(vert_bytes)
        print("vertex_bytearray size", vertex_bytearray.size())
        vertex_buffer.setData(vertex_bytearray)

        idx_bytes = bytes()
        # Front
        idx_bytes += struct.pack('H', 0)
        idx_bytes += struct.pack('H', 1)
        idx_bytes += struct.pack('H', 2)
        # Bottom
        idx_bytes += struct.pack('H', 3)
        idx_bytes += struct.pack('H', 1)
        idx_bytes += struct.pack('H', 0)
        # Left
        idx_bytes += struct.pack('H', 0)
        idx_bytes += struct.pack('H', 2)
        idx_bytes += struct.pack('H', 3)
        # Right
        idx_bytes += struct.pack('H', 1)
        idx_bytes += struct.pack('H', 3)
        idx_bytes += struct.pack('H', 2)

        idx_bytearray = QByteArray(idx_bytes)
        print("idx_bytearray size", idx_bytearray.size())
        idx_buffer.setData(idx_bytearray)

        float_size = len(struct.pack('f', 1.0))  # 4
        ushort_size = len(struct.pack('H', 1))  # 2

        # Attributes
        pos_attr = QAttribute()
        pos_attr.setAttributeType(QAttribute.VertexAttribute)
        pos_attr.setBuffer(vertex_buffer)
        pos_attr.setVertexBaseType(QAttribute.Float)
        pos_attr.setVertexSize(3)
        pos_attr.setByteOffset(0)
        pos_attr.setByteStride(9)
        # pos_attr.setByteStride(9 * float_size)
        pos_attr.setCount(4)
        pos_attr.setName(QAttribute.defaultPositionAttributeName())

        norm_attr = QAttribute()
        norm_attr.setAttributeType(QAttribute.VertexAttribute)
        norm_attr.setBuffer(vertex_buffer)
        norm_attr.setVertexBaseType(QAttribute.Float)
        norm_attr.setVertexSize(3)
        norm_attr.setByteOffset(3 * float_size)
        norm_attr.setByteStride(9)
        # norm_attr.setByteStride(9 * float_size)
        norm_attr.setCount(4)
        norm_attr.setName(QAttribute.defaultNormalAttributeName())

        col_attr = QAttribute()
        col_attr.setAttributeType(QAttribute.VertexAttribute)
        col_attr.setBuffer(vertex_buffer)
        col_attr.setVertexBaseType(QAttribute.Float)
        col_attr.setVertexSize(3)
        col_attr.setByteOffset(6 * float_size)
        col_attr.setByteStride(9)
        # col_attr.setByteStride(9 * float_size)
        col_attr.setCount(12)
        col_attr.setName(QAttribute.defaultColorAttributeName())

        idx_attr = QAttribute()
        idx_attr.setAttributeType(QAttribute.IndexAttribute)
        idx_attr.setBuffer(idx_buffer)
        idx_attr.setVertexBaseType(QAttribute.UnsignedShort)
        idx_attr.setVertexSize(1)
        idx_attr.setByteOffset(0)
        idx_attr.setByteStride(ushort_size)
        idx_attr.setCount(12)

        # See if we can unpack our stored values
        # i = 0
        # vals = []
        # for val in struct.iter_unpack('!f', pos_attr.buffer().data()):
        #     vals.append(val[0])
        #     i += 1
        #     if i % 9 == 0:
        #         print(vals)
        #         vals = []

        geo.addAttribute(pos_attr)
        geo.addAttribute(norm_attr)
        geo.addAttribute(col_attr)
        geo.addAttribute(idx_attr)

        mesh.setFirstInstance(0)
        mesh.setFirstVertex(0)
        mesh.setInstanceCount(1)
        mesh.setPrimitiveType(QGeometryRenderer.Triangles)
        mesh.setVertexCount(4)
        mesh.setGeometry(geo)

        trans = QTransform()
        trans.setTranslation(QVector3D(x, y, -z))
        mat = QPerVertexColorMaterial(parent_entity)

        self.addComponent(mesh)
        self.addComponent(trans)
        self.addComponent(mat)
    # end def
# end class


class LineSegment(QEntity):
    def __init__(self, parent_entity):
        super(LineSegment, self).__init__(parent_entity)

        v0 = QVector3D(0.0, 0.0, 0.0)
        v1 = QVector3D(1.0, 1.0, 0.0)

        self._mesh = mesh = QGeometryRenderer(parent_entity)
        self._geometry = geo = QGeometry(mesh)

        vertex_buffer = QBuffer(QBuffer.VertexBuffer, geo)

        vertices = [v0, v1]
        # vertices = [v3]
        vert_bytes = bytes()
        for v in vertices:
            vert_bytes += struct.pack('f', v.x())
            vert_bytes += struct.pack('f', v.y())
            vert_bytes += struct.pack('f', v.z())

        vertex_bytearray = QByteArray(vert_bytes)
        vertex_buffer.setData(vertex_bytearray)

        # float_size = len(struct.pack('!f', 1.0))  # 4

        # Attributes
        pos_attr = QAttribute()
        pos_attr.setAttributeType(QAttribute.VertexAttribute)
        pos_attr.setBuffer(vertex_buffer)
        pos_attr.setVertexBaseType(QAttribute.Float)
        pos_attr.setVertexSize(3)
        pos_attr.setByteOffset(0)
        pos_attr.setByteStride(3)
        pos_attr.setCount(2)
        pos_attr.setName(QAttribute.defaultPositionAttributeName())

        col_attr = QAttribute()
        col_attr.setAttributeType(QAttribute.VertexAttribute)
        col_attr.setBuffer(vertex_buffer)
        # col_attr.setVertexBaseType(QAttribute.Float)
        # col_attr.setVertexSize(3)
        # col_attr.setByteOffset(0)
        # col_attr.setByteStride(9)
        col_attr.setCount(4)
        col_attr.setName(QAttribute.defaultColorAttributeName())

        geo.addAttribute(pos_attr)
        geo.addAttribute(col_attr)

        mesh.setFirstInstance(0)
        mesh.setFirstVertex(0)
        mesh.setInstanceCount(4)
        mesh.setPrimitiveType(QGeometryRenderer.Lines)
        # mesh.setVertexCount(4)
        mesh.setGeometry(geo)

        trans = QTransform()
        mat = QPerVertexColorMaterial(parent_entity)

        self.addComponent(mesh)
        self.addComponent(trans)
        self.addComponent(mat)
    # end def
# end class


_CYLINDER_RADIUS = 1.0
_CYLINDER_RINGS = 20
_CYLINDER_SLICES = 10


class Cylinder(QEntity):
    """docstring for Cube"""

    def __init__(self, x, y, z, length, color, parent_entity):
        super(Cylinder, self).__init__(parent_entity)
        self._x = x
        self._y = y
        self._z = -z
        self._length = length
        self._color = color
        self._parent_entity = parent_entity
        self._mesh = mesh = QCylinderMesh()
        self._trans = trans = QTransform()
        self._mat = mat = QGoochMaterial()
        self._mat = mat = QPhongAlphaMaterial()
        mat.setAlpha(0.5)

        # mat.setCool(getColorObj("#0000cc"))
        # mat.setWarm(getColorObj("#cccc00"))

        mesh.setRadius(_CYLINDER_RADIUS)
        mesh.setRings(_CYLINDER_RINGS)
        mesh.setSlices(_CYLINDER_SLICES)
        mesh.setLength(length)

        trans.setTranslation(QVector3D(x, y, -z))
        trans.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), 90.0))

        # print(mat.cool().name(), mat.warm().name())
        mat.setDiffuse(getColorObj(color))

        self.addComponent(mesh)
        self.addComponent(trans)
        self.addComponent(mat)


_SPHERE_RINGS = 16
_SPHERE_SLICES = 16


class Sphere(QEntity):
    """docstring for Cube"""

    def __init__(self, x, y, z, color, parent_entity, radius=0.25):
        super(Sphere, self).__init__(parent_entity)
        self._x = x
        self._y = y
        self._z = -z
        self._parent_entity = parent_entity

        self._mesh = mesh = QSphereMesh()
        self._trans = trans = QTransform()
        self._mat = mat = QGoochMaterial()
        self._color = color

        mat.setCool(getColorObj(color))
        mat.setWarm(getColorObj(color))

        mesh.setRings(_SPHERE_RINGS)
        mesh.setSlices(_SPHERE_SLICES)
        mesh.setRadius(radius)

        trans.setTranslation(QVector3D(x, y, -z))

        self.addComponent(mesh)
        self.addComponent(trans)
        self.addComponent(mat)
    # end def
# end class


class Points(QEntity):
    def __init__(self, points, color_str, parent_entity):
        super(Points, self).__init__(parent_entity)

        color_obj = getColorObj(color_str)
        self._mesh = mesh = QGeometryRenderer(parent_entity)
        self._geometry = geo = QGeometry(mesh)

        vertex_buffer = QBuffer(QBuffer.VertexBuffer, geo)
        color_buffer = QBuffer(QBuffer.VertexBuffer, geo)

        vertices = []
        for p in points:
            vertices.append(QVector3D(p[0], p[1], p[2]))

        vertex_bytes = bytes()
        for v in vertices:
            vertex_bytes += struct.pack('f', v.x())
            vertex_bytes += struct.pack('f', v.y())
            vertex_bytes += struct.pack('f', -v.z())

        vertex_bytearray = QByteArray(vertex_bytes)
        vertex_buffer.setData(vertex_bytearray)

        color_bytes = bytes()
        cr, cg, cb, calpha = color_obj.getRgbF()
        for c in range(len(vertices)):
            color_bytes += struct.pack('f', cr)
            color_bytes += struct.pack('f', cg)
            color_bytes += struct.pack('f', cb)
            # color_bytes += struct.pack('!f', c.w())
        color_bytearray = QByteArray(color_bytes)
        color_buffer.setData(color_bytearray)

        self._pos_attr = pos_attr = QAttribute()
        pos_attr.setAttributeType(QAttribute.VertexAttribute)
        pos_attr.setBuffer(vertex_buffer)
        pos_attr.setVertexBaseType(QAttribute.Float)
        pos_attr.setVertexSize(3)
        pos_attr.setByteOffset(0)
        pos_attr.setByteStride(3)
        pos_attr.setCount(len(vertices))
        pos_attr.setName(QAttribute.defaultPositionAttributeName())

        self._col_attr = col_attr = QAttribute()
        col_attr.setAttributeType(QAttribute.VertexAttribute)
        col_attr.setBuffer(color_buffer)
        col_attr.setVertexBaseType(QAttribute.Float)
        col_attr.setVertexSize(3)
        col_attr.setByteOffset(0)
        col_attr.setByteStride(3)
        col_attr.setCount(len(vertices))
        col_attr.setName(QAttribute.defaultColorAttributeName())

        geo.addAttribute(pos_attr)
        geo.addAttribute(col_attr)

        mesh.setFirstInstance(0)
        mesh.setFirstVertex(0)
        mesh.setInstanceCount(1)
        mesh.setGeometry(geo)
        mesh.setPrimitiveType(QGeometryRenderer.Points)

        trans = QTransform()
        mat = QPerVertexColorMaterial(parent_entity)

        self.addComponent(mesh)
        self.addComponent(trans)
        self.addComponent(mat)
    # end def

    def setPosVertexSize(self, val):
        self._pos_attr.setVertexSize(val)

    def setPosByteOffset(self, val):
        self._pos_attr.setByteOffset(val)

    def setPosByteStride(self, val):
        self._pos_attr.setByteStride(val)

    def setPosCount(self, val):
        self._pos_attr.setPosCount(val)

    def setColVertexSize(self, val):
        self._col_attr.setVertexSize(val)

    def setColByteOffset(self, val):
        self._col_attr.setByteOffset(val)

    def setColByteStride(self, val):
        self._col_attr.setByteStride(val)

    def setColCount(self, val):
        self._col_attr.setCount(val)

    def setByteStride(self, val):
        self._pos_attr.setByteStride(val)
        # self._norm_attr.setByteStride(val)
        self._col_attr.setByteStride(val)

# end class
