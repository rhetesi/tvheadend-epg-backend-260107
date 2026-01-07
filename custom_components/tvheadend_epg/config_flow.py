import logging
from typing import Any

import voluptuous as vol
from urllib.parse import urlparse

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .api.http import (
    TVHHttpApi,
    TVHHttpAuthError,
    TVHHttpConnectionError,
    TVHHttpRequestError,
)

_LOGGER = logging.getLogger(__name__)


class TVHeadendEPGConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for TVHeadend EPG."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            url = user_input["url"].strip().rstrip("/")

            # --- URL VALIDATION ---
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https"):
                errors["url"] = "invalid_url"

            if not parsed.hostname:
                errors["url"] = "invalid_url"

            if not errors:
                try:
                    # --- AUTH + CONNECTION TEST ---
                    api = TVHHttpApi(
                        base_url=url,
                        username=user_input["username"],
                        password=user_input["password"],
                    )

                    # small test request
                    await api.get_epg(limit=1)

                except TVHHttpAuthError:
                    errors["base"] = "auth_failed"

                except TVHHttpConnectionError:
                    errors["base"] = "cannot_connect"

                except TVHHttpRequestError:
                    errors["base"] = "api_error"

                except Exception as err:
                    _LOGGER.exception("Unexpected error during config flow")
                    errors["base"] = "unknown"

                else:
                    # SUCCESS → create entry
                    return self.async_create_entry(
                        title=f"TVHeadend ({parsed.hostname})",
                        data={
                            "url": url,
                            "username": user_input["username"],
                            "password": user_input["password"],
                        },
                    )

        schema = vol.Schema(
            {
                vol.Required("url"): str,
                vol.Required("username"): str,
                vol.Required("password"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
