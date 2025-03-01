# disable deprecation warnings

```python
import warnings
from langchain._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
```

