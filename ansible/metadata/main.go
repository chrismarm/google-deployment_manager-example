package main

import (
	"fmt"
	"github.com/hokaccha/go-prettyjson"
	"io/ioutil"
	"log"
	"net/http"
)

const SHOW_ALL = "/?recursive=true&alt=json"
const METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/%s"

func main() {
	http.HandleFunc("/metadata", func(w http.ResponseWriter, r *http.Request) {
		remoteAddress := r.RemoteAddr
		projId := makeRequest(w, "project/projectid", false)
		projNumId := makeRequest(w, "project/numeric-project-id", false)
		metadata := makeRequest(w, "instance", true)

		w.Write([]byte(fmt.Sprintf("Connection from %s\nProject ID: %s ( %s )\nInstance metadata:\n%s", remoteAddress, projId, projNumId, metadata)))
	})
	log.Fatal(http.ListenAndServe(":8000", nil))
}

func writeError(w http.ResponseWriter, endpoint string) {
	w.Write([]byte(fmt.Sprintf("Error retrieving metadata from endpoint %s", endpoint)))
	w.WriteHeader(500)
}

func makeRequest(w http.ResponseWriter, endpoint string, showAll bool) string {
	client := &http.Client{}
	url := fmt.Sprintf(METADATA_URL, endpoint)
	if showAll {
		url += SHOW_ALL
	}
	req, err := http.NewRequest("GET", url, nil)
	req.Header.Add("Metadata-Flavor", "Google")
	response, err := client.Do(req)
	if err != nil {
		log.Fatal("The HTTP request failed with error %s\n", err)
		writeError(w, endpoint)
		return ""
	} else {
		w.WriteHeader(200)
		data, _ := ioutil.ReadAll(response.Body)
		formattedData, _ := prettyjson.Format(data)
		return string(formattedData)
	}
}
