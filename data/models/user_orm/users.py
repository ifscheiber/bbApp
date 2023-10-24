from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

import datetime

from .base import Base

"""
The Users module defines the parent LeapNode User class and its childs
"""


class LeapNodeUser(Base):
    """
    Represents a user in the LeapNode system.

    :ivar id: Unique identifier for each employee.
    :vartype id: str
    :ivar first_name: Employee's first name.
    :vartype first_name: str
    :ivar middle_names: Employee's middle name(s), if any.
    :vartype middle_names: Optional[str]
    :ivar last_name: Employee's last name.
    :vartype last_name: str
    :ivar email: The user's email address.
    :vartype email: str
    :ivar password: The user's password.
    :vartype password: str
    :ivar client: The user's employee (Must be a client of LeapNode).
    :vartype client: str
    :ivar status: Flag indicating whether the user is active or inactive (blocked).
    :vartype status: int
    :ivar registration_date: Date the user has been registered with LeapNode.
    :vartype registration_date: datetime

    :method __repr__: Return a string representation of the object.
    """
    __tablename__ = "leapnode_users"
    __table_args__ = {"schema": Base.schema, "extend_existing": True}

    id: Mapped[str] = mapped_column(
        primary_key=True, comment="Unique identifier for each employee"
    )
    first_name: Mapped[str] = mapped_column(
        String(30), comment="Employee's first name"
    )
    middle_names: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, comment="Employee's middle name(s), if any"
    )
    last_name: Mapped[str] = mapped_column(
        String(30), comment="Employee's last name"
    )
    email: Mapped[str] = mapped_column(
        String(50), comment="The Users EMail address"
    )
    password: Mapped[str] = mapped_column(
        comment="The Users password"
    )
    client: Mapped[str] = mapped_column(
        comment="The Users employee (Must be client of LeapNode)"  #TODO must map client of LeapNode
    )
    status: Mapped[int] = mapped_column(
        Integer, comment="Flag indicating whether the user is active or inactive (blocked)"
    )
    registration_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, comment="Date the user has been registered with LeapNode"
    )

    def __repr__(self) -> str:
        """
        Return a string representation of the object.

        :return: A string representation of the object.
        :rtype: str
        """
        return f"id=(id={self.id!r}, first_name={self.first_name!r}, middle_names={self.middle_names!r}, " \
               f"last_name={self.last_name!r}, email={self.email}, " \
               f"status={self.status}, registration_date={self.registration_date})"


class LeapNodeBillingUser(LeapNodeUser):
    """
    Represents a billing user in the LeapNode system, extending the LeapNodeUser class.

    This class holds additional information related to the user's role and is used for billing purposes.

    :ivar id: Unique identifier for each LeapNodeUser, foreign key referencing LeapNodeUser.id.
    :vartype id: str
    :ivar role: The user's role, i.e., access level.
    :vartype role: str

    TODO Another table must be created that holds the data licenses the user is allowed to view.
    """
    __tablename__ = "leapnode_billing_users"
    __table_args__ = {"schema": Base.schema, "extend_existing": True}

    id: Mapped[str] = mapped_column(
        ForeignKey(f"{Base.schema}.leapnode_users.id"),
        primary_key=True,
        comment="Unique identifier for each LeapNodeUser"
    )
    role: Mapped[str] = mapped_column(
        String(50), comment="The Users Role, i.e. access level"
    )


