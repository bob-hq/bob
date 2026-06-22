import abc
from typing import Any, Self


class Scope(abc.ABC):
    @abc.abstractmethod
    def close(self) -> None: ...

    def __enter__(self) -> "Scope":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def __or__(self, other: Self | "ScopeList") -> "Scope":
        return ScopeList([self]) | other


class ScopeList(Scope):
    def __init__(self, scopes: list[Scope]) -> None:
        self.scopes = scopes

    def close(self) -> None:
        for scope in self.scopes:
            scope.close()

    def __or__(self, other: Scope | Self) -> Scope:
        if isinstance(other, ScopeList):
            return ScopeList(self.scopes + other.scopes)
        return ScopeList(self.scopes + [other])


class DictionaryScope(Scope):
    def __init__(self, variables: dict[str, Any], changes: dict[str, Any]) -> None:
        self.variables = variables
        self.changes = changes

        original: dict[str, Any] = {}
        for key, value in changes.items():
            if key in variables:
                original[key] = variables.pop(key)

            variables[key] = value

        self.original = original

    def close(self) -> None:
        for key in self.changes:
            assert self.variables[key] == self.changes[key]

            if key in self.original:
                self.variables[key] = self.original[key]
            else:
                self.variables.pop(key)

        self.original = {}
        self.changes = {}
        self.variables = {}


class AttributeScope(Scope):
    def __init__(self, object: Any, changes: dict[str, Any]) -> None:
        self.object = object
        self.changes = changes

        original: dict[str, Any] = {}
        for key, value in changes.items():
            if hasattr(object, key):
                original[key] = getattr(object, key)

            setattr(object, key, value)

        self.original = original

    def close(self) -> None:
        for key in self.changes:
            # The `object` mustn't have changed underneath our feet, we have no sensible action in that case.
            assert getattr(self.object, key) == self.changes[key]

            if key in self.original:
                setattr(self.object, key, self.original[key])
            else:
                delattr(self.object, key)

        self.original = {}
        self.changes = {}
        self.object = None
