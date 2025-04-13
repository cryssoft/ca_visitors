#!/usr/bin/python3
"""
Cellular automaton simulation using a visitor pattern for solving simple mazes even in the
presence of loops.
"""
from sys    import argv as g_argv       #  global variables get a g_ prefix
from typing import Callable 


def visitor_for_adjacency(p_grid: list[list[str]], p_row: int, p_column: int) -> int:
    """
    Visitor function to be used on each cell to compute the maximum adjcency of "open"
    paths possible from the current cell in the grid.  We're only allowing up/down/left/right
    with no horizontals in this simulation.
    """
    l_open_adjacent: int = 0

    #  Skip the walls
    if (p_grid[p_row][p_column] != 'X'):
        #  Up
        if ((p_row - 1) < 0):
            l_open_adjacent += 1
        elif (p_grid[p_row-1][p_column] in ['S','E',' ']):
            l_open_adjacent += 1
        #  Left
        if ((p_column - 1) < 0):
            l_open_adjacent += 1
        elif (p_grid[p_row][p_column-1] in ['S','E',' ']):
            l_open_adjacent += 1
        #  Right
        if ((p_column + 1) >= len(p_grid[p_row])):
            l_open_adjacent += 1
        elif (p_grid[p_row][p_column+1] in ['S','E',' ']):
            l_open_adjacent += 1
        #  Down
        if ((p_row + 1) >= len(p_grid)):
            l_open_adjacent += 1
        elif (p_grid[p_row+1][p_column] in ['S','E',' ']):
            l_open_adjacent += 1

    #  Return the adjacency count
    return(l_open_adjacent)


def visitor_for_length(p_grid: list[list[str]], p_row: int, p_column: int) -> int:
    """
    Visitor function to be used on each cell to try to convert an actual path
    length back into an integer.  Negative one is a decent default here, since
    we're trying to compute a maximum that will never be less than one.
    """
    try:
        l_length: int = int(p_grid[p_row][p_column])
    except ValueError:
        l_length: int = -1

    #  Return the length here 
    return(l_length)


def visitor_for_path(p_grid: list[list[str]], p_row: int, p_column: int) -> int:
    """
    Visitor function to be used on each cell to knock out dead end paths (adjacency
    of one).
    """
    l_changed: int = 0
    l_open_adjacent: int = visitor_for_adjacency(p_grid, p_row, p_column)

    if (l_open_adjacent == 1):
        p_grid[p_row][p_column] = 'X'
        l_changed = 1

    #  Return the int/bool for whether we changed values
    return(l_changed)


def visitor_for_path_length(p_grid: list[list[str]], p_row: int, p_column: int) -> int:
    """
    Visitor function to be used on each cell to compute the actual path length from the 
    'S' (start) position.  We do this by adding one to an adjacent path with a real length.
    """
    l_changed: int = 0
    l_adjacent_lengths: list[int] = []

    #  Ignore walls, start, and end cells
    if (p_grid[p_row][p_column] not in ['X','S','E']):
        #  For now, don't re-compute - we'll explore this decision later
        if (p_grid[p_row][p_column] == ' '):
            #  Up
            if ((p_row - 1) >= 0):
                if (p_grid[p_row-1][p_column] == 'S'):
                    l_adjacent_lengths.append(1)
                else:
                    try:
                        l_length: int = int(p_grid[p_row-1][p_column])
                        l_adjacent_lengths.append(l_length + 1)
                    except ValueError:
                        pass
            #  Left
            if ((p_column - 1) >= 0):
                if (p_grid[p_row][p_column-1] == 'S'):
                    l_adjacent_lengths.append(1)
                else:
                    try:
                        l_length: int = int(p_grid[p_row][p_column-1])
                        l_adjacent_lengths.append(l_length + 1)
                    except ValueError:
                        pass
            #  Right
            if ((p_column + 1) < len(p_grid[p_row])):
                if (p_grid[p_row][p_column+1] == 'S'):
                    l_adjacent_lengths.append(1)
                else:
                    try:
                        l_length: int = int(p_grid[p_row][p_column+1])
                        l_adjacent_lengths.append(l_length + 1)
                    except ValueError:
                        pass
            #  Down
            if ((p_row + 1) < len(p_grid)):
                if (p_grid[p_row+1][p_column] == 'S'):
                    l_adjacent_lengths.append(1)
                else:
                    try:
                        l_length: int = int(p_grid[p_row+1][p_column])
                        l_adjacent_lengths.append(l_length + 1)
                    except ValueError:
                        pass

        #  If we saved any actual lengths, save our new minimum
        if (len(l_adjacent_lengths) > 0):
            l_minimum: str = str(min(l_adjacent_lengths))
            if (l_minimum != p_grid[p_row][p_column]):
                l_changed = 1
            p_grid[p_row][p_column] = l_minimum

    #  Return the int/bool of whether we changed an open to a length
    return(l_changed)


def print_prettier(p_grid: list[list[str]]) -> None:
    """
    Not exactly pretty, but at least prettier than a raw print(list[list[str]]) would be.
    """
    print('\n')
    for l_row in range(len(p_grid)):
        print(p_grid[l_row])
    print('\n')

    #  Return explicitly
    return


def read_grid_from_file(p_filename: str) -> list[list[str]]:
    """
    Trivially read the grid data from an external CSV file.  We may add validation logic
    here or elsewhere later.
    """
    l_grid: list[list[str]] = []

    #  Simple open->read->close with a context manager
    with open(p_filename, 'r') as l_file:
        for l_data in l_file:
            l_grid.append(l_data.strip().split(','))

    #  Return the grid data
    return(l_grid)


def apply_visitor_compute_max(p_grid: list[list[str]], p_visitor_fn: Callable[[list[list[str]],int,int],int]) -> int:
    """
    Loop over the grid and apply a visitor function we got as a parameter looking for the max value.
    """
    l_loops: int = 0
    l_max: int = 0
    while ((l_loops == 0) or (l_changes != 0)):
        l_changes = 0
        for l_row in range(len(p_grid)):
            for l_column in range(len(p_grid[l_row])):
                l_max = max(l_max,p_visitor_fn(p_grid, l_row, l_column))
        l_loops += 1

    #  Return the maximum value we got from applying the visitor function to every cell
    return(l_max)


def apply_visitor_until_stable(p_grid: list[list[str]], p_visitor_fn: Callable[[list[list[str]],int,int],int]) -> None:
    """
    Loop over the grid and apply a visitor function we got as a parameter until it makes no more changes.
    """
    l_changes: int = 0
    l_loops: int = 0
    while ((l_loops == 0) or (l_changes != 0)):
        l_changes = 0
        for l_row in range(len(p_grid)):
            for l_column in range(len(p_grid[l_row])):
                l_changes += p_visitor_fn(p_grid, l_row, l_column)
        html_svg_write_matrix(p_grid, f'Stable loop {l_loops}')
        l_loops += 1

    #  Return explicitly
    return


def break_loops(p_grid: list[list[str]], p_max: str) -> None:
    """
    For this trivial solution, we can turn the cells with the maximum path length into 'X'
    to be new walls and cut loops into two dead ends.
    """
    for l_row in range(len(p_grid)):
        for l_column in range(len(p_grid[l_row])):
            #  A cell with the maximum path length becomes a new wall
            if (p_grid[l_row][l_column] == p_max):
                p_grid[l_row][l_column] = 'X'
            else:
                #  A cell with a path length (int) become open/empty again
                try:
                    l_path_length: int = int(p_grid[l_row][l_column])
                    p_grid[l_row][l_column] = ' '
                except:
                    pass

    #  Return explicitly
    return


def html_write_headings() -> None:
    """
    Trivial function to dump out some HTML headings and stuff.
    """
    print('<html>')
    print('  <head>')
    print('    <style>')
    print('rect.blocked { fill: black; stroke-width: 1; stroke: black; }')
    print('rect.destination { fill: green; stroke-width: 1; stroke: black; }')
    print('rect.start { fill: blue; stroke-width: 1; stroke: black; }')
    print('rect.empty { fill: white; stroke-width: 1; stroke: black; }')
    print('text.path { fill: red; text-anchor: middle; }')
    print('    </style>')
    print('  </head>')
    print('  <body>')

    #  Return explicitly
    return


def html_svg_write_matrix(p_grid: list[list[str]], p_heading: str) -> None:
    """
    This replaces the text print version with a simplified SVG graphic (HTML5) that uses the internal CSS
    directives to save some space in the output file.
    """
    l_x_start: int = 20
    l_y_start: int = 40
    l_y: int = l_y_start
    l_x_step: int = 40
    l_y_step: int = 40

    print(f'<p><svg width="{(len(p_grid[0]))*l_x_step+(l_x_step*2)}" height="{(len(p_grid))*l_y_step+l_y_step}">')
    print(f'<text x="5" y="25">(0,0)</text>')
    print(f'<text x="{(len(p_grid[0]))*l_x_step+(l_x_step-10)}" y="25" style="text-anchor: end">{p_heading}</text>')

    for l_row in range(len(p_grid)):
        l_x: int = l_x_start
        for l_col in range(len(p_grid[0])):
            l_output: str = p_grid[l_row][l_col]
            if (p_grid[l_row][l_col] == 'E'):
                l_class: str = 'destination'
            elif (p_grid[l_row][l_col] == 'S'):
                l_class: str = 'start'
            elif (p_grid[l_row][l_col][0] in [' ','1','2','3','4','5','6','7','8','9']):
                l_class: str = 'empty'
            else:
                l_class: str = 'blocked'
                l_output: str = ' '
            print(f'<rect x="{l_x}" y="{l_y}" height="{l_y_step}" width="{l_x_step}" class="{l_class}"/>')
            print(f'<text x="{l_x+l_x_step/2}" y="{l_y+25}" class="path">{l_output}</text>')
            l_x += l_x_step
        l_y += l_y_step

    print('</svg></p>')

    #  Return explicitly
    return


def html_write_footings() -> None:
    """
    Trivial function to dump out some HTML footings and stuff.
    """
    print('  </body>')
    print('</html>')

    #  Return explicitly
    return


def main(p_argv: list[str]) -> None:
    """
    Simple main program/loop.  Infinite-ish.  We loop until we no longer need to.
    """
    html_write_headings()

    #  Load and print the (hopefully rectangular) grid
    l_grid: list[list[str]] = read_grid_from_file(p_argv[1])
    html_svg_write_matrix(l_grid, 'Starting')

    #  Loop until we no longer need to make changes
    while (True):
        #  Knock out all dead ends
        apply_visitor_until_stable(l_grid, visitor_for_path)
        l_max_adjacency: int = apply_visitor_compute_max(l_grid, visitor_for_adjacency)
        #  If there are loops, knock one or more out
        if (l_max_adjacency > 2):
            apply_visitor_until_stable(l_grid, visitor_for_path_length)
            l_max_path_length: int = apply_visitor_compute_max(l_grid, visitor_for_length)
            break_loops(l_grid, str(l_max_path_length))
            html_svg_write_matrix(l_grid, 'After loop break')
        #  No loops means we're done
        else:
            break

    #  Print the final form of the grid
    html_svg_write_matrix(l_grid, 'Final')

    html_write_footings()

    #  Return explicitly
    return


#  The usual thing to keep modules safe-r
if (__name__ == '__main__'):
    main(g_argv)