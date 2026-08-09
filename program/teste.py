from a_maze_ing import Settings, Maze


def main() -> None:
    settings = Settings(
        width=5, height=5,
        entry=(0, 0), exit=(4, 4),
        output="maze.txt", seed="abc123", perfect=True
    )
    maze = Maze(settings)

    print("=== Antes de gerar (tudo deve ser 15) ===")
    maze.representation.debug_print()

    maze.generator.generate()

    print("\n=== Depois de gerar ===")
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


if __name__ == "__main__":
    main()
