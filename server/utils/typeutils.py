from typing import Dict, List, Union


JsonSerializable = Union[None, int, str, bool, List['JsonSerializable'], Dict[str, 'JsonSerializable']]