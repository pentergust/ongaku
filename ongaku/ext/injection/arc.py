"""Arc Injection.

Adds arc's ensure player, so you don't have to make sure its a player.
"""

from ongaku import errors
from ongaku.client import Client

try:
    import arc
except ImportError:
    raise ImportError("Arc is required for you to use arc_ensure_player.")


async def arc_ensure_player(ctx: arc.GatewayContext):
    """Arc ensure player.

    This is an arc hook, that ensures that the player you are injecting, exists.

    Example
    -------
    ```py
    from ongaku.ext import injection


    @arc.with_hook(injection.arc_ensure_player)
    @arc.slash_command("name", "description")
    async def example_command(
        ctx: arc.GatewayContext, player: ongaku.Player
    ) -> None:
        await player.pause()
    ```

    Parameters
    ----------
    ctx
        The context for the hook.
    """
    if ctx.guild_id is None:
        raise arc.GuildOnlyError

    try:
        client = ctx.get_type_dependency(Client)
    except KeyError as e:
        raise errors.PlayerMissingError from e

    client.fetch_player(ctx.guild_id)
