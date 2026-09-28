"""Generate original, deliberately schematic two-pose exercise illustrations."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "dist" / "animations"
OUT.mkdir(parents=True, exist_ok=True)
BG = "#102238"
PANEL = "#18324a"
BODY = "#a9c8da"
ACTIVE = "#c6f073"
MUTED = "#608398"


def line(x1, y1, x2, y2, color=BODY, width=25):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'


def circle(x, y, radius, color=BODY):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}"/>'


def label(txt, x=34, y=50):
    # Captions live in HTML so a left-leg mirror never reverses written text.
    return ''


def common_scene():
    # A simplified side view: head to the right, hips at x=450, wall at x=445.
    return ''.join([
        '<rect width="800" height="400" fill="'+PANEL+'"/>',
        line(20, 345, 780, 345, MUTED, 3),
        line(445, 35, 445, 342, MUTED, 4),
        line(465, 294, 630, 294, BODY, 55),
        circle(688, 286, 35),
        line(615, 313, 530, 326, BODY, 13),
        line(450, 292, 450, 83, BODY, 27),
        line(450, 83, 469, 57, BODY, 15),
        circle(450, 292, 15),
    ])


def moving_leg(knee, ankle, toe=None, color=ACTIVE):
    toe = toe or (ankle[0]-12, ankle[1]-21)
    return ''.join([
        line(450, 292, *knee, color, 27),
        circle(*knee, 14, color),
        line(*knee, *ankle, color, 24),
        line(*ankle, *toe, color, 13),
    ])


def foot_scene(angle, title):
    # Close-up of a *single* raised ankle against a wall.
    toe = {
        'point': (403, 79),
        'demi': (445, 93),
        'flex': (486, 137),
    }[angle]
    return ''.join([
        '<rect width="800" height="400" fill="'+PANEL+'"/>',
        line(520, 30, 520, 365, MUTED, 4),
        line(405, 345, 405, 166, BODY, 46),
        circle(405, 166, 24, ACTIVE),
        line(405, 166, *toe, ACTIVE, 34),
        circle(*toe, 16, ACTIVE),
        label(title),
    ])


def rotation_scene(direction, title, angle):
    import math
    dx = int(72*math.sin(math.radians(angle)))
    dy = int(72*math.cos(math.radians(angle)))
    x, y = 405+dx, 82+dy
    return ''.join([
        '<rect width="800" height="400" fill="'+PANEL+'"/>',
        line(520, 30, 520, 365, MUTED, 4),
        line(405, 345, 405, 190, BODY, 45),
        circle(405, 190, 23, ACTIVE),
        line(405, 190, x, y, ACTIVE, 33),
        circle(x, y, 17, ACTIVE),
        f'<path d="M280 220 Q405 290 530 220" fill="none" stroke="{MUTED}" stroke-width="4" stroke-dasharray="10 10"/>',
        label(title),
    ])


def panel(content, y):
    return f'<g transform="translate(0 {y})">{content}</g>'


def save(n, first, second):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" role="img">
    {panel(first,0)}<rect y="396" width="800" height="8" fill="{BG}"/>
    {panel(second,400)}</svg>'''
    (OUT / f'{n:02d}.svg').write_text(svg)


def full(knee, ankle, title, toe=None):
    return common_scene()+moving_leg(knee, ankle, toe)+label(title)


save(1, full((355, 295), (315, 329), 'ZGIĘTA NOGA · DÓŁ'),
     full((365, 205), (296, 172), 'ZGIĘTA NOGA · GÓRA'))
save(2, full((340, 321), (207, 329), 'STOPA ODSUNIĘTA'),
     full((380, 260), (337, 329), 'STOPA PRZYCIĄGNIĘTA'))
save(3, full((365, 205), (284, 194), 'KOLANO ZGIĘTE'),
     full((320, 305), (173, 328), 'NOGA OPUSZCZONA'))
save(4, full((315, 312), (170, 330), 'NOGA PRZY PODŁODZE'),
     full((325, 250), (184, 209), 'UNIEŚ PROSTĄ NOGĘ'))
save(5, full((310, 329), (178, 329), 'POŁÓŻ PROSTĄ NOGĘ'),
     full((310, 333), (178, 335), 'DOCIŚ PIĘTĘ I KOLANO'))
save(6, foot_scene('point', 'POINT'), foot_scene('demi', 'DEMI POINT'))
save(7, foot_scene('demi', 'DEMI POINT'), foot_scene('flex', 'FLEX'))
save(8, full((450, 110), (450, 72), 'WYPROST'),
     common_scene().replace(line(450, 292, 450, 83, BODY, 27), '')
     .replace(line(450, 83, 469, 57, BODY, 15), '')
     +moving_leg((512, 227), (445, 220), (445, 190))+label('ZEGNIJ I ZSUŃ STOPĘ'))
save(9, rotation_scene('out', 'POINT · NA ZEWNĄTRZ', -18),
     rotation_scene('in', 'POINT · DO ŚRODKA', 18))
save(10, rotation_scene('out', 'DEMI POINT · NA ZEWNĄTRZ', -14),
     rotation_scene('in', 'DEMI POINT · DO ŚRODKA', 14))
save(11, rotation_scene('out', 'FLEX · NA ZEWNĄTRZ', -12),
     rotation_scene('in', 'FLEX · DO ŚRODKA', 12))
save(12, common_scene()+label('ODERWIJ NOGĘ OD ŚCIANY'),
     common_scene().replace(line(450, 292, 450, 83, BODY, 27), '')
     .replace(line(450, 83, 469, 57, BODY, 15), '')
     +line(450, 292, 410, 95, ACTIVE, 27)+line(410, 95, 416, 63, ACTIVE, 14)
     +label('UTRZYMAJ NOGĘ SAMODZIELNIE'))

rest = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400">
<rect width="800" height="400" fill="{PANEL}"/>{line(40,345,760,345,MUTED,3)}
{circle(156,273,34)}{line(190,290,485,292,BODY,55)}
{line(470,293,660,319,BODY,30)}{line(470,305,650,331,BODY,24)}
{line(270,312,195,332,BODY,16)}{label('MINUTA SPOKOJNEGO ODPOCZYNKU')}
</svg>'''
(OUT / '13.svg').write_text(rest)
