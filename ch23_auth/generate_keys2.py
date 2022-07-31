import streamlit_authenticator as stauth

names = ['Kwang Myung Yu', 'Bo Kyung Jin']
usernames = ['sguys99', 'anotherme82']
passwords = ['qhrud0724*']

hashed_passwords = stauth.Hasher(['qhrud0724*']).generate()
print(hashed_passwords)

