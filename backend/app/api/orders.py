"""Order/payment API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import (
    User, Order, OrderItem, OrderStatus, FixPackage, Issue,
    Implementation, ImplementationStatus, Audit,
)
from app.schemas.schemas import (
    OrderCreate, OrderResponse, OrderItemResponse,
)

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new order for fix packages."""
    # Verify audit exists and belongs to user
    audit_result = await db.execute(
        select(Audit).where(Audit.id == data.audit_id, Audit.user_id == user.id)
    )
    audit = audit_result.scalar_one_or_none()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    total_cents = 0
    items = []

    for pkg_id in data.fix_package_ids:
        pkg_result = await db.execute(select(FixPackage).where(FixPackage.id == pkg_id))
        pkg = pkg_result.scalar_one_or_none()
        if not pkg:
            raise HTTPException(status_code=404, detail=f"Fix package {pkg_id} not found")

        total_cents += pkg.price_cents
        item = OrderItem(
            fix_package_id=pkg.id,
            description=pkg.name,
            price_cents=pkg.price_cents,
        )
        items.append(item)

    if not items:
        raise HTTPException(status_code=400, detail="No fix packages selected")

    order = Order(
        user_id=user.id,
        audit_id=data.audit_id,
        status=OrderStatus.PENDING,
        total_cents=total_cents,
    )
    db.add(order)
    await db.flush()

    for item in items:
        item.order_id = order.id
        db.add(item)

    await db.flush()
    await db.refresh(order)

    # Re-fetch items
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    order.items = items_result.scalars().all()

    return OrderResponse(
        id=order.id,
        status=order.status.value,
        total_cents=order.total_cents,
        items=[OrderItemResponse.model_validate(i) for i in order.items],
        created_at=order.created_at,
    )


@router.get("/", response_model=list[OrderResponse])
async def list_orders(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all orders for the current user."""
    result = await db.execute(
        select(Order)
        .where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
    )
    orders = result.scalars().all()

    response = []
    for order in orders:
        items_result = await db.execute(
            select(OrderItem).where(OrderItem.order_id == order.id)
        )
        items = items_result.scalars().all()
        response.append(OrderResponse(
            id=order.id,
            status=order.status.value,
            total_cents=order.total_cents,
            items=[OrderItemResponse.model_validate(i) for i in items],
            created_at=order.created_at,
            paid_at=order.paid_at,
        ))
    return response


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get order details."""
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == user.id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    items = items_result.scalars().all()

    return OrderResponse(
        id=order.id,
        status=order.status.value,
        total_cents=order.total_cents,
        items=[OrderItemResponse.model_validate(i) for i in items],
        created_at=order.created_at,
        paid_at=order.paid_at,
    )