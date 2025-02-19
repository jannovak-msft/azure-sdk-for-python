# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import asyncio
import os
from azure.keyvault.certificates import CertificatePolicy
from azure.keyvault.certificates.aio import CertificateClient
from azure.identity.aio import DefaultAzureCredential

# ----------------------------------------------------------------------------------------------------------
# Prerequisites:
# 1. An Azure Key Vault (https://docs.microsoft.com/azure/key-vault/quick-create-cli)
#
# 2. azure-keyvault-certificates and azure-identity packages (pip install these)
#
# 3. Set up your environment to use azure-identity's DefaultAzureCredential. For more information about how to configure
#    the DefaultAzureCredential, refer to https://aka.ms/azsdk/python/identity/docs#azure.identity.DefaultAzureCredential
#
# ----------------------------------------------------------------------------------------------------------
# Sample - demonstrates the basic recover and purge operations on a vault(certificate) resource for Azure Key Vault
#
# 1. Create a certificate (create_certificate)
#
# 2. Delete a certificate (delete_certificate)
#
# 3. Recover a deleted certificate (recover_deleted_certificate)
#
# 4. Purge a deleted certificate (purge_deleted_certificate)
# ----------------------------------------------------------------------------------------------------------


async def run_sample():
    # Instantiate a certificate client that will be used to call the service.
    # Here we use the DefaultAzureCredential, but any azure-identity credential can be used.
    VAULT_URL = os.environ["VAULT_URL"]
    credential = DefaultAzureCredential()
    client = CertificateClient(vault_url=VAULT_URL, credential=credential)

    # Let's create certificates holding storage and bank accounts credentials. If the certificate
    # already exists in the Key Vault, then a new version of the certificate is created.
    print("\n.. Create Certificates")
    bank_cert_name = "BankRecoverCertificateAsync"
    storage_cert_name = "ServerRecoverCertificateAsync"

    bank_certificate = await client.create_certificate(
        certificate_name=bank_cert_name, policy=CertificatePolicy.get_default()
    )
    storage_certificate = await client.create_certificate(
        certificate_name=storage_cert_name, policy=CertificatePolicy.get_default()
    )

    print(f"Certificate with name '{bank_certificate.name}' was created.")
    print(f"Certificate with name '{storage_certificate.name}' was created.")

    # The storage account was closed, need to delete its credentials from the Key Vault.
    print("\n.. Delete a Certificate")
    deleted_bank_certificate = await client.delete_certificate(bank_cert_name)
    # To ensure certificate is deleted on the server side.
    await asyncio.sleep(30)

    print(
        f"Certificate with name '{deleted_bank_certificate.name}' was deleted on date "
        f"{deleted_bank_certificate.deleted_on}."
    )

    # We accidentally deleted the bank account certificate. Let's recover it.
    # A deleted certificate can only be recovered if the Key Vault is soft-delete enabled.
    print("\n.. Recover Deleted Certificate")
    recovered_bank_certificate = await client.recover_deleted_certificate(deleted_bank_certificate.name)
    print(f"Recovered Certificate with name '{recovered_bank_certificate.name}'.")

    # Let's delete storage account now.
    # If the keyvault is soft-delete enabled, then for permanent deletion deleted certificate needs to be purged.
    await client.delete_certificate(storage_cert_name)

    # Certificates will still purge eventually on their scheduled purge date, but calling `purge_deleted_certificate` immediately
    # purges.
    print("\n.. Purge Deleted Certificate")
    await client.purge_deleted_certificate(storage_cert_name)
    print("Certificate has been permanently deleted.")

    print("\nrun_sample done")
    await credential.close()
    await client.close()


if __name__ == "__main__":
    asyncio.run(run_sample())
