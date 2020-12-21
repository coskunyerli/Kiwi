from model.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship


class DatabaseFileItem(Base):
	__tablename__ = 'data'
	id = Column(Integer(), primary_key = True)
	name = Column(String())
	type = Column(Integer())

	file_item_id = Column(Integer(), ForeignKey('file_item.id'))
	file_item = relationship('DatabaseOrder')


	def __repr__(self):
		return f'DatabaseSoldProduct({self.id}, {self.amount}, {self.product_barcode}, {self.product_name}, {self.unit}, {self.order})'
