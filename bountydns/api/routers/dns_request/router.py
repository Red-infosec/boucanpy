from fastapi import APIRouter, Depends
from bountydns.core import logger
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core.entities import (
    DnsRequestRepo,
    PaginationQS,
    DnsRequestsResponse,
    DnsRequestResponse,
    DnsRequestData,
    DnsRequestCreateForm,
    ZoneRepo,
)

router = APIRouter()
options = {"prefix": ""}


@router.get(
    "/dns-request", name="dns_request.index", response_model=DnsRequestsResponse
)
async def index(
    pagination: PaginationQS = Depends(PaginationQS),
    dns_request_repo: DnsRequestRepo = Depends(DnsRequestRepo),
    token: TokenPayload = ScopedTo("dns-request:list"),
):
    pg, items = (
        dns_request_repo.paginate(pagination).set_data_model(DnsRequestData).data()
    )
    return DnsRequestsResponse(pagination=pg, dns_requests=items)


@router.post(
    "/dns-request", name="dns_request.store", response_model=DnsRequestResponse
)
async def index(
    form: DnsRequestCreateForm,
    dns_request_repo: DnsRequestRepo = Depends(DnsRequestRepo),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: str = ScopedTo("dns-request:list"),
):

    data = dict(form)
    zone = (
        zone_repo.query()
        .filter(zone_repo.model().domain.like(f"%data['name']"))
        .first()
    )
    if zone:
        data["zone_id"] = zone.id
    else:
        logger.warning(f"No zone found for dns request {data['name']}")
    dns_request = dns_request_repo.create(data).set_data_model(DnsRequestData).data()

    return DnsRequestResponse(dns_request=dns_request)