from faker import Faker

fake = Faker(['en-US', 'uk_UA'])
Faker.seed = 313

def generate_row(columns):
    operations = {
        'Address': fake['en-US'].address(),
        'Company name': fake['en-US'].company(),
        'Date': fake.date_time(),
        'Domain name': fake['en-US'].domain_name(),
        'Email': fake.email(),
        'Full name': fake['en-US'].name(),
        'Job': fake['en-US'].job(),
        'Phone number': fake.phone_number(),
    }

    for column in columns:
        if column.type.name == 'Integer':
            operations[column.name] = fake.pyint(min_value=column.from_range, max_value=column.to_range)
        elif column.type.name == 'Text':
            operations[column.name] = fake['en-US'].paragraphs(nb=column.to_range)
    
    row = {column.name: operations.get(column.type.name) if column.type.name in operations else operations.get(column.name) for column in columns}
    return row
