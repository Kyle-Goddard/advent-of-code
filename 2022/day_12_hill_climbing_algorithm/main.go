package main

import (
	"bufio"
	"bytes"
	"fmt"
	"math"
	"os"
	"strings"
)

type Position struct {
	x int
	y int
}

type Node struct {
	Parent   *Node
	Position Position
	Height   int

	g int
	h int
	f int
}

func (n *Node) height(elevationMap [][]int) int {
	return elevationMap[n.Position.y][n.Position.x]
}

func NewNode(pos Position, z int, parent *Node) *Node {
	return &Node{
		Parent:   parent,
		Position: pos,
		Height:   z,
		g:        0,
		h:        0,
		f:        0,
	}
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func parseFile(data []byte) (*Position, *Position, [][]int, int, int) {
	var result [][]int
	var startCoords Position
	var endCoords Position

	y := 0

	reader := bytes.NewReader(data)
	scanner := bufio.NewScanner(reader)
	rowLen := 0
	for scanner.Scan() {
		line := scanner.Text()
		line = strings.TrimSpace(line)

		row := []int{}
		rowLen = len(line)
		for x, char := range line {
			if char == 'S' {
				startCoords = Position{x, y}
				char = 'a'
			}
			if char == 'E' {
				endCoords = Position{x, y}
				char = 'z'
			}
			row = append(row, int(char)-96)
		}

		result = append(result, row)
		y++
	}

	return &startCoords, &endCoords, result, rowLen, y
}

func main() {
	data, err := os.ReadFile("/Users/kyle/Documents/Learning/advent-of-code/2022/day_12_hill_climbing_algorithm/puzzle_input.txt")
	check(err)

	start, end, elevationMap, xLen, yLen := parseFile(data)

	// fmt.Printf("start: %v ; end: %v", start, end)
	// fmt.Printf("%v\n", elevationMap)

	path := aStar(start, end, elevationMap, xLen, yLen)

	// fmt.Printf("path: %v\n", path)
	fmt.Printf("%v\n", len(path)-1)
	// displayPath(path)
}

func displayPath(path []*Node) {
	visited := make(map[Position]int)

	minX, maxX, minY, maxY := path[0].Position.x, path[0].Position.x, path[0].Position.y, path[0].Position.y

	for n, node := range path {
		visited[node.Position] = n % 10
		if node.Position.x > maxX {
			maxX = node.Position.x
		}
		if node.Position.x < minX {
			minX = node.Position.x
		}
		if node.Position.y > maxY {
			maxY = node.Position.y
		}
		if node.Position.y < minY {
			minY = node.Position.y
		}
	}

	show := ""

	for j := minY; j <= maxY; j++ {
		for i := minX; i <= maxX; i++ {
			if visited[Position{i, j}] > 0 {
				show += fmt.Sprintf("%v", visited[Position{i, j}])
			} else {
				show += "_"
			}
		}
		show += "\n"
	}
	fmt.Println(show)
}

func displayNodes(openList []*Node, closedList map[Position]bool, elevationMap [][]int, xLen int, yLen int) {
	open := make(map[Position]bool)
	for _, node := range openList {
		open[node.Position] = true
	}

	show := ""

	for j := 0; j < yLen; j++ {
		for i := 0; i < xLen; i++ {
			if open[Position{i, j}] {
				show += "@"
			} else if closedList[Position{i, j}] {
				show += "+"
			} else {
				show += string(rune(elevationMap[j][i] + 96))
			}
		}
		show += "\n"
	}
	fmt.Printf("\033[0;0H")
	fmt.Println(show)
}

func aStar(start *Position, end *Position, elevationMap [][]int, xLen int, yLen int) []*Node {
	// Create start and end node
	startNode := NewNode(*start, 1, nil)
	endNode := NewNode(*end, 26, nil)

	// Initialize both open and closed list
	openList := []*Node{}
	closedList := make(map[Position]bool)

	openList = append(openList, startNode)

	// what squares do we search
	allowDiagonalMovement := false
	adjacentSquares := [][]int{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}

	if allowDiagonalMovement {
		adjacentSquares = [][]int{
			{0, -1},
			{0, 1},
			{-1, 0},
			{1, 0},
			{-1, -1},
			{-1, 1},
			{1, -1},
			{1, 1},
		}
	}

	for len(openList) > 0 {
		displayNodes(openList, closedList, elevationMap, xLen, yLen)
		node_idx := 0
		currentNode := openList[node_idx]

		for i, node := range openList {
			if node.f < currentNode.f {
				node_idx = i
				currentNode = openList[node_idx]
			}
		}

		openList = remove(openList, node_idx)
		closedList[currentNode.Position] = true

		// Found the goal
		if currentNode.Position == endNode.Position {

			path := []*Node{}
			current := currentNode
			for current != nil {
				path = append(path, current)
				current = current.Parent
			}
			return reverse(path)
		}

		children := []*Node{}
		for _, nextPos := range adjacentSquares {
			// Get node position
			nodePosition := Position{
				currentNode.Position.x + nextPos[0],
				currentNode.Position.y + nextPos[1],
			}

			// Make sure within range
			if nodePosition.x < 0 ||
				nodePosition.y < 0 ||
				nodePosition.x > len(elevationMap[0])-1 ||
				nodePosition.y > len(elevationMap)-1 {
				continue
			}

			newNode := NewNode(nodePosition, elevationMap[nodePosition.y][nodePosition.x], currentNode)

			// Make sure walkable terrain
			if newNode.Height-currentNode.Height > 1 {
				continue
			}
			children = append(children, newNode)
		}

		for _, child := range children {
			if closedList[child.Position] {
				continue
			}

			// Create the f, g, and h values
			child.g = currentNode.g + 10
			child.h = int(math.Pow(float64(child.Position.x-endNode.Position.x), 2)) +
				int(math.Pow(float64(child.Position.y-endNode.Position.y), 2)) +
				int(math.Pow(26-float64(child.height(elevationMap)), 3))
			child.f = child.g + child.h

			if contains(openList, child) {
				continue
			}

			openList = append(openList, child)

		}

	}
	return []*Node{}
}

func remove(s []*Node, i int) []*Node {
	s[i] = s[len(s)-1]
	return s[:len(s)-1]
}

func reverse[S ~[]E, E any](s S) S {
	for i, j := 0, len(s)-1; i < j; i, j = i+1, j-1 {
		s[i], s[j] = s[j], s[i]
	}
	return s
}

func contains(haystack []*Node, needle *Node) bool {
	for _, val := range haystack {
		if val == needle {
			return true
		}
	}

	return false
}
