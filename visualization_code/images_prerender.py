from mlx import Mlx
from math import sqrt, pow, sin, cos, pi


class ImgData():
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0


class Tile():
    north = False
    east = False
    south = False
    west = False
    path = False
    start = False
    end = False

    def __init__(self, value: int):
        self.image = ImgData()
        self.value = value
        if self.value >> 0 & 1:
            self.north = True
        if self.value >> 1 & 1:
            self.east = True
        if self.value >> 2 & 1:
            self.south = True
        if self.value >> 3 & 1:
            self.west = True
        if self.value >> 4 & 1:
            self.path = True
        if self.value >> 5 & 1:
            self.start = True
        if self.value >> 6 & 1:
            self.end = True


tile_1 = Tile(0b0000)
tile_2 = Tile(0b0001)
tile_3 = Tile(0b0010)
tile_4 = Tile(0b0100)
tile_5 = Tile(0b1000)
tile_6 = Tile(0b0011)
tile_7 = Tile(0b0101)
tile_8 = Tile(0b1001)
tile_9 = Tile(0b0110)
tile_10 = Tile(0b1010)
tile_11 = Tile(0b1100)
tile_12 = Tile(0b0111)
tile_13 = Tile(0b1011)
tile_14 = Tile(0b1101)
tile_15 = Tile(0b1110)
tile_16 = Tile(0b1111)
maze_tiles = ([tile_1, tile_2, tile_3, tile_4,
              tile_5, tile_6, tile_7, tile_8,
              tile_9, tile_10, tile_11, tile_12,
              tile_13, tile_14, tile_15, tile_16])

tile_path_north = Tile(0b10001)
tile_path_east = Tile(0b10010)
tile_path_south = Tile(0b10100)
tile_path_west = Tile(0b11000)
tile_start = Tile(0b100000)
tile_end = Tile(0b1000000)
symbol_tiles = ([tile_path_north, tile_path_east,
                 tile_path_south, tile_path_west,
                 tile_start, tile_end])


def init_tiles(m: Mlx, mlx_ptr: int, height: int, pre_tiles: list[Tile]) \
                -> list[Tile]:
    x, y = height, height
    for tile in pre_tiles:
        tile.image.img = m.mlx_new_image(mlx_ptr, x, y)
        tile.image.width = x
        tile.image.height = y
        tile.image.data, tile.image.bpp, tile.image.sl, tile.image.iformat = \
            m.mlx_get_data_addr(tile.image.img)
    return (pre_tiles)


def special_tiles(m: Mlx, mlx_ptr: int, height: int, Colours: dict = {
    "wall_colour": (0xEEFFFFFF).to_bytes(4, 'little'),
    "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
    "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
    "path_colour": (0xEEFF0000).to_bytes(4, "little")
}
                     ) -> list[Tile]:
    path_colour = Colours["path_colour"]
    transparent = (0x00000000).to_bytes(4, "little")
    y = height
    radius = y / 3
    smaller_r = radius - (radius / 4)
    r_squared = pow(radius, 2)
    sr_squared = pow(smaller_r, 2)
    other_tiles = init_tiles(m, mlx_ptr, height, symbol_tiles)
    sl = other_tiles[0].image.sl
    bpp = other_tiles[0].image.bpp
    h_bpp = bpp / 2
    line_thickness = y / 16
    line_width = sl / 16
    for tile in other_tiles:
        m.mlx_sync(mlx_ptr, Mlx.SYNC_IMAGE_WRITABLE, tile.image.img)
        for offset in range(0, tile.image.sl * y, 4):
            if not (tile.start or tile.end):
                if ((tile.west or tile.east) and
                        (((offset / sl)) < (((y / 2) + line_thickness)))
                        and ((offset / sl) > ((y / 2) - line_thickness))):
                    tile.image.data[offset:offset+4] = path_colour
                elif ((tile.north or tile.south) and
                        ((offset % sl)) < ((sl / 2) + line_width) and
                        ((offset % sl)) > ((sl / 2) - line_width)):
                    tile.image.data[offset:offset+4] = path_colour
                else:
                    tile.image.data[offset:offset+4] = transparent
            elif r_squared > ((pow((offset % sl - (sl / 2)), 2) / h_bpp +
                              pow((offset / sl) - (y / 2), 2))):
                tile.image.data[offset:offset+4] = (0xBBFFFFFF). \
                    to_bytes(4, "little")
                if sr_squared > ((pow((offset % sl - (sl / 2)), 2) / h_bpp +
                                 pow((offset / sl) - (y / 2), 2))):
                    if tile.start:
                        tile.image.data[offset:offset+4] = (0xBB00EE00). \
                            to_bytes(4, "little")
                    if tile.end:
                        tile.image.data[offset:offset+4] = (0xBBEE0000). \
                            to_bytes(4, "little")
            else:
                tile.image.data[offset:offset+4] = transparent
    return (other_tiles)


def pre_render_tiles(m: Mlx, mlx_ptr: int, height: int, Colours: dict = {
    "wall_colour": (0xEEFFFFFF).to_bytes(4, 'little'),
    "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
    "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
    "path_colour": (0xEEFFFF00).to_bytes(4, "little")
}
                     ) -> list[Tile]:
    wall_colour = Colours["wall_colour"]
    tunnel_colour = Colours["tunnel_colour"]
    logo_colour = Colours["logo_colour"]
    y = height
    tiles = init_tiles(m, mlx_ptr, height, maze_tiles)
    sl = tiles[0].image.sl
    bpp = tiles[0].image.bpp
    h_bpp = bpp / 2
    corner_radius = y / 4
    radius = (sqrt(pow(y, 2) + (pow(sl, 2) / h_bpp)) / 2) - corner_radius
    c_r_squared = pow(corner_radius, 2)
    r_squared = pow(radius, 2)
    corner_coords = [(0, 0), (sl, 0), (0, y), (sl, y)]
    horizontal_offset = (sl / 4) - cos(pi / 4) * radius
    vertical_offset = (y / 2) - (sin(pi / 4) * radius)
    for tile in tiles:
        m.mlx_sync(mlx_ptr, Mlx.SYNC_IMAGE_WRITABLE, tile.image.img)
        for offset in range(0, tile.image.sl * y, 4):
            tile.image.data[offset:offset+4] = tunnel_colour
            for corner_x, corner_y in corner_coords:
                if c_r_squared > (((pow((offset % sl) - (corner_x), 2) / h_bpp)
                                   ) + pow((offset / sl) - (corner_y), 2)):
                    tile.image.data[offset:offset+4] = wall_colour
            if tile.north and (offset / sl) < vertical_offset:
                # north side closed
                tile.image.data[offset:offset+4] = wall_colour
            if tile.east and (offset % sl) > (sl - horizontal_offset):
                # east side closed
                tile.image.data[offset:offset+4] = wall_colour
            if tile.south and (offset / sl) > (y - vertical_offset):
                # south side closed
                tile.image.data[offset:offset+4] = wall_colour
            if tile.west and (offset % sl) < horizontal_offset:
                # west side closed
                tile.image.data[offset:offset+4] = wall_colour
            if r_squared > ((pow((offset % sl - (sl / 2)), 2) / h_bpp +
                            pow((offset / sl) - (y / 2), 2))):
                if tile.north and tile.east and tile.south and tile.west:
                    tile.image.data[offset:offset+4] = \
                        logo_colour
                else:
                    tile.image.data[offset:offset+4] = tunnel_colour
    other_tiles = special_tiles(m, mlx_ptr, height, Colours)
    return (tiles + other_tiles)
