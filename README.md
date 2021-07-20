# hodlthevoid

### WIP

Add a .env file:

```
export PRIVATE_KEY=''
export WEB3_INFURA_PROJECT_ID=''
export ATTACKER_KEY=''
export USER_KEY=''

export ETHERSCAN_TOKEN=''
# export IPFS_URL=http://127.0.0.1:5001
# export UPLOAD_IPFS=true
export PINATA_API_KEY=''
export PINATA_API_SECRET=''
export PINATA_JWT_SECRET='' 
```

Run `source .env`

To build the smart contracts and generate ABIs, run `brownie compile`

To deploy a contract, run `brownie run scripts/your_deployment_script.py --network rinkeby`

To run a script, run `brownie run scripts/script.py --network rinkeby`

Current scripts include
`create_collectible.py`
`view_token.py`
`withdraw_funds.py`

