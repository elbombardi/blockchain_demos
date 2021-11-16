package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"

	"github.com/julienschmidt/httprouter"
)

type ExternalAdapterResponse struct {
	JobRunId string              `json:"id"`
	Data     ExternalAdapterData `json:"data"`
	Error    error               `json:"error"`
}

type ExternalAdapterData struct {
	Result []int `json:"result"`
}

const adapterPort = ":6060"
const jsonHeader = "application/json; charset=UTF-8"

// {
// 	"data":{
// 	   "data1": value1
// 	},
// 	"id":"8f8d40f5-c8c9-46b3-8b72-7b76bfb7ee56",
// 	"meta":{
// 	   "oracleRequest":{
// 		  "callbackAddr":"0x9D00A688Bf8C84a240868AF27eEA7923fAA8BD98",
// 		  "callbackFunctionId":"0x6461adc5",
// 		  "cancelExpiration":"1637079108",
// 		  "data":"0x6473697a6501",
// 		  "dataVersion":"1",
// 		  "payment":"1000000000000000000",
// 		  "requestId":"0x183031f397c04f512fa691eee89e725fc4c0c37bb8e7c3edc62628843d3d7b69",
// 		  "requester":"0x9D00A688Bf8C84a240868AF27eEA7923fAA8BD98",
// 		  "specId":"0x3866386434306635633863393436623338623732376237366266623765653536"
// 	   }
// 	}
//  }

type QueryParameter struct {
	Data map[string]interface{} `json:"data"`
	Id   string                 `json:"id"`
}

// starts an external adapter on specified port
func main() {
	router := httprouter.New()
	router.GET("/random", randomNumber)
	router.POST("/random", randomNumber)

	http.ListenAndServe(adapterPort, router)
}

// RandomNumber returns a random int from 0 to 100
func randomNumber(w http.ResponseWriter, r *http.Request, params httprouter.Params) {
	w.Header().Set("Content-Type", jsonHeader)
	queryParams, _ := readQueryParams(r)
	size := queryParams.Data["size"].(float64)
	num := []int{}
	for i := 0; i < int(size); i++ {
		num = append(num, rand.Intn(100))
	}
	result := &ExternalAdapterResponse{
		JobRunId: queryParams.Id,
		Data:     ExternalAdapterData{Result: num},
		Error:    nil,
	}
	fmt.Printf("Size: %v, Randoms: %v \n", size, num)
	_ = json.NewEncoder(w).Encode(result)
}

func readQueryParams(r *http.Request) (*QueryParameter, error) {
	body, err := ioutil.ReadAll(r.Body)
	fmt.Println("--------------")
	fmt.Println(string(body))
	fmt.Println("--------------")
	if err != nil {
		return nil, err
	}
	qp := QueryParameter{}
	if err = json.Unmarshal(body, &qp); err != nil {
		return nil, err
	}
	return &qp, nil
}
