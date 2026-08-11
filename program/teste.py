import random
from a_maze_ing import Settings, Maze


def main() -> None:
    settings = Settings(
        width=5, height=5,
        entry=(0, 0), exit=(4, 4),
        output="maze.txt", seed="abc123", perfect=False
    )
    random.seed(settings.seed)
    maze = Maze(settings)

    print("=== Antes de gerar (tudo deve ser 15) ===")
    maze.representation.debug_print()

    maze.generator.generate()

    print(f"\nSEED ==== {settings.seed}")
    print("=== Depois de gerar ===")
    maze.representation.debug_print()

    # Confere se sobrou alguma célula intocada (walls == 15),
    # o que indicaria que ela nunca foi visitada pelo algoritmo.
    intocadas = []
    for linha in maze.representation.grid:
        for celula in linha:
            if celula.walls == 15 and not celula.is_42:
                intocadas.append((celula.x, celula.y))

    print("\n=== Células nunca visitadas (deveria ser vazio) ===")
    print(intocadas)

    print("\n=== Caminho mais curto (entry -> exit) ===")
    caminho = maze.representation.find_shortest_path()
    print("".join(caminho))
    print(f"Total de passos: {len(caminho)}")


if __name__ == "__main__":
    main()
