from abc import abstractmethod, ABCMeta
from typing import Dict, overload

from svgtools.primitives import Point, Rect, DefsSection, SvgElement, SvgRect, SvgLine, SvgText, SvgCircle, SvgEllipse, SvgFigure
from svgtools.smartarray import SmartArray


class SmartWidget(SvgElement, metaclass=ABCMeta):
    __slots__ = ("id", "class_name", "min_value", "max_value", "thresholds", "bound_rect")

    def __init__(self, id: str = '', class_name: str = ''):
        super().__init__(id, class_name)
        self.min_value: float = float(0)
        self.max_value: float = float(100)
        self.thresholds = dict()
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

    def set_thresholds(self, thr_str: str | dict):
        self.thresholds = dict()

        if type(thr_str) == dict:
            self.thresholds = thr_str.copy()
        else:
            thr_str = thr_str.removeprefix('{')
            thr_str = thr_str.removesuffix('}')

            thr_a = thr_str.split(",")
            for thr in thr_a:
                v, c = thr.split(":")
                self.thresholds.update({int(v):c})

        self.set_attributes([f'thr:{self.thresholds.__str__()}'])


class SmartBulb(SmartWidget):
    __slots__ = ("is_3d", "is_web_comp", "body", "active", "cx", "cy", "r", "body_color", "body_width")

    def __init__(self, cx, cy, r, id: str = '',
                 body_color="black", body_width=0, is_3d: bool = True, is_web_comp: bool = False):
        super().__init__(id, class_name='SmartBulb')

        self.is_3d = is_3d
        self.is_web_comp = is_web_comp
        self.body = None
        self.active = None
        self.cx = cx
        self.cy = cy
        self.r = r
        self.body_color = body_color
        self.body_width = body_width

        self.build_ctrl()
        self.set_attributes([
            f'is_3d:{is_3d}',
            f'is_web_comp:{is_web_comp}',
            f'w_r:{r}',
            f'body_color:{body_color}',
            f'body_width:{body_width}',
            f'thr:{self.thresholds}'
        ])

    def build_ctrl(self):
        self.body = SvgCircle(cx=self.cx, cy=self.cy, r=self.r, fill="none", attrs='{"pointer-events":"none"}')
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
        if self.is_web_comp:
            pass
        else:
            svg_str += f'<g {self.to_attr_string()}>\n' \
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

        for v in self.thresholds:
            if value > v:
                color = self.thresholds[v]

        attr_list.append(f"fill:{color}")
        self.active.set_attributes(attr_list)

    def set_state(self, state):
        attrs = [f"fill:url(#alert_state_{state})"]
        self.active.set_attributes(attrs)


class SmartBulbGrid(SmartWidget):
    __slots__ = ("id", "class_name", "is_3d", "is_web_comp", "body_color", "body_width", "bulb_counts",
                 "x", "y", "bulb_radius", "bulb_gap", "orient", "bound_rect", "bulbs")

    def __init__(self, id: str, x=0, y=0, bulb_radius: int = 24, count: int = 2, gap: int = 2, orient: str = 'hor',
                 body_color="gray", body_width=1, is_3d: bool = True, is_web_comp: bool = False):
        super().__init__(id=id, class_name="'SmartBulbGrid'")
        self.is_3d = is_3d
        self.is_web_comp = is_web_comp
        self.body_color = body_color
        self.body_width = body_width
        self.bulb_counts = count
        self.x = x
        self.y = y
        self.bulb_radius = bulb_radius
        self.bulb_gap = gap
        self.orient = orient

        self.bound_rect = SvgRect(attrs='{"display":"none"}')
        self.bulbs: list = []
        self.build_ctrl()
        self.set_attributes([
            f'is_3d:{is_3d}',
            f'is_web_comp:{is_web_comp}',
            f'count:{count}',
            f'orient:{orient}',
            f'body_color:{body_color}',
            f'body_width:{body_width}',
            f'bulb_radius:{bulb_radius}',
            f'gap:{gap}',
            f'thr:{self.thresholds}'
        ])

    def build_ctrl(self):
        cx = self.bulb_radius
        cy = self.bulb_radius
        for index in range(self.bulb_counts):
            offset = (self.bulb_radius * 2 + self.bulb_gap) * index + self.bulb_radius
            if self.orient == "vert":
                x = self.x + cy
                y = self.y + offset
            else:
                x = self.x + offset
                y = self.y + cy
            bulb = SmartBulb(x, y, self.bulb_radius, id=f"{self.id}-bulb-{index}", body_color=self.body_color,
                             body_width=self.body_width, is_3d=self.is_3d, is_web_comp=self.is_web_comp)
            bulb.set_state(5)   # default state (no value)
            self.bulbs.append(bulb)

        length = cx * 2 * self.bulb_counts + self.bulb_gap * (self.bulb_counts - 1)
        wide = cy * 2
        if self.orient == "vert":
            self.bound_rect.set_rect(Rect(0, 0, wide, length))
        else:
            self.bound_rect.set_rect(Rect(0, 0, length, wide))

    def get_bound_rect(self):
        return self.bound_rect.get_bound_rect()

    def set_thresholds(self, thr_str: str | dict):
        super().set_thresholds(thr_str)
        for bulb in self.bulbs:
            bulb.set_thresholds(thr_str)

    def set_states(self, states: list):
        for stz in zip(self.bulbs, states):
            stz[0].set_state(stz[1])

    def set_values(self, values: list):
        for vlz in zip(self.bulbs, values):
            vlz[0].set_value(vlz[1])

    def __str__(self):
        return self.to_svg()

    def to_svg(self) -> str:
        if self.is_web_comp:
            pass
        else:
            svg_str = f'<g {self.to_attr_string()}>\n'
            svg_str += self.bound_rect.to_svg()
            for el in self.bulbs:
                bulb_str = el.to_svg()
                svg_str += bulb_str

            svg_str += f'</g>\n'
        return svg_str


class SmartRect(SmartWidget):
    __slots__ = ("is_3d", "is_web_comp", "body", "active", "x", "y", "rx", "ry", "width", "height",
                 "body_color", "body_width")

    def __init__(self, x, y, width, height, rx=0, ry=0, id: str = '',
                 body_color="black", body_width=0, is_3d: bool = True, is_web_comp: bool = False):
        super().__init__(id, class_name='SmartRect')
        self.is_3d = is_3d
        self.is_web_comp = is_web_comp
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
        self.set_attributes([
            f'is_3d:{is_3d}',
            f'is_web_comp:{is_web_comp}',
            f'w_width:{width}',
            f'w_height:{height}',
            f'w_rx:{rx}',
            f'w_ry:{ry}',
            f'body_color:{body_color}',
            f'body_width:{body_width}',
            f'thr:{self.thresholds}'
        ])

    def build_ctrl(self):
        self.body = SvgRect(self.x, self.y, self.width, self.height, rx=self.rx, ry=self.ry,
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
        if self.is_web_comp:
            pass
        else:
            svg_str += f'<g {self.to_attr_string()}>\n' \
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

        for v in self.thresholds:
            if value > v:
                color = self.thresholds[v]

        attr_list.append(f"fill:{color}")
        self.active.set_attributes(attr_list)

    def set_state(self, state):
        attrs = [f"fill:url(#alert_state_{state})"]
        self.active.set_attributes(attrs)


class SmartRectGrid(SmartWidget):
    __slots__ = ("id", "class_name", "is_3d", "is_web_comp", "body_color", "body_width", "rect_counts",
                 "x", "y", "width", "height", "rx", "ry", "rect_gap", "orient", "bound_rect", "children")

    def __init__(self, id: str, x, y, width, height, rx=0, ry=0, count: int = 2, gap: int = 2, orient: str = 'hor',
                 body_color="gray", body_width=1, is_3d: bool = True, is_web_comp: bool = False):
        super().__init__(id, 'SmartRectGrid')
        self.is_3d = is_3d
        self.is_web_comp = is_web_comp
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
        self.orient = orient

        self.bound_rect = SvgRect(attrs='{"display":"none"}')
        self.children: list = []
        self.build_ctrl()

        self.set_attributes([
            f'is_3d:{is_3d}',
            f'is_web_comp:{is_web_comp}',
            f'count:{count}',
            f'orient:{orient}',
            f'body_color:{body_color}',
            f'body_width:{body_width}',
            f'w_width:{width}',
            f'w_height:{height}',
            f'w_rx:{rx}',
            f'w_ry:{ry}',
            f'gap:{gap}',
            f'thr:{self.thresholds}'
        ])

    def build_ctrl(self):
        for index in range(self.rect_counts):
            if self.orient == "vert":
                x = self.x
                y = (self.height + self.rect_gap) * index + self.y
            else:
                x = (self.width + self.rect_gap) * index + self.x
                y = self.y

            rect = SmartRect(x, y, self.width, self.height, rx=self.rx, ry=self.ry, id=f"{self.id}-rect-{index}",
                             body_color=self.body_color, body_width=self.body_width,
                             is_3d=self.is_3d, is_web_comp=self.is_web_comp)
            rect.set_state(5)   # default state (no value)
            self.children.append(rect)

        if self.orient == "vert":
            length = (self.height * self.rect_counts) + self.rect_gap * (self.rect_counts - 1)
            self.bound_rect.set_rect(Rect(self.x, self.y, self.width, length))
        else:
            length = (self.width * self.rect_counts) + self.rect_gap * (self.rect_counts - 1)
            self.bound_rect.set_rect(Rect(self.x, self.y, length, self.height))

    def get_bound_rect(self):
        return self.bound_rect.get_bound_rect()

    def set_thresholds(self, thr_str: str | dict):
        super().set_thresholds(thr_str)
        for child in self.children:
            child.set_thresholds(thr_str)

    def set_states(self, states: list):
        for stz in zip(self.children, states):
            stz[0].set_state(stz[1])

    def set_values(self, values: list):
        for vlz in zip(self.children, values):
            vlz[0].set_value(vlz[1])

    def __str__(self):
        return self.to_svg()

    def to_svg(self) -> str:
        if self.is_web_comp:
            pass
        else:
            svg_str = f'<g {self.to_attr_string()}>\n'
            svg_str += self.bound_rect.to_svg()
            for el in self.children:
                svg_str += el.to_svg()

            svg_str += f'</g>\n'
        return svg_str


class SmartBar(SmartRect):
    """
    orient: str = hor[izontal], vert[ical], sq[uare]
    direction: str = right, left, top, bottom, left-top, left-bottom, right-top, right-bottom, default: right
    """
    def __init__(self, x, y, width, height, rx=0, ry=0, id: str = '', orient: str = 'hor', direction: str = 'right',
                 body_color="black", body_width=0, is_3d: bool = True, is_web_comp: bool = False):
        super().__init__(x, y, width, height, rx, ry, id, body_color, body_width, is_3d, is_web_comp)

        self.class_name = "SmartBar"
        self.orient = orient
        self.direction = direction
        self.abrc = self.active.get_bound_rect()    # store original active body rectangle
        self.set_attributes([
            f'orient:{orient}',
            f'direction:{direction}'
        ])

    def to_svg(self):
        svg_str = ''
        if self.is_web_comp:
            pass
        else:
            svg_str += f'<g {self.to_attr_string()}>\n' \
                f'{self.bound_rect.to_svg()}\n' \
                f'{self.body.to_svg()}\n' \
                f'{self.active.to_svg()}\n' \
                f'</g>\n'
        return svg_str

    def normalize_value(self, value):
        if value > self.max_value:
            print(f'{self.id}: ValueException: input value {value} greater max value {self.max_value}')
            value = self.max_value

        if value < self.min_value:
            print(f'{self.id}: ValueException: input value {value} lower min value {self.min_value}')
            value = self.max_value

        norm_v = value * 100 / self.max_value

        norm_w = (self.abrc.width / (self.max_value - self.min_value)) * value
        norm_h = (self.abrc.height / (self.max_value - self.min_value)) * value
        offset_y = self.abrc.height - norm_h
        offset_x = self.abrc.width - norm_w
        return {"norm_v": norm_v, "norm_w": norm_w, "norm_h": norm_h, "offset_y": offset_y, "offset_x": offset_x}

    def set_value(self, value):
        color = 'black'
        attr_list = []
        if self.is_3d:
            attr_list.append('filter:url(#MyFilter)')

        norm = self.normalize_value(value)
        for v in self.thresholds:
            if norm["norm_v"] > v:
                color = self.thresholds[v]

        # for index in range(self.thresholds.length()):
        #     thr = self.thresholds.at(index)
        #     for trigger in thr:
        #         if norm["norm_v"] > trigger:
        #             color = thr[trigger]
        #
        attr_list.append(f"fill:{color}")
        self.active.set_attributes(attr_list)

        if self.orient == 'hor':
            self.active.set_width(norm["norm_w"])
            self.active.offset(norm["offset_x"] if self.direction == "left" else 0, 0)
        elif self.orient == 'vert':
            self.active.set_height(norm["norm_h"])
            self.active.offset(0, norm["offset_y"] if self.direction == "top" else 0)
        elif self.orient == 'sq':
            self.active.set_size(norm["norm_w"], norm["norm_h"])
            dir_arr = self.direction.split("-")
            if len(dir_arr) < 2:
                raise AttributeError("Square bar must have one of directions: left-top, "
                                     "left-bottom, right-top, right-bottom")
            o_x = norm["offset_x"] if dir_arr[0] == "left" else 0
            o_y = norm["offset_y"] if dir_arr[1] == "top" else 0
            self.active.offset(o_x, o_y)


class SmartBars(SmartWidget):
    def __init__(self, id: str, x, y, width, height, rx=0, ry=0, count=2, gap=2, orient='vert', direction='top',
                 bar_body_color='black', bar_body_width=0, is_3d: bool = True, is_web_comp: bool = False):
        super().__init__(id, 'SmartBars')
        self.is_3d = is_3d
        self.is_web_comp = is_web_comp
        self.body_color = bar_body_color
        self.body_width = bar_body_width
        self.bars_count = count
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        self.ry = ry
        self.bars_gap = gap
        self.orient = orient
        self.direction = direction
        self.bound_rect = SvgRect(attrs='{"display":"none"}')
        self.children: list = []
        self.build_ctrl()
        self.set_attributes([
            f'is_3d:{is_3d}',
            f'is_web_comp:{is_web_comp}',
            f'count:{count}',
            f'orient:{orient}',
            f'direction:{direction}',
            f'body_color:{bar_body_color}',
            f'body_width:{bar_body_width}',
            f'w_width:{width}',
            f'w_height:{height}',
            f'w_rx:{rx}',
            f'w_ry:{ry}',
            f'gap:{gap}',
            f'thr:{self.thresholds}'
        ])

    def build_ctrl(self):
        pass

    def get_bound_rect(self):
        return self.bound_rect.get_bound_rect()

    def set_thresholds(self, thr_str: str | dict):
        super().set_thresholds(thr_str)
        for child in self.children:
            child.set_thresholds(thr_str)

    def set_values(self, values: list):
        for vlz in zip(self.children, values):
            vlz[0].set_value(vlz[1])

    def __str__(self):
        return self.to_svg()

    def to_svg(self) -> str:
        if self.is_web_comp:
            pass
        else:
            svg_str = f'<g {self.to_attr_string()}>\n'
            svg_str += self.bound_rect.to_svg()
            for el in self.children:
                svg_str += el.to_svg()

            svg_str += f'</g>\n'
        return svg_str





