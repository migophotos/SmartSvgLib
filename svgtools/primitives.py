from abc import abstractmethod, ABCMeta
from dataclasses import dataclass
from math import pi, sin, cos
import json


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: float = 0, y: float = 0):
        self.x: float = 0
        self.y: float = 0

    # def __post_init__(self, x: float = 0, y: float = 0):
    #     self.x = x
    #     self.y = y

    def __str__(self) -> str:
        return f'{self.x} {self.y}'

    def __repr__(self) -> str:
        return f'Point: x: {self.x}, y: {self.y}'

    def to_string(self):
        print(f'({self.x}, {self.y})')
        return self

    def to_dict(self):
        return {'x': self.x, 'y': self.y}

    def to_list(self):
        return [self.x, self.y]

    def get_point(self):
        return self.x, self.y

    def set_point(self, x, y):
        self.x = x
        self.y = y
        return self

    def move(self, dx: float = 0, dy: float = 0):
        self.x += dx
        self.y += dy
        return self

    def offset(self, dx: float = 0, dy: float = 0):
        return self.move(dx, dy)

    def rotate(self):
        self.x, self.y = self.y, self.x
        return self


class Rect(object):
    __slots__ = ("pt", "width", "height")

    def __init__(self, x=0, y=0, width=0, height=0):
        self.pt = Point(x, y)
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f'{self.pt.x} {self.pt.y} {self.width} {self.height}'

    def __repr__(self) -> str:
        return f'Rect: x: {self.pt.x}, y: {self.pt.y}, width:{self.width}, height:{self.height}'

    def to_attr_string(self):
        return f'x="{self.pt.x}"y="{self.pt.y}"width="{self.width}"height="{self.height}"'

    def to_dict(self):
        return {'x': self.pt.x, 'y': self.pt.y, 'width': self.width, 'height': self.height}

    def to_list(self):
        return [self.pt.x, self.pt.y, self.width, self.height]

    def from_coord(self, x1, y1, x2, y2):
        self.pt = Point(x1, y1)
        self.width = x2 - self.pt.x
        self.height = y2 - self.pt.y
        return self

    def to_coord(self):
        x1 = self.pt.x
        y1 = self.pt.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        return x1, y1, x2, y2

    def set_rect(self, x, y, width, height):
        self.pt.set_point(x, y)
        self.width = width
        self.height = height
        return self

    def set_size(self, width: int = None, height: int = None):
        self.width = self.width if width is None else width
        self.height = self.height if height is None else height
        return self

    def set_width(self, width):
        return self.set_size(width=width)

    def set_height(self, height):
        return self.set_size(height=height)

    def move(self, dx: float = 0, dy: float = 0):
        return self.pt.move(dx, dy)

    def offset(self, dx: float = 0, dy: float = 0):
        return self.pt.offset(dx, dy)


class DefsSection:
    def __init__(self):
        pass

    def __str__(self):
        return self.to_svg()

    @staticmethod
    def to_svg():
        defs_str = "<defs>\n"
        filters_str = ''
        with open("svgtools/filters.txt", "r") as filters:
            filters_str += filters.read()
        with open("svgtools/gradients.txt", "r") as gradients:
            filters_str += gradients.read()
        defs_str += f"{filters_str}</defs>\n"
        return defs_str


class SvgElement(object, metaclass=ABCMeta):
    __slots__ = ("id", "class_name", "attributes")

    def __init__(self, id='', class_name='', attrs: list | str = None,
                 fill: str = '', stroke: str = '', stroke_width: float = 0):
        self.id = id
        self.class_name = class_name
        self.attributes = {}

        # self.set_attributes([f'fill:{fill}',
        #                      f'stroke:{stroke}',
        #                      f'stroke-width:{stroke_width}'])

        if attrs is not None:
            if type(attrs) == str:
                self.set_attr_from_json(attrs)
            elif type(attrs) == list:
                self.set_attributes(attrs)

        if fill:
            self.attributes['fill'] = SvgElement.normalize_color_value(fill)
        if stroke:
            self.attributes['stroke'] = SvgElement.normalize_color_value(stroke)
        if stroke_width:
            self.attributes['stroke-width'] = stroke_width

    @staticmethod
    def normalize_color_value(value: str | int) -> str:
        """
            Check and normalize the color value.
            In SVG the color of fill and stroke attributes may be represented as known and predefines string,
            hexadecimal value, rgb string, or keyword 'none'
            :param value - color value tobe validated and converted to string
        """
        if type(value) == str:
            return value
        if type(value) == int:
            return f"#{str(hex(value)).removeprefix('0x')}"

    def set_attributes(self, attr_list: list):
        """ Add/Set additional attributes to svg element
            :param attr_list: list of attributes, represented as a pair of key and value separated by colon
            Example: ['opacity:0.5', 'id:elem-id', 'class_name:hidden']
        """
        for attr_pair in attr_list:
            name, value = attr_pair.split(':')
            if name == 'id':
                self.id = value
                continue
            if name == 'class_name':
                self.class_name = value
                continue

            self.attributes[name] = value

    def set_attr_from_json(self, attr_json: str):
        """
        parce json string such as '{ "name":"John", "age":30, "city":"New York"}' and interpret it as set of parameters
        :param attr_json:
        :return: none
        """
        if attr_json:
            attrs = json.loads(attr_json)
            for name in attrs.keys():
                value = attrs[name]
                if name == 'id':
                    self.id = value
                    continue
                if name == 'class_name':
                    self.class_name = value
                    continue
                self.attributes[name] = value

    def set_id(self, id):
        self.id = id | ''

    def set_class(self, class_name):
        self.class_name = class_name | ''

    def to_attr_string(self):
        attrs_str = ''
        if self.id:
            attrs_str += f'id="{self.id}"'
        if self.class_name:
            attrs_str += f'class="{self.class_name}"'
        for key in self.attributes.keys():
            if key == "opacity" and float(self.attributes[key]) == 1.0:
                continue
            attrs_str += f'{key}="{self.attributes[key]}"'

        return attrs_str

    @abstractmethod
    def get_bound_rect(self):
        ...


class SvgRoot(SvgElement):
    __slots__ = ("is_autobound", "rc", "elements")

    def __init__(self, id: str = '', class_name: str = '', view_box: list = [],
                 attrs: list | str = None, autobound: bool = True):
        super().__init__(id, class_name, attrs)
        self.is_autobound = autobound
        x, y, w, h = view_box
        self.rc = Rect(x, y, w, h)
        self.elements = []

    def __str__(self) -> str:
        return self.to_svg()

    def calc_bound_rect(self):
        left = Point()
        right = Point()

        for el in self.elements:
            rect = el.get_bound_rect()
            x1, y1, x2, y2 = rect.to_coord()
            left.x = x1 if left.x == 0 or x1 < left.x else left.x
            left.y = y1 if left.y == 0 or y1 < left.y else left.y
            right.x = x2 if x2 > right.x else right.x
            right.y = y2 if y2 > right.y else right.y

        rc = Rect().from_coord(left.x, left.y, right.x, right.y)
        if rc.pt.x > 0:
            rc.offset(dx=-rc.pt.x)
        if rc.pt.y > 0:
            rc.offset(dy=-rc.pt.y)
        return rc

    def to_svg(self):
        namespace = 'xmlns="http://www.w3.org/2000/svg"'
        # viewbox = ' '.join(str(element) for element in self.view_box)

        elements = '\n'.join(element.to_svg() for element in self.elements)

        # calculate bound rect
        if self.is_autobound:
            self.rc = self.calc_bound_rect()
        viewbox = str(self.rc)

        defs_section = DefsSection.to_svg()

        return f'<svg {namespace} viewBox="{viewbox}" width="{self.rc.width}" height="{self.rc.height}" {self.to_attr_string()}>\n{defs_section}{elements}</svg>'

    def add_element(self, element):
        self.elements.append(element)

    def add_elements(self, elements: list):
        for element in elements:
            self.elements.append(element)

    def get_bound_rect(self):
        return self.rc


class SvgRect(SvgElement):
    """ SvgRect
        The <rect> element is a basic SVG shape that draws rectangle, defined by their position (x, y)
        and size (width and height)

        :param x: The x coordinate of the rect. Value type <length>|<percentage>;
        :param y: The y coordinate of the rect. Value type <length>|<percentage>;
        :param width: The width of the rect.  Value type auto|<length>|<percentage>;
        :param height: The height of the rect.  Value type auto|<length>|<percentage>;
        :param rx: The horizontal corner radius  of the rect. Defaults to ry if it is specified. Default value: 0;
        :param ry: The horizontal corner radius  of the rect. Defaults to rx if it is specified. Default value: 0;
        :param attrs: attributes in json format string, for ex: '{"attr_name":"attr_value",...}',
                    or comma separated list of strings in form key and value separated by colon
        :param fill: The fill color of the rect. Default value is none
        :param stroke: The color used to paint the outline of the rect. Default value is none
        :param stroke-width: The width of the outline of the rect. Value type <length>|<percentage>; Default value is 1px

        Note: A percentage value is always computed as a percentage of the normalized viewBox diagonal length.
    """
    __slots__ = ("rc", "rx", "ry")

    def __init__(self, x=0, y=0, width=0, height=0, rx=0, ry=0, id='', class_name='',
                 attrs: list | str = None, fill='', stroke='', stroke_width: float | int = 0):
        super().__init__(id, class_name, attrs, fill, stroke, stroke_width)
        self.rc = Rect(x, y, width, height)
        self.rx = rx
        self.ry = ry

    def __str__(self) -> str:
        return self.to_svg()

    def get_bound_rect(self) -> Rect:
        return self.rc

    def set_rect(self, rect: Rect):
        self.rc.set_rect(rect.pt.x, rect.pt.y, rect.width, rect.height)

    def to_svg(self):
        rc_str = self.rc.to_attr_string()

        radius_str = ''
        if self.rx or self.ry:
            if self.rx:
                radius_str = f'rx="{self.rx}"'
            if self.ry:
                radius_str += f'ry="{self.ry}"'
        return f'<rect {rc_str}{radius_str}{self.to_attr_string()}/>'


class SvgLine(SvgElement):
    """ SvgLine
        The <line> element is an SVG basic shape used to create a line connecting two points.
        :param x1:  Defines the x-axis coordinate of the line starting point.
                    Value type: <length>|<percentage>|<number> ; Default value: 0; Animatable: yes
        :param x2:  Defines the x-axis coordinate of the line ending point.
                    Value type: <length>|<percentage>|<number> ; Default value: 0; Animatable: yes
        :param y1:  Defines the y-axis coordinate of the line starting point.
                    Value type: <length>|<percentage>|<number> ; Default value: 0; Animatable: yes
        :param y2:  Defines the y-axis coordinate of the line ending point.
                    Value type: <length>|<percentage>|<number> ; Default value: 0; Animatable: yes
        :param attrs: attributes in json format string, for ex: '{"attr_name":"attr_value",...}',
                    or comma separated list of strings in form key and value separated by colon
        :param fill: The fill color of the rect. Default value is none
        :param stroke: The color used to paint the outline of the rect. Default value is none
        :param stroke-width: The width of the outline of the rect. Value type <length>|<percentage>; Default value is 1px

        Note: A percentage value is always computed as a percentage of the normalized viewBox diagonal length.
    """

    __slots__ = ("x1", "x2", "y1", "y2")

    def __init__(self, x1, x2, y1, y2, id='', class_name='',
                 attrs: list | str = None, fill='', stroke='', stroke_width: float | int = 0):
        super().__init__(id, class_name, attrs, fill, stroke, stroke_width)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def __str__(self) -> str:
        return self.to_svg()

    def __repr__(self):
        return f'Line: x1: {self.x1}, y1: {self.y1}, x2:{self.x2}, y2:{self.y2}{self.to_attr_string()}'

    def get_bound_rect(self):
        rc = Rect().from_coord(self.x1, self.y1, self.x2, self.y2)
        return rc

    def to_svg(self):
        coordinates_str = f'x1="{self.x1}"x2="{self.x2}"y1="{self.y1}"y2="{self.y2}"'
        return f'<line {coordinates_str}{self.to_attr_string()}/>'


class SvgCircle(SvgElement):
    """ SvgCircle
        The <circle> SVG element is an SVG basic shape, used to draw circles based on a center point and a radius.
        cx - The x-axis coordinate of the center of the circle.
             Value type: <length>|<percentage> ; Default value: 0; Animatable: yes
        cy - The y-axis coordinate of the center of the circle.
             Value type: <length>|<percentage> ; Default value: 0; Animatable: yes
        r  - The radius of the circle. A value lower or equal to zero disables rendering of the circle.
             Value type: <length>|<percentage> ; Default value: 0; Animatable: yes
        :param attrs: attributes in json format string, for ex: '{"attr_name":"attr_value",...}',
                    or comma separated list of strings in form key and value separated by colon
        :param fill: The fill color of the rect. Default value is none
        :param stroke: The color used to paint the outline of the rect. Default value is none
        :param stroke-width: The width of the outline of the rect. Value type <length>|<percentage>; Default value is 1px
    """

    __slots__ = ("cx", "cy", "r")

    def __init__(self, cx, cy, r, id='', class_name='',
                 attrs: list | str = None, fill='', stroke='', stroke_width: float | int = 0):
        super().__init__(id, class_name, attrs, fill, stroke, stroke_width)
        self.cx = cx
        self.cy = cy
        self.r = r

    def __str__(self) -> str:
        return self.to_svg()

    def get_bound_rect(self):
        rc = Rect().from_coord(self.cx - self.r, self.cy - self.r, self.cx + self.r, self.cy + self.r)
        return rc

    def to_svg(self):
        return f'<circle cx="{self.cx}"cy="{self.cy}"r="{self.r}"{self.to_attr_string()}/>'


class SvgEllipse(SvgElement):
    """ SvgEllipse
        The <ellipse> element is an SVG basic shape, used to create ellipses based on a center coordinate,
        and both their x and y radius.
        cx - The x-axis coordinate of the center of the circle.
             Value type: <length>; Default value: 0; Animatable: yes
        cy - The y-axis coordinate of the center of the circle.
             Value type: <length>; Default value: 0; Animatable: yes
        rx - The radius of the ellipse on the x-axis.
             Value type: auto|<length>|<percentage> ; Default value: auto; Animatable: yes
        ry - The radius of the ellipse on the y-axis.
             Value type: auto|<length>|<percentage> ; Default value: auto; Animatable: yes
        :param attrs: attributes in json format string, for ex: '{"attr_name":"attr_value",...}',
                    or comma separated list of strings in form key and value separated by colon
        :param fill: The fill color of the rect. Default value is none
        :param stroke: The color used to paint the outline of the rect. Default value is none
        :param stroke-width: The width of the outline of the rect. Value type <length>|<percentage>; Default value is 1px
    """

    __slots__ = ("cx", "cy", "rx", "ry")

    def __init__(self, cx, cy, rx, ry, id='', class_name='',
                 attrs: list | str = None, fill='', stroke='', stroke_width: float | int = 0):
        super().__init__(id, class_name, attrs, fill, stroke, stroke_width)
        self.cx = cx
        self.cy = cy
        self.rx = rx
        self.ry = ry

    def __str__(self) -> str:
        return self.to_svg()

    def get_bound_rect(self):
        rc = Rect().from_coord(self.cx - self.rx, self.cy - self.ry, self.cx + self.rx, self.cy + self.ry)
        return rc

    def to_svg(self):
        return f'<circle cx="{self.cx}"cy="{self.cy}"rx="{self.rx}"ry="{self.ry}"{self.to_attr_string()}/>'


class SvgFigure(SvgElement):
    """ SvgFigure
        Draw A polygon with a given number of corners, or a star. The number of corners can be anything, starting from 3
        :param cx: The x-axis coordinate of the center of the outer circle.
                    Value type: <length>;
        :param cy: The y-axis coordinate of the center of the outer circle.
                    Value type: <length>;
        :param r_out: radius of a circle enclosing a polygonl; Value type: <float>
        :param r_inner: inner radius, as a percentage of outer, to display a star, instead of a polygon;
                    Value type: <percentage> from 0 utto 100
        :param angels_count: Number of star or polygon vertices; Value type: <number>
        :param attrs: attributes in json format string, for ex: '{"attr_name":"attr_value",...}',
                    or comma separated list of strings in form key and value separated by colon
        :param fill: The fill color of the rect. Default value is none
        :param stroke: The color used to paint the outline of the rect. Default value is none
        :param stroke-width: The width of the outline of the rect. Value type <length>|<percentage>; Default value is 1px

        Note: A percentage value is always computed as a percentage of the normalized viewBox diagonal length.
    """

    __slots__ = ("cx", "cy", "r_out", "r_inner_pct", "angels", "start_angle", "rotation")

    def __init__(self, cx, cy, r_out, r_inner, angels_count, start_angle=0, rotation=0,
                 id='', class_name='', attrs: list | str = None, fill='', stroke='', stroke_width: float | int = 0):
        super().__init__(id, class_name, attrs, fill, stroke, stroke_width)

        self.cx = cx
        self.cy = cy
        self.r_out = r_out
        self.r_inner_pct = r_inner
        self.angels = angels_count
        self.start_angle = start_angle
        self.rotation = rotation

    def __str__(self) -> str:
        return self.to_svg()

    def get_bound_rect(self):
        rc = Rect().from_coord(self.cx - self.r_out, self.cy - self.r_out, self.cx + self.r_out, self.cy + self.r_out)
        return rc

    def to_svg(self):
        path = self.build_figure(counterclockwise=0)
        return f'<polygon points="{path}"{self.to_attr_string()}/>'

    def build_figure(self, counterclockwise=0):
        start_angle = self.start_angle / 2 if self.r_inner_pct else self.start_angle
        angels_count = self.angels * 2 if self.r_inner_pct else self.angels

        start_angle_rad = ((start_angle + self.rotation) * pi) / 180
        # self.start_angle = ((self.start_angle + self.rotation) * pi) / 180   # convert degrees to radians
        inner_radius = (self.r_out / 100) * self.r_inner_pct

        points = ''
        if self.r_inner_pct:
            points += f'{self.cx + inner_radius * sin(start_angle_rad)}, ' \
                      f'{self.cy - inner_radius * cos(start_angle_rad)}'
        else:
            points += f'{self.cx + self.r_out * sin(start_angle_rad)}, ' \
                      f'{self.cy - self.r_out * cos(start_angle_rad)}'

        delta = (2 * pi) / angels_count

        for i in range(1, angels_count):
            if counterclockwise:
                start_angle_rad += -delta
            else:
                start_angle_rad += delta   # correct an angle
            if self.r_inner_pct:
                if i % 2:
                    points += f' {self.cx + self.r_out * sin(start_angle_rad)},' \
                              f'{self.cy - self.r_out * cos(start_angle_rad)}'
                else:
                    points += f' {self.cx + inner_radius * sin(start_angle_rad)},' \
                              f'{self.cy - inner_radius * cos(start_angle_rad)}'
            else:
                points += f' {self.cx + self.r_out * sin(start_angle_rad)},' \
                          f'{self.cy - self.r_out * cos(start_angle_rad)}'

        return points


class SvgText(SvgElement):
    __slots__ = ("rc", "text")

    def __init__(self, x, y, width, height, text: str = '', id: str = '', class_name: str = '', attrs: str | list = [],
                 fill: str = '', stroke: str = '', stroke_width: float = 0 ):
        super().__init__(id, class_name, attrs, fill, stroke, stroke_width)
        self.rc = Rect(x, y, width, height)
        self.text = text

    def __str__(self) -> str:
        return self.to_svg()

    def to_svg(self):
        coordinates_str = f'x1="{self.x1}"x2="{self.x2}"y1="{self.y1}"y2="{self.y2}"'
        return f'<line {coordinates_str}{self.to_attr_string()}/>'

    def get_bound_rect(self):
        return self.rc

