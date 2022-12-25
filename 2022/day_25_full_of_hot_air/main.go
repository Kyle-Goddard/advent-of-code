package main

import (
	"bufio"
	"bytes"
	"fmt"
	"math"
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func parseFile(data []byte) []string {
	var result []string

	reader := bytes.NewReader(data)
	scanner := bufio.NewScanner(reader)
	for scanner.Scan() {
		line := scanner.Text()
		line = strings.TrimSpace(line)

		result = append(result, line)

	}

	return result
}

func main() {
	data, err := os.ReadFile("/Users/kyle/Documents/Learning/advent-of-code/2022/day_25_full_of_hot_air/puzzle_input.txt")
	check(err)

	fuelRequirements := parseFile(data)

	// fmt.Printf("%v", fuelRequirements)

	sum := 0
	for _, f := range fuelRequirements {
		sum += SnafuToDecimal(f)
	}

	fmt.Printf("%s\n", DecimalToSnafu(sum))
}

func SnafuToDecimal(snafu string) int {
	maxLen := len(snafu) - 1
	result := 0

	for i, s := range snafu {
		multiplier := 0
		switch s {
		case '2':
			multiplier = 2
		case '1':
			multiplier = 1
		case '-':
			multiplier = -1
		case '=':
			multiplier = -2
		}

		result += multiplier * int(math.Pow(5, float64(maxLen)-float64(i)))
	}

	return result
}

func DecimalToSnafu(decimal int) string {
	maxLen := 0
	if decimal < 1 {
		maxLen = 1
	} else {
		maxLen = int(math.Floor(math.Log(float64(decimal))/math.Log(5)) + 1)
	}
	result := ""

	for maxLen >= 0 {

		remainders := []int{2, 1, 0, -1, -2}
		for i := 0; i < 5; i++ {
			remainders[i] = decimal - remainders[i]*int(math.Pow(5, float64(maxLen)))
		}

		idx := indexOfMinAbsoluteVal(remainders)
		switch idx {
		case 0:
			result += "2"
		case 1:
			result += "1"
		case 2:
			if len(result) > 0 {
				result += "0"
			}
		case 3:
			result += "-"
		case 4:
			result += "="
		}

		maxLen--
		decimal = remainders[idx]
	}

	return result
}

func indexOfMinAbsoluteVal(arr []int) int {
	idx := 0
	min := math.Abs(float64(arr[idx]))
	for i, val := range arr {
		if math.Abs(float64(val)) < min {
			idx = i
			min = math.Abs(float64(arr[idx]))
		}
	}
	return idx
}
