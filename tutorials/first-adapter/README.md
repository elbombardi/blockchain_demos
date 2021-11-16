1. Deploy the contracts using Remix : 
    - Deploy `Operator.sol` first, and copy it's address
    - Deploy `RandomEAConsumer.sol`, and fund it with Link.

2. Launch the adapter : `go run main.go`

3. Chainlink node configuration (local node): 
    - Add a bridge that points to the adapter (`http://localhost:6060/random`)
    - Add a job specification as in `chainlink_job_specification.toml`
        - In the specification replace the placeholders with your Operator contract address.
    - Go to Key Management, and copy the "Regular" account address.
    - Go to remix where your Operator contract is deployed and call : `setAuthorizedSenders()` by giving your Node address that you just copied.

4. Call `RandomEAConsumer.requestRandomArray()` by giving :
    - The Operator contract address
    - The Job Id
    - The size of the array  