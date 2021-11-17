package main

import (
	"fmt"
	"net/http"
)

func main() {
	fmt.Println("Starting server at http://localhost:9090...")
	err := http.ListenAndServe(":9090", http.FileServer(http.Dir("./assets")))
	if err != nil {
		fmt.Println("Failed to start web server : ", err)
	}
}
