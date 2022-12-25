package elf

type Direction string

type Elf struct {
	pos     *Position
	nextPos *Position
}

type Position struct {
	x int
	y int
}

const (
	NORTH Direction = "N"
	SOUTH Direction = "S"
	EAST  Direction = "E"
	WEST  Direction = "W"
)

var DirectionCycle DirSlice = []Direction{NORTH, SOUTH, WEST, EAST}

type DirSlice []Direction

func NewElf(x, y int) *Elf {
	newElf := Elf{
		pos: &Position{
			x: x,
			y: y,
		},
		nextPos: &Position{
			x: x,
			y: y,
		},
	}

	return &newElf
}

func NewPos(x, y int) *Position {
	return &Position{
		x: x,
		y: y,
	}
}

func (e *Elf) ResetPosition(x, y int) {
	e.pos = &Position{
		x: x,
		y: y,
	}
	e.nextPos = &Position{
		x: x,
		y: y,
	}
}

func (e *Elf) Xpos() int {
	return e.pos.x
}

func (e *Elf) Ypos() int {
	return e.pos.y
}

func (e *Elf) Position() Position {
	return Position{x: e.pos.x, y: e.pos.y}
}

func (e *Elf) NextPosition() Position {
	return Position{x: e.nextPos.x, y: e.nextPos.y}
}

func (e *Elf) SetNextPosition(dir Direction) *Position {
	switch dir {
	case NORTH:
		e.nextPos = &Position{x: e.pos.x, y: e.pos.y + 1}
	case SOUTH:
		e.nextPos = &Position{x: e.pos.x, y: e.pos.y - 1}
	case EAST:
		e.nextPos = &Position{x: e.pos.x + 1, y: e.pos.y}
	case WEST:
		e.nextPos = &Position{x: e.pos.x - 1, y: e.pos.y}
	}

	return e.nextPos
}

func (e *Elf) shouldMove(elfMap map[Position]bool) bool {
	surrounds := []Position{
		{x: 1, y: 0},
		{x: 0, y: 1},
		{x: -1, y: 0},
		{x: 0, y: -1},
		{x: 1, y: 1},
		{x: 1, y: -1},
		{x: -1, y: 1},
		{x: -1, y: -1},
	}

	for _, s := range surrounds {
		if elfMap[Position{x: e.pos.x + s.x, y: e.pos.y + s.y}] {
			return true
		}
	}
	return false
}

func (e *Elf) ProposeNextMove(elfMap map[Position]bool, preferredDirection Direction) *Position {
	if !e.shouldMove(elfMap) {
		return nil
	}
	idx := DirectionCycle.indexOf(preferredDirection)

	for i := 0; i < 4; i++ {
		tempDir := DirectionCycle[(idx+i)%4]
		moves := make(map[int]Position)

		switch tempDir {
		case NORTH:
			moves[0] = Position{x: e.pos.x, y: e.pos.y + 1}
			moves[1] = Position{x: e.pos.x + 1, y: e.pos.y + 1}
			moves[2] = Position{x: e.pos.x - 1, y: e.pos.y + 1}
		case SOUTH:
			moves[0] = Position{x: e.pos.x, y: e.pos.y - 1}
			moves[1] = Position{x: e.pos.x + 1, y: e.pos.y - 1}
			moves[2] = Position{x: e.pos.x - 1, y: e.pos.y - 1}
		case EAST:
			moves[0] = Position{x: e.pos.x + 1, y: e.pos.y}
			moves[1] = Position{x: e.pos.x + 1, y: e.pos.y + 1}
			moves[2] = Position{x: e.pos.x + 1, y: e.pos.y - 1}
		case WEST:
			moves[0] = Position{x: e.pos.x - 1, y: e.pos.y}
			moves[1] = Position{x: e.pos.x - 1, y: e.pos.y + 1}
			moves[2] = Position{x: e.pos.x - 1, y: e.pos.y - 1}
		}
		if !elfMap[moves[0]] && !elfMap[moves[1]] && !elfMap[moves[2]] {
			return e.SetNextPosition(tempDir)
		}

	}
	// samePos := e.Position()
	return nil
}

func (e *Elf) MakeMove() {
	e.pos = e.nextPos
}

func (d *DirSlice) indexOf(value Direction) int {
	for i, v := range *d {
		if v == value {
			return i
		}
	}
	return -1
}
