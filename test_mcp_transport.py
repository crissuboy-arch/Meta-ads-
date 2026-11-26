"""Real MCP transport; SDK is installed by CI, no live service credentials."""
import asyncio
import os
import shutil
import sys
from pathlib import Path
import pytest

mcp = pytest.importorskip("mcp", reason="MCP SDK installed by the CI dependency step")
from mcp.client.stdio import stdio_client


def test_real_stdio_proposal_listing_and_human_approval_gate(tmp_path):
    for name in ('server.py', 'approvals.py', 'meta_api.py'):
        shutil.copy2(Path(__file__).parent / 'mcp' / name, tmp_path / name)
    env = os.environ.copy()
    for name in ('SUPABASE_URL', 'SUPABASE_SERVICE_KEY', 'META_ACCESS_TOKEN', 'META_AD_ACCOUNT_ID'):
        env.pop(name, None)
    env['SSLKEYLOGFILE'] = ''

    async def check():
        parameters = mcp.StdioServerParameters(command=sys.executable,
            args=[str(tmp_path / 'server.py')], env=env, cwd=str(tmp_path))
        async with stdio_client(parameters) as streams:
            async with mcp.ClientSession(*streams) as session:
                await session.initialize()
                tools = await session.list_tools()
                assert {'list_proposals', 'approve_proposal'} <= {tool.name for tool in tools.tools}
                proposals = await session.call_tool('list_proposals', {})
                assert not proposals.isError
                decision = await session.call_tool('approve_proposal', {'proposal_id': 'AUDIT-NO-EXECUTION'})
                assert 'human_approval_required' in ''.join(item.text for item in decision.content if hasattr(item, 'text'))

    asyncio.run(asyncio.wait_for(check(), timeout=20))
