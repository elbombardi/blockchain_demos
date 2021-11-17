package main

import (
	"encoding/json"
	"fmt"
	"syscall/js"
)

func main() {
	fmt.Println("GO Web Assembly Demo!")
	js.Global().Set("formatJSON", jsonWrapper())
	<-make(chan bool)
}

func prettyJson(input string) (string, error) {
	var raw interface{}
	err := json.Unmarshal([]byte(input), &raw)
	if err != nil {
		return "", err
	}
	prettyJson, err := json.MarshalIndent(raw, "", "  ")
	if err != nil {
		return "", err
	}
	return string(prettyJson), nil
}

func jsonWrapper() js.Func {
	return js.FuncOf(func(this js.Value, args []js.Value) interface{} {
		fmt.Printf("this %v \nargs %v \n", this, args)
		if len(args) != 1 {
			return fmt.Sprintf("Expected 1 argument, found %d argument(s) ", len(args))
		}
		input := args[0].String()
		pretty, err := prettyJson(input)
		if err != nil {
			return fmt.Sprint(err)
		}
		return pretty
	})
}
