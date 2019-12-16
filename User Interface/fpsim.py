#exemplo de teste para windows de fingerprint enroll
#simula comportamento do sensor DY-50 na funcao example_enroll
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

def main():
    print("Waiting for Finger...")
    temp = int(input("Enter template position: \t"))
    print("Found Template Position at #" + str(temp))
    print("Fingerprint Registered")
    input('hit enter to exit')

if __name__ == "__main__":
    main()
