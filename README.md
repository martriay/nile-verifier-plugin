# ⛵️✅ Nile verifier plugin

Plugin for [Nile](https://github.com/OpenZeppelin/nile) to verify contracts on [starkscan.co](https://starkscan.co).

## Installation

```
pip install nile-verifier
```

## Usage

```
nile verify CONTRACT_PATH --network NETWORK [--compiler_version COMPILER_VERSION --cairo_path CAIRO_PATH]
```

For example:
```
$ nile verify contracts/uwu.cairo --network goerli
🔎 Verifying uwu on goerli...
✅ Success! https://testnet.starkscan.co/class/0x226718449b40fa299d718eb50f72af707f2210e540e11a830c2ad72a235d5e0#code
```

Note that the contract has to be declared, or the verification will fail
```
$ nile verify contracts/uwu.cairo --network goerli
❌ Could not find any contract with hash 0x226718449b40fa299d718eb50f72af707f2210e540e11a830c2ad72a235d5e0
🤔 Are you sure you deployed to goerli?
```

Include the `--cairo_path` argument or `CAIRO_PATH` environment variable as a colon-separated list if you have libraries in different directories:
```
$ nile verify contracts/uwu.cairo --network goerli --cairo_path contracts:lib
🔎 Verifying uwu on goerli...
✅ Success! https://testnet.starkscan.co/class/0x226718449b40fa299d718eb50f72af707f2210e540e11a830c2ad72a235d5e0#code
```

## License

MIT.

