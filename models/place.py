#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('places_id', String(60), ForeignKey('places.id'), primary_key=True,
           nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'),
                     nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    # relationship between Place and Review
    reviews = relationship('Review', backref='place',
                           cascade='all, delete-orphan')

    amenities = relationship(
        'Amenity',
        secondary='place_amenity',
        backref='place_amenities',
        viewonly=False
    )

    def __init__(self, *args, **kwargs):
        """Constructor"""
        super().__init__(*args, **kwargs)

    @property
    def reviews(self):
        """ Returns the list of Review instances with place_id
        equalling the current Place.id.
        """
        from models import storage
        from models.review import Review
        return [obj for obj in storage.all(Review).values()
                if obj.place_id == self.id]

    @property
    def amenities(self):
        """Returns the list of Amenity instances based on the attribute
        amenity_ids."""
        from models import storage
        from models.amenity import Amenity
        return [obj for obj in storage.all(Amenity).values()
                if obj.id in self.amenity_ids]

    @amenities.setter
    def amenities(self, value):
        """adds a Amenity obj's id into the amenity_ids class attribute.
        """
        from models.amenity import Amenity
        if type(value) is Amenity:
            self.amenity_ids.append(value.id)
