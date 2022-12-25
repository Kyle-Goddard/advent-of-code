package main

import (
	"bufio"
	"bytes"
	"fmt"
	"os"
	"strings"

	"day23/elf"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func parseFile(data []byte) []*elf.Elf {
	var result []*elf.Elf

	y := 0

	reader := bytes.NewReader(data)
	scanner := bufio.NewScanner(reader)
	for scanner.Scan() {
		line := scanner.Text()
		line = strings.TrimSpace(line)

		for x, char := range line {
			if char == '#' {
				result = append(result, elf.NewElf(x, -y))
			}
		}
		y++
	}

	for _, e := range result {
		e.ResetPosition(e.Xpos(), e.Ypos()+y-1)
	}

	return result
}

func displayMap(elves []*elf.Elf) {
	minX, maxX, minY, maxY := elves[0].Xpos(), elves[0].Xpos(), elves[0].Ypos(), elves[0].Ypos()

	current := make(map[elf.Position]bool)
	for _, e := range elves {
		current[e.Position()] = true
		if e.Xpos() > maxX {
			maxX = e.Xpos()
		}
		if e.Xpos() < minX {
			minX = e.Xpos()
		}
		if e.Ypos() > maxY {
			maxY = e.Ypos()
		}
		if e.Ypos() < minY {
			minY = e.Ypos()
		}
	}

	show := ""

	for j := maxY; j >= minY; j-- {
		for i := minX; i <= maxX; i++ {
			pos := elf.NewPos(i, j)
			if !current[*pos] {
				show += "_"
			} else {
				show += "#"
			}

		}
		show += "\n"
	}

	fmt.Printf("%s", show)
}

func getScore(elves []*elf.Elf) int {
	minX, maxX, minY, maxY := elves[0].Xpos(), elves[0].Xpos(), elves[0].Ypos(), elves[0].Ypos()

	current := make(map[elf.Position]bool)
	for _, e := range elves {
		current[e.Position()] = true
		if e.Xpos() > maxX {
			maxX = e.Xpos()
		}
		if e.Xpos() < minX {
			minX = e.Xpos()
		}
		if e.Ypos() > maxY {
			maxY = e.Ypos()
		}
		if e.Ypos() < minY {
			minY = e.Ypos()
		}
	}

	score := 0
	for i := minX; i <= maxX; i++ {
		for j := minY; j <= maxY; j++ {
			pos := elf.NewPos(i, j)
			if !current[*pos] {
				score++
			}

		}
	}
	return score
}

func main() {
	data, err := os.ReadFile("/Users/kyle/Documents/Learning/advent-of-code/2022/day_23_unstable_diffusion/puzzle_input.txt")
	check(err)

	elves := parseFile(data)

	// fmt.Printf("%v", elves)

	movers := 1
	t := 0
	score := 0

	for movers > 0 {
		current := make(map[elf.Position]bool)
		for _, e := range elves {
			current[e.Position()] = true
		}

		proposed := make(map[elf.Position]int)
		for _, e := range elves {
			nextPos := e.ProposeNextMove(current, elf.DirectionCycle[t%4])
			if nextPos != nil {
				proposed[*nextPos] += 1
			}
		}

		score = getScore(elves)
		movers = len(proposed)
		fmt.Printf("t= %v, score = %v, movers = %v \n", t, score, movers)
		// displayMap(elves)

		for _, e := range elves {
			nextPosition := e.NextPosition()
			if proposed[nextPosition] == 1 {
				e.MakeMove()
			}
		}

		t += 1
	}
	fmt.Printf("FINAL: %v\n", t)
}
