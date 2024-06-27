from unittest.mock import AsyncMock, patch

import pytest
from discord import Client
from discord.abc import Messageable

from main import previously_upnormal, send_notification


@pytest.mark.asyncio
@patch.object(Client, 'get_channel', return_value=Messageable())
@patch.object(Messageable, 'send', return_value=None, new_callable=AsyncMock)
async def test_notification_send_only_on_ris_change_below_30_or_under_70(mock_get_chanel: AsyncMock, mock_send: AsyncMock):
    previously_upnormal.set(False)
    
    await send_notification(66)
    mock_send.assert_not_called()
    await send_notification(71)
    mock_send.assert_called_once()
    await send_notification(71)
    mock_send.assert_called_once()
