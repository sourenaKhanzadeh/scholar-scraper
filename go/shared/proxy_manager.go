package shared

import (
	"math/rand"
	"sync"
)

var proxies = []string{
	"http://proxy1.example.com",
	"http://proxy2.example.com",
	"http://proxy3.example.com",
}

var mu sync.Mutex

func GetProxy() string {
	mu.Lock()
	defer mu.Unlock()
	return proxies[rand.Intn(len(proxies))]
}
