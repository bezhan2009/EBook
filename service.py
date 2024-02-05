import repository
from models import Staff
import utils


def create_staff(staff: Staff):
    staff.password = utils.hash_string(staff.password)
    return repository.add_staff(staff)


def get_staff(name, password):
    password = utils.hash_string(password)
    staff = repository.get_staff(name, password)
    if staff is None:
        return None, "Incorrect username or password"
    return staff.id, None

