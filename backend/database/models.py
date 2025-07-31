from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Table
from sqlalchemy.orm import relationship
from database.db import Base

# Association Table for Playlist and Track
playlist_track = Table(
    "playlist_track",
    Base.metadata,
    Column("PlaylistId", Integer, ForeignKey("playlists.PlaylistId"), primary_key=True),
    Column("TrackId", Integer, ForeignKey("tracks.TrackId"), primary_key=True),
)


class Album(Base):
    __tablename__ = "albums"
    AlbumId = Column(Integer, primary_key=True, index=True)
    Title = Column(String(160))
    ArtistId = Column(Integer, ForeignKey("artists.ArtistId"))

    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album")


class Artist(Base):
    __tablename__ = "artists"
    ArtistId = Column(Integer, primary_key=True, index=True)
    Name = Column(String(120))
    
    albums = relationship("Album", back_populates="artist")


class Customer(Base):
    __tablename__ = "customers"
    CustomerId = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String(40))
    LastName = Column(String(20))
    Company = Column(String(80))
    Address = Column(String(70))
    City = Column(String(40))
    State = Column(String(40))
    Country = Column(String(40))
    PostalCode = Column(String(10))
    Phone = Column(String(24))
    Fax = Column(String(24))
    Email = Column(String(60))
    SupportRepId = Column(Integer, ForeignKey("employees.EmployeeId"))

    support_rep = relationship("Employee", back_populates="customers")
    invoices = relationship("Invoice", back_populates="customer")


class Employee(Base):
    __tablename__ = "employees"
    EmployeeId = Column(Integer, primary_key=True, index=True)
    LastName = Column(String(20))
    FirstName = Column(String(20))
    Title = Column(String(30))
    ReportsTo = Column(Integer, ForeignKey("employees.EmployeeId"))
    BirthDate = Column(DateTime)
    HireDate = Column(DateTime)
    Address = Column(String(70))
    City = Column(String(40))
    State = Column(String(40))
    Country = Column(String(40))
    PostalCode = Column(String(10))
    Phone = Column(String(24))
    Fax = Column(String(24))
    Email = Column(String(60))

    subordinates = relationship("Employee", remote_side=[EmployeeId])
    customers = relationship("Customer", back_populates="support_rep")


class Genre(Base):
    __tablename__ = "genres"
    GenreId = Column(Integer, primary_key=True, index=True)
    Name = Column(String(120))

    tracks = relationship("Track", back_populates="genre")


class Invoice(Base):
    __tablename__ = "invoices"
    InvoiceId = Column(Integer, primary_key=True, index=True)
    CustomerId = Column(Integer, ForeignKey("customers.CustomerId"))
    InvoiceDate = Column(DateTime)
    BillingAddress = Column(String(70))
    BillingCity = Column(String(40))
    BillingState = Column(String(40))
    BillingCountry = Column(String(40))
    BillingPostalCode = Column(String(10))
    Total = Column(Numeric(10, 2))

    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    InvoiceLineId = Column(Integer, primary_key=True, index=True)
    InvoiceId = Column(Integer, ForeignKey("invoices.InvoiceId"))
    TrackId = Column(Integer, ForeignKey("tracks.TrackId"))
    UnitPrice = Column(Numeric(10, 2))
    Quantity = Column(Integer)

    invoice = relationship("Invoice", back_populates="items")
    track = relationship("Track", back_populates="invoice_items")


class MediaType(Base):
    __tablename__ = "media_types"
    MediaTypeId = Column(Integer, primary_key=True, index=True)
    Name = Column(String(120))

    tracks = relationship("Track", back_populates="media_type")


class Playlist(Base):
    __tablename__ = "playlists"
    PlaylistId = Column(Integer, primary_key=True, index=True)
    Name = Column(String(120))

    tracks = relationship("Track", secondary=playlist_track, back_populates="playlists")


class Track(Base):
    __tablename__ = "tracks"
    TrackId = Column(Integer, primary_key=True, index=True)
    Name = Column(String(200))
    AlbumId = Column(Integer, ForeignKey("albums.AlbumId"))
    MediaTypeId = Column(Integer, ForeignKey("media_types.MediaTypeId"))
    GenreId = Column(Integer, ForeignKey("genres.GenreId"))
    Composer = Column(String(220))
    Milliseconds = Column(Integer)
    Bytes = Column(Integer)
    UnitPrice = Column(Numeric(10, 2))

    album = relationship("Album", back_populates="tracks")
    media_type = relationship("MediaType", back_populates="tracks")
    genre = relationship("Genre", back_populates="tracks")
    playlists = relationship(
        "Playlist", secondary=playlist_track, back_populates="tracks"
    )
    invoice_items = relationship("InvoiceItem", back_populates="track")