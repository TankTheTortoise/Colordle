from PIL import ImageColor
import itertools
import pandas as pd


class Color:
    def __init__(self, color: tuple[int, int, int]):
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]

    def __add__(self, other):
        return Color((self.r + other.r, self.g + other.g, self.b + other.b))

    def __sub__(self, other):
        return Color((self.r - other.r, self.g - other.g, self.b - other.b))

    def __mul__(self, other):
        return Color((self.r * other.r, self.g * other.g, self.b * other.b))

    def __pow__(self, exponent):
        r = self.r
        g = self.g
        b = self.b

        return Color((r ** exponent, g ** exponent, b ** exponent))

    def sum(self):
        return self.r + self.g + self.b

    def __str__(self):
        return f'({self.r},{self.g},{self.b})'






def hex_distance(color1, color2):
    color1_rgb = ImageColor.getrgb(color1)
    color2_rgb = ImageColor.getrgb(color2)
    c1 = Color(color1_rgb)
    c2 = Color(color2_rgb)

    return ((c1 - c2)**2).sum() ** 0.5
def max_distance(color: Color):
    vertex_possibilities = [0, 255]
    vertices = itertools.combinations_with_replacement(vertex_possibilities, 3)
    max_distance = 0
    for vertex in vertices:
        max_distance = max(max_distance, ((color - Color(vertex)) ** 2).sum() ** 0.5)
    return max_distance

def percent_difference(correct_color, color2):
    return 100-100*(hex_distance(correct_color, color2) / max_distance(Color(ImageColor.getrgb(correct_color))))


def color_to_hex(color: str):
    colors_dict = pd.read_csv('static/colors.csv')
    colors_dict["Nombre"] = colors_dict["Nombre"].str.lower()
    colors_dict["Nombre"] = colors_dict["Nombre"].str.replace(u'\u200b', '')

    colors_dict = dict(zip(colors_dict["Nombre"], colors_dict["Cod. Hex."]))
    print(colors_dict)
    try:
        return colors_dict[color.lower()]
    except KeyError:
        return -1


if __name__ == "__main__":
    print(color_to_hex("Marrón"))