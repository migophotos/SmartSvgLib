# import svg

# from svgtools import tools
from svgtools.primitives import Point, Rect, DefsSection, SvgRect, SvgLine, SvgCircle, SvgFigure, SvgRoot
from svgtools.figures import SmartBulb, SmartBulbGrid, SmartRect, SmartRectGrid, SmartBar
# from xml.dom import minidom
# import xml.dom.minidom
# from pympler import asizeof


if __name__ == '__main__':

    # svgLine = SvgLine(x1=10, y1=10, x2=50, y2=50, stroke=0xff0000, stroke_width=4)
    #
    # svgRect = SvgRect(x=10, y=10, width=50, height=50, rx=10, fill='yellow', id='yellow-rect')
    # svgRect.set_attributes(["pointer-events:none", "opacity:0.5"])
    #
    # svgCircle = SvgCircle(30, 30, 15, attrs='{"fill":"blue","opacity":"0.5"}', class_name='svg-circles')
    #
    # svgFigure = SvgFigure(30, 30, 10, 50, 6, fill='blue', attrs='{"opacity": "0.40"}')
    #
    # rc1 = SvgRect(20, 20, 100, 24, attrs='{"fill":"green", "pointer-events":"none"}')

    # print(rc1.to_svg())
    # rc_str = f'rect "rc1" = {rc1}'
    # print(rc_str)

    # print(svgLine.to_svg())

    # bulb_1 = SmartBulb(150, 150, 30, "bulb")
    # bulb_1.set_value(94)
    # svgCanvas = SvgRoot(view_box=[0, 0, 100, 100])
    # svgCanvas.add_element(rc1)
    # svgCanvas.add_elements([svgLine, svgRect, svgCircle, svgFigure])
    # svgCanvas.add_elements([bulb_1])

    # svg with automatically calculated viewbbox (autobound = True by default), used for single widget
    svgCanvas_02 = SvgRoot(view_box=[0, 0, 100, 100])
    h_bulb_grid = SmartBulbGrid("HorBulbGrid", bulb_radius=16, count=6, gap=1, body_width=3)
    svgCanvas_02.add_elements([h_bulb_grid])
    h_bulb_grid.set_states([0, 1, 2, 3, 4, 5])

    # svg with manual defined viewbox (autobound = False), used for more than one widget on canvas
    svgCanvas_05 = SvgRoot(view_box=[0, 0, 500, 400], autobound=False)
    h_rect_grid = SmartRectGrid("HorRectGrid", x=0, y=0, width=30, height=30, rx="2%", ry="2%",
                                count=6, gap=1, body_width=2, body_color="lightgray", orient="hor")
    v_rect_grid = SmartRectGrid("VerRectGrid", x=77, y=35, width=30, height=20,
                                count=6, gap=2, body_width=0, orient="vert")
    v_bulb_grid = SmartBulbGrid("VerBulbGrid", x=10, y=35, bulb_radius=10, count=6, gap=1, body_width=3,
                                orient="vert")
    bulb_el = SmartBulb(cx=150, cy=80, r=35, id="BigBulb", body_color="red", body_width=2)
    rect_el = SmartRect(x=120, y=120, width=60, height=60, rx="3%", ry="3%", id="BigRect", body_color="red", body_width=2)

    # smart bar
    bar1 = SmartBar(x=225, y=15, width=100, height=18, id="HorBar", body_width=1, body_color="lightgray", is_3d=False)
    bar2 = SmartBar(x=200, y=40, width=20, height=150, id="VertBar", orient="vert", direction="top", body_width=1, body_color="lightgray", is_3d=False)
    bar3 = SmartBar(x=225, y=40, width=100, height=150, id="SqBar", orient="sq", direction="right-top", rx="0.1%", ry="0.1%", body_width=1, body_color="lightgray", is_3d=False)

    svgCanvas_05.add_elements([h_rect_grid, v_rect_grid, v_bulb_grid, bulb_el, rect_el, bar1, bar2, bar3])

    thresholds = {0: "blue", 5: "green", 55: "yellow", 65: "red", 95: "crimson"}

    h_rect_grid.set_states([0, 1, 2, 3, 4, 5])
    v_rect_grid.set_states([5, 4, 3, 2, 1, 0])

    # v_bulb_grid.set_states([0, 1, 2, 3, 4, 5])
    v_bulb_grid.set_thresholds(thresholds)
    v_rect_grid.set_thresholds(thresholds)
    v_bulb_grid.set_values([3, 25, 60, 80, 98])

    bulb_el.set_thresholds(thresholds)
    bulb_el.set_value(55)
    rect_el.set_state(1)

    thresholds = '{0:blue,25:green,50:yellow,75:red}'
    bar1.set_thresholds(thresholds)
    bar1.set_max_value(200)
    bar1.set_value(250)

    bar2.set_thresholds(thresholds)
    bar2.set_value(54)

    thresholds = '{0:red,25:green,75:red}'
    bar3.set_thresholds(thresholds)
    bar3.set_value(54)


    tmpl = ''
    with open("temlate.html", "r") as tmpl_file:
        tmpl += tmpl_file.read()

    canvas_01 = f'{tmpl.format(svgCanvas_02.to_svg(), svgCanvas_05.to_svg())}'
    with open("index.html", "w") as file:
        file.write(canvas_01)

    # print(asizeof.asizeof(svgCanvas_05))



    #
    # canvas = svg.SVG(
    #     width=60,
    #     height=60,
    #     elements=[
    #         svg.Circle(
    #             id="active",
    #             cx=30, cy=30, r=20,
    #             stroke="red",
    #             fill="white",
    #             stroke_width=5,
    #         ),
    #     ],
    # )
    # print(canvas)


    # def func(x: str = '') -> str:
    #     if type(x) != str:
    #         return 'Invalid argument type'
    #
    #     if not x:
    #         x = 'empty arg x'
    #
    #     print(x)
    #     return x
    #
    # func(10)
    # func("abcd")
    # func()
    # func(["abc", "qwerty"])

    # Using Regular Expression
    # import re
    #
    # def find_all_chars(string_):
    #     pattern = '[a-zA-Z]'
    #     result = re.findall(pattern, string_)
    #     return result
    #
    # def coding_char(ch):
    #     # insert you coding here
    #     ch = ch
    #     return ch
    #
    # inp_string = "123qweaZSDF/"
    # found_str = find_all_chars(inp_string)
    # coded_str = ''
    # for found_char in found_str:
    #     # print(found_char)
    #     coded_str += coding_char(found_char)
    #
    # print(coded_str)

    # document = """\
    # <slideshow>
    #     <title>Demo slideshow</title>
    #     <slide><title>Slide title</title>
    #         <point>This is a demo</point>
    #         <point>Of a program for processing slides</point>
    #     </slide>
    #
    #     <slide><title>Another demo slide</title>
    #         <point>It is important</point>
    #         <point>To have more than</point>
    #         <point>one slide</point>
    #     </slide>
    # </slideshow>
    # """
    #
    # dom = xml.dom.minidom.parseString(document)
    #
    #
    # def getText(nodelist):
    #     rc = []
    #     for node in nodelist:
    #         if node.nodeType == node.TEXT_NODE:
    #             rc.append(node.data)
    #     return ''.join(rc)
    #
    #
    # def handleSlideshow(slideshow):
    #     print("<html>")
    #     handleSlideshowTitle(slideshow.getElementsByTagName("title")[0])
    #     slides = slideshow.getElementsByTagName("slide")
    #     handleToc(slides)
    #     handleSlides(slides)
    #     print("</html>")
    #
    #
    # def handleSlides(slides):
    #     for slide in slides:
    #         handleSlide(slide)
    #
    #
    # def handleSlide(slide):
    #     handleSlideTitle(slide.getElementsByTagName("title")[0])
    #     handlePoints(slide.getElementsByTagName("point"))
    #
    #
    # def handleSlideshowTitle(title):
    #     print(f"<title>{getText(title.childNodes)}</title>")
    #
    #
    # def handleSlideTitle(title):
    #     print(f"<h2>{getText(title.childNodes)}</h2>")
    #
    #
    # def handlePoints(points):
    #     print("<ul>")
    #     for point in points:
    #         handlePoint(point)
    #     print("</ul>")
    #
    #
    # def handlePoint(point):
    #     print(f"<li>{getText(point.childNodes)}</li>")
    #
    #
    # def handleToc(slides):
    #     for slide in slides:
    #         title = slide.getElementsByTagName("title")[0]
    #         print(f"<p>{getText(title.childNodes)}</p>")
    #
    #
    # handleSlideshow(dom)

    # sp = Point()
    # sp.set_point(10, 20)
    # sp.to_string()
    # point = sp.set_point(100, 200).move(10, 10)
    # print(point.to_dict())
    #
    # print(Rect().from_coord(10, 10, 100, 200).to_string())
    #
    # xml = '<html><title>Foo</title> <p>Some text <div>and more</div></p> </html>'
    # doc = minidom.parseString(xml)
    #
    # rc_params = Rect(10, 10, 100, 30).to_dict()
    # rc_params['fill'] = 'gray'
    # rc_params['stroke'] = 'black'
    # rc_params['stroke-width'] = 2
    # rect = tools.add_element('rect', rc_params, doc)
    # print(rect)
