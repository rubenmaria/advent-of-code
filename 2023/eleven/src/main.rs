use std::{collections::{HashSet, HashMap, BinaryHeap}, ops::Range, cmp::Ordering};
use itertools::Itertools;


#[derive(Debug,Clone,Copy)]
enum UniverseNode {
    EmptySpace,
    Galaxy(u16)
}

impl UniverseNode {
    pub fn is_empty_space(&self) -> bool {
        match self {
            &Self::EmptySpace => true,
            _ => false
        }
    }

    pub fn is_galaxy(&self) -> bool {
        match self {
            &Self::Galaxy(_) => true,
            _ => false
        }
    }
}

#[derive(Debug)]
struct Vertex {
    vertex: (usize,usize),
    distance: u128,
}

impl Ord for Vertex{
    fn cmp(&self, other: &Self) -> Ordering {
        other.distance.cmp(&self.distance)
    }
}

impl PartialOrd for Vertex{
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl PartialEq for Vertex{
    fn eq(&self, other: &Self) -> bool {
        self.distance.eq(&other.distance)
    }
}

impl Eq for Vertex{}

fn main() {
    let galaxy_map = parse_galaxy(include_str!("galaxy-map.input"));
    let universe = enumerate_universe(&galaxy_map);
    let galaxy_count = get_galaxy_count(&universe);
    let unique_galaxies = (1..=galaxy_count)
            .combinations(2)
            .map(|x| (x[0], x[1]))
            .collect_vec();
    let  distances = shortes_distance_galaxies(&universe, &1000000);
    let shortes_path_sum: usize = distances.into_iter()
            .filter(|(x, _)| unique_galaxies.contains(x))
            .map(|(_,d)| d as usize)
            .sum();
    println!("shortes paths sum: {}", shortes_path_sum);
}

fn shortes_distance_galaxies(universe: &Vec<Vec<UniverseNode>>, free_cost: &u128)
    -> Vec<((usize,usize), u128)> {
    let mut name_distances = vec![];
    for position in get_all_galaxies(universe) {
        let galaxy_name = galaxy_position_to_name(position, universe);
        let distances_from_galaxy = get_distances_to_galaxies(
            position,
            universe,
            free_cost
        );
        name_distances.extend(
            distances_from_galaxy.into_iter()
                .map(|(p,d)| 
                 ((galaxy_name, galaxy_position_to_name(p, universe)), d))
        );
    }

    name_distances
}

fn get_galaxy_count(universe: &Vec<Vec<UniverseNode>>) -> usize {
    get_cartesian_product_range(0..universe.len(), 0..universe[0].len())
        .into_iter()
        .filter(|(y,x)| {
            match universe[*y][*x] {
                 UniverseNode::EmptySpace => false,
                 UniverseNode::Galaxy(_) => true
            }
        })
    .count() 
}

fn get_distances_to_galaxies(start: (usize,usize),
                             universe: &Vec<Vec<UniverseNode>>,
                             free_cost: &u128) 
        -> Vec<((usize,usize),u128)> {
    let distances = dijkstra(&start, universe, free_cost);
    get_all_galaxies(universe)
        .into_iter()
        .filter(|&x| x != start)
        .map(|(y,x)| ((y,x), distances[&(y,x)]))
        .collect()
}

fn dijkstra(start: &(usize,usize), universe: &Vec<Vec<UniverseNode>>,
            free_cost: &u128) 
    -> HashMap<(usize,usize), u128> {
    let mut distances = HashMap::new();
    let mut visited = HashSet::new();
    let mut to_visit = BinaryHeap::new();

    distances.insert(*start, 0);
    to_visit.push(Vertex {
        vertex: *start,
        distance: 0,
    });

    let free_rows: HashSet<usize> = HashSet::from_iter(
        get_free_rows(universe).into_iter()
    );
    let free_columns: HashSet<usize> = HashSet::from_iter(
        get_free_columns(universe).into_iter()
    );

    while let Some(Vertex { vertex, distance }) = to_visit.pop() {
        if !visited.insert(vertex) {
            continue;
        }
        for neighbor in get_neighbors(&vertex, universe) {
            let new_distance = distance + get_distance(
                &neighbor,
                &free_columns,
                &free_rows,
                *free_cost
            );
            let is_shorter = distances
                .get(&neighbor)
                .map_or(true, |&current| new_distance < current);

            if is_shorter {
                distances.insert(neighbor, new_distance);
                to_visit.push(Vertex {
                    vertex: neighbor,
                    distance: new_distance,
                });
            }
        }
    }

    distances
}

fn get_distance(node: &(usize,usize), free_columns: &HashSet<usize>,
                free_rows: &HashSet<usize>, free_cost: u128) ->  u128 {
    if free_rows.contains(&node.0) || free_columns.contains(&node.1) {
        free_cost
    } else {
        1
    }
}

fn draw_universe_with_distance(distance: &HashMap<(usize,usize), u16>, 
                               universe: &Vec<Vec<UniverseNode>>) {
    for row in 0..universe.len() {
        for column in 0..universe[0].len() {
            if distance.contains_key(&(row,column)) {
                print!("({})", distance[&(row,column)].to_string());
            } else {
                match universe[row][column] {
                    UniverseNode::EmptySpace => print!("."),
                    UniverseNode::Galaxy(_) => print!("#"),
                }
            }
        }
        println!()
    }
}

fn get_cartesian_product_range(x: Range<usize>, y: Range<usize>)
    -> Vec<(usize,usize)> {
    x.map(|row| y.clone().map(move |column| (row,column)))
        .flatten()
        .collect()
}

fn get_all_galaxies(universe: &Vec<Vec<UniverseNode>>) -> Vec<(usize,usize)> {
    get_cartesian_product_range(0..universe.len(), 0..universe[0].len())
        .into_iter()
        .filter(|(y,x)| {
            match universe[*y][*x] {
                 UniverseNode::EmptySpace => false,
                 UniverseNode::Galaxy(_) => true
            }
        })
    .collect()
}

fn get_neighbors(node: &(usize,usize), universe: &Vec<Vec<UniverseNode>>) 
    -> Vec<(usize, usize)> {
    let neighbors = [
        (node.0 as i64, node.1 as i64 + 1),
        (node.0 as i64, node.1 as i64 - 1),
        (node.0 as i64 - 1, node.1 as i64),
        (node.0 as i64 + 1, node.1 as i64)
    ];
    neighbors.into_iter()
        .filter(|(y,x)| 
            (0..universe.len() as i64).contains(y) 
            && (0..universe[0].len() as i64).contains(x)
        )
        .map(|(y,x)| (y as usize, x as usize))
        .collect()
}


fn double_row(row: usize, mut galaxy_map: Vec<Vec<char>>) -> Vec<Vec<char>> {
    galaxy_map.insert(row, galaxy_map[row].clone());
    galaxy_map
}

fn double_column(column: usize, mut galaxy_map: Vec<Vec<char>>) 
    -> Vec<Vec<char>> {
    for row in galaxy_map.iter_mut() {
        row.insert(column, row[column]);
    }
    galaxy_map
}

fn parse_galaxy(raw: &str) -> Vec<Vec<char>> {
     raw.split("\n")
        .filter(|x| !x.is_empty())
        .map(|x| Vec::from_iter(x.chars()))
        .collect::<Vec<Vec<char>>>()
}

fn get_free_rows(galaxy_map: &Vec<Vec<UniverseNode>>) -> Vec<usize> {
    galaxy_map.iter().enumerate()
        .filter(|(_,x)| x.iter().all(|&x| x.is_empty_space()))
        .map(|(index,_)| index)
        .collect()
}

fn get_free_columns(galaxy_map: &Vec<Vec<UniverseNode>>) -> Vec<usize> {
    let mut free_columns = vec![];
    for column in 0..galaxy_map[0].len() {
        if galaxy_map.iter().map(|x| x[column]).all(|x| x.is_empty_space()) {
            free_columns.push(column);
        }
    }
    free_columns
}


fn draw_galaxy(galaxy_map: &Vec<Vec<char>>) {
    for row in galaxy_map.iter() {
        println!("{}", String::from_iter(row.iter()))
    }
}

fn draw_universe(galaxy_map: &Vec<Vec<UniverseNode>>) {
    for row in galaxy_map.iter() {
        for &column in row.iter() {
            match column {
                UniverseNode::EmptySpace => print!("."),
                UniverseNode::Galaxy(num) => print!("{}", num.to_string()),
            }
        }
        println!()
    }
}

fn enumerate_universe(galaxy_map: &Vec<Vec<char>>) -> Vec<Vec<UniverseNode>> {
    let mut enumerated_galaxy = vec![];
    let mut enumerated_galaxy_row;
    let mut counter = 1;
    for row in galaxy_map.iter() {
        enumerated_galaxy_row = vec![];
        for &column in row.iter() {
            if column == '#' {
                enumerated_galaxy_row.push(UniverseNode::Galaxy(counter));
                counter += 1;
            } else {
                enumerated_galaxy_row.push(UniverseNode::EmptySpace);
            }
        }
        enumerated_galaxy.push(enumerated_galaxy_row);
    }
    enumerated_galaxy
}

fn galaxy_position_to_name(position: (usize,usize), 
                           universe: &Vec<Vec<UniverseNode>>) -> usize {
    match universe[position.0][position.1] {
        UniverseNode::EmptySpace => panic!("Invalid parameter: Not a galaxy"),
        UniverseNode::Galaxy(x) => x as usize,
    }
}


#[cfg(test)]
mod tests {
    use super::*;
    const PART_ONE: &str = 
        "...#......\n\
         .......#..\n\
         #.........\n\
         ..........\n\
         ......#...\n\
         .#........\n\
         .........#\n\
         ..........\n\
         .......#..\n\
         #...#.....";

    const PART_ONE_EXPANDED: &str =
       "....#........\n\
        .........#...\n\
        #............\n\
        .............\n\
        .............\n\
        ........#....\n\
        .#...........\n\
        ............#\n\
        .............\n\
        .............\n\
        .........#...\n\
        #....#.......";

    #[test]
    fn part1() {
        let galaxy = parse_galaxy(PART_ONE);
        let expanded_galaxy = parse_galaxy(PART_ONE_EXPANDED);


        let universe = enumerate_universe(&galaxy);
        assert_eq!(
            (get_free_rows(&universe), get_free_columns(&universe)),
            (vec![3,7], vec![2,5,8])
        );
        let distances = get_distances_to_galaxies((5,1), &universe, &2);
        assert_eq!((1..=get_galaxy_count(&universe)).combinations(2)
            .map(|x| (x[0], x[1])).count(), 36);
        println!("distances: {:?}", distances);
        assert_eq!(
            distances[
             distances.iter()
                .position(|((y,x),_)| *y == 9 && *x == 4).unwrap()
            ].1,
            9
            );


        let unique_galaxies  = (1..=get_galaxy_count(&universe))
            .combinations(2)
            .map(|x| (x[0], x[1]))
            .collect_vec();
        println!("pairs: {:?}", unique_galaxies);
        let shortes_path_sum: usize =  shortes_distance_galaxies(&universe,&2)
            .into_iter()
            .filter(|(x, _)| unique_galaxies.contains(x))
            .map(|(_,d)| d as usize)
            .sum();
        assert_eq!(shortes_path_sum, 374);

        let shortes_path_sum: usize =  shortes_distance_galaxies(&universe,&10)
            .into_iter()
            .filter(|(x, _)| unique_galaxies.contains(x))
            .map(|(_,d)| d as usize)
            .sum();
        assert_eq!(shortes_path_sum, 1030);

        let shortes_path_sum: usize =  shortes_distance_galaxies(&universe,&100)
            .into_iter()
            .filter(|(x, _)| unique_galaxies.contains(x))
            .map(|(_,d)| d as usize)
            .sum();
        assert_eq!(shortes_path_sum, 8410);
    }
}


