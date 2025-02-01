package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)


// ScholarArticle represents an article in the database
type ScholarArticle struct {
	Title        string `json:"title"`
	Link         string `json:"link"`
	Snippet      string `json:"snippet"`
	CitationInfo string `json:"citation_info"`
}

var collection *mongo.Collection

// Connect to MongoDB
func connectDB() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	clientOptions := options.Client().ApplyURI(os.Getenv("MONGO_URI"))
	client, err := mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		log.Fatal(err)
	}

	err = client.Ping(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("✅ Connected to MongoDB")
	collection = client.Database(os.Getenv("DB_NAME")).Collection(os.Getenv("COLLECTION_NAME"))
}

// Get all articles
func getAllArticles(w http.ResponseWriter, r *http.Request) {
	var articles []ScholarArticle
	cursor, err := collection.Find(context.TODO(), bson.M{})
	if err != nil {
		http.Error(w, "Failed to retrieve articles", http.StatusInternalServerError)
		return
	}
	defer cursor.Close(context.TODO())

	for cursor.Next(context.TODO()) {
		var article ScholarArticle
		cursor.Decode(&article)
		articles = append(articles, article)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(articles)
}

// Get article by title
func getArticleByTitle(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	title := params["title"]

	var article ScholarArticle
	err := collection.FindOne(context.TODO(), bson.M{"title": title}).Decode(&article)
	if err != nil {
		http.Error(w, "Article not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(article)
}

func main() {
	connectDB()

	r := mux.NewRouter()
	r.HandleFunc("/articles", getAllArticles).Methods("GET")
	r.HandleFunc("/articles/{title}", getArticleByTitle).Methods("GET")

	fmt.Println("🚀 API Server running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", r))
}
