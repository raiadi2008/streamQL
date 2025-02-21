from logic


Base = declarative_base()

engine = create_engine("sqlite:///workspace/products.sqlite")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.add(Product(name="iPhone", category="Electronics"))
session.commit()

results = session.query(Product).filter_by(category="Electronics").all()
