# Go Load Balancer and API Server

## Load Balancer
- **Location:** `go/load_balancer/main.go`
- **Description:** Manages proxy rotation and forwards requests to scraper services.

## API Server
- **Location:** `go/api_server/server.go`
- **Description:** Receives scraping requests and interacts with the load balancer to distribute tasks.

### Running Services:
1. **Load Balancer:**
   ```bash
   go run go/load_balancer/main.go
   ```

2. **API Server:**
   ```bash
   go run go/api_server/server.go
   ```