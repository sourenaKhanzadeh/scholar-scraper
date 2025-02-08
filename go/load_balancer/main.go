package main

import (
	"io"
	"log"
	"net/http"
	"net/url"
	"scholar-scraper-server/shared"
)

func main() {
	log.Println("Starting Load Balancer on port 8080...")
	http.HandleFunc("/scrape", handleRequest)
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query().Get("query")

	if query == "" {
		http.Error(w, "Query parameter is required", http.StatusBadRequest)
		return
	}

	// Forward the request to the Python Scraper API
	targetURL := "http://localhost:8000/search?query=" + query

	// Using the selected proxy
	proxyURL, _ := url.Parse(shared.GetProxy())
	client := &http.Client{
		Transport: &http.Transport{
			Proxy: http.ProxyURL(proxyURL),
		},
	}
	req, err := http.NewRequest("GET", targetURL, nil)
	if err != nil {
		http.Error(w, "Failed to create request", http.StatusInternalServerError)
		return
	}

	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, "Failed to forward request to scraper", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	w.Header().Set("Content-Type", "application/json")
	io.Copy(w, resp.Body)
}
