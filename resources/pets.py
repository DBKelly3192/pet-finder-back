import models


from flask import Blueprint, jsonify, request, session
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


pet = Blueprint('pets', 'pet')


@pet.route('/all', methods=['GET'])
# @login_required
def get_all_the_pets():
    try:
        allPets = [model_to_dict(pet) for pet in models.Pet]
        # print(f"here is the list of pets. {allPets}")
        return jsonify(data=allPets, status={"code": 201, "message": "success"})

    except models.DoesNotExist:
        return jsonify(
        data={}, status={"code": 401, "message": "Error getting Resources"})


@pet.route('/', methods=['GET'])
@login_required
def get_all_pets():
    try:
        pets = [model_to_dict(pet) for pet in current_user.pets]
        print(f"here is the list of pets. {pets}")
        return jsonify(data=pets, status={"code": 201, "message": "success"})

    except models.DoesNotExist:
        return jsonify(
        data={}, status={"code": 401, "message": "Error getting Resources"})


@pet.route('/', methods=["POST"])
@login_required
def create_pets():
    # try:
        payload = request.get_json()
        print(type(payload), 'payload')
        pet = models.Pet.create(petName=payload['petName'], aboutPet=payload['aboutPet'],
        dateLost=payload['dateLost'], user=current_user.id, photo=payload['photo'],
        status=payload['status'], zipCode=payload['zipCode'])
        # print(payload['photo'])
        # print(type(payload['photo']))
        # createdPet = models.Pet.create(
        # petName='Timofey',
        # aboutPet='The boy.',
        # dateLost=payload['dateLost'],
        # user=1,
        # photo='https://i.imgur.com/bJfRyEI.jpg',
        # status='Found',
        # zipCode='30309')
        print(pet.__dict__)
        print(dir(pet))
    #
    #     pet_dict = model_to_dict(createdPet)
    #     print("Printing createdPet")
    #     print(createdPet)
    #     print("Printing pet_dict")
    #     print(pet_dict)
    #     to_return = jsonify(data=pet_dict, status={"code": 201, "message": "Success"})
    #     print("Printing 201 response")
    #     print(to_return)
    #     return to_return
    # except Exception as e:
    #     print(e)
    #     return jsonify(status={"code": 400, "message": "Not Successful"})
        print(model_to_dict(pet), 'model to dict')
        pet_dict = model_to_dict(pet)
        return jsonify(data=pet_dict, status={"code": 201, "message": "Success"})

@pet.route('/<id>', methods=["GET"])
@login_required
def get_one_pet(id):
    pet = models.Pet.get_by_id(id)
    return jsonify(data=model_to_dict(pet), status={"code": 200, "message": "Success"})


@pet.route('/<id>', methods=["PUT"])
@login_required
def update_pet(id):
    payload = request.get_json()
    query = models.Pet.update(**payload).where(models.Pet.id==id)
    query.execute()
    pet = model_to_dict(models.Pet.get_by_id(id))
    return jsonify(data=pet, status={"code": 200, "message": "Success"})


@pet.route('/<id>', methods=["DELETE"])
@login_required
def delete_pet(id):
    delete_query = models.Pet.delete().where(models.Pet.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
    data={},
    message="{} Woof Woof Meow Meow went home. Pet with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )


# end
