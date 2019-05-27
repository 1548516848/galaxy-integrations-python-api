# GOG Galaxy - Community Integration - Python API

This document is still work in progress.

## Basic Usage

Basic implementation:

```python
import asyncio
from galaxy.api.plugin import Plugin

class PluginExample(Plugin):
    # implement methods
    async def authenticate(self, stored_credentials=None):
        pass

# run plugin event loop
if __name__ == "__main__":
    asyncio.run(PluginExample().run())
```

Use [pyinstaller](https://www.pyinstaller.org/) to create plugin executable.

## Development

Install required packages:
```bash
pip install -r requirements.txt
```

Run tests:
```bash
pytest
```
## Methods Documentation
TODO

## Changelog

### 0.16
* Do not log sensitive data.
* Return `LocalGameState` as int (possible combination of flags).
### 0.15
* `shutdown()` is called on socket disconnection.
### 0.14
* Added required version parameter to Plugin constructor.
