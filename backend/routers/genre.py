from fastapi import APIRouter

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct, func, desc
from sqlalchemy.orm import aliased

from database.db import AsyncSessionLocal
from database.models import Invoice, Genre, Track, InvoiceItem, Employee

from typing import Annotated

from security.helpers import get_current_active_user


router = APIRouter(
    tags=["Genre"]
)


# Dependency to get async DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/total-genre")
async def get_total_genre(db: AsyncSession = Depends(get_db)):
    """
    Get the total number of genres sold.

    ## Sample response:
    ```json
    {
        "total-genre-sold": 5
    }
    ```
    """
    query = (
        select(distinct(Track.GenreId))
        .select_from(InvoiceItem)
        .join(Track, InvoiceItem.TrackId == Track.TrackId)
        .where(Track.GenreId != None)
    )

    result = await db.execute(query)
    genre_ids = result.scalars().all()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"total-genre-sold": len(set(genre_ids))},
    )


@router.get("/recent-sale")
async def get_total_genre(db: AsyncSession = Depends(get_db)):
    """
    Get the most recent genre sold and the date of sale.
    
    ## Sample response:
    ```json
    {
        "genre": "Rock",
        "date-sold": "2023-10-01"
    }
    """
    query = (
        select(Genre.Name, Invoice.InvoiceDate)
        .select_from(InvoiceItem)
        .join(Track, InvoiceItem.TrackId == Track.TrackId)
        .join(Genre, Track.GenreId == Genre.GenreId)
        .join(Invoice, InvoiceItem.InvoiceId == Invoice.InvoiceId)
        .order_by(desc(Invoice.InvoiceDate))
        .limit(1)
    )

    result = await db.execute(query)
    genre_name, invoice_date = result.one()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"genre": genre_name, "date-sold": str(invoice_date)},
    )


@router.get("/genre-sale-summary")
async def get_genre_sale_summary(
    current_user: Annotated[Employee, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):

    """
    Get a summary of sales by genre.
    
    ## Sample response:
    ```json
    [
        {
            "genre": "Rock",
            "sales-count": 10,
            "last-sale-date": "2023-10-01",
            "last-track-sold": "Track A"
        },
        {
            "genre": "Pop",
            "sales-count": 5,
            "last-sale-date": "2023-09-15",
            "last-track-sold": "Track B"
        }
    ]
    """
    # Define windowed columns:
    sales_count_w = (
        func.count(InvoiceItem.InvoiceLineId)
        .over(partition_by=Genre.GenreId)
        .label("sales_count")
    )

    last_sale_date_w = (
        func.row_number()
        .over(partition_by=Genre.GenreId, order_by=desc(Invoice.InvoiceDate))
        .label("rn")
    )

    # Build the inner query (joined and windowed):
    inner = (
        select(
            Genre.GenreId.label("genre_id"),
            Genre.Name.label("genre_name"),
            sales_count_w,
            Invoice.InvoiceDate.label("invoice_date"),
            Track.Name.label("track_name"),
            last_sale_date_w,
        )
        .select_from(InvoiceItem)
        .join(Track, InvoiceItem.TrackId == Track.TrackId)
        .join(Genre, Track.GenreId == Genre.GenreId)
        .join(Invoice, InvoiceItem.InvoiceId == Invoice.InvoiceId)
        .where(Genre.GenreId != None)
    ).subquery()

    # Pull only the first row per genre:
    query = (
        select(
            inner.c.genre_name,
            inner.c.sales_count,
            inner.c.invoice_date.label("last_sale_date"),
            inner.c.track_name.label("last_track_sold"),
        )
        .where(inner.c.rn == 1)
        .order_by(inner.c.genre_name)
    )

    result = await db.execute(query)
    rows = result.all()

    # Format for JSON
    genre_stats = [
        {
            "genre": row.genre_name,
            "sales-count": row.sales_count,
            "last-sale-date": str(row.last_sale_date),
            "last-track-sold": row.last_track_sold,
        }
        for row in rows
    ]

    return JSONResponse(status_code=status.HTTP_200_OK, content=genre_stats)


@router.get("/not-sold")
async def get_total_genre(db: AsyncSession = Depends(get_db)):
    """
    Get genres that have never been sold.
    
    ## Sample response:
    ```json
    [
        {
            "GenreId": 3,
            "Name": "Jazz"
        },
        {
            "GenreId": 4,
            "Name": "Classical"
        }
    ]
    """
    # 1. Build a subquery of all GenreIds that *have* sales
    sold_genres_subq = (
        select(distinct(Track.GenreId))
        .join(InvoiceItem, InvoiceItem.TrackId == Track.TrackId)
        .subquery()
    )

    # 2. Select genres whose GenreId is *not* in that list
    query = (
        select(Genre.GenreId, Genre.Name)
        .where(~Genre.GenreId.in_(sold_genres_subq))
        .order_by(Genre.Name)
    )

    result = await db.execute(query)
    rows = result.all()

    if not rows:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=[]
        )  # all genres have sales

    unsold_genres = [{"GenreId": row.GenreId, "Name": row.Name} for row in rows]

    return JSONResponse(status_code=status.HTTP_200_OK, content=unsold_genres)
