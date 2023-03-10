from django.db import models


class CssColor(models.Model):
    class ColorShade(models.TextChoices):
        PINK = 'pink', 'Pink'
        PURPLE = 'purple', 'Purple'
        RED = 'red', 'Red'
        ORANGE = 'orange', 'Orange'
        YELLOW = 'yellow', 'Yellow'
        GREEN = 'green', 'Green'
        CYAN = 'cyan', 'Cyan'
        BLUE = 'blue', 'Blue'
        BROWN = 'brown', 'Brown'
        WHITE = 'white', 'White'
        GRAY = 'gray', 'Gray'

    class CssLevel(models.TextChoices):
        LEVEL1 = 1, 'Level 1'
        LEVEL2 = 2, 'Level 2'
        LEVEL3 = 3, 'Level 3'
        LEVEL4 = 4, 'Level 4'

    keyword = models.CharField(max_length=100, unique=True)
    hex_value = models.CharField(max_length=7)
    color_shade = models.CharField(max_length=10, choices=ColorShade.choices, default=None)
    css_level = models.SmallIntegerField(choices=CssLevel.choices, default=None)

    def __repr__(self) -> str:
        return f"CssColor {self.keyword}"

    @staticmethod
    def get_css_level(keyword: str) -> CssLevel:
        if keyword in CssColor.level1_colors():
            return CssColor.CssLevel.LEVEL1
        elif keyword in CssColor.level2_colors():
            return CssColor.CssLevel.LEVEL2
        elif keyword in CssColor.level4_colors():
            return CssColor.CssLevel.LEVEL4
        else:
            return CssColor.CssLevel.LEVEL3

    @staticmethod
    def level1_colors() -> tuple:
        return (
            'black', 'silver', 'gray', 'white',
            'maroon', 'red', 'purple', 'fuchsia',
            'green', 'lime', 'olive', 'yellow',
            'navy', 'blue', 'teal', 'aqua',
        )

    @staticmethod
    def level2_colors() -> tuple:
        return 'orange',

    @staticmethod
    def level4_colors() -> tuple:
        return 'rebeccapurple',
