
from svgtools import tools
from svgtools.primitives import Point, Rect, SvgRect, SvgLine, SvgCircle, SvgFigure, SvgRoot
# from xml.dom import minidom
import xml.dom.minidom


if __name__ == '__main__':

    pt = Point()
    print(pt)
    rect = Rect()
    print(rect)

    svgLine = SvgLine(x1=10, y1=10, x2=50, y2=50, stroke=0xff0000, stroke_width=4)

    svgRect = SvgRect(x=10, y=10, width=50, height=50, rx=10, fill='yellow', id='yellow-rect')
    svgRect.set_attributes(["pointer-events:none", "opacity:0.5"])

    svgCircle = SvgCircle(30, 30, 15, attrs='{"fill":"blue","opacity":"0.5"}', class_name='svg-circles')

    svgFigure = SvgFigure(30, 30, 10, 50, 6, fill='blue', attrs='{"opacity": "0.40"}')

    rc1 = SvgRect(20, 20, 100, 24, attrs='{"fill":"green", "pointer-events":"none"}')

    # print(rc1.to_svg())
    rc_str = f'rect "rc1" = {rc1}'
    # print(rc_str)

    # print(svgLine.to_svg())
    # print(svgLine)
    # print(svgRect)
    # print(svgCircle)
    # print(svgFigure)

    svgCanvas = SvgRoot(view_box=[0, 0, 100, 100])
    svgCanvas.add_element(rc1)
    svgCanvas.add_elements([svgLine, svgRect, svgCircle, svgFigure])
    print(svgCanvas)

    tmpl = ''
    with open("temlate.html", "r") as tmpl_file:
        tmpl = tmpl_file.read()

    canvas = f'{tmpl.format(svgCanvas.to_svg())}'
    with open("index.html", "w") as file:
        file.write(canvas)


    # import svg
    #
    # canvas = svg.SVG(
    #     width=60,
    #     height=60,
    #     elements=[
    #         svg.Circle(
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
