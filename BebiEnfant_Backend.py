#Backend
# BeTag du bébé qui doit povoir communiquer avec celui des parents
from microbit import *
import radio
import random
radio.config(group=23)
radio.on()

key = "Betag"

def hashing(string):
	"""
	Hachage d'une chaîne de caractères fournie en paramètre.
	Le résultat est une chaîne de caractères.
	Attention : cette technique de hachage n'est pas suffisante (hachage dit cryptographique) pour une utilisation en dehors du cours.

	:param (str) string: la chaîne de caractères à hacher
	:return (str): le résultat du hachage
	"""
	def to_32(value):
		"""
		Fonction interne utilisée par hashing.
		Convertit une valeur en un entier signé de 32 bits.
		Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.

		:param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
		:return (int): entier signé de 32 bits représentant 'value'
		"""
		value = value % (2 ** 32)
		if value >= 2**31:
			value = value - 2 ** 32
		value = int(value)
		return value

	if string:
		x = ord(string[0]) << 7
		m = 1000003
		for c in string:
			x = to_32((x*m) ^ ord(c))
		x ^= len(string)
		if x == -1:
			x = -2
		return str(x)
	return ""

def vigenere(message, key, decryption=False):
    text = ""
    key_length = len(key)
    key_as_int = [ord(k) for k in key]

    for i, char in enumerate(str(message)): #le i fait réf à la position du str et le char fait réf ay caractère de la position 
        key_index = i % key_length
        #Letters encryption/decryption
        if char.isalpha():
            if decryption:
                modified_char = chr((ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord('A'))
            else : 
                modified_char = chr((ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord('A'))
            #Put back in lower case if it was
            #La fonction ord() permet de renvoyer la valeur unicode associé au caractère
            #la fonction chr() fait l'inverse càd qu'elle renvoie le caractère associé à la valeur unicode
            if char.islower():
                modified_char = modified_char.lower()
            text += modified_char
        #Digits encryption/decryption
        elif char.isdigit():
            if decryption:
                modified_char = str((int(char) - key_as_int[key_index]) % 10)
            else:
                modified_char = str((int(char) + key_as_int[key_index]) % 10)
            text += modified_char
        else:
            text += char
    return text


def unpack_data (encrypted_packed,key) : 
    decryption_message = encrypted_packed.split('|')
    message_en_clair = decryption_message[2].split(':')
    encrypted_packet = tuple(message_en_clair)
    nonce,content = encrypted_packet
    dictionnary = {}
    lst = ['00','01','02','03']
    for element in lst : 
        dictionnary[element] = [] 
    if decryption_message[0] == '00' :
        for clef in dictionnary : 
            if clef == '00' : 
                if nonce in dictionnary['00'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['00'].append(nonce)
                    display.scroll('Message added')
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    return message_decripte_vigenere 
            if clef == '01' : 
                if nonce in dictionnary['01'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['01'].append(nonce)
                    display.scroll('Message added')
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    return message_decripte_vigenere
            if clef == '02' : 
                if nonce in dictionnary['02'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['02'].append(nonce)
                    display.scroll('Message added')
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    return message_decripte_vigenere
                    
            if clef == '03' : 
                if nonce in dictionnary['03'] : 
                    display.scroll('ERROR message already received')
                else : 
                    dictionnary['03'].append(nonce)
                    display.scroll('Message added')
                    message_decripte_vigenere = vigenere(content,key,True) #Here we will decrypt the content of the message
                    return message_decripte_vigenere

def establish_connexion(key): 
    global nbre_alea 
    global content
    if button_b.was_pressed() :
        display.scroll("Connexion ...")
        content= random.randrange(5000)
        nbre_alea = random.randrange(5000)
        nbre_alea_crypted = vigenere(nbre_alea,key)
        message_a_decrypter = vigenere(content,key)
        encrypted_message = nbre_alea_crypted + ':' + message_a_decrypter
        len_message = len(encrypted_message)
        radio_send = '{0}|{1}|{2}'.format('00',str(len_message),encrypted_message)
        radio.send(radio_send)
        return 

def send_message (type_message,contenu,key): 
    contenu_vigenered = vigenere(contenu,key)
    nbre_aleatoire = random.randrange(5000)
    encrypted_message = str(nbre_aleatoire) + ':' + contenu_vigenered
    long_message = len(encrypted_message)
    radio_send = '{0}|{1}|{2}'.format(type_message,str(long_message),encrypted_message)
    display.scroll(radio_send,300)
    radio.send(radio_send)

def calcul_response (message) :
    global key
    global content
    if message : 
        message_deballe = unpack_data(message,key)
        answer_challenge = content *5
        hashing_value_challenge = hashing(str(answer_challenge)) 
        if message_deballe == str(hashing_value_challenge) :
            display.scroll("Clef authentifiée")
            key += str(answer_challenge)
            display.scroll(key)
        
display.scroll('Welcome')
if __name__ == '__main__' :
    while True : 
        message = radio.receive()
        response = establish_connexion(key)
        calcul_response(message)
