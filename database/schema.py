


def oraganization_data(organization) -> dict:
    return {
        "id": str(organization["_id"]),
        "organization_name": organization["organization_name"],
        "updated_at": organization["updated_at"],
        "created_at": organization["created_at"],
        "is_active": organization["is_active"],
    }
    
def all_organization(organization) -> dict:
    return [ oraganization_data(org) for org in organization]