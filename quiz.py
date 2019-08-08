from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABdMZu5PyhLOmt4yLlNZTWtxrAu-F5sXgsTERDelHHcMwLKvw-\
FMDp88p4Lfn8YnXxkpWTnEozJl7Bi3o0xvqTQ1eorAxBj6iUINLm3jMCrv_KuJKGMzPIhOljXtK8KcCprXStzsqynAUFoIfoaQrNrwLZIxCRkLTrD8HdVU17jQo3dMC4='


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
