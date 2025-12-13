

## TheWeddingCompany Backend — FastAPI + MongoDB

A backend service built using FastAPI + MongoDB, supporting dynamic organization creation where each organization receives:

1. Its own dedicated collection

2. Its own admin account

3. JWT-based authentication

4. CRUD operations

5. Protected organization-level access


**Swagger UI Execution of backend application**

*Works with fastAPIs inbuilt swagger documentation at http://127.0.0.1:8000/docs after execution in local machine port*

a. Logging in with Admin account
<img width="1796" height="807" alt="image" src="https://github.com/user-attachments/assets/60704a11-ca5c-4bbd-bdb1-2010c7621098" />

b. Copy the jwt access token for using update and delete operations (authenticated)
<img width="1770" height="216" alt="image" src="https://github.com/user-attachments/assets/d5873866-1e22-4208-a7d1-cd8d7fac6967" />

c. Click on the authenticate button and paste the copied access for authenticating (required for update and delete)
<img width="1879" height="738" alt="image" src="https://github.com/user-attachments/assets/dafffcb0-bee0-4d4b-bc56-79be55c10975" />

d. Create an Organization
<img width="1775" height="446" alt="image" src="https://github.com/user-attachments/assets/f75914dd-3e0e-4d74-b7a4-cc1e1f7b4c4e" />
<img width="1770" height="214" alt="image" src="https://github.com/user-attachments/assets/0e892532-2055-4ec4-8b05-0dc94b20d819" />

e. Get Organization by Organization Name
<img width="1775" height="430" alt="image" src="https://github.com/user-attachments/assets/8d92cd15-f012-4771-b3bc-5d0d68f1eead" />
<img width="1776" height="261" alt="image" src="https://github.com/user-attachments/assets/4e4df16b-d1db-4cf4-a7d5-3383baf5ab8d" />

f. Update the Organization (works only with Authentication)[*Here the authentication is blank because we have already filled authentication in button above*] 
<img width="1771" height="675" alt="image" src="https://github.com/user-attachments/assets/5470200a-63e2-4dac-b2fd-4706f8afb903" />
<img width="1778" height="273" alt="image" src="https://github.com/user-attachments/assets/418de619-aef1-4c62-9688-3239f915cd2d" />
copy the newly generated jwt token for future authentications

d. Delete the Organization (works only with Authentication)[*Here the authentication is blank because we have already filled authentication in button above*]
<img width="1768" height="500" alt="image" src="https://github.com/user-attachments/assets/7ede31f0-658d-4932-b688-1c9c34b62bcb" />


## High-Level Architecture Diagram

```mermaid
flowchart TB
    Client[Client / Swagger UI]
    FastAPI[FastAPI Backend]
    Auth[JWT Authentication]
    Org[Organization Module]
    Access[Org-Level Access Control]
    MongoDB[(MongoDB)]

    Client -->|HTTP Requests| FastAPI
    FastAPI --> Auth
    FastAPI --> Org
    FastAPI --> Access
    FastAPI --> MongoDB

    MongoDB --> Admin[Admin Collection]
    MongoDB --> OrgA[Organization Collection]
```

## Design Choices

- **FastAPI** is used for its high performance and automatic Swagger UI support.
- **MongoDB** enables flexible schemas and dynamic organization-specific collections.
- **JWT-based authentication** ensures secure, stateless access to protected endpoints.
- **Dedicated collections per organization** provide data isolation and better access control.
- **Swagger UI** allows easy testing of authentication and CRUD operations.




