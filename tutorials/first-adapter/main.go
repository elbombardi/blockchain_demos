package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"

	"github.com/julienschmidt/httprouter"
)

type AdapterResponse struct {
	JobRunId string      `json:"id"`
	Data     AdapterData `json:"data"`
	Error    error       `json:"error"`
}

type AdapterData struct {
	Result []int `json:"result"`
}

type QueryParameter struct {
	Data map[string]interface{} `json:"data"`
	Id   string                 `json:"id"`
}

const adapterPort = ":6060"
const jsonHeader = "application/json; charset=UTF-8"

func main() {
	router := httprouter.New()
	router.GET("/random", randomNumber)
	router.POST("/random", randomNumber)

	http.ListenAndServe(adapterPort, router)
}

func randomNumber(w http.ResponseWriter, r *http.Request, params httprouter.Params) {
	w.Header().Set("Content-Type", jsonHeader)
	size := 1
	id := "0"
	queryParams, err := readQueryParams(r)
	if err == nil {
		id = queryParams.Id
		sizeParam := queryParams.Data["size"]
		if sizeParam != nil {
			size = int(sizeParam.(float64))
		}
	}
	num := []int{}
	for i := 0; i < size; i++ {
		num = append(num, rand.Intn(100))
	}
	result := &AdapterResponse{
		JobRunId: id,
		Data:     AdapterData{Result: num},
		Error:    nil,
	}
	fmt.Printf("Size: %v, Randoms: %v \n", size, num)
	_ = json.NewEncoder(w).Encode(result)
}

func readQueryParams(r *http.Request) (*QueryParameter, error) {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		return nil, err
	}
	qp := QueryParameter{}
	if err = json.Unmarshal(body, &qp); err != nil {
		return nil, err
	}
	return &qp, nil
}
