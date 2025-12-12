# from fastapi import FastAPI, APIRouter, HTTPException
# from config import org_collection, admin_collection,db
# from database.schema import all_organization
# from database.models import Organization, OrgUpdate, OrgDelete
# from bson.objectid import ObjectId
# from datetime import datetime
# import bcrypt

# app = FastAPI()
# router = APIRouter()

# @router.get("/")
# async def get_all_organizations():
#     data = org_collection.find({"is_active": True})
#     return all_organization(data)


# @router.post("/org/create")
# async def create_organization(org: Organization):
#     try:
#         org_name = org.organization_name
#         existing = org_collection.find_one({"organization_name": org_name})
#         if existing:
#             return HTTPException(status_code=400, detail="Organization already exists")
#         dynamic_collection_name = f"org_{org_name}"
#         db.create_collection(dynamic_collection_name)
        
#         admin_data = {
#             "email": org.email,
#             "password": org.password,  # ❗ HASH PASSWORD IN REAL APP
#             "organization": org_name
#         }
        
#         admin_id = admin_collection.insert_one(admin_data).inserted_id
        
#         organization = {
#             "organization_name": org_name,
#             "collection_name": dynamic_collection_name,
#             "admin_user_id": str(admin_id)
#         }
        
#         org_collection.insert_one(organization)
        
#         return {
#             "message": "Organization created successfully",
#             "organization": {
#                 "name": org_name,
#                 "collection": dynamic_collection_name,
#                 "admin_user_id": str(admin_id)
#             }
#         }
#     except Exception as e:
#         return HTTPException(status_code=500, detail=str(e))
    
#     # if existing:
#     #     raise HTTPException(status_code=400, detail="Organization already exists")
#     # try:
#     #     response = org_collection.insert_one(dict(org))
#     #     return {"status": "valid", "id": str(response.inserted_id)}
#     # except Exception as e:
#     #     return HTTPException(status_code=500, detail=str(e))
    
# @router.get("/org/{org_name}")
# async def get_organization(org_name: str):
#     try:
#         org_name = org_name

#         organization = org_collection.find_one({"organization_name": org_name})
#         if not organization:
#             raise HTTPException(status_code=404, detail="Organization not found")

#         # Fetch admin details using ObjectId
#         admin = admin_collection.find_one({"_id": ObjectId(organization["admin_user_id"])})

#         return {
#             "organization_name": organization["organization_name"],
#             "collection_name": organization["collection_name"],
#             "admin_user_id": organization["admin_user_id"],
#             organization["collection_name"] : {
#                 "email": admin["email"] if admin else None,
#                 "password": admin["password"] if admin else None
#             }
            
#         }
#     except Exception as e:
#         return HTTPException(status_code=500, detail=str(e))
    
# @router.put("/org/get/{org_name}")
# async def update_organization(org_name: str, org: OrgUpdate):

#     old_name = org_name

#     organization = org_collection.find_one({"organization_name": old_name})
#     if not organization:
#         return HTTPException(status_code=404, detail="Organization not found")

#     update_data = {}
#     admin_update = {}

#     if org.new_organization_name:
#         new_name = org.new_organization_name

#         exists = org_collection.find_one({"organization_name": new_name})
#         if exists:
#             raise HTTPException(status_code=400, detail="New organization name already exists")

#         old_collection = organization["collection_name"]
#         new_collection = f"org_{new_name}"

#         db[old_collection].rename(new_collection)

#         update_data["organization_name"] = new_name
#         update_data["collection_name"] = new_collection


#     admin_id = ObjectId(organization["admin_user_id"])

#     if org.email:
#         admin_update["email"] = org.email

#     if org.password:
#         admin_update["password"] = org.password  # Should hash

#     if admin_update:
#         admin_collection.update_one(
#             {"_id": admin_id},
#             {"$set": admin_update}
#         )

#     if update_data:
#         org_collection.update_one(
#             {"organization_name": old_name},  # find by OLD name
#             {"$set": update_data}
#         )

#     final_data = update_data | admin_update

#     return {
#         "message": "Organization updated successfully",
#         "updated_fields": final_data
#     }

#     # try:
#     #     id = ObjectId(org_id)
#     #     existing_org = org_collection.find_one({"_id": id,"is_active": True})
#     #     if not existing_org:
#     #         return HTTPException(status_code=404, detail="Organization not found")
#     #     org.updated_at = datetime.timestamp(datetime.now())
#     #     response = org_collection.update_one({"_id": id}, {"$set": dict(org)})
#     #     return {"status": "valid", "message": "Organization updated successfully"}
#     # except Exception as e:
#     #     return HTTPException(status_code=500, detail=str(e))

# @router.delete("/org/update/{org_id}")
# async def delete_organization(org_id: str):
#     try:
#         id = ObjectId(org_id)
#         existing_org = org_collection.find_one({"_id": id,"is_active": True})
#         if not existing_org:
#             return HTTPException(status_code=404, detail="Organization not found")
#         response = org_collection.update_one({"_id": id}, {"$set": {"is_active": False}})
#         return {"status": "valid", "message": "Organization deleted successfully"}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=str(e))
    


# app.include_router(router)


  
# main.py

from fastapi import FastAPI, APIRouter, HTTPException, Depends
from config import master_db, org_collection, admin_collection
from database.schema import all_organization
from database.models import Organization, OrgUpdate, OrgDelete,AdminLogin
from bson.objectid import ObjectId
from datetime import datetime
from auth.jwt_handler import create_access_token
import bcrypt
from auth.auth_middleware import auth_user
from fastapi.openapi.utils import get_openapi




app = FastAPI()
app.openapi_schema = None
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0",
        description="JWT Authentication Added",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply security globally (if you want)
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

router = APIRouter()



# ----------------------------------------------
# 2. CREATE ORGANIZATION
# ----------------------------------------------
from database.models import AdminLogin

@router.post("/admin/login")
async def admin_login(data: AdminLogin):

    admin = admin_collection.find_one({"email": data.email})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    if not bcrypt.checkpw(data.password.encode(), admin["password"].encode()):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({
        "admin_id": str(admin["_id"]),
        "organization": admin["organization"]
    })

    return {"access_token": token, "token_type": "bearer"}


@router.post("/org/create")
async def create_organization(org: Organization):
    try:
        org_name = org.organization_name.strip().lower()

        existing = org_collection.find_one({"organization_name": org_name})
        if existing:
            raise HTTPException(status_code=400, detail="Organization already exists")

        dynamic_collection_name = f"org_{org_name}"

        # Create dynamic collection in master DB
        master_db.create_collection(dynamic_collection_name)

        hashed = bcrypt.hashpw(org.password.encode(), bcrypt.gensalt()).decode()

        # Create admin user
        admin_data = {
            "email": org.email,
            "password": hashed,  # TODO: hash password
            "organization": org_name
        }

        admin_id = admin_collection.insert_one(admin_data).inserted_id

        # Insert org metadata
        organization = {
            "organization_name": org_name,
            "collection_name": dynamic_collection_name,
            "admin_user_id": str(admin_id),
            "is_active": True
        }

        org_collection.insert_one(organization)

        return {
            "message": "Organization created successfully",
            "organization": {
                "name": org_name,
                "collection": dynamic_collection_name,
                "admin_user_id": str(admin_id)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------
# 3. GET ORGANIZATION BY NAME
# ----------------------------------------------
@router.get("/org/{org_name}")
async def get_organization(org_name: str):
    try:
        org_name = org_name.strip().lower()

        organization = org_collection.find_one({"organization_name": org_name})
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        admin = admin_collection.find_one(
            {"_id": ObjectId(organization["admin_user_id"])}
        )

        return {
            "organization_name": organization["organization_name"],
            "collection_name": organization["collection_name"],
            "admin": {
                "email": admin["email"] if admin else None,
                "password": admin["password"] if admin else None
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------
# 4. UPDATE ORGANIZATION
# ----------------------------------------------
@router.put("/org/get/{org_name}")
async def update_organization(org_name: str, org: OrgUpdate, current_admin=Depends(auth_user)):

    # Ensure admin belongs to this org
    if current_admin["organization"].strip().lower() != org_name.strip().lower():
        raise HTTPException(status_code=403, detail="Not allowed")

    old_name = org_name.strip().lower()

    organization = org_collection.find_one({"organization_name": old_name})
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    update_data = {}
    admin_update = {}

    # --------------------------
    # Update Organization Name
    # --------------------------
    if org.new_organization_name:
        new_name = org.new_organization_name.strip().lower()

        exists = org_collection.find_one({"organization_name": new_name})
        if exists:
            raise HTTPException(status_code=400, detail="New organization name already exists")

        old_collection = organization["collection_name"]
        new_collection = f"org_{new_name}"

        # Rename collection inside master DB
        master_db[old_collection].rename(new_collection)

        update_data["organization_name"] = new_name
        update_data["collection_name"] = new_collection

    # --------------------------
    # Update Admin Details
    # --------------------------
    admin_id = ObjectId(organization["admin_user_id"])

    if org.email:
        admin_update["email"] = org.email

    if org.password:
        hashed_pass = bcrypt.hashpw(org.password.encode(), bcrypt.gensalt()).decode()
        admin_update["password"] = hashed_pass


    if admin_update:
        admin_collection.update_one(
            {"_id": admin_id},
            {"$set": admin_update}
        )

    # --------------------------
    # Apply Org Metadata Changes
    # --------------------------
    if update_data:
        org_collection.update_one(
            {"organization_name": old_name},
            {"$set": update_data}
        )

    final_data = update_data | admin_update
    
    new_token = create_access_token({
    "admin_id": str(admin_id),
    "organization": update_data.get("organization_name", old_name)
    })


    return {
    "message": "Organization updated successfully",
    "updated_fields": final_data,
    "new_token": new_token
    }


# ----------------------------------------------
# 5. DELETE (SOFT DELETE) ORGANIZATION
# ----------------------------------------------
@router.delete("/org/delete/{org_name}")
async def delete_organization(org_name: str, current_admin=Depends(auth_user)):

    # Normalize names
    req_name = org_name.strip().lower()
    token_name = current_admin["organization"].strip().lower()

    # Block users trying to delete other orgs
    if token_name != req_name:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Find organization
    organization = org_collection.find_one({"organization_name": req_name})
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    # 1️⃣ Delete admin
    admin_id = organization["admin_user_id"]
    admin_collection.delete_one({"_id": ObjectId(admin_id)})

    # 2️⃣ Delete dynamic collection (org_<name>)
    collection_name = organization["collection_name"]
    if collection_name in master_db.list_collection_names():
        master_db.drop_collection(collection_name)

    # 3️⃣ Delete organization record from master table
    org_collection.delete_one({"organization_name": req_name})

    return {"message": "Organization and admin deleted successfully"}


# Register Router
app.include_router(router)
