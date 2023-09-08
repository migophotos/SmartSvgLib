from svgtools.primitives import Point, Rect, DefsSection, SvgRect, SvgLine, SvgText, SvgCircle, SvgEllipse, SvgFigure
from svgtools.smartarray import SmartArray


class SmartWidget:
    def __init__(self, id: str = '', class_name: str = ''):
        self.id = id
        self.class_name = class_name
        self.min_value: float = float(0)
        self.max_value: float = float(100)
        self.thresholds = SmartArray()
        self.bound_rect = SvgRect(attrs='{"display":"none"}')

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
    def __init__(self, cx, cy, r, id: str = '', class_name: str = 'SmartBulb', is_3d: bool = True):
        super().__init__(id, class_name)

        self.is_3d = is_3d
        self.body = SvgCircle(cx=cx, cy=cy, r=r, id=self.build_id('body'))
        rc = self.body.get_bound_rect()
        self.set_bound_rect(rc)

        self.active = SvgCircle(cx=cx, cy=cy, r=r - 1, id=self.build_id("active"))

    def __str__(self) -> str:
        return self.to_svg()

    def get_bound_rect(self):
        return self.bound_rect.get_bound_rect()

    def to_svg(self, is_web_component: bool = False):
        if is_web_component:
            pass
        else:
            b_rect_str = self.bound_rect.to_svg()
            body_str = self.body.to_svg()
            active_str = self.active.to_svg()

        svg_str = f'<g id="{self.id}" class-name="{self.class_name}">\n' \
            f'{b_rect_str}\n' \
            f'{body_str}\n' \
            f'{active_str}\n' \
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
