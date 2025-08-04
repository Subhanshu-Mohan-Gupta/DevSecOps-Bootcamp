# T13 - Secure Supply Chain with Cosign

## Steps Performed

1. Installed Cosign on Ubuntu 24.04
2. Generated a key pair:
3. Signed the Docker image:
4. Verified the image:
5. Signature verification is saved in `SIGNATURE_VERIFICATION.txt`.

## Notes

- The keys are stored in `cosign-keypair/`
- The image is now signed and verifiable by anyone with the public key.
output:
 - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The signatures were verified against the specified public key

