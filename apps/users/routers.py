from aiohttp.web import RouteTableDef, json_response


router = RouteTableDef()


@router.get("/")
async def sex(request): return json_response({"sex": True})