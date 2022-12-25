package elf

import (
	"testing"

	"github.com/alecthomas/assert/v2"
)

func TestProposeNextMove(t *testing.T) {
	testCases := []struct {
		desc        string
		elf         Elf
		preferedDir Direction
		elfMap      map[Position]bool
		assertions  func(t *testing.T, output *Position)
	}{
		{
			desc: "should not propose a new move when other elves are further away",
			elf: Elf{
				pos: &Position{x: 0, y: 0},
			},
			preferedDir: NORTH,
			elfMap: map[Position]bool{
				{
					x: 0,
					y: 2,
				}: true,
			},
			assertions: func(t *testing.T, output *Position) {
				assert.Equal(t, nil, output)
			},
		},
		{
			desc: "should propose to move north",
			elf: Elf{
				pos: &Position{x: 0, y: 0},
			},
			preferedDir: NORTH,
			elfMap: map[Position]bool{
				{
					x: 1,
					y: 0,
				}: true,
			},
			assertions: func(t *testing.T, output *Position) {
				assert.Equal(t, 0, output.x)
				assert.Equal(t, 1, output.y)
			},
		},
		{
			desc: "should propose to move south",
			elf: Elf{
				pos: &Position{x: 0, y: 0},
			},
			preferedDir: SOUTH,
			elfMap: map[Position]bool{
				{
					x: 1,
					y: 0,
				}: true,
			},
			assertions: func(t *testing.T, output *Position) {
				assert.Equal(t, 0, output.x)
				assert.Equal(t, -1, output.y)
			},
		},
		{
			desc: "should propose to move east",
			elf: Elf{
				pos: &Position{x: 0, y: 0},
			},
			preferedDir: EAST,
			elfMap: map[Position]bool{
				{
					x: 0,
					y: 1,
				}: true,
			},
			assertions: func(t *testing.T, output *Position) {
				assert.Equal(t, 1, output.x)
				assert.Equal(t, 0, output.y)
			},
		},
		{
			desc: "should propose to move west",
			elf: Elf{
				pos: &Position{x: 0, y: 0},
			},
			preferedDir: WEST,
			elfMap: map[Position]bool{
				{
					x: 0,
					y: 1,
				}: true,
			},
			assertions: func(t *testing.T, output *Position) {
				assert.Equal(t, -1, output.x)
				assert.Equal(t, 0, output.y)
			},
		},
		{
			desc: "should propose to move north when surrounded",
			elf: Elf{
				pos: &Position{x: 0, y: 0},
			},
			preferedDir: WEST,
			elfMap: map[Position]bool{
				{
					x: 0,
					y: -1,
				}: true,
				{
					x: 1,
					y: 0,
				}: true,
				{
					x: -1,
					y: 0,
				}: true,
			},
			assertions: func(t *testing.T, output *Position) {
				assert.Equal(t, 0, output.x)
				assert.Equal(t, 1, output.y)
			},
		},
		{
			desc: "should propose to move south when surrounded",
			elf: Elf{
				pos: &Position{x: 0, y: 0},
			},
			preferedDir: WEST,
			elfMap: map[Position]bool{
				{
					x: 0,
					y: 1,
				}: true,
				{
					x: 1,
					y: 0,
				}: true,
				{
					x: -1,
					y: 0,
				}: true,
			},
			assertions: func(t *testing.T, output *Position) {
				assert.Equal(t, 0, output.x)
				assert.Equal(t, -1, output.y)
			},
		},
		{
			desc: "should propose to move east when surrounded",
			elf: Elf{
				pos: &Position{x: 0, y: 0},
			},
			preferedDir: NORTH,
			elfMap: map[Position]bool{
				{
					x: 0,
					y: 1,
				}: true,
				{
					x: 0,
					y: -1,
				}: true,
				{
					x: -1,
					y: 0,
				}: true,
			},
			assertions: func(t *testing.T, output *Position) {
				assert.Equal(t, 1, output.x)
				assert.Equal(t, 0, output.y)
			},
		},
		{
			desc: "should propose to move west when surrounded",
			elf: Elf{
				pos: &Position{x: 0, y: 0},
			},
			preferedDir: NORTH,
			elfMap: map[Position]bool{
				{
					x: 0,
					y: 1,
				}: true,
				{
					x: 0,
					y: -1,
				}: true,
				{
					x: 1,
					y: 0,
				}: true,
			},
			assertions: func(t *testing.T, output *Position) {
				assert.Equal(t, -1, output.x)
				assert.Equal(t, 0, output.y)
			},
		},
	}
	for _, tc := range testCases {
		t.Run(tc.desc, func(t *testing.T) {
			elf := tc.elf
			output := elf.ProposeNextMove(tc.elfMap, tc.preferedDir)
			tc.assertions(t, output)
		})
	}
}

func TestResetPosition(t *testing.T) {
	old := Position{
		x: 0,
		y: 0,
	}
	new := Position{
		x: 5,
		y: 4,
	}

	newElf := NewElf(old.x, old.y)

	newElf.ResetPosition(new.x, new.y)

	assert.Equal(t, new, *newElf.pos)
	assert.Equal(t, new, *newElf.nextPos)
}
