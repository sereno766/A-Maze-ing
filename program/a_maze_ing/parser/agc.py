from a_maze_ing.includes.includes import gen_nbr, gen_chars, split_by
from a_maze_ing.seed.seed import gen_seed
from a_maze_ing import Settings


def gen_size(min: int, max: int) -> int:
    size = int(gen_nbr(2))
    while size > max or size <= min:
        size = int(gen_nbr(2))
    return size


def agc() -> Settings:
    width = gen_size(min=15, max=25)
    height = gen_size(min=15, max=20)
    entry = split_by(gen_nbr(2), 1, 2)
    exit = split_by(gen_nbr(4), 0, 2)
    valid = False
    while valid == False:
        if ((int(exit[0]) >= width or int(exit[0]) >= height)
           or (int(exit[1]) >= width or int(exit[1]) >= height)):
            exit = split_by(gen_nbr(4), 0, 2)
        else:
            valid = True
    seed = gen_seed(entry, exit, width, height)
    return(Settings(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        output="maze.txt",
        seed=seed,
        perfect=True
    ))

"HqVdnsM4vijhrTDpxP60"
"""
0100100001110001
0101011001100100
0110111001110011
0100110100110100
0111011001101001
0110101001101000
0111001001010100
0100010001110000
0111100001010000
0011011000110000
"""
