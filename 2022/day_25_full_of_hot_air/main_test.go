package main

import (
	"fmt"
	"testing"
)

func TestSnafuToDecimal(t *testing.T) {
	testCases := []struct {
		snafu   string
		decimal int
	}{
		{
			"1=-0-2",
			1747,
		},
		{
			"12111",
			906,
		},
		{
			"2=0=",
			198,
		},
		{
			"21",
			11,
		},
		{
			"1121-1110-1=0",
			314159265,
		},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("convert %s to %v", tc.snafu, tc.decimal), func(t *testing.T) {
			ans := SnafuToDecimal(tc.snafu)
			if ans != tc.decimal {
				t.Errorf("snafu to decimal conversion failed: %v converted to %v but %v expected", tc.snafu, ans, tc.decimal)
			}
		})
	}
}

func TestDecimalToSnafu(t *testing.T) {
	testCases := []struct {
		snafu   string
		decimal int
	}{
		{
			"1=-0-2",
			1747,
		},
		{
			"12111",
			906,
		},
		{
			"2=0=",
			198,
		},
		{
			"21",
			11,
		},
		{
			"1121-1110-1=0",
			314159265,
		},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("convert %s to %v", tc.snafu, tc.decimal), func(t *testing.T) {
			ans := DecimalToSnafu(tc.decimal)
			if ans != tc.snafu {
				t.Errorf("decimal to snafu conversion failed: %v converted to %v but %v expected", tc.decimal, ans, tc.snafu)
			}
		})
	}
}
