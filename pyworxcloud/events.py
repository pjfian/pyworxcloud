"""Landroid Cloud callback events"""
# pylint: disable=unnecessary-lambda
from __future__ import annotations

from enum import IntEnum
from typing import Any


class LandroidEvent(IntEnum):
    """Enum for Landroid event types."""

    DATA_RECEIVED = 0
    MQTT_CONNECTION = 1
    MQTT_RATELIMIT = 2
    MQTT_PUBLISH = 3
    LOG = 4


def check_syntax(args: dict[str, Any], objs: list[str], expected_type: Any) -> bool:
    """Check if the object is of the expected type."""
    for obj in objs:
        if not obj in args:
            return False
        if not isinstance(args[obj], expected_type):
            return False

    return True


class EventHandler:
    """Event handler for Landroid Cloud."""

    __events: dict[LandroidEvent, Any] = {}

    def __init__(self) -> None:
        """Initialize the event handler object."""

    def set_handler(self, event: LandroidEvent, func: Any) -> None:
        """Set handler for a LandroidEvent"""
        self.__events.update({event: func})

    def del_handler(self, event: LandroidEvent) -> None:
        """Remove a handler for a LandroidEvent."""
        self.__events.pop(event)

    def call(self, event: LandroidEvent, **kwargs) -> bool:
        """Call a handler if it was set."""
        if not event in self.__events:
            # Event was not set
            return False

        if LandroidEvent.DATA_RECEIVED == event:
            if not check_syntax(kwargs, ["name", "device"], str):
                return False

            self.__events[event](name=kwargs["name"], device=kwargs["device"])
            return True
        elif LandroidEvent.MQTT_CONNECTION == event:
            if not check_syntax(kwargs, ["state"], bool):
                return False

            self.__events[event](state=kwargs["state"])
            return True
        elif LandroidEvent.MQTT_RATELIMIT == event:
            if not check_syntax(kwargs, ["message"], str):
                return False

            self.__events[event](message=kwargs["message"])
            return True
        elif LandroidEvent.MQTT_PUBLISH == event:
            if not check_syntax(kwargs, ["message", "device", "topic"], str):
                return False

            if not check_syntax(kwargs, ["qos"], int):
                return False

            if not check_syntax(kwargs, ["retain"], bool):
                return False

            self.__events[event](
                message=kwargs["message"],
                qos=kwargs["qos"],
                retain=kwargs["retain"],
                device=kwargs["device"],
                topic=kwargs["topic"],
            )
            return True
        elif LandroidEvent.LOG == event:
            if not check_syntax(kwargs, ["message", "level"], str):
                return False

            self.__events[event](
                message=kwargs["message"],
                level=kwargs["level"],
            )
            return True
        else:
            # Not a valid LandroidEvent
            return False
