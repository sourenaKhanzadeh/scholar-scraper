package main

import (
	"encoding/json"
	"net/http"
	"scholar-scraper-server/shared"
)

func scrapeHandler(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query().Get("query")
	if query == "" {
		http.Error(w, "Query parameter is required", http.StatusBadRequest)
		return
	}

	proxy := shared.GetProxy()
	result := map[string]string{
		"query":  query,
		"proxy":  proxy,
		"status": "Request forwarded to scraper service",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(result)
}
