package main

import (
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

// fast_scan.go
// High-performance Go-based port scanner for AegisScan

func scanPort(protocol, hostname string, port int, wg *sync.WaitGroup) {
	defer wg.Done()
	address := fmt.Sprintf("%s:%d", hostname, port)
	conn, err := net.DialTimeout(protocol, address, 2*time.Second)
	if err == nil {
		fmt.Printf("[OPEN] %d/%s\n", port, protocol)
		conn.Close()
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: fast_scan <hostname>")
		os.Exit(1)
	}

	hostname := os.Args[1]
	var wg sync.WaitGroup

	fmt.Printf("[*] Scanning host: %s\n", hostname)

	// Scanning common ports for high performance
	commonPorts := []int{21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080, 8443}

	for _, port := range commonPorts {
		wg.Add(1)
		go scanPort("tcp", hostname, port, &wg)
	}

	wg.Wait()
	fmt.Println("[*] Port scan completed.")
}
