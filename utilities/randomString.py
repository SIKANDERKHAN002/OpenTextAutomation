from faker import Faker
fake = Faker()
def random_string_generator(size=5):
    return fake.pystr(min_chars=size,max_chars=5)