# LagosCP Postman Collection

This directory contains the Postman assets for the Lagos State Crime Profiling System (LagosCP).

### Usage

1. **Local Development**: Use `LagosCP_API_Collection.postman_collection.json` with `LagosCP_Local_Environment.json`.
2. **Setup**: Refer to the [POSTMAN_GUIDE.md](./POSTMAN_GUIDE.md) for detailed import and workflow instructions.
3. **Seeding**: Ensure you have run `python create_admin.py` to populate your local database with the credentials required for the login requests.

### Key Workflows

- **Login**: Always start by running the Login request in the Authentication folder.
- **Identify & Track**: Follow the flow from Field Scan → Profile View → Log Offence to test the integrated profiling system.
