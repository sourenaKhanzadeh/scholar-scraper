package main

import (
	"log"
	"net/http"
)

func StartAPIServer() {
	log.Println("Starting API Server on port 8090...")
	http.HandleFunc("/api/scrape", scrapeHandler)
	err := http.ListenAndServe(":8090", nil)
	if err != nil {
		log.Fatalf("API Server failed to start: %v", err)
	}
}

func main() {
	StartAPIServer()
}
