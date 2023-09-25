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
        xx, yy, ww, hh = self.active.get_bound_rect().to_list()
        self.abrc = Rect(xx, yy, ww, hh)    # store original active body rectangle
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


class SmartBarsCtrl(SmartWidget):
    def __init__(self, id: str, x, y, width, height, rx=0, ry=0, count=2, gap=2, orient='vert', direction='top',
                 body_color='black', body_width=0, is_3d: bool = True, is_web_comp: bool = False, show_grid: bool = False,
                 bkg_color='none', bkg_border_color='none', bkg_border_width=0, bkg_gap=0, bkg_rx=0, bkg_shadow=False):
        super().__init__(id, 'SmartBarsCtrl')
        self.show_grid = show_grid
        self.is_3d = is_3d
        self.is_web_comp = is_web_comp
        self.bars_body_color = body_color
        self.bars_body_width = body_width
        self.count = count
        self.x = x
        self.y = y
        self.bars_width = width
        self.bars_height = height
        self.bars_rx = rx
        self.bars_ry = ry
        self.bars_gap = gap
        self.bars_orient = orient
        self.bars_direction = direction
        self.bkg_color = bkg_color
        self.bkg_border_color = bkg_border_color
        self.bkg_border_width = bkg_border_width
        self.bkg_gap = bkg_gap
        self.bkg_rx = bkg_rx
        self.bkg_shadow = bkg_shadow

        self.bound_rect = SvgRect(attrs='{"display":"none"}')
        self.children: list = []
        self.build_ctrl()
        self.set_attributes([
            f'bkg_color:{bkg_color}',
            f'bkg_border_color:{bkg_border_color}',
            f'bkg_border_width:{bkg_border_width}',
            f'bkg_gap:{bkg_gap}',
            f'bkg_rx:{bkg_rx}',
            f'bkg_shadow:{bkg_shadow}',
            f'show_grid:{show_grid}',
            f'is_3d:{is_3d}',
            f'is_web_comp:{is_web_comp}',
            f'count:{count}',
            f'bars_orient:{orient}',
            f'bars_direction:{direction}',
            f'bars_body_color:{body_color}',
            f'bars_body_width:{body_width}',
            f'bars_width:{width}',
            f'bars_height:{height}',
            f'bars_rx:{rx}',
            f'bars_ry:{ry}',
            f'bars_gap:{gap}',
            f'thr:{self.thresholds}'
        ])

    def build_ctrl(self):
        for index in range(self.count):
            if self.bars_orient == "hor":
                x = self.x
                y = (self.bars_height + self.bars_gap) * index + self.y
            else:
                x = (self.bars_width + self.bars_gap) * index + self.x
                y = self.y

            bar = SmartBar(x + self.bkg_gap, y + self.bkg_gap,
                           self.bars_width, self.bars_height,
                           id=f"{self.id}-bar-{index}",
                           rx=self.bars_rx, ry=self.bars_ry,
                           orient=self.bars_orient, direction=self.bars_direction,
                           body_color=self.bars_body_color, body_width=self.bars_body_width,
                           is_3d=self.is_3d, is_web_comp=self.is_web_comp)
            self.children.append(bar)

        if self.bars_orient == "hor":
            gap = (self.bkg_gap * 5) if self.show_grid else (self.bkg_gap * 2)
            bars_size = (self.bars_height * self.count) + self.bars_gap * (self.count - 1)
            self.bound_rect.set_rect(Rect(self.x, self.y, self.bars_width + self.bkg_gap * 2, bars_size + gap))
        else:
            gap = (self.bkg_gap * 6) if self.show_grid else (self.bkg_gap * 2)
            bars_size = (self.bars_width * self.count) + self.bars_gap * (self.count - 1)
            self.bound_rect.set_rect(Rect(self.x, self.y, bars_size + gap, self.bars_height + self.bkg_gap * 2))

        self.bound_rect.set_attributes([
            'display:true',
            f'fill:{self.bkg_color}', f'stroke:{self.bkg_border_color}', f'stroke-width:{self.bkg_border_width}',
            f'rx:{self.bkg_rx}', f'ry:{self.bkg_rx}'
        ])
        if self.bkg_shadow:
            self.bound_rect.set_attributes(['filter:url(#dropShadow)'])

    def get_bound_rect(self):
        return self.bound_rect.get_bound_rect()

    def set_min_value(self, value: float | int):
        for child in self.children:
            child.set_min_value(value)

    def set_max_value(self, value: float | int):
        for child in self.children:
            child.set_max_value(value)

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
        svg_str = ""
        if self.is_web_comp:
            pass
        else:
            svg_str = f'<g {self.to_attr_string()}>\n'
            svg_str += self.bound_rect.to_svg()

            if self.show_grid:
                min_value = int(self.children[0].min_value)
                max_value = int(self.children[0].max_value)
                v50 = int((max_value - min_value) / 2)
                s10 = int((max_value - min_value) / 10)

                bars_b_rc = Rect()
                for index, child in enumerate(self.children):
                    if index == 0:
                        child.abrc.copy_to(bars_b_rc)
                    else:
                        x1, y1, x2, y2 = child.abrc.to_coord()
                        bars_b_rc.expand(x2, y2)

                l_x_start = l_y_start = l_x_end = l_y_end = dot_x = dot_y = text_x = text_y = 0
                text_val = text_anchor = text_baseline = ''
                is_draw_text = False
                line = dot = t_value = None
                x1, y1, x2, y2 = bars_b_rc.to_coord()

                for li in range(min_value, s10 * 10 + s10, s10):
                    norm = self.children[0].normalize_value(li)
                    if self.bars_orient == 'vert':
                        l_x_start = x1 - 1
                        l_y_start = y1 + norm["norm_h"]
                        l_x_end = x2 + 1
                        l_y_end = l_y_start

                        dot_x = l_x_end + 2
                        dot_y = l_y_end

                        text_x = dot_x + self.bars_gap
                        text_y = dot_y
                        text_val = str(100 - li)
                        text_anchor = 'left'
                        text_baseline = 'middle'

                    elif self.bars_orient == 'hor':
                        l_x_start = x1 + norm["norm_w"]
                        l_y_start = y1 - 1
                        l_x_end = l_x_start
                        l_y_end = y2 + 1

                        dot_x = l_x_end
                        dot_y = l_y_end + 2

                        text_x = dot_x
                        text_y = dot_y + self.bars_gap
                        text_val = str(li)
                        text_anchor = 'middle'
                        text_baseline = 'hanging'

                    line = SvgLine(id=f'li-{li}', x1=l_x_start, y1=l_y_start, x2=l_x_end, y2=l_y_end, stroke_width=0.5, stroke="gray", attrs='{"stroke-dasharray":"1"}')
                    svg_str += line.to_svg()

                    if li == min_value:
                        text_anchor = 'left' if self.bars_orient == 'vert' else 'left'
                        text_baseline = 'hanging' if self.bars_orient == 'hor' else 'hanging'
                        is_draw_text = True
                    elif li == v50:
                        text_anchor = 'left' if self.bars_orient == 'vert' else 'middle'
                        text_baseline = 'hanging' if self.bars_orient == 'hor' else 'middle'
                        is_draw_text = True
                    elif li == max_value:
                        text_anchor = 'left' if self.bars_orient == 'vert' else 'end'
                        text_baseline = 'hanging' if self.bars_orient == 'hor' else 'auto'
                        is_draw_text = True
                    else:
                        is_draw_text = False

                    if is_draw_text:
                        dot = SvgCircle(dot_x, dot_y, 1, fill=SvgText.var_font_color)
                        t_value = SvgText(text_x, text_y, text=text_val, fill="white", baseline=text_baseline, anchor=text_anchor)
                        svg_str += dot.to_svg()
                        svg_str += t_value.to_svg()

            for el in self.children:
                svg_str += el.to_svg()

            svg_str += f'</g>\n'
        return svg_str





