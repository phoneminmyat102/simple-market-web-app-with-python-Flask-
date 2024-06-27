from market import app
from market.models import db, Item

with app.app_context():


    item = Item(name='iPhone 11', price=500, description='lorem you know lorem', barcode='4359825682')
    db.session.add(item)
    db.session.commit()

    item1 = Item(name='Tablet', price=300, description='lorem something lorem', barcode='436876390')
    db.session.add(item1)
    db.session.commit()

    item2 = Item(name='Mac Air', price=1500, description='lorem not everything lorem', barcode='967563258')
    db.session.add(item2)
    db.session.commit()
