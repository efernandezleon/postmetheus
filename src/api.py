from aiohttp import web
from metrics import metrics_to_text

routes = web.RouteTableDef()


def run_api(loop):
    """ Setup an AIOHTTP app and run it in a non-blocking mode """
    loop.create_task(_run_server())


async def _run_server():
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "localhost", 8080)
    await site.start()


@routes.get("/metrics")
async def get_metrics(request):
    return web.Response(text=metrics_to_text())
