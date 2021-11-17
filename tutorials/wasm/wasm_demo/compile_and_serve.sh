 #!/bin/bash

echo "Cleaning..."
rm -fr "./assets/wasm_exec.js"
rm -fr "./assets/json.wasm"

echo "Copying wasm_exec.js to ./assets/"
cp $GOROOT/misc/wasm/wasm_exec.js ./assets/  

echo "Compiling wasm/main.go json.wasm and copying to ./assets/"
cd wasm
GOOS=js GOARCH=wasm go build -o ../assets/json.wasm
cd ..

echo "Running server..."
open "http://localhost:9090"
go run main.go