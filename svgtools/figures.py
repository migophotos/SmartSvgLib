from abc import abstractmethod, ABCMeta
from svgtools.primitives import Point, Rect, DefsSection, SvgRect, SvgLine, SvgText, SvgCircle, SvgEllipse, SvgFigure
from svgtools.smartarray import SmartArray


class SmartWidget(metaclass=ABCMeta):
    __slots__ = ("id", "class_name", "min_value", "max_value", "thresholds", "bound_rect")

    def __init__(self, id: str = '', class_name: str = ''):
        self.id = id
        self.class_name = class_name
        self.min_value: float = float(0)
        self.max_value: float = float(100)
        self.thresholds = SmartArray()
        self.bound_rect = SvgRect(attrs='{"display":"none"}')

    @abstractmethod
    def build_ctrl(self):
        ...

    def build_id(self, name: str):
        return f"{self.id}-{name}"

    def set_bound_rect(self, rect: Rect):
        self.bound_rect.set_rect(rect)

    def set_min_value(self, value: float | int):
        self.min_value = float(value)

    def set_max_value(self, value: float | int):
        self.max_value = float(value)

    def set_thresholds(self, thresholds: dict):
        self.thresholds.from_dict(thresholds)


class SmartBulb(SmartWidget):
    __slots__ = ("is_3d", "is_web_component", "body", "active", "cx", "cy", "r", "body_color", "body_width")

    def __init__(self, cx, cy, r, id: str = '',
                 body_color="black", body_width=0, is_3d: bool = True, is_web_component: bool = False):
        super().__init__(id, class_name='SmartBulb')

        self.is_3d = is_3d
        self.is_web_component = is_web_component
        self.body = None
        self.active = None
        self.cx = cx
        self.cy = cy
        self.r = r
        self.body_color = body_color
        self.body_width = body_width

        self.build_ctrl()

    def build_ctrl(self):
        self.body = SvgCircle(cx=self.cx, cy=self.cy, r=self.r, id=self.build_id("body"),
                              attrs='{"fill":"none", "stroke":"none", "stroke-width":"0", "pointer-events":"none"}')
        self.active = SvgCircle(cx=self.cx, cy=self.cy, r=self.r - self.body_width, id=self.build_id("active"),
                                stroke=self.body_color, stroke_width=self.body_width)
        self.set_bound_rect(self.body.get_bound_rect())
        self.set_state(5)  # default state (no value)

    def __str__(self) -> str:
        return self.to_svg()

    def get_bound_rect(self):
        return self.bound_rect.get_bound_rect()

    def to_svg(self):
        svg_str = ''
        if self.is_web_component:
            pass
        else:
            svg_str += f'<g id="{self.id}" class-name="{self.class_name}">\n' \
                f'{self.bound_rect.to_svg()}\n' \
                f'{self.body.to_svg()}\n' \
                f'{self.active.to_svg()}\n' \
                f'</g>\n'
        return svg_str

    def set_value(self, value):
        color = 'black'
        attr_list = []
        if self.is_3d:
            attr_list.append('filter:url(#MyFilter)')
        for index in range(self.thresholds.length()):
            thr = self.thresholds.at(index)
            for trigger in thr:
                if value > trigger:
                    color = thr[trigger]

        attr_list.append(f"fill:{color}")
        self.active.set_attributes(attr_list)

    def set_state(self, state):
        attrs = [f"fill:url(#alert_state_{state})"]
        self.active.set_attributes(attrs)


class SmartBulbGrid:
    __slots__ = ("id", "class_name", "is_3d", "is_web_component", "body_color", "body_width", "bulb_counts",
                 "x", "y", "bulb_radius", "bulb_gap", "direction", "bound_rect", "bulbs")

    def __init__(self, id: str, x=0, y=0, bulb_radius: int = 24, count: int = 2, gap: int = 2, direction: str = 'horizontal',
                 body_color="gray", body_width=1, is_3d: bool = True, is_web_component: bool = False):
        self.id = id
        self.class_name = 'SmartBulbGrid'
        self.is_3d = is_3d
        self.is_web_component = is_web_component
        self.body_color = body_color
        self.body_width = body_width
        self.bulb_counts = count
        self.x = x
        self.y = y
        self.bulb_radius = bulb_radius
        self.bulb_gap = gap
        self.direction = direction

        self.bound_rect = SvgRect(attrs='{"display":"none"}')
        self.bulbs: list = []
        self.build_ctrl()

    def build_ctrl(self):
        cx = self.bulb_radius
        cy = self.bulb_radius
        for index in range(self.bulb_counts):
            offset = (self.bulb_radius * 2 + self.bulb_gap) * index + self.bulb_radius
            if self.direction == "vertical":
                x = self.x + cy
                y = self.y + offset
            else:
                x = self.x + offset
                y = self.y + cy
            bulb = SmartBulb(x, y, self.bulb_radius, id=f"{self.id}-bulb-{index}", body_color=self.body_color,
                             body_width=self.body_width, is_3d=self.is_3d, is_web_component=self.is_web_component)
            bulb.set_state(5)   # default state (no value)
            self.bulbs.append(bulb)

        length = cx * 2 * self.bulb_counts + self.bulb_gap * (self.bulb_counts - 1)
        wide = cy * 2
        if self.direction == "vertical":
            self.bound_rect.set_rect(Rect(0, 0, wide, length))
        else:
            self.bound_rect.set_rect(Rect(0, 0, length, wide))

    def get_bound_rect(self):
        return self.bound_rect.get_bound_rect()

    def set_states(self, states: list):
        for stz in zip(self.bulbs, states):
            stz[0].set_state(stz[1])

    def set_values(self, values: list):
        for vlz in zip(self.bulbs, values):
            vlz[0].set_value(vlz[1])

    def __str__(self):
        return self.to_svg()

    def to_svg(self) -> str:
        if self.is_web_component:
            pass
        else:
            svg_str = f'<g id="{self.id}" class-name="{self.class_name}">\n'
            svg_str += self.bound_rect.to_svg()
            for el in self.bulbs:
                bulb_str = el.to_svg()
                svg_str += bulb_str

            svg_str += f'</g>\n'
        return svg_str


class SmartRect(SmartWidget):
    __slots__ = ("is_3d", "is_web_component", "body", "active", "x", "y", "rx", "ry", "width", "height",
                 "body_color", "body_width")

    def __init__(self, x, y, width, height, rx=0, ry=0, id: str = '',
                 body_color="black", body_width=0, is_3d: bool = True, is_web_component: bool = False):
        super().__init__(id, class_name='SmartRect')
        self.is_3d = is_3d
        self.is_web_component = is_web_component
        self.body = None
        self.active = None
        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry
        self.width = width
        self.height = height
        self.body_color = body_color
        self.body_width = body_width

        self.build_ctrl()

    def build_ctrl(self):
        self.body = SvgRect(self.x, self.y, self.width, self.height, rx=self.rx, ry=self.ry, id=self.build_id("body"),
                            fill=self.body_color, attrs='{"pointer-events":"none"}')
        self.active = SvgRect(self.x + self.body_width, self.y + self.body_width, self.width - self.body_width * 2,
                              self.height - self.body_width * 2, rx=self.rx, ry=self.ry, id=self.build_id("active"))
        self.set_bound_rect(self.body.get_bound_rect())
        self.set_state(5)   # default state (no value)

    def __str__(self) -> str:
        return self.to_svg()

    def get_bound_rect(self):
        return self.bound_rect.get_bound_rect()

    def to_svg(self):
        svg_str = ''
        if self.is_web_component:
            pass
        else:
            svg_str += f'<g id="{self.id}" class-name="{self.class_name}">\n' \
                f'{self.bound_rect.to_svg()}\n' \
                f'{self.body.to_svg()}\n' \
                f'{self.active.to_svg()}\n' \
                f'</g>\n'
        return svg_str

    def set_value(self, value):
        color = 'black'
        attr_list = []
        if self.is_3d:
            attr_list.append('filter:url(#MyFilter)')
        for index in range(self.thresholds.length()):
            thr = self.thresholds.at(index)
            for trigger in thr:
                if value > trigger:
                    color = thr[trigger]

        attr_list.append(f"fill:{color}")
        self.active.set_attributes(attr_list)

    def set_state(self, state):
        attrs = [f"fill:url(#alert_state_{state})"]
        self.active.set_attributes(attrs)


class SmartRectGrid:
    __slots__ = ("id", "class_name", "is_3d", "is_web_component", "body_color", "body_width", "rect_counts",
                 "x", "y", "width", "height", "rx", "ry", "rect_gap", "direction", "bound_rect", "rects")

    def __init__(self, id: str, x, y, width, height, rx=0, ry=0, count: int = 2, gap: int = 2, direction: str = 'horizontal',
                 body_color="gray", body_width=1, is_3d: bool = True, is_web_component: bool = False):
        self.id = id
        self.class_name = 'SmartRectGrid'
        self.is_3d = is_3d
        self.is_web_component = is_web_component
        self.body_color = body_color
        self.body_width = body_width
        self.rect_counts = count
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        self.ry = ry
        self.rect_gap = gap
        self.direction = direction

        self.bound_rect = SvgRect(attrs='{"display":"none"}')
        self.rects: list = []
        self.build_ctrl()

    def build_ctrl(self):
        for index in range(self.rect_counts):
            if self.direction == "vertical":
                x = self.x
                y = (self.height + self.rect_gap) * index + self.y
            else:
                x = (self.width + self.rect_gap) * index + self.x
                y = self.y

            rect = SmartRect(x, y, self.width, self.height, rx=self.rx, ry=self.ry, id=f"{self.id}-rect-{index}",
                             body_color=self.body_color, body_width=self.body_width,
                             is_3d=self.is_3d, is_web_component=self.is_web_component)
            rect.set_state(5)   # default state (no value)
            self.rects.append(rect)

        if self.direction == "vertical":
            length = (self.height * self.rect_counts) + self.rect_gap * (self.rect_counts - 1)
            self.bound_rect.set_rect(Rect(self.x, self.y, self.width, length))
        else:
            length = (self.width * self.rect_counts) + self.rect_gap * (self.rect_counts - 1)
            self.bound_rect.set_rect(Rect(self.x, self.y, length, self.height))

    def get_bound_rect(self):
        return self.bound_rect.get_bound_rect()

    def set_states(self, states: list):
        for stz in zip(self.rects, states):
            stz[0].set_state(stz[1])

    def set_values(self, values: list):
        for vlz in zip(self.rects, values):
            vlz[0].set_value(vlz[1])

    def __str__(self):
        return self.to_svg()

    def to_svg(self) -> str:
        if self.is_web_component:
            pass
        else:
            svg_str = f'<g id="{self.id}" class-name="{self.class_name}">\n'
            svg_str += self.bound_rect.to_svg()
            for el in self.rects:
                svg_str += el.to_svg()

            svg_str += f'</g>\n'
        return svg_str


